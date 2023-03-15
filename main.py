import os
import io
import csv
import re
import time
import logging

import requests
import telebot
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader


# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=os.getenv("LOG_FILE"),
    format="%(asctime)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

# bot
api_bot = os.getenv("API_BOT")
user_id_admin = os.getenv("USERID_BOT")
bot = telebot.TeleBot(api_bot)


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


def get_from_csv():
    with open("log-nums.csv") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        data_read = [item for sublist in reader for item in sublist]
        data_in_lists = list(set(data_read))
    return data_in_lists


def append_api(ls):
    headers = {"Authorization": "Bearer " + os.getenv("AUTH_TOKEN")}
    api_url = os.getenv("API_URL")
    try:
        for name, ordine, link in ls:
            requests.post(
                api_url,
                json={"Ordine": ordine, "Link": link, "Name": name},
                headers=headers,
            )
    except Exception as err:
        print(err)


def add_to_csv(row):
    with open("log-nums.csv", "a", newline="") as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerows(row)


def file_extract_csv(urls, csv_urls):
    print("Begining...")
    bot.send_message(user_id_admin, "Begining...")
    all_numbers = []
    all_cnt = 0
    pattern = re.compile(r"\((.*?)\)", re.MULTILINE | re.DOTALL)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
    }
    for url, number in urls:
        if url not in csv_urls:
            try:
                all_numbers = []
                response = requests.get(url, headers=headers)
                with io.BytesIO(response.content) as file:
                    pdf = PdfReader(file)
                    for i in range(len(pdf.pages)):
                        pageObj = pdf.pages[i]
                        content = pageObj.extract_text().strip()
                        info = pattern.findall(content)
                        for item in info:
                            it = []
                            item = item.replace("\n", "")
                            if item != "UE":
                                it.extend([item, number, url])
                                all_numbers.append(it)
            except Exception:
                logger.exception(f"problem was with document {url}")

            finally:
                logging.info(f"I've done with {url}!")

            time.sleep(5)
            cnt = len(all_numbers)

            if cnt > 0:
                append_api(all_numbers)
                all_cnt += cnt
            add_to_csv([[url, number, cnt]])

    msg = f"I have {all_cnt} new documents"
    logging.info(msg)
    bot.send_message(user_id_admin, msg)


def main():
    url = os.getenv("URL")
    urls = get_data(get_html(url))
    urls_csv = get_from_csv()
    file_extract_csv(urls, urls_csv)


if __name__ == "__main__":
    main()
