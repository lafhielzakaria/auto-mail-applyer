import gspread
from google.oauth2.service_account import Credentials
import sys

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

print("Listing all accessible spreadsheets:", file=sys.stderr)
sheets = client.openall()
if not sheets:
    print("  NONE - service account has no sheets shared with it", file=sys.stderr)
else:
    for s in sheets:
        print(f"  - '{s.title}' id={s.id}", file=sys.stderr)
        ws = s.sheet1
        rows = ws.get_all_values()
        print(f"    rows: {len(rows)}", file=sys.stderr)
        for r in rows[:5]:
            print(f"    {r}", file=sys.stderr)
