import requests
from bs4 import BeautifulSoup
import re, sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

r = requests.get("https://www.google.com/search?q=agence+web+maroc+email+recrutement&num=10", headers=HEADERS, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

# Try all anchor tags with href containing http
all_links = [a.get("href","") for a in soup.find_all("a")]
http_links = [l for l in all_links if l.startswith("http") and "google" not in l]
print("Direct http links:", len(http_links), file=sys.stderr)
for l in http_links[:10]:
    print(" ", l[:100], file=sys.stderr)

# Try jsname divs (Google result containers)
print("\nAll div classes sample:", file=sys.stderr)
divs = soup.find_all("div", class_=True)
classes = set()
for d in divs:
    for c in d.get("class", []):
        classes.add(c)
print(list(classes)[:30], file=sys.stderr)

# Save HTML for manual inspection
with open("google_debug.html", "w", encoding="utf-8") as f:
    f.write(r.text)
print("\nSaved HTML to google_debug.html", file=sys.stderr)
