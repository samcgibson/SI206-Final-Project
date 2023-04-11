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

cur.execute('DROP TABLE SportsArticles')
cur.execute('DROP TABLE PrintStatus')