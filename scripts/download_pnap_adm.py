"""Download current PNAP ADM PDF documents from the official Buildings Department page."""
from pathlib import Path
from urllib.parse import urljoin, urlparse
import hashlib, json, re, requests
from bs4 import BeautifulSoup

PAGE = "https://www.bd.gov.hk/en/resources/codes-and-references/practice-notes-and-circular-letters/index_pnap.html"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "documents" / "PNAP" / "ADM"
TIMEOUT = 45

def main():
    session = requests.Session()
    session.headers["User-Agent"] = "RSE-knowledge-library/1.0 (document archival)"
    response = session.get(PAGE, timeout=TIMEOUT)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    found = {}
    # Only official Part A ADM current main-document links; no obsolete-version links.
    for a in soup.find_all("a", href=True):
        label = a.get_text(" ", strip=True)
        match = re.fullmatch(r"ADM\s*-\s*(\d{1,2})", label, re.I)
        if not match:
            continue
        num = int(match.group(1))
        if not 1 <= num <= 23:
            continue
        url = urljoin(PAGE, a["href"])
        if urlparse(url).hostname != "www.bd.gov.hk":
            raise ValueError("Unexpected document host: " + url)
        if not urlparse(url).path.lower().endswith(".pdf"):
            raise ValueError("ADM document link is not a PDF: " + url)
        found[num] = url
    # ADM-12 was repealed and is not an active practice note.
    expected = set(range(1, 24)) - {12}
    missing = expected - set(found)
    if missing:
        raise RuntimeError(f"Official page missing current ADM documents: {sorted(missing)}")
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for num in sorted(expected):
        url = found[num]
        r = session.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        content = r.content
        if not content.startswith(b"%PDF-"):
            raise ValueError(f"ADM-{num} did not return a valid PDF")
        path = OUT / f"ADM-{num:02d}.pdf"
        if not path.exists() or path.read_bytes() != content:
            path.write_bytes(content)
        manifest.append({"code": f"ADM-{num}", "path": path.relative_to(ROOT).as_posix(),
                         "url": url, "sha256": hashlib.sha256(content).hexdigest(),
                         "bytes": len(content)})
    (ROOT / "pnap_adm_sources.json").write_text(
        json.dumps({"official_index": PAGE, "scope": "Current ADM only; ADM-12 repealed",
                    "count": len(manifest), "documents": manifest}, indent=2) + "\n",
        encoding="utf-8")
    print(f"Downloaded/verified {len(manifest)} current ADM PDF files.")

if __name__ == "__main__":
    main()
