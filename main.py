import glob
import os
import datetime
import concurrent.futures
import pandas as pd
from unittest import result
from functools import partial
import time
from Scraper import Scraper

if __name__ == "__main__":

    start = time.perf_counter()

    os.chdir(os.getcwd())
    url = "https://quotes.toscrape.com/"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        pages = range(1, 11)
        results = executor.map(partial(Scraper().etl, url), pages)
        for result in results:
            print(result)

    finish = time.perf_counter()
    print(f"Finished in {round(finish-start,2)} second(s)")

    # Combine all csv files
    all_filenames = glob.glob("QuotesPage*.{}".format("csv"))
    final_filename = "Quotes-" + datetime.date.today().strftime("%Y%m%d") + ".csv"
    combined_df = pd.concat([pd.read_csv(f) for f in all_filenames]).sort_values(
        by=["page"]
    )
    combined_df["index"] = range(1, len(combined_df) + 1)  # Add index col
    combined_df.set_index("index").to_csv(final_filename)
    for f in all_filenames:
        os.remove(f)  # Remove unwanted csv files
    print(f"Final csv: {final_filename}")
    assert os.path.exists(final_filename)  # Checks successful creation of csv
