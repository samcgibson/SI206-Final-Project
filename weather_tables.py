import requests
import json
import sqlite3
import os
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

apikey = '4b5e9d16-84f7-47f5-a9f4-bfbb6fd32895'

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

cur, conn = open_database('AQI.db')

def make_states_table(ak, country):
    url = f"http://api.airvisual.com/v2/states?country={country}&key={ak}"
    r = requests.request('GET', url)
    json = r.json()
       
    cur.execute('CREATE TABLE IF NOT EXISTS States (primary_key INTEGER PRIMARY KEY, state TEXT UNIQUE)')

    c = 1
    for state in json['data']:
        cur.execute('INSERT OR IGNORE INTO States (primary_key, state) VALUES (?, ?)', (c, state['state']))
        c+=1

    conn.commit()

make_states_table(apikey, 'USA')