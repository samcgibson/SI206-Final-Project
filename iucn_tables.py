import requests
import json
import sqlite3
import os
from matplotlib import pyplot as plt
import seaborn as sb
import numpy as np

apikey = 

def get_countries(key):
    url = f'https://www.iucnredlist.org/api/ve/country/list?token={apikey}'
    r = requests.get(url)
    a = r.content
    data = json.loads(a)

    for row in data:
        print(row)

get_countries(apikey)