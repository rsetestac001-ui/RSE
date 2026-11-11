"""Sync the five requested BD code families and all their listed PDF supplements.

Official current catalogue is the discovery source; obsolete ZIPs and duplicate
chapter downloads are excluded. Original PDFs are never merged or rewritten.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import fitz
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = "https://www.bd.gov.hk/en/resources/codes-and-references/codes-and-design-manuals/index.html"
FAMILIES = {
    "foundations": "Code of Practice for Foundations",
    "concrete": "Code of Practice for Structural Use of Concrete",
    "steel": "Code of Practice for the Structural Use of Steel",
    "dead-imposed-loads": "Code of Practice for Dead and Imposed Loads",
    "wind": "Code of Practice on Wind Effects in Hong Kong",
}
EXPLANATIONS = {
    "Explanatory Materials to Code of Practice for the Structural Use of Steel": "steel",
    "Explanatory Notes to the Code of Practice on Wind Effects in Hong Kong": "wind",
}


def discover(html):
    found = {}
    mains = set()
    for row in BeautifulSoup(html, "html.parser").select("tr"):
        anchors = row.select("a[href]")
        if not anchors:
            continue
        title = anchors[0].get_text(" ", strip=True)
        family = next((key for key, prefix in FAMILIES.items() if title.startswith(prefix)), None)
        kind = "code"
        if family:
            mains.add(family)
        else:
            family = next((key for prefix, key in EXPLANATIONS.items() if title.startswith(prefix)), None)
            kind = "explanatory"
        if not family:
            continue
        for i, a in enumerate(anchors):
            url = urljoin(CATALOGUE, a["href"])
            parsed = urlparse(url)
            if parsed.hostname != "www.bd.gov.hk" or not parsed.path.lower().endswith(".pdf") or "/oldversions/" in parsed.path.lower():
                continue
            label = a.get_text(" ", strip=True)
            name = Path(parsed.path).name
            path = f"documents/BD_CODES/{family}/{name}"
            found[url] = {"family": family, "kind": kind if i == 0 else "amendment",
                          "title": title if i == 0 else f"{title} — {label}",
                          "catalogue_label": label, "url": url, "source_pdf": path,
                          "text_file": str(Path(path.replace("documents/", "indexed_text/", 1)).with_suffix(".txt")),
                          "must_read_with": [] if i == 0 else [urljoin(CATALOGUE, anchors[0]["href"])]}
    if mains != set(FAMILIES):
        raise ValueError(f"Missing requested code families: {set(FAMILIES) - mains}")
    for item in found.values():
        if item["kind"] != "amendment":
            item["must_read_with"] = [r["url"] for r in found.values() if item["url"] in r["must_read_with"]]
    return list(found.values())


def refresh():
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=Retry(total=4, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])))
    session.headers["User-Agent"] = "RSE-official-code-archive/1.0"
    response = session.get(CATALOGUE, timeout=(20, 120))
    response.raise_for_status()
    records = discover(response.content)
    checked = datetime.now(timezone.utc).isoformat()
    # Validate every download before replacing any existing PDF or manifest.
    staged = []
    for item in records:
        r = session.get(item["url"], timeout=(20, 180))
        r.raise_for_status()
        if not r.content.startswith(b"%PDF-"):
            raise ValueError(f"Not a PDF: {item['url']}")
        with fitz.open(stream=r.content, filetype="pdf") as doc:
            if not len(doc) or doc.needs_pass:
                raise ValueError(f"Empty or encrypted PDF: {item['url']}")
            empty = [i for i, p in enumerate(doc, 1) if not p.get_text().strip()]
            if len(empty) == len(doc):
                raise ValueError(f"No extractable text: {item['url']}")
            item.update(pages=len(doc), empty_pages=empty)
        item.update(sha256=hashlib.sha256(r.content).hexdigest(), bytes=len(r.content),
                    checked_at=checked, last_modified=r.headers.get("Last-Modified"))
        staged.append((ROOT / item["source_pdf"], r.content))
        print(f"Validated {item['source_pdf']}: {item['pages']} pages", flush=True)
    for dest, data in staged:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists() or dest.read_bytes() != data:
            dest.write_bytes(data)
    out = ROOT / "codes"
    out.mkdir(exist_ok=True)
    manifest = {"catalogue_url": CATALOGUE, "checked_at": checked,
                "catalogue_sha256": hashlib.sha256(response.content).hexdigest(),
                "scope": list(FAMILIES), "documents": records,
                "note": "Official English PDFs. Read main codes with listed amendments and relevant PNAP; explanatory publications have a separate role. Historical PDFs retained locally are not necessarily current. PDF page numbers are 1-based file pages, not printed clause/page labels."}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    catalog = {family: [r for r in records if r["family"] == family] for family in FAMILIES}
    (out / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Validated and saved {len(records)} official PDFs", flush=True)


if __name__ == "__main__":
    refresh()
