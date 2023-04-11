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

# cur.execute('DROP TABLE SportsArticles')
# cur.execute('DROP TABLE PrintStatus')

apikey = 'l2OgQ2UpixpbiGjUPhXIooxmVBExphRS'

url = f'https://api.nytimes.com/svc/archive/v1/2023/3.json?api-key={apikey}'
r = requests.get(url)
articlesjson = r.json()

alist = []

for article in articlesjson['response']['docs']:
    if article['news_desk'] == 'Sports' and article['document_type'] == 'article' and article['word_count']:
        alist.append(article)

def create_sportsarticles_table(lst, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS SportsArticles (id INTEGER PRIMARY KEY AUTOINCREMENT, headline TEXT UNIQUE, pub_date INTEGER, print_page INTEGER, word_count INTEGER, print_status INTEGER)')
    cur.execute("SELECT COUNT(*) FROM SportsArticles")
    result = cur.fetchone()[0]

    for i in range(result, result + 25):
        if i >= len(lst):
            break
        pday = int(lst[i]['pub_date'].split('T')[0].replace('-', ''))   
        hline = lst[i]['headline']['main']
        pnum = int(lst[i].get('print_page', 0))
        wc = lst[i]['word_count']
        if pnum == 0:
            cur.execute('INSERT OR IGNORE INTO SportsArticles (headline, pub_date, print_page, word_count, print_status) VALUES (?, ?, ?, ?, ?)', (hline, pday, pnum, wc, pnum))
        else:
            cur.execute('INSERT OR IGNORE INTO SportsArticles (headline, pub_date, print_page, word_count, print_status) VALUES (?, ?, ?, ?, ?)', (hline, pday, pnum, wc, 1))

        print(f'Added article #{i+1}.')

    conn.commit()

create_sportsarticles_table(alist, cur, conn)

def create_printstatus_table(cur, conn):

    cur.execute('CREATE TABLE IF NOT EXISTS PrintStatus (status_id INTEGER PRIMARY KEY, status TEXT UNIQUE)')
    
    for i in range(2):
        if i == 0:
            cur.execute('INSERT OR IGNORE INTO PrintStatus (status_id, status) VALUES (?, ?)', (i, 'Not Printed'))
        if i == 1:
            cur.execute('INSERT OR IGNORE INTO PrintStatus (status_id, status) VALUES (?, ?)', (i, 'Printed'))

    conn.commit()

create_printstatus_table(cur, conn)
