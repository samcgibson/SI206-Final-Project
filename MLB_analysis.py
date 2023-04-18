import os
import sqlite3

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

cur, conn = open_database('MLB.db')

def calculate_month_win_pct(month_num, cur, conn):
    
    #takes the number of a month and returns the win pct for that month, rounded to three decimal places ( and tuple with num_games? )
    
    month_list = []
    cur.execute("SELECT win_loss_outcome FROM Outcomes JOIN Games ON Games.outcome_id = Outcomes.outcome_id WHERE month = ?", (month_num,))
    outcomes = cur.fetchall()
    for outcome in outcomes:
        month_list.append(outcome[0])
    
    num_wins = month_list.count('Win')
    win_pct = num_wins / len(month_list)
    rounded_win_pct = round(win_pct, 3)
    
    return rounded_win_pct
    
april = calculate_month_win_pct(4, cur, conn)

def create_month_dict(start_month, end_month):
    
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_dict = {}
    
    for month_num in range(start_month, end_month + 1):
        month_win_pct = calculate_month_win_pct(month_num, cur, conn)
        round_win_pct = format(month_win_pct, '.3f')
        
        month_dict[month_list[month_num - 1]] = round_win_pct
    
    return month_dict

print(create_month_dict(4, 10))

# def write_csv(month_dict):

# def create_plot()
    
    

    