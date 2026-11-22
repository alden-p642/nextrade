"""Fetch NSE F&O files from NSE's static archive host (no reports-page session)."""
from __future__ import annotations
import csv, gzip, io, json, sys, time, zipfile, re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import requests

OUT = Path("data")
OUT.mkdir(exist_ok=True)
GIFT_ARCHIVE = OUT / "gift_nifty_history.csv"
GIFT_FIELDS = ["Date", "Session", "Contract", "Open", "High", "Low", "Close", "Previous close", "Change points", "Change %", "Volume", "Contracts traded", "Turnover"]
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
            elif expected == "zip":
                with zipfile.ZipFile(io.BytesIO(body)) as archive:
                    if not any(name.lower().endswith(".csv") for name in archive.namelist()):
                        raise RuntimeError("UDiFF ZIP has no CSV member")
            elif expected == "csv":
                header = next(csv.reader(io.StringIO(body.decode("utf-8-sig", errors="replace"))))
                required = {"CONTRACT_D", "PREVIOUS_S", "CLOSE_PRIC", "SETTLEMENT"}
                if not required.issubset(set(header)):
                    raise RuntimeError(f"Unexpected GIFT bhavcopy columns: {header}")
            return body
        except Exception as exc:
            last = exc
            print(f"Download attempt {attempt + 1}/{attempts} failed for {url}: {exc}", file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"Unable to fetch {url}: {last}")



def gift_rows_from_csv(body: bytes, report_date, session_name: str):
    """Extract the front-month GIFT Nifty index-futures row from an NSE IX bhavcopy."""
    text = body.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise RuntimeError(f"{session_name} GIFT file has no CSV header")
    required = {"CONTRACT_D", "PREVIOUS_S", "CLOSE_PRIC", "SETTLEMENT"}
    if not required.issubset(set(reader.fieldnames)):
        raise RuntimeError(f"Unexpected {session_name} GIFT columns: {reader.fieldnames}")
    candidates = []
    for row in reader:
        contract = (row.get("CONTRACT_D") or "").strip().upper()
        # Exact GIFT Nifty index future only; exclude NIFTY FPI, NIFTY IT,
        # NIFTY NEXT 50 and all other similarly named contracts.
        match = re.fullmatch(r"FUTIDXNIFTY(\d{1,2}-[A-Z]{3}-\d{4})", contract)
        if not match:
            continue
        try:
            expiry = datetime.strptime(match.group(1), "%d-%b-%Y").date()
            previous = float((row.get("PREVIOUS_S") or "").replace(",", ""))
            close_raw = (row.get("CLOSE_PRIC") or "").replace(",", "").strip()
            settlement_raw = (row.get("SETTLEMENT") or "").replace(",", "").strip()
            close = float(close_raw) if close_raw and close_raw.lower() != "nan" else float(settlement_raw)
            if previous <= 0 or close <= 0:
                continue
            def num(key):
                value = (row.get(key) or "").replace(",", "").strip()
                try:
                    x = float(value)
                    return x if x > 0 else None
                except Exception:
                    return None
            points = close - previous
            pct = points / previous * 100.0
            candidates.append({
                "Date": report_date.isoformat(), "Session": session_name,
                "Contract": contract, "Open": num("OPEN_PRICE"),
                "High": num("HIGH_PRICE"), "Low": num("LOW_PRICE"),
                "Close": close, "Previous close": previous,
                "Change points": points, "Change %": pct,
                "Volume": num("TRADED_QUA"),
                "Contracts traded": num("TRD_NO_CON"),
                "Turnover": num("TRADED_VAL"),
                "_expiry": expiry
            })
        except Exception:
            continue
    if not candidates:
        raise RuntimeError(f"No valid FUTIDXNIFTY front-month record in {session_name} report")
    # The nearest expiry is the front month. Do not use far-month contracts.
    candidates.sort(key=lambda item: item["_expiry"])
    chosen = candidates[0]
    chosen.pop("_expiry", None)
    return chosen


def update_gift_archive(session: requests.Session):
    """Fetch both NSE IX sessions, then append/replace date+session rows."""
    session.headers.update({
        "Referer": "https://www1.nseix.com/markets/reports",
        "Origin": "https://www1.nseix.com",
        "Accept": "text/csv,application/octet-stream,*/*",
    })
    today = datetime.now(ZoneInfo("Asia/Kolkata")).date()
    last_error = None
    for offset in range(0, 9):
        day = today - timedelta(days=offset)
        suffix = day.strftime("%d%m%y")
        urls = {
            "Session 1": f"https://www1.nseix.com/api/content/daily_report/G_T_Bhavcopy_FO_{suffix}.CSV",
            "Session 2": f"https://www1.nseix.com/api/content/daily_report/G_T1_Bhavcopy_FO_{suffix}.CSV",
        }
        try:
            rows = []
            for session_name, url in urls.items():
                body = get_file(session, url, "csv", attempts=3)
                rows.append(gift_rows_from_csv(body, day, session_name))
            existing = []
            if GIFT_ARCHIVE.exists():
                with GIFT_ARCHIVE.open("r", encoding="utf-8-sig", newline="") as handle:
                    existing = list(csv.DictReader(handle))
            # Keep a durable history and replace only the same date/session pair.
            keyed = {(r.get("Date"), r.get("Session")): r for r in existing}
            for row in rows:
                keyed[(row["Date"], row["Session"])] = row
            ordered = sorted(keyed.values(), key=lambda r: (r.get("Date", ""), r.get("Session", "")))
            with GIFT_ARCHIVE.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=GIFT_FIELDS, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(ordered)
            print(f"GIFT Nifty updated: {day.isoformat()} — " + ", ".join(f"{r['Session']} {r['Change points']:+.2f} pts ({r['Change %']:+.2f}%)" for r in rows))
            return {"status": "updated", "data_date": day.isoformat(), "sessions": rows, "source_urls": urls, "archive_rows": len(ordered)}
        except Exception as exc:
            last_error = exc
            print(f"No complete GIFT Nifty session pair for {day}: {exc}", file=sys.stderr)
    print(f"GIFT Nifty refresh skipped; existing archive retained: {last_error}", file=sys.stderr)
    return {"status": "unavailable", "error": str(last_error), "archive_exists": GIFT_ARCHIVE.exists()}


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
            gift_status = update_gift_archive(session)
            metadata["gift_nifty"] = gift_status
            (OUT / "nse_futures_data_status.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
            print(json.dumps(metadata, indent=2))
            return
        except Exception as exc:
            last_error = exc
            print(f"No complete F&O file pair for {day}: {exc}", file=sys.stderr)
    raise SystemExit(f"NSE archive update failed for the last 8 calendar days: {last_error}")

if __name__ == "__main__":
    main()
