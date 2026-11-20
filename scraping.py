import requests
import time
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

url = "https://www.musashino-u.ac.jp/"
domain = urlparse(url).netloc

pages = {}
url_list = [url]
visited = set()

while url_list:
    current_url = url_list.pop(0)

    if current_url in visited:
        continue

    visited.add(current_url)

    try:
        time.sleep(0.3)

        res = requests.get(current_url, timeout=10)
        res.raise_for_status()

        if "text/html" not in res.headers.get("Content-Type", ""):
            continue

        soup = BeautifulSoup(res.content, "html.parser")

        if soup.title is not None:
            pages[current_url] = soup.title.get_text(strip=True)
        else:
            pages[current_url] = ""

        print(current_url, pages[current_url])

        for a in soup.find_all("a", href=True):
            link = urljoin(current_url, a["href"])
            link = link.split("#")[0]

            if (urlparse(link).netloc == domain
                    and urlparse(link).scheme in ("http", "https")
                    and link not in visited
                    and link not in url_list):
                url_list.append(link)

    except requests.RequestException as e:
        print("エラー:", current_url, e)

with open("sitemap.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Title"])

    for url, title in pages.items():
        writer.writerow([url, title])

print("完了:", len(pages), "ページ")