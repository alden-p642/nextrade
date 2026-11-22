"""Fetch NSE F&O files from NSE's static archive host (no reports-page session)."""
from __future__ import annotations
import csv, gzip, io, json, sys, time, zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import requests

OUT = Path("data")
OUT.mkdir(exist_ok=True)
ARCHIVE = "https://nsearchives.nseindia.com/content/fo"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.nseindia.com/",
}


def get_file(session: requests.Session, url: str, expected: str, attempts: int = 2) -> bytes:
    last = None
    for attempt in range(attempts):
        try:
            response = session.get(url, timeout=60)
            response.raise_for_status()
            body = response.content
            if len(body) < 1000:
                raise RuntimeError(f"File too small: {len(body)} bytes")
            if expected == "gz":
                with gzip.GzipFile(fileobj=io.BytesIO(body)) as stream:
                    header = next(csv.reader(io.TextIOWrapper(stream, encoding="utf-8-sig")))
                required = {"FinInstrmNm", "TckrSymb", "XpryDt"}
                if not required.issubset(set(header)):
                    raise RuntimeError(f"Unexpected contract-master columns: {header[:15]}")
            else:
                with zipfile.ZipFile(io.BytesIO(body)) as archive:
                    if not any(name.lower().endswith(".csv") for name in archive.namelist()):
                        raise RuntimeError("UDiFF ZIP has no CSV member")
            return body
        except Exception as exc:
            last = exc
            print(f"Download attempt {attempt + 1}/{attempts} failed for {url}: {exc}", file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"Unable to fetch {url}: {last}")


def main():
    session = requests.Session()
    session.headers.update(HEADERS)
    # NSE may not publish until after the close. Search recent calendar days,
    # skipping weekends naturally by trying the most recent dates first.
    today = datetime.now(ZoneInfo("Asia/Kolkata")).date()
    last_error = None
    for offset in range(0, 8):
        day = today - timedelta(days=offset)
        ddmmyyyy = day.strftime("%d%m%Y")
        yyyymmdd = day.strftime("%Y%m%d")
        contract_url = f"{ARCHIVE}/NSE_FO_contract_{ddmmyyyy}.csv.gz"
        bhav_url = f"{ARCHIVE}/BhavCopy_NSE_FO_0_0_0_{yyyymmdd}_F_0000.csv.zip"
        try:
            contract_bytes = get_file(session, contract_url, "gz")
            bhav_bytes = get_file(session, bhav_url, "zip")
            (OUT / "latest_nse_fo_contract.csv.gz").write_bytes(contract_bytes)
            (OUT / "latest_nse_fo_bhavcopy.csv.zip").write_bytes(bhav_bytes)
            metadata = {
                "updated_at_utc": datetime.now(timezone.utc).isoformat(),
                "data_date": day.isoformat(),
                "contract_master": {"filename": "latest_nse_fo_contract.csv.gz", "bytes": len(contract_bytes), "source_url": contract_url},
                "udiff_bhavcopy": {"filename": "latest_nse_fo_bhavcopy.csv.zip", "bytes": len(bhav_bytes), "source_url": bhav_url},
                "source": ARCHIVE,
                "note": "Fetched directly from NSE static archive URLs. Current directional prediction model remains an underlying-cash proxy until futures-specific history is integrated."
            }
            (OUT / "nse_futures_data_status.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
            print(json.dumps(metadata, indent=2))
            return
        except Exception as exc:
            last_error = exc
            print(f"No complete F&O file pair for {day}: {exc}", file=sys.stderr)
    raise SystemExit(f"NSE archive update failed for the last 8 calendar days: {last_error}")

if __name__ == "__main__":
    main()
