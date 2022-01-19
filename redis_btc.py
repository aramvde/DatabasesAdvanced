from bs4 import BeautifulSoup
import requests
import time
import re   
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

    client = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
    

    for bitcoinItems in hashc:
        items = {
                "Hash": bitcoinItems[0],
                "Time": bitcoinItems[1], 
                "BTC": bitcoinItems[2], 
                "USD": bitcoinItems[4]
                }
        client.hset(bitcoinItems[0], mapping=items)

    starttime = time.time()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))