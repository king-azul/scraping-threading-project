import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date


class Scraper:
    # Extract, Transform, Load
    def etl(self, url="", page=0):
        # Set object variables
        return self.load(self.transform(self.extract(url, page), page), page)

    # Takes page number, returns soup html
    def extract(self, url="", page=0):
        full_url = url + f"/page/{page}/"
        # print("BEGIN EXTRACT")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36"
        }
        r = requests.get(full_url, headers)
        # print("STATUS CODE:", r.status_code)
        soup = BeautifulSoup(r.content, "html.parser")
        # print("END EXTRACT")
        return soup

    # Takes html page, parses the data, returns list of quotes found
    def transform(self, soup, page=0):
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
                "page": page,
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
    def load(self, data, page=0):
        df = pd.DataFrame(data)
        csv_filename = (
            "QuotesPage" + str(page) + "-" + date.today().strftime("%Y%m%d") + ".csv"
        )
        df.to_csv(
            csv_filename,
            index=False,
        )
        return csv_filename
