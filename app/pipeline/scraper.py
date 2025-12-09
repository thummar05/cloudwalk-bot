import requests
from bs4 import BeautifulSoup
from app.config import CLOUDWALK_URLS
from app.utils.file_io import save_text


def scrape_cloudwalk():
    """Scrapes all CloudWalk URLs defined in config."""
    all_texts = []

    for url in CLOUDWALK_URLS:
        print(f"[SCRAPER] Fetching: {url}")
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"[SCRAPER] Failed: {url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator=" ", strip=True)
        all_texts.append(text)

        save_text(f"data/raw/{url.replace('https://', '').replace('/', '_')}.txt", text)

    print(f"[SCRAPER] Total pages scraped: {len(all_texts)}")
    return all_texts


if __name__ == "__main__":
    scrape_cloudwalk()