import glob
import os
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
all_filenames = [i for i in glob.glob("Quotes*.{}".format("csv"))]
combined_df = pd.concat([pd.read_csv(f) for f in all_filenames])
combined_df = combined_df.sort_values(by=["page"])
combined_df["index"] = range(1, len(combined_df) + 1)
combined_df.set_index("index").to_csv("All_Quotes.csv")

# Remove unwanted csv files
for f in all_filenames:
    os.remove(f)
