import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
CREDS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials.json")
SHEET_NAME = os.getenv("GOOGLE_SHEETS_SHEET_NAME", "applications")

def get_sheet():
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

def log_application(company_name, email, city="Morocco"):
    try:
        sheet = get_sheet()
        existing_names = sheet.col_values(1)   # Company Name
        existing_emails = sheet.col_values(4)   # job url col
        if company_name in existing_names or email in existing_emails:
            print(f"  Skipping Sheets (already exists): {company_name}")
            return
        # Columns: Company Name | Date | Post Name | job url | status
        row = [
            company_name,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            "MERN Stack Developer",
            email,
            "nok",
        ]
        sheet.append_row(row)
        print(f"  Logged to Sheets: {company_name}")
    except Exception as e:
        print(f"  Sheets error: {e}")
