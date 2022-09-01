import glob
import os
import datetime
import pandas as pd
from time import sleep
from Scraper import Scraper


os.chdir(os.getcwd())
url = "https://quotes.toscrape.com/"

# Scrape to csv
for page in range(1, 11):
    Scraper(url, page)

# Combine all csv files
sleep(1)
all_filenames = [i for i in glob.glob("QuotesPage*.{}".format("csv"))]
combined_df = pd.concat([pd.read_csv(f) for f in all_filenames])
combined_df = combined_df.sort_values(by=["page"])
combined_df["index"] = range(1, len(combined_df) + 1)  # Add index col
combined_df.set_index("index").to_csv(
    "Quotes" + datetime.date.today().strftime("%Y%m%d") + ".csv"
)

# Remove unwanted csv files
for f in all_filenames:
    os.remove(f)
