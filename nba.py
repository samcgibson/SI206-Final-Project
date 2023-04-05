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
# cur.execute("DROP TABLE Games")


# def make_games_table(list, cur, conn):
#     cur.execute("CREATE TABLE IF NOT EXISTS Games (game_id INTEGER PRIMARY KEY, day INTEGER, time INTEGER, home_team_id INTEGER, away_team_id INTEGER, winner_id INTEGER, score_diff INTEGER)")
#     for gameId in list:
#         box = boxscore.BoxScore(gameId)
#         data = box.get_dict()
#         gid = int(data['game']['gameId'])
#         date = data['game']['gameTimeLocal'].split("T")[0]
#         date = int(date.replace('-', ''))
#         time = data['game']['gameTimeLocal'].split("T")[1]
#         time = time.split('-')[0]
#         time = int(time.replace(':', '')[:-2])
#         homeid = data['game']['homeTeam']['teamId']
#         awayid = data['game']['awayTeam']['teamId']

#         if data['game']['homeTeam']['score'] > data['game']['awayTeam']['score']:
#             winnerid = homeid
#             scorediff = data['game']['homeTeam']['score'] - data['game']['awayTeam']['score']
#         else:
#             winnerid = awayid
#             scorediff = data['game']['awayTeam']['score'] - data['game']['homeTeam']['score']
        
#         cur.execute("INSERT OR IGNORE INTO Games (game_id, day, time, home_team_id, away_team_id, winner_id, score_diff) VALUES (?, ?, ?, ?, ?, ?, ?)", (gid, date, time, homeid, awayid, winnerid, scorediff))
#     conn.commit()

# def make_teams_table(cur, conn):
#     teamlist = teams.get_teams()
#     cur.execute("CREATE TABLE IF NOT EXISTS Teams (team_id INTEGER PRIMARY KEY, team_name TEXT UNIQUE)")
#     for team in teamlist:
#         cur.execute("INSERT OR IGNORE INTO Teams (team_id, team_name) VALUES (?, ?)", (team['id'], team['full_name']))

#     conn.commit()

# make_teams_table(cur, conn)
# make_games_table(gameIdList, cur, conn)

def make_players_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Players (player_id INTEGER PRIMARY KEY, player_name TEXT UNIQUE)")
    playerlist = players.get_players()
    for player in playerlist:
        if player['is_active'] == True:
            cur.execute("INSERT OR IGNORE INTO Players (player_id, player_name) VALUES (?, ?)", (player['id'], player['full_name']))

    conn.commit()


make_players_table(cur, conn)
