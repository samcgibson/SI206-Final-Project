from nba_api.live.nba.endpoints import playbyplay
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.static import teams
from nba_api.stats.static import players
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

# def make_games_table(list, cur, conn):
#     cur.execute("CREATE TABLE IF NOT EXISTS Games (game_id INTEGER PRIMARY KEY, day INTEGER, time INTEGER, home_team_id INTEGER, away_team_id INTEGER, winner_id INTEGER, score_diff INTEGER)")

#     cur.execute("SELECT COUNT(*) FROM Games")
#     result = cur.fetchone()[0]

#     for i in range(result, result + 25):
#         if i >= len(list):
#             break
#         box = boxscore.BoxScore(list[i])
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
#         print(f'Row {i + 1} inserted.')
    
#     conn.commit()

# make_games_table(gameIdList, cur, conn)

# def make_players_table(list, cur, conn):
#     cur.execute("CREATE TABLE IF NOT EXISTS Players (player_id INTEGER PRIMARY KEY, player_name TEXT UNIQUE)")

#     cur.execute("SELECT COUNT(*) FROM Players")
#     result = cur.fetchone()[0]

#     for i in range(result, result + 25):
#         if i >= len(list):
#             break
#         pbp = playbyplay.PlayByPlay(list[i])
#         data = pbp.get_dict()
#         for shot in data['game']['actions']:
#             if shot['period'] == 1 and shot.get('shotResult') == 'Made':
                
#                 pname = shot['playerNameI']
#                 pid = shot['personId']
#                 break

#         cur.execute("INSERT OR IGNORE INTO Players (player_id, player_name) VALUES (?, ?)", (pid, pname))
#         print(f'Inserted {pname} ({pid}) into the database (Row {i +1}).')   

#     conn.commit()

#     cur.execute("SELECT COUNT(*) FROM Players")
#     num_rows = cur.fetchone()[0]
#     if num_rows == 78:
#         print("----All players added----")

# make_players_table(gameIdList, cur, conn)

cur.execute('DROP TABLE Teams')