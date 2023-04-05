from nba_api.live.nba.endpoints import playbyplay
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.static import teams
from nba_api.stats.static import players


import time
import re
import sqlite3
import json
import os

february1 = '0022200770'
february28 = '0022200932'

gameIdList = []
for id in range(int(february1), int(february28) + 1): # add game IDs to gamelist
    gameIdList.append("00" + str(id)) # have to add '00' here because integers don't allow leading 0's

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

cur, conn = open_database('NBA.db')
cur.execute("DROP TABLE Games")
