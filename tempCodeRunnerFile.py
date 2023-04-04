from nba_api.live.nba.endpoints import playbyplay
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.static import teams

import time
import re
import sqlite3
import json
import os

october18 = '0022200001' # first game of the regular season october 18th, 2022
january1 = '022200547'
january31 = '0022200768'
february1 = '0022200770'
february28 = '0022200932'
march22 = '0022201092' # last game on march 22nd, 2023
#test

gameIdList = []
for id in range(int(february1), int(february28) + 1): # add game IDs to gamelist
    gameIdList.append("00" + str(id)) # have to add '00' here because integers don't allow leading 0's

firstbucketsdict = {}
firstbucketslist = []

# for gameId in gameIdList:
#     pbp = playbyplay.PlayByPlay(gameId)
#     pbpdict = pbp.get_dict()
#     pbpjson = pbp.get_json()
    
    # box = boxscore.BoxScore(gameId)
    # bdict = box.get_dict()
    # bjson = box.get_json()

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

cur, conn = open_database('NBA.db')
cur.execute("DROP TABLE Games")