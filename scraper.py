import requests
import time
import re
import sys
from ddgs import DDGS

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

QUERIES = [
    # By city
    "agence web Casablanca contact email",
    "agence web Rabat contact email",
    "agence web Marrakech contact email",
    "agence web Agadir contact email",
    "agence web Fes contact email",
    "agence web Tanger contact email",
    # By sector
    "société développement logiciel Maroc email",
    "ESN entreprise services numeriques Maroc email",
    "cabinet informatique Maroc recrutement email",
    "agence digitale Maroc email contact",
    "startup informatique Maroc email",
    "web agency Morocco email",
    "software company Casablanca email",
    "IT services Morocco email contact",
    "développement application mobile Maroc email",
    "e-commerce agency Morocco email",
    # Direct email hunting
    "site:*.ma \"developpeur\" \"recrutement\" email",
    "site:*.ma \"offre emploi\" \"développeur web\" email",
    "contact agence web maroc \"@\" email",
    "recrutement développeur Maroc email RH",
]

MAX_EMAILS = 100

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
SKIP = {
    "example", "test", "noreply", "no-reply", "sentry", "w3.org", "schema",
    "google", "github", ".png", ".jpg", ".svg", ".webp", ".gif", "wix", "wordpress", "yourdomain",
    "jquery", "bootstrap", "cloudflare", "facebook", "twitter", "linkedin",
    "privacy", "legal", "abuse", "spam", "info@w3", "email@email",
    "&quot", "&#", "votre@", "vous@", "nom@", "exemple", "jane", "acme",
    "name@", "user@", "email@", "your@", "mon@", "prenom", "votreentreprise",
    "u003e",
}

def is_valid_email(email):
    return not any(s in email.lower() for s in SKIP)

def extract_emails_from_url(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=5)
        # Decode HTML entities like &quot; before extracting emails
        from html import unescape
        text = unescape(res.text)
        emails = EMAIL_RE.findall(text)
        valid = [e for e in set(emails) if is_valid_email(e)]
        # Prefer .ma domains and contact/info/rh/jobs emails
        priority = [e for e in valid if ".ma" in e or any(k in e.lower() for k in ["contact", "info", "rh", "hr", "jobs", "career", "recrutement"])]
        return priority if priority else valid
    except Exception:
        return []

def get_company_name(url, email):
    try:
        # Use email domain as company name — more accurate than URL
        domain = email.split("@")[1].split(".")[0].capitalize()
        return domain
    except Exception:
        try:
            domain = url.split("//")[-1].split("/")[0].replace("www.", "")
            return domain.split(".")[0].capitalize()
        except Exception:
            return url

def fetch_company_emails():
    seen_emails = set()
    seen_urls = set()
    companies = []

    with DDGS() as ddgs:
        for query in QUERIES:
            if len(companies) >= MAX_EMAILS:
                break

            print(f"Searching: {query}")
            try:
                results = list(ddgs.text(query, region="ma-fr", max_results=15))
            except Exception as e:
                print(f"  Search error: {e}")
                time.sleep(5)
                continue

            print(f"  -> {len(results)} results")

            for r in results:
                if len(companies) >= MAX_EMAILS:
                    break

                url = r.get("href", "")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)

                print(f"  Visiting: {url[:70]}")
                emails = extract_emails_from_url(url)

                for email in emails:
                    if email not in seen_emails:
                        seen_emails.add(email)
                        name = get_company_name(url, email)
                        companies.append({"name": name, "email": email, "website": url})
                        print(f"  OK Found: {name} -> {email}")

                time.sleep(1)

            time.sleep(2)

    print(f"\nTotal companies found: {len(companies)}")
    return companies
