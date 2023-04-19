import requests
import json
import os
import sqlite3

def create_game_json(start_date, end_date):
    
    # This function takes a start date (start_date, str) and end date (end_date, str)
    # as inputs and uses the MLB API to return a dictionary with information about
    # every MLB game from the start date to the end date
    
    url = 'http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={}&endDate={}'.format(start_date, end_date)
    response = requests.get(url)
    json_file = response.content
    data = json.loads(json_file)
    
    return data

def return_team_games_list(data, team_name):
    
    # This function takes the dictionary returned by create_game_json (data, dict) and a team name
    # (team_name, str) as inputs and iterates through all of the games in the dictionary, creating
    # a list of all of the games for the given team. The function then iterates through that list
    # and returns a list of tuples for the given team, with each tuple representing a separate game.
    # Each tuple is made up of the game's date (with no hyphens), the opponent team name, and the outcome
    
    game_list = []
    for date in data['dates']:
        for game in date['games']:
            if game['teams']['away']['team']['name'] == team_name or game['teams']['home']['team']['name'] == team_name:
                if game['status']['detailedState'] == 'Final' or game['status']['detailedState'] == 'Completed Early':
                    game_list.append(game)
    
    tup_list = []
    for game in game_list:
        date = game['officialDate'].replace('-', '')
        if game['teams']['away']['team']['name'] == team_name:
            opponent = game['teams']['home']['team']['name']
            outcome = game['teams']['away']['isWinner']
            if outcome == True:
                win_loss = "Win"
            elif outcome == False:
                win_loss = "Loss"
        elif game['teams']['home']['team']['name'] == team_name:
            opponent = game['teams']['away']['team']['name']
            outcome = game['teams']['home']['isWinner']
            if outcome == True:
                win_loss = "Win"
            elif outcome == False:
                win_loss = "Loss"
        
        game_tup = (date, opponent, win_loss)
        tup_list.append(game_tup)

    return tup_list

def create_team_ids(game_tuples_list):
    
    # This function takes the list of tuples returned by return_team_games_list
    # (game_tuples_list, list) as an input, iterating through the list to return a
    # dictionary with id numbers representing every opponent that the team played: 1001
    # for the first team, 1002 for the second team, 1003 for the third team, and so on
    
    team_id_dict = {}
    id = 1001
    for game_tup in game_tuples_list:
        if game_tup[1] not in team_id_dict:
            team_id_dict[game_tup[1]] = id
            id += 1
    
    return team_id_dict

def open_database(db_name):
    
    # This function takes a name as input (db_name, str) and opens a database
    # with that name, returning cur and conn for the database
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def make_teams_table(teams, cur, conn):
    
    # This function takes the dictionary returned by create_team_ids (teams, dict) and
    # cur and conn for the database as inputs and creates a table in the database with
    # each row consisting of the team id number and the team name
    
    cur.execute("CREATE TABLE IF NOT EXISTS Teams (team_id INTEGER PRIMARY KEY, team_name TEXT)")
    
    for team in teams.items():
        team_id = team[1]
        team_name = team[0]
        
        cur.execute("INSERT OR IGNORE INTO Teams (team_id, team_name) VALUES (?,?)", (team_id, team_name,))
    
    conn.commit()

def make_outcomes_table(cur, conn):
    
    # This function takes cur and conn for the database as inputs and creates a table 
    # in the database with two rows, each consisting of an outcome id and a game outcome:
    # the first row has an outcome id of 1, which represents 'Win', and the second row
    # has an outcome id of 2, which represents 'Loss'
    
    cur.execute("CREATE TABLE IF NOT EXISTS Outcomes (outcome_id INTEGER PRIMARY KEY, win_loss_outcome TEXT)")
    
    cur.execute("INSERT OR IGNORE INTO Outcomes (outcome_id, win_loss_outcome) VALUES (?,?)", (1, "Win"))
    cur.execute("INSERT OR IGNORE INTO Outcomes (outcome_id, win_loss_outcome) VALUES (?,?)", (2, "Loss"))
    
    conn.commit()

def make_games_table(game_tuples_list, cur, conn):
    
    # This function takes the list of tuples returned by return_team_games_list (game_tuples_list, list)
    # and cur and conn for the database as inputs and creates a table in the database representing all
    # of the games, adding a maximum of 25 rows of data at a time. Each row of data in the table has the
    # game number, month, day, opponent id, and outcome id for the game
    
    cur.execute("CREATE TABLE IF NOT EXISTS Games (game_number INTEGER PRIMARY KEY, month INTEGER, day INTEGER, opponent_id INTEGER, outcome_id INTEGER)")
    
    cur.execute("SELECT COUNT(*) FROM Games")
    result = cur.fetchone()[0]
        
    if result < (len(game_tuples_list) - 25):
        for i in range(result, result + 25):
            game_id = i + 1
                    
            month = int(game_tuples_list[i][0][4:6])
            day = int(game_tuples_list[i][0][6:])

            opponent = game_tuples_list[i][1]
            cur.execute("SELECT team_id FROM Teams WHERE team_name = ?", (opponent,))
            opponent_id = cur.fetchone()[0]
                
            outcome = game_tuples_list[i][2]
            cur.execute("SELECT outcome_id FROM Outcomes WHERE win_loss_outcome = ?", (outcome,))
            outcome_id = cur.fetchone()[0]
                
            cur.execute("INSERT OR IGNORE INTO Games (game_number, month, day, opponent_id, outcome_id) VALUES (?,?,?,?,?)", (game_id, month, day, opponent_id, outcome_id,))
    
    else:
        for i in range(result, len(game_tuples_list)):
            game_id = i + 1
                    
            month = int(game_tuples_list[i][0][4:6])
            day = int(game_tuples_list[i][0][6:])

            opponent = game_tuples_list[i][1]
            cur.execute("SELECT team_id FROM Teams WHERE team_name = ?", (opponent,))
            opponent_id = cur.fetchone()[0]
                
            outcome = game_tuples_list[i][2]
            cur.execute("SELECT outcome_id FROM Outcomes WHERE win_loss_outcome = ?", (outcome,))
            outcome_id = cur.fetchone()[0]
                
            cur.execute("INSERT OR IGNORE INTO Games (game_number, month, day, opponent_id, outcome_id) VALUES (?,?,?,?,?)", (game_id, month, day, opponent_id, outcome_id,))            
        
    conn.commit()
    
def main():
    
    # The main function calls all of the functions above, taking the data for all of the
    # games that the New York Yankees played in the 2022 season and creating a database
    # to represent this data
    
    season_2022_dict = create_game_json('2022-04-07', '2022-10-05')
    yankees_tuple_list = return_team_games_list(season_2022_dict, 'New York Yankees')
    team_ids = create_team_ids(yankees_tuple_list)
    
    cur, conn = open_database('MLB.db')
    make_teams_table(team_ids, cur, conn)
    make_outcomes_table(cur, conn)
    make_games_table(yankees_tuple_list, cur, conn)

main()
