import os
from datetime import datetime, timezone
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def _client():
    sa_path = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    print(sa_path)
    creds = Credentials.from_service_account_file(sa_path, scopes=SCOPES)
    print(creds)
    return gspread.authorize(creds)

def upsert_response(client_email: str, host_date: str, answer: str, tab_name: str):
    sheet_id = os.environ["GOOGLE_SHEET_ID"]

    gc = _client()
    sh = gc.open_by_key(sheet_id)
    ws = sh.worksheet(tab_name)

    headers = ws.row_values(1)
    if not headers:
        ws.append_row(["client_email", "date", "answer", "answered_at"])

    rows = ws.get_all_records()
    now = datetime.now(timezone.utc).isoformat()

    for idx, row in enumerate(rows, start=2):
        if str(row.get("client_email", "")).strip().lower() == client_email.strip().lower() and str(row.get("date", "")).strip() == host_date.strip():
            ws.update(f"C{idx}:D{idx}", [[answer, now]])
            return

    ws.append_row([client_email, host_date, answer, now])
