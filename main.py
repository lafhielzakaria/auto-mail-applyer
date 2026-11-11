import json
import os
import time
import random
import sys
from dotenv import load_dotenv
from scraper import fetch_company_emails
from mailer import send_email
from sheets import log_application

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()

SENT_LOG = "sent.json"
DAILY_LIMIT = 15  # Gmail safe limit per session

def load_sent():
    if os.path.exists(SENT_LOG):
        with open(SENT_LOG) as f:
            return set(json.load(f))
    return set()

def save_sent(sent):
    with open(SENT_LOG, "w") as f:
        json.dump(list(sent), f)

def main():
    sent = load_sent()
    print("Fetching companies...\n")
    companies = fetch_company_emails()
    print(f"\nFound {len(companies)} companies with emails.\n")

    sent_this_session = 0

    for company in companies:
        if sent_this_session >= DAILY_LIMIT:
            print(f"\nReached daily limit of {DAILY_LIMIT} emails. Run again tomorrow.")
            break

        email = company["email"]
        if email in sent:
            print(f"  Skipping {company['name']} (already sent)")
            continue

        try:
            send_email(email, company["name"])
            log_application(company["name"], email, city=company.get("city", "Morocco"))
            sent.add(email)
            save_sent(sent)
            sent_this_session += 1

            # Random delay between 45s and 90s — mimics human behavior
            delay = random.randint(45, 90)
            print(f"  [{sent_this_session}/{DAILY_LIMIT}] Waiting {delay}s...")
            time.sleep(delay)

        except Exception as e:
            print(f"  Failed to send to {email}: {e}")
            time.sleep(30)

    print(f"\nDone. Sent {sent_this_session} emails this session.")

if __name__ == "__main__":
    main()
