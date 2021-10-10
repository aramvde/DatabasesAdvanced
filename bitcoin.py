from bs4 import BeautifulSoup
import requests
import time
import csv
import re
import pandas as pd
from request import Scrape
from timer import Timer

while True:    
    scraper = Scrape()
    scraper.text_list()

    timer = Timer()
    timer.starttime()

