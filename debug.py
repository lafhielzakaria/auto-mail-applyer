import requests
from bs4 import BeautifulSoup
import sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

r = requests.get("https://www.google.com/search?q=agence+web+maroc+email+recrutement", headers=HEADERS, timeout=10)
print("Status:", r.status_code, file=sys.stderr)
print("Length:", len(r.text), file=sys.stderr)

soup = BeautifulSoup(r.text, "html.parser")
links = [a["href"] for a in soup.select("a[href]") if "/url?q=" in a["href"]]
print("Links found:", len(links), file=sys.stderr)
for l in links[:5]:
    print(l[:120], file=sys.stderr)

# Also check if Google returned a CAPTCHA
if "captcha" in r.text.lower() or "unusual traffic" in r.text.lower():
    print("CAPTCHA DETECTED", file=sys.stderr)
