import sys

import traceback

import requests

from bs4 import BeautifulSoup

import pandas as pd

 

URL = "https://licensing.copyright.gov/lds/servlet/lds.SearchIDCTL"

MAX_ID = 100

 

if __name__ == "__main__":

    try:

        for i in range(MAX_ID):

            pass

        obj = { "selectedID" : 4 }

        data = requests.post(URL, data=obj)

        soup = BeautifulSoup(data.text)

        table = soup.find_all("table", { "class" : "compact display"})

        rows = table[0].find_all("tr")

        if len(rows) > 1:

            main_text = soup.find_all("div", {"class" : "main_text"})

            h4s = main_text[0].find_all("h4")

            system = str(h4s[0]).replace("<h4 align=\"left\">System ID:", "").replace("</h4>", "").strip()

            # system_id

            community = str(h4s[1]).replace("<h4 align=\"left\">Community:", "").replace("</h4>", "").strip()

            cols = []

            cols_values = [[] for i in range(13)]

            for i in range(len(rows)):

                if i == 0:

                    cols = rows[0].find_all("th")

                    cols = [str(col).replace("<th>", "").replace("</th>", "") for col in cols]

                    print(len(cols))

                else:

                    row = rows[i].find_all("td")

                    row = [str(r).replace("<td>", "").replace("</td>", "") for r in row]

            #         print(row)

                    for i in range(len(row)):

                        cols_values[i].append(row[i])

                       

            final_dict = {}

            for i in range(13):

                final_dict[cols[i]] = cols_values[i]

            final_dict["System_ID"] = [system] * (len(rows) - 1)

            final_dict["Community"] = [community] * (len(rows) - 1)

            df = pd.DataFrame(final_dict)

            df.to_csv("library_congress.csv", mode="a", index=True, header=False)

    except Exception as err:

        traceback.print_exc()

        sys.exit(err)