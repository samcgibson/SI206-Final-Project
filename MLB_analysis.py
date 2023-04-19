import os
import sqlite3
import csv
import matplotlib
import matplotlib.pyplot as plt

def open_database(db_name):
    
    # This function takes a name as input (db_name, str) and opens a database
    # with that name, returning cur and conn for the database
    
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def calculate_month_win_pct(month_num, cur, conn):
    
    # This function takes the number of a month (month_num, int) and cur and conn for the
    # database as inputs and returns the win percentage for that month, rounded to three
    # decimal places. The month numbers for the inputs are as follows: 1 for January, 2
    # for February, ... 10 for October, 11 for November, etc
    
    month_list = []
    cur.execute("SELECT win_loss_outcome FROM Outcomes JOIN Games ON Games.outcome_id = Outcomes.outcome_id WHERE month = ?", (month_num,))
    outcomes = cur.fetchall()
    for outcome in outcomes:
        month_list.append(outcome[0])
    
    num_wins = month_list.count('Win')
    win_pct = num_wins / len(month_list)
    rounded_win_pct = round(win_pct, 3)
    
    return rounded_win_pct

def create_month_dict(start_month_num, end_month_num, cur, conn):
    
    # This function takes a start month number (start_month_num, int) and end month number
    # (end_month_num, int) as well as cur and conn for the database as inputs and calls
    # calculate_month_win_pct to calculate the win percentage for each month in the given
    # range. The function then returns a dictionary for every month in the given range with
    # the months (in text format) as the keys and the monthly win percentages as the values.
    # Similarly to the calculate_month_win_pct function, the month numbers for the inputs are
    # as follows: 1 for January, 2 for February, ... 10 for October, 11 for November, etc
    
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_dict = {}
    
    for month_num in range(start_month_num, end_month_num + 1):
        month_win_pct = calculate_month_win_pct(month_num, cur, conn)
        round_win_pct = format(month_win_pct, '.3f')
        
        month_dict[month_list[month_num - 1]] = round_win_pct
    
    return month_dict

def write_csv(month_dict, file_name):
    
    # This function takes the monthly win percentage dictionary returned by create_month_dict
    # (month_dict, dict) and a file name (file_name, str) as inputs and uses csv writer to write
    # a csv file to the passed file name. The header row is 'month, win_pct' and each data row
    # contains the name of the month and that month's win percentage

    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, file_name)
    f = open(full_path, 'w')
    csv_writer = csv.writer(f)
    
    header = ['month', 'win_pct']
    csv_writer.writerow(header)
    
    for tup in month_dict.items():
        csv_writer.writerow(tup)
    
    f.close()
    return None

def create_bar_graph(month_dict, figure_name):
    
    # This function takes the monthly win percentage dictionary returned by create_month_dict
    # (month_dict, dict) and a figure name (figure_name, str) as inputs and creates a bar graph
    # where each bar represents the win percentage for a different month. The title of the figure
    # is '2022 Yankees Win Percentage by Month', the x-axis is labeled 'month', and the y-axis is
    # labeled 'win percentage'
    
    months = []
    for month in month_dict:
        months.append(month)    
    
    win_pcts = []
    for pct in month_dict.values():
        win_pcts.append(float(pct))

    fig, ax = plt.subplots()
    ax.bar(months, win_pcts)
    ax.set_xlabel('month')
    ax.set_ylabel('win percentage')
    ax.set_title('2022 Yankees Win Percentage by Month')
    
    fig.savefig(figure_name)
    plt.show()

def main():
    
    # The main function calls all of the functions above, taking the data from
    # the database and using it to write a csv file that contains monthly win
    # percentages for the 2022 New York Yankees and create a bar graph which
    # represents these monthly win percentages
    
    cur, conn = open_database('MLB.db')
    yankees_win_pcts = create_month_dict(4, 10, cur, conn)
    write_csv(yankees_win_pcts, 'monthly_win_pct.csv')
    create_bar_graph(yankees_win_pcts, 'MLB_win_pct.png')

main()
