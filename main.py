import os
import logging
import requests

from bs4 import BeautifulSoup


# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename=os.getenv("LOG_FILE"))


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
    }
    try:
        response = requests.get(url, headers=headers)
        return response.text
    except Exception:
        logger.exception(f"Problem was with document {url}")


def get_data(html):
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    lists = soup.find("div", {"class": "penci-entry-content entry-content"})
    for li in lists.find_all("li"):
        for a in li.find_all("a", href=True):
            if "href" in a.attrs:
                url = a.get("href")
                number = a.text
                urls.append([url, number])
    return urls


def main():
    url = os.getenv("URL")
    urls = get_data(get_html(url))


if __name__ == "__main__":
    main()
