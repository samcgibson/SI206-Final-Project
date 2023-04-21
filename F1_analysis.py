import requests
import json
import sqlite3
import os
from matplotlib import pyplot as plt
import numpy as np

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn



def create_SPFP_plot(cur):
    x_lst = []
    y_lst = []
    cur.execute('SELECT DISTINCT Starting_Position, AVG(Finishing_Position) AS Avg_FP FROM Finishes GROUP BY Starting_Position')
    for row in cur:
        x_lst.append(row[0])
        y_lst.append(row[1])
    plt.scatter(x_lst,y_lst)
    z = np.polyfit(x_lst, y_lst, 2)
    p = np.poly1d(z)
    plt.xlabel("Starting Position")
    plt.ylabel("Finishing Likelihood")
    plt.plot(x_lst, p(x_lst))
    plt.show()

def create_crash_plot(cur):
    x_lst = []
    y_lst = []
    cur.execute('SELECT DISTINCT Starting_Position, AVG(Status) AS FP_pct FROM Finishes GROUP BY Starting_Position')
    for row in cur:
        x_lst.append(row[0])
        y_lst.append(row[1])
    plt.scatter(x_lst, y_lst)
    plt.xlabel("Starting Position")
    plt.ylabel("Finishing Likelihood")
    plt.show()

def create_leaderboards_csv(cur, results = 10):
    f = open('Finishing_pct.csv', 'w')
    f.write('Race, Finishing_pct')
    f.write('\n')
    cur.execute('SELECT Race, AVG(Status) AS FP_pct FROM Finishes JOIN Race_ids ON Finishes.Race_Location = Race_ids.primary_key GROUP BY Race_Location ORDER BY FP_pct LIMIT {}'.format(results))
    
    for row in cur:
        string = row[0] + "," + str(round(row[1], 3)*100) + "%"
        f.write(string)
        f.write('\n')

def create_csv(cur, filename):
    f = open(filename, 'w')
    header = 'Name,Race_Location,Starting_Position,Finishing_Position,Status'
    f.write(header)
    f.write('\n')

    cur.execute('SELECT Driver_ids.Name, Race_ids.Race, Finishes.Starting_Position, Finishes.Finishing_Position, Finishes.Status FROM Finishes JOIN Driver_ids ON Finishes.Name = Driver_ids.primary_key        JOIN Race_ids ON Finishes.Race_Location = Race_ids.primary_key' )
    
    for row in cur:
        string = ''
        for i in row:
            if i == row[-1]:
                if i == '1':
                    string += 'yes'
                else:
                    string += 'no'
            else:
                string += str(i)
            string += ','
        f.write(string)
        f.write('\n')


    

### Initialize DB

cur, conn = setUpDatabase('Driver_index.db')

create_csv(cur,'F1.csv')


## How finishing position is affected by starting position on average

create_SPFP_plot(cur)

### How chance of crashing is affected by starting position

create_crash_plot(cur)


### Which races have the lowest finishing rate?

create_leaderboards_csv(cur)







