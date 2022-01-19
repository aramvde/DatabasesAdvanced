import time
import pymongo
import redis

while True:    
    client = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
    
    value = []
    next = []
    
    for key in client.scan_iter():
        value.append(client.hmget(key, "USD"))

    for item in value:    
        next.append(item[0])

    max = 0.0

    for i in range(0, len(next)):
        if max < float(next[i]):
            max = float(next[i])

    lst = []
    keys = client.keys('*')
    hash = ""

    for key in keys:
        item = client.hgetall(key)
        lst.append(item)
        client.delete(key)

    newlst = sorted(lst, key=lambda d: float(d["USD"]))

    valueitem = newlst[-1]

    hash = valueitem["Hash"]
    times = valueitem["Time"]
    btc = valueitem["BTC"]
    dollars = valueitem["USD"]
    
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
    database = mongo_client["database"]
    collection = database["bitcoin"]

    dict = {
        "Hash": hash,
        "Time": times,
        "BTC": btc,
        "USD": dollars
    }

    x = collection.insert_one(dict)

    starttime = time.time()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))