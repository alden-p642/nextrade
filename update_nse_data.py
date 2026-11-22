"""Download the latest NSE F&O contract master and UDiFF bhavcopy."""
from __future__ import annotations
import json, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

REPORTS_URLS = [
    "https://www.nseindia.in/all-reports-derivatives",
    "https://www.nseindia.com/all-reports-derivatives",
]
OUT = Path("data")
OUT.mkdir(exist_ok=True)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.in/",
}


def collect_links(html: str, base: str):
    soup = BeautifulSoup(html, "html.parser")
    found = []
    for a in soup.find_all("a", href=True):
        href = urljoin(base, a["href"])
        text = " ".join(a.get_text(" ", strip=True).split())
        hay = f"{text} {href}"
        contract = re.search(r"NSE_FO_contract_(\d{8})\.csv\.gz", hay, re.I)
        bhav = re.search(r"BhavCopy_NSE_FO_0_0_0_(\d{8})_F_0000\.csv\.zip", hay, re.I)
        if contract:
            found.append(("contract", contract.group(1), href))
        if bhav:
            found.append(("bhavcopy", bhav.group(1), href))
    return found


def download(session, kind, links):
    candidates = sorted((x for x in links if x[0] == kind), key=lambda x: x[1], reverse=True)
    errors = []
    for _, date_code, url in candidates:
        try:
            r = session.get(url, timeout=90)
            r.raise_for_status()
            if len(r.content) < 1000:
                raise RuntimeError(f"Downloaded file too small ({len(r.content)} bytes)")
            if kind == "contract":
                # Quick gzip integrity check and verify the expected NSE MII fields.
                import gzip, io, csv
                with gzip.GzipFile(fileobj=io.BytesIO(r.content)) as gz:
                    header = next(csv.reader(io.TextIOWrapper(gz, encoding="utf-8-sig")))
                required = {"FinInstrmNm", "TckrSymb", "XpryDt"}
                if not required.issubset(set(header)):
                    raise RuntimeError(f"Unexpected contract columns: {header[:12]}")
                filename = "latest_nse_fo_contract.csv.gz"
            else:
                import zipfile, io
                with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                    csv_names = [n for n in z.namelist() if n.lower().endswith(".csv")]
                    if not csv_names:
                        raise RuntimeError("UDiFF ZIP did not contain a CSV")
                filename = "latest_nse_fo_bhavcopy.csv.zip"
            (OUT / filename).write_bytes(r.content)
            return {"date": datetime.strptime(date_code, "%Y%m%d").date().isoformat(), "filename": filename, "bytes": len(r.content), "source_url": url}
        except Exception as exc:
            errors.append(f"{date_code}: {exc}")
    raise RuntimeError(f"Could not download {kind}. Tried {len(candidates)} candidates. " + " | ".join(errors[-3:]))


def main():
    session = requests.Session(); session.headers.update(HEADERS)
    last_error = None
    for attempt in range(4):
        for reports_url in REPORTS_URLS:
            try:
                # NSE operates both .in and .com report hosts. Try .in first because
                # the .com host returned HTTP 403 from GitHub-hosted runners.
                base_url = reports_url.rsplit("/all-reports-derivatives", 1)[0] + "/"
                session.headers["Referer"] = base_url
                home = session.get(base_url, timeout=30)
                home.raise_for_status()
                page = session.get(reports_url, timeout=45)
                page.raise_for_status()
                links = collect_links(page.text, reports_url)
                if not any(x[0] == "contract" for x in links):
                    raise RuntimeError(f"No dated NSE_FO_contract links found at {reports_url}")
                contract = download(session, "contract", links)
                bhavcopy = download(session, "bhavcopy", links)
                metadata = {
                    "updated_at_utc": datetime.now(timezone.utc).isoformat(),
                    "contract_master": contract,
                    "udiff_bhavcopy": bhavcopy,
                    "source": reports_url,
                    "note": "Daily files downloaded from NSE reports. Bhavcopy is stored for future futures-price analytics; current app directional model remains an underlying-cash proxy."
                }
                (OUT / "nse_futures_data_status.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
                print(json.dumps(metadata, indent=2)); return
            except Exception as exc:
                last_error = exc
                print(f"Attempt {attempt+1}/4 at {reports_url} failed: {exc}", file=sys.stderr)
        time.sleep(10 * (attempt + 1))
    raise SystemExit(f"NSE daily update failed after retries on both official hosts: {last_error}")

if __name__ == "__main__":
    main()
