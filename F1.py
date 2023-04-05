import requests
import json
import sqlite3
import os
from matplotlib import pyplot as plt
import numpy as np

##create json

def create_driver_lst(year):
    url = 'http://ergast.com/api/f1/{}/drivers.json?'.format(str(year))
    response = requests.get(url)

    a = response.content

    my_json = a.decode('utf8').replace("'", '"')

    data = json.loads(my_json)

    driver_lst = []

    for row in data['MRData']['DriverTable']['Drivers']:
        driver_lst.append(row['driverId'])
    
    return driver_lst

# create_driver_lst(2009)

def create_driver_dict(year, driver):
    url = 'http://ergast.com/api/f1/{}/drivers/{}/results.json?'.format(str(year), driver)
    response = requests.get(url)

    a = response.content

    my_json = a.decode('utf8').replace("'", '"')

    data = json.loads(my_json)

    json_data = json.dumps(data, indent=4)

    return data

create_driver_dict(2008, 'hamilton')
# print(test)

# for yr in range(2000,2016,1):
#     driver_lst = create_driver_lst(yr)
#     for driver in driver_lst:
#         driver_data = create_driver_dict(yr,driver)
#         for round in driver_data['MRData']['RaceTable']['Races']:
#             print(round['Results'][0]['Driver']['driverId'])
#             print(round['raceName'])
#             print(int(round['Results'][0]['position']))
            

#### setting up database (have to actually create the database now)

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def create_drivers_table(cur, conn):
    cur.execute('DROP TABLE IF EXISTS Drivers')
    cur.execute('CREATE TABLE Drivers (Year INT, Name TEXT, Race_Location TEXT, Starting_Position INT, Finishing_Position INT, Status TEXT, Finish INT)')
    conn.commit()

def add_to_drivers_table(cur, conn, start_yr, end_yr):
    for yr in range(start_yr,end_yr + 1,1):
        driver_lst = create_driver_lst(yr)
        for driver in driver_lst:
            driver_data = create_driver_dict(yr,driver)
            for round in driver_data['MRData']['RaceTable']['Races']:
                cur.execute('INSERT INTO Drivers (Year, Name, Race_Location, Starting_Position, Finishing_Position, Status, Finish) VALUES (?,?,?,?,?,?,?)',(yr, round['Results'][0]['Driver']['driverId'], round['raceName'], int(round['Results'][0]['grid']), int(round['Results'][0]['position']), round['Results'][0]['status'],0))

    conn.commit()
    cur.execute('SELECT * FROM Drivers')
    for row in cur:
        print(row)

def update_table(cur, conn):
    cur.execute("UPDATE Drivers SET Finish = 1 WHERE Status = 'Finished' OR Status = '+1 Lap' OR Status = '+2 Laps' OR Status = '+3 Laps' OR Status = '+4 Laps'")
    cur.execute('SELECT * FROM Drivers')
    # for row in cur:
    #     print(row)

def update_table_2(cur, conn):
    cur.execute("UPDATE Drivers SET Finish = 1 WHERE Status != 'Accident' OR Status != 'Collision'")
    cur.execute("UPDATE Drivers SET Finish = 0 WHERE Status = 'Accident' OR Status = 'Collision'")
    cur.execute('SELECT * FROM Drivers')
    # for row in cur:
    #     print(row)


def create_SPFP_plot(cur, conn):
    x_lst = []
    y_lst = []
    cur.execute('SELECT DISTINCT Starting_Position, AVG(Finishing_Position) AS Avg_FP FROM Drivers GROUP BY Starting_Position')
    for row in cur:
        x_lst.append(row[0])
        y_lst.append(row[1])
    plt.scatter(x_lst, y_lst)
    plt.xlabel("Starting Position")
    plt.ylabel("Finishing Position")
    plt.show()

def create_crash_plot(cur, conn):
    x_lst = []
    y_lst = []
    cur.execute('SELECT DISTINCT Starting_Position, AVG(Finish) AS FP_pct FROM Drivers GROUP BY Starting_Position')
    for row in cur:
        x_lst.append(row[0])
        y_lst.append(row[1])
    plt.scatter(x_lst, y_lst)
    z = np.polyfit(x_lst, y_lst, 2)
    p = np.poly1d(z)
    plt.xlabel("Starting Position")
    plt.ylabel("Finishing Likelihood")
    plt.plot(x_lst, p(x_lst))
    plt.show()

def create_race_crash_lead(cur, conn, results = 10):
    cur.execute('SELECT DISTINCT Race_Location, AVG(Finish) AS FP_pct FROM Drivers GROUP BY Race_Location ORDER BY FP_pct LIMIT {}'.format(results))
    for row in cur:
        print(row[0] + ": " + str(round(row[1], 3)*100) + "%")

    


cur, conn = setUpDatabase('Driver_index.db')

### Initialize DB

# create_drivers_table(cur, conn)

# add_to_drivers_table(cur, conn, 2009, 2010)

### How finishing position is affected by starting position on average

# update_table(cur, conn)

# create_SPFP_plot(cur, conn)

### How chance of crashing is affected by starting position

# update_table_2(cur, conn)

# create_crash_plot(cur, conn)


### Which races have the lowest finishing rate?

update_table_2(cur, conn)

create_race_crash_lead(cur, conn)







