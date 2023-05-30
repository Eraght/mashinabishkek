import requests
from bs4 import BeautifulSoup as BS
import csv

def parse_multiple_pages(start_page, end_page):
    for page in range(start_page, end_page + 1):
        url = f"https://www.mashina.kg/search/all/?page={page}"
        source = requests.get(url).text
        soup = BS(source, "lxml")
        process_info(soup)

def write_to_csv(data):
    with open("data.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow(
            [data["title"], data["price"], data["image"], data["description"]]
        )

def process_info(soup):
    info = soup.find_all("div", class_="list-item list-label")
    for i in info:
        title = i.find("h2", class_="name").text.strip()
        price = i.find("strong").text
        image = i.find("img", class_="lazy-image").get("data-src")
        description = (
            i.find("div", class_="block info-wrapper item-info-wrapper")
            .text.replace("\n", "")
            .replace(" ", "")
            .replace(",", " ")
        )
        dict_ = {"title": title, "price": price, "image": image, "description": description}
        write_to_csv(dict_)

parse_multiple_pages(1,10)
