from bs4 import BeautifulSoup
import requests
import time
import csv
import re
import pandas as pd
import pymongo
import redis

while True:    
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

    # dec = redis.StrictRedis(decode_responses=True)
    client = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

    client.set(name = "Hash", value = splitted[0], ex = 61)
    client.set(name = "Time", value = splitted[2], ex = 61)
    client.set(name = "BTC", value = splitted[4], ex = 61)
    client.set(name = "USD", value = splitted[6], ex = 61)
    
    hash_red = client.get("Hash")
    time_red = client.get("Time")
    btc_red = client.get("BTC")
    usd_red = client.get("USD")

    mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
    database = mongo_client["database"]
    collection = database["bitcoin"]

    dict = {
        "Hash": hash_red,
        "Time": time_red,
        "BTC": btc_red,
        "USD": usd_red
    }

    x = collection.insert_one(dict)

    starttime = time.time()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))