from bs4 import BeautifulSoup
import requests
import re
import csv
import pandas as pd
import pymongo

class Scrape:
    def __init__(self):
        pass

    def text_list(self):
        lst = []
        hashc = []

        req = requests.get("https://www.blockchain.com/btc/unconfirmed-transactions")
        soup = BeautifulSoup(req.text, features="html.parser")
        tags = soup.findAll('div', attrs={"class": "sc-1g6z4xm-0 hXyplo"})

        for tag in tags:
            lst.append(tag.getText())

        for item in lst:
            newitem = re.sub("Time", " ", item)
            finalitem = re.sub("Amount", " ", newitem)
            a = re.sub(",", "", finalitem)
            x = re.sub("  ", " ", a)
            b = re.sub("[\b()\b]", "", x)
            c = re.sub("[\bBTC\b]", "", b)
            e = re.sub("[\bHash\b]", "", c)
            f = re.sub("[\bUSD$\b]", "", e)
            hashc.append(f.split(" "))

        header = ["Hash", "Time", "BTC", "W", "USD"]

        with open("hash.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(hashc)

        f.close()

        data_df = pd.read_csv("hash.csv")
        data_df = data_df.drop(["W"], axis = 1)

        column = data_df["USD"]
        max_value = column.max()
        highest = data_df.loc[data_df["USD"] == max_value]
        highest_string = highest.to_string()
        x = highest_string.split("\n")
        
        y = "".join([str(elem) for elem in x[1]])
        no = re.sub(r"^\d* ", "", y)
        good = no.lstrip()
        splitted = good.split(" ")

        client = pymongo.MongoClient("mongodb://localhost:27017")
        database = client["database"]
        collection = database["bitcoin"]

        dict = {
            "Hash": splitted[0],
            "Time": splitted[2],
            "BTC": splitted[4],
            "USD": splitted[6]
        }

        x = collection.insert_one(dict)