import os
import logging
import requests


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


def main():
    url = os.getenv("URL")
    html = get_html(url)


if __name__ == "__main__":
    main()
