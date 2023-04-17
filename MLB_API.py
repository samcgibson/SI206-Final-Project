import requests
import json
import sqlite3

def create_game_json(start_date, end_date):
    
    # This function uses the MLB API to return a dictionary with information about every
    # MLB game from the start date (start_date, str) to the end date (end_date, str)
    
    url = 'http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={}&endDate={}'.format(start_date, end_date)
    response = requests.get(url)
    json_file = response.content
    data = json.loads(json_file)
    
    return data

season_2022_dict = create_game_json('2022-04-07', '2022-10-05')

def return_team_games_list(data, team_name):
    
    # This function takes the dictionary returned by create_game_json (data, dict) and iterates
    # through all of the games in the dictionary, returning a list of all of the games for the
    # given team (team_name, str)
    
    # This function iterates through the list returned by return_team_games_list (game_list, list)
    # and returns a list of tuples for the given team (team_name, str), with each tuple representing
    # a separate game. Each tuple is made up of the game's date (with no hyphens), the team name, the
    # opponent, and the outcome (True if the team won, False if the team lost)
    
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
        elif game['teams']['home']['team']['name'] == team_name:
            opponent = game['teams']['away']['team']['name']
            outcome = game['teams']['home']['isWinner']
        
        game_tup = (date, opponent, outcome)
        tup_list.append(game_tup)

    return tup_list

yankees_tuple_list = return_team_games_list(season_2022_dict, 'New York Yankees')

def create_team_ids(game_tuples_list):
    
    team_id_dict = {}
    id = 1001
    for game_tup in game_tuples_list:
        if game_tup[1] not in team_id_dict:
            team_id_dict[game_tup[1]] = id
            id += 1
    
    return team_id_dict

team_ids = create_team_ids(yankees_tuple_list)

# def prepare_for_db(game_tuples_list, team_id_dict):
    






def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# cur, conn = open_database('MLB.db')

# team id table, outcome table