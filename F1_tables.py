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

def create_driver_id_table(cur, conn):
    url = 'http://ergast.com/api/f1/2015/drivers.json?'
    response = requests.get(url)

    a = response.content

    my_json = a.decode('utf8').replace("'", '"')

    data = json.loads(my_json)

    driver_lst = []

    for row in data['MRData']['DriverTable']['Drivers']:
        driver_lst.append((row['driverId']))
    

    cur.execute('CREATE TABLE IF NOT EXISTS Driver_ids (primary_key INTEGER PRIMARY KEY, Name TEXT)')
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM Driver_ids")
    result = cur.fetchone()[0]

    for i in range(result, result + 25):
        if i >= len(driver_lst):
            break
        cur.execute('INSERT OR IGNORE INTO Driver_ids (primary_key, Name) VALUES (?,?)',(i, driver_lst[i]))
    conn.commit()


def create_race_location_id_table(cur, conn):
    url = 'http://ergast.com/api/f1/2015.json?'
    response = requests.get(url)

    a = response.content

    my_json = a.decode('utf8').replace("'", '"')

    data = json.loads(my_json)

    race_lst = []

    for row in data['MRData']['RaceTable']['Races']:
        race_lst.append((row['raceName']))
    

    cur.execute('CREATE TABLE IF NOT EXISTS Race_ids (primary_key INTEGER PRIMARY KEY, Race TEXT)')
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM Race_ids")
    result = cur.fetchone()[0]

    for i in range(result, result + 25):
        if i >= len(race_lst):
            break
        cur.execute('INSERT OR IGNORE INTO Race_ids (primary_key, Race) VALUES (?,?)',(i, race_lst[i]))
    conn.commit()


def create_status_id_table(cur, conn):
    url = 'https://ergast.com/api/f1/2015/results.json?'
    response = requests.get(url)

    a = response.content

    my_json = a.decode('utf8').replace("'", '"')

    data = json.loads(my_json)

    status_lst = []

    cur.execute('SELECT * FROM Driver_ids')
    driver_lst = []
    for row in cur:
        driver_lst.append(row[1])

    for driver in driver_lst:
        data = create_driver_dict(driver)
        for round in data['MRData']['RaceTable']['Races']:
                if round['Results'][0]['status'] not in status_lst:
                    status_lst.append(round['Results'][0]['status'])
    

    cur.execute('CREATE TABLE IF NOT EXISTS Status_ids (finish_key INT, Status TEXT)')
    conn.commit()

    

    for a in range(2):
        cur.execute("SELECT COUNT(*) FROM Status_ids")
        result = cur.fetchone()[0]
        for i in range(result, result + 25):
            if i >= len(status_lst):
                break
            cur.execute('INSERT OR IGNORE INTO Status_ids (finish_key, Status) VALUES (?,?)',(0, status_lst[i]))
        conn.commit()

    cur.execute("UPDATE Status_ids SET finish_key = 1 WHERE Status = 'Finished' OR Status = '+1 Lap' OR Status = '+2 Laps' OR Status = '+6 Laps'")
    conn.commit()





def create_driver_dict(driver):
    url = 'http://ergast.com/api/f1/2015/drivers/{}/results.json?'.format(driver)
    response = requests.get(url)

    a = response.content

    my_json = a.decode('utf8').replace("'", '"')

    data = json.loads(my_json)

    return data


def create_finishes_table(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS Finishes (Name TEXT, Race_Location TEXT, Starting_Position INT, Finishing_Position INT, Status TEXT)')
    conn.commit()

    cur.execute('SELECT * FROM Driver_ids')
    driver_lst = []
    for row in cur:
        driver_lst.append(row[1])

    data_lst = []
    for driver in driver_lst:
        data = create_driver_dict(driver)
        for round in data['MRData']['RaceTable']['Races']:
                data_lst.append((2015, round['Results'][0]['Driver']['driverId'], round['raceName'], int(round['Results'][0]['grid']), int(round['Results'][0]['position']), round['Results'][0]['status']))


    cur.execute("SELECT COUNT(*) FROM Finishes")
    result = cur.fetchone()[0]
    data = create_driver_dict(driver)
    for i in range(result, result + 25):
        if i >= len(data_lst):
            break
        cur.execute('INSERT INTO Finishes (Name, Race_Location, Starting_Position, Finishing_Position, Status) VALUES (?,?,?,?,?)',(data_lst[i][1],data_lst[i][2],data_lst[i][3],data_lst[i][4],data_lst[i][5]))
    conn.commit()




def create_final_table(cur, conn):
    ## update drivers
    drivers_lst = []
    cur.execute('SELECT * FROM Driver_ids')
    for row in cur:
        drivers_lst.append((row[0],row[1]))


    for i in drivers_lst:
        string = "UPDATE Finishes SET Name = '{}' WHERE Name = '{}'".format(i[0], i[1])
        cur.execute(string)
    conn.commit()
    
    ## update races

    race_lst = []
    cur.execute('SELECT * FROM Race_ids')
    for row in cur:
        race_lst.append((row[0],row[1]))


    for i in race_lst:
        string = "UPDATE Finishes SET Race_Location = '{}' WHERE Race_Location = '{}'".format(i[0], i[1])
        cur.execute(string)
    conn.commit()

    ## update statuses

    status_lst = []
    cur.execute('SELECT * FROM Status_ids')
    for row in cur:
        status_lst.append((row[0],row[1]))


    for i in status_lst:
        string = "UPDATE Finishes SET Status = '{}' WHERE Status = '{}'".format(i[0], i[1])
        cur.execute(string)
    conn.commit()



cur, conn = setUpDatabase('F1.db')

## Create table for drivers' ids
create_driver_id_table(cur, conn)

## Create table for race ids
create_race_location_id_table(cur, conn)

create_status_id_table(cur,conn)


for i in range(12):
    create_finishes_table(cur,conn)

create_final_table(cur, conn)