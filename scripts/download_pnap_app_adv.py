"""Sync current APP and ADV PNAP PDFs from the Buildings Department official index."""
from pathlib import Path
from urllib.parse import urljoin, urlparse
import hashlib
import json
import re
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

PAGE = "https://www.bd.gov.hk/en/resources/codes-and-references/practice-notes-and-circular-letters/index_pnap.html"
ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ("APP", "ADV")
CHUNK_SIZE = 128 * 1024
MAX_ATTEMPTS = 5


def download_pdf(session, url, path):
    """Stream to a temporary file, retry interrupted transfers, then replace atomically."""
    temp = path.with_suffix(".pdf.part")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            digest = hashlib.sha256()
            size = 0
            first = b""
            with session.get(url, timeout=(20, 120), stream=True) as response:
                response.raise_for_status()
                with temp.open("wb") as target:
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                        if not chunk:
                            continue
                        if not first:
                            first = chunk[:5]
                            if not first.startswith(b"%PDF-"):
                                raise ValueError(f"Not a PDF: {url}")
                        target.write(chunk)
                        digest.update(chunk)
                        size += len(chunk)
            if not size:
                raise ValueError(f"Empty PDF: {url}")
            # Only replace an existing good copy after a complete successful transfer.
            temp.replace(path)
            return {"sha256": digest.hexdigest(), "bytes": size}
        except (requests.RequestException, OSError, ValueError) as exc:
            temp.unlink(missing_ok=True)
            if attempt == MAX_ATTEMPTS:
                raise RuntimeError(f"Download failed after {MAX_ATTEMPTS} attempts: {url}") from exc
            wait = min(2 ** attempt, 30)
            print(f"Retry {attempt}/{MAX_ATTEMPTS} for {url}: {exc}; waiting {wait}s", flush=True)
            time.sleep(wait)


def main():
    session = requests.Session()
    session.headers["User-Agent"] = "RSE-PNAP-archiver/1.0"
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retry))
    response = session.get(PAGE, timeout=(20, 60))
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    results = {}
    failures = []
    for category in CATEGORIES:
        entries = {}
        for a in soup.select("a[href]"):
            match = re.fullmatch(rf"{category}\s*-\s*(\d{{1,3}})", a.get_text(" ", strip=True), re.I)
            if not match:
                continue
            num = int(match.group(1))
            url = urljoin(PAGE, a["href"])
            parsed = urlparse(url)
            if parsed.hostname != "www.bd.gov.hk" or not parsed.path.lower().endswith(".pdf"):
                raise ValueError(f"Unexpected PDF link for {category}-{num}: {url}")
            if num in entries and entries[num] != url:
                raise RuntimeError(f"Duplicate document code: {category}-{num}")
            entries[num] = url
        if not entries:
            raise RuntimeError(f"No active {category} PDFs found. Official page structure may have changed.")
        print(f"{category}: {len(entries)} active links; numbered range {min(entries)}–{max(entries)}", flush=True)
        out = ROOT / "documents" / "PNAP" / category
        out.mkdir(parents=True, exist_ok=True)
        manifest = []
        for num, url in sorted(entries.items()):
            code = f"{category}-{num}"
            path = out / f"{category}-{num:03d}.pdf"
            try:
                info = download_pdf(session, url, path)
                manifest.append({"code": code, "path": path.relative_to(ROOT).as_posix(),
                                 "url": url, **info})
                print(f"OK {code} ({info['bytes']} bytes)", flush=True)
            except RuntimeError as exc:
                failures.append({"code": code, "url": url, "error": str(exc)})
                print(f"WARNING {code}: {exc}", flush=True)
        results[category] = {"count": len(manifest), "expected": len(entries), "documents": manifest}
    report = {"official_index": PAGE, "scope": "Current linked APP and ADV PDFs; repealed excluded",
              "categories": results, "failures": failures, "complete": not failures}
    (ROOT / "pnap_app_adv_sources.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Downloaded:", {k: v["count"] for k, v in results.items()}, flush=True)
    if failures:
        print(f"WARNING: {len(failures)} PDFs failed; partial results saved to manifest.", flush=True)
    else:
        print("All PDFs downloaded successfully.", flush=True)


if __name__ == "__main__":
    main()
