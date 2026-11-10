"""Sync current APP and ADV PNAP PDFs from the Buildings Department official index."""
from pathlib import Path
from urllib.parse import urljoin, urlparse
import hashlib
import json
import re
import requests
from bs4 import BeautifulSoup

PAGE = "https://www.bd.gov.hk/en/resources/codes-and-references/practice-notes-and-circular-letters/index_pnap.html"
ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ("APP", "ADV")

def main():
    session = requests.Session()
    session.headers["User-Agent"] = "RSE-PNAP-archiver/1.0"
    response = session.get(PAGE, timeout=60)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    results = {}
    for category in CATEGORIES:
        entries = {}
        # Official index hyperlinks have exact labels such as APP-1, ADV-1.
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
        # Never silently accept large missing ranges; repealed numbers have no live PDF link.
        print(f"{category}: {len(entries)} active links; numbered range {min(entries)}–{max(entries)}")
        out = ROOT / "documents" / "PNAP" / category
        out.mkdir(parents=True, exist_ok=True)
        manifest = []
        for num, url in sorted(entries.items()):
            r = session.get(url, timeout=90)
            r.raise_for_status()
            body = r.content
            if not body.startswith(b"%PDF-"):
                raise ValueError(f"Not a PDF: {category}-{num} {url}")
            path = out / f"{category}-{num:03d}.pdf"
            if not path.exists() or path.read_bytes() != body:
                path.write_bytes(body)
            manifest.append({"code": f"{category}-{num}", "path": path.relative_to(ROOT).as_posix(),
                             "url": url, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)})
        results[category] = {"count": len(manifest), "documents": manifest}
    (ROOT / "pnap_app_adv_sources.json").write_text(
        json.dumps({"official_index": PAGE, "scope": "Current linked APP and ADV PDFs; repealed excluded",
                    "categories": results}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Successfully downloaded:", {k:v["count"] for k,v in results.items()})

if __name__ == "__main__":
    main()
