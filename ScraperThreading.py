import threading
import glob
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep


class Scraper:
    def __init__(self, url="", page=0):
        # Set object variables
        self.url = url + f"/page/{page}/"
        self.page = page

        # Start multithreading
        t = threading.Thread(target=self.etl)
        t.start()

    # Extract, Transform, Load
    def etl(self):
        print("START:", datetime.now())
        self.load(self.transform(self.extract()))
        print("END:", datetime.now())

    # Takes page number, returns soup html
    def extract(self):
        # print("BEGIN EXTRACT")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36"
        }
        r = requests.get(self.url, headers)
        # print("STATUS CODE:", r.status_code)
        soup = BeautifulSoup(r.content, "html.parser")
        # print("END EXTRACT")
        return soup

    # Takes html page, parses the data, returns list of quotes found
    def transform(self, soup):
        # print("BEGIN TRANSFORM")
        quotes = []
        divs = soup.find_all("div", class_="quote")
        # print("LENGTH:", len(divs))
        for item in divs:
            text = (
                item.find("span", class_="text")
                .text.strip()
                .replace("“", "")  # Remove unwanted symbols
                .replace("”", "")
                .replace('"', "")
                .replace("'", "")
                .replace("′", "")
                .replace("’", "")
                .replace(",", "")
            )
            # print("TEXT:", text)
            author = item.find("small", class_="author").text.strip()
            # print("AUTHOR:", author)
            tags = list(
                map(lambda item: item.text.strip(), item.find_all("a", class_="tag"))
            )
            # print("TAGS:", tags)
            quote = {
                "page": self.page,
                "text": text,
                "author": author,
                "tags": "[" + "; ".join(tags) + "]",
            }
            # print("QUOTE:", quote)
            quotes.append(quote)
        # print("QUOTES:", quotes)
        # print("END TRANSFORM")
        return quotes

    # Outputs to a CSV file
    def load(self, data):
        df = pd.DataFrame(data)
        df.to_csv("Quotes" + str(self.page) + ".csv", index=False)
        return


os.chdir(os.getcwd())
url = "https://quotes.toscrape.com/"

# Scrape to csv
for page in range(1, 11):
    Scraper(url, page)

# Combine all csv files
sleep(1)
all_filenames = [i for i in glob.glob("Quotes*.{}".format("csv"))]
combined_df = pd.concat([pd.read_csv(f) for f in all_filenames])
combined_df = combined_df.sort_values(by=["page"])
combined_df["index"] = range(1, len(combined_df) + 1)
combined_df.set_index("index").to_csv("All_Quotes.csv")

# Remove unwanted csv files
for f in all_filenames:
    os.remove(f)
