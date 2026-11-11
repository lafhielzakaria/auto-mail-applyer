import requests
from bs4 import BeautifulSoup
import sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

res = requests.post(
    "https://html.duckduckgo.com/html/",
    data={"q": "agence web maroc email", "kl": "ma-fr"},
    headers=HEADERS,
    timeout=15,
)
print("Status:", res.status_code, file=sys.stderr)
print("Length:", len(res.text), file=sys.stderr)

soup = BeautifulSoup(res.text, "html.parser")

# Print all anchor tags
all_a = soup.find_all("a")
print(f"Total <a> tags: {len(all_a)}", file=sys.stderr)
for a in all_a[:10]:
    print(f"  class={a.get('class')} href={str(a.get('href',''))[:80]}", file=sys.stderr)

with open("ddg_debug.html", "w", encoding="utf-8") as f:
    f.write(res.text)
print("Saved ddg_debug.html", file=sys.stderr)
