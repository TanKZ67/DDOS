import requests
from bs4 import BeautifulSoup
import time
import random

BASE_URL = "https://bangumi.tv"
START_URL = "https://bangumi.tv/anime/browser"

headers = {
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()
session.headers.update(headers)


def fetch(url):
    res = session.get(url, timeout=20)
    res.raise_for_status()
    res.encoding = "utf-8"
    return res.text


def parse_titles_and_scores(html):
    soup = BeautifulSoup(html, "lxml")
    results = []

    items = soup.select("ul.browserFull li")

    for item in items:
        title_tag = item.select_one("h3 a.l")
        score_tag = item.select_one(".rateInfo .fade")

        if not title_tag or not score_tag:
            continue

        title = title_tag.get_text(strip=True)

        try:
            score = float(score_tag.get_text(strip=True))
        except:
            continue

        results.append((title, score))

    return results


def main():
    print("开始抓评分 ≥ 8.0 的动漫（找到5个就停止）...\n")

    found = 0
    page = 1

    while True:
        if page == 1:
            url = START_URL
        else:
            url = f"{START_URL}?page={page}&sort=title"

        print(f"抓第 {page} 页...")
        html = fetch(url)

        results = parse_titles_and_scores(html)

        for title, score in results:
            if score >= 8.0:
                print(title)
                found += 1

                if found >= 5:
                    print("\n已找到5个，停止抓取 ✔")
                    return  # 直接结束整个程序

        page += 1
        time.sleep(random.uniform(2, 4))


if __name__ == "__main__":
    main()