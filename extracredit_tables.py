import requests
import json
import sqlite3
import os
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

cur, conn = open_database('NYT.db')

apikey = 'l2OgQ2UpixpbiGjUPhXIooxmVBExphRS'

url = f'https://api.nytimes.com/svc/archive/v1/2023/3.json?api-key={apikey}'
r = requests.get(url)
articlesjson = r.json()

cur.execute('CREATE TABLE IF NOT EXISTS Stories (id INTEGER PRIMARY KEY AUTOINCREMENT, headline TEXT UNIQUE, pub_date INTEGER, print_page INTEGER, word_count INTEGER)')

for article in articlesjson['response']['docs']:
    if article['news_desk'] == 'Sports' and article['document_type'] == 'article' and article['word_count']:
        print(article['word_count'])

