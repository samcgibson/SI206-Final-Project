import sqlite3
import json
import os
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import numpy as np
import random
import string
from PIL import Image

sb.set_theme(style="white")

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'NBA.db')
cur = conn.cursor()

def make_basic_charts(cur):
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

    cur.execute("SELECT FirstBuckets.points, ShotTypes.shot_type FROM FirstBuckets JOIN ShotTypes ON FirstBuckets.points = ShotTypes.points")

    dct = {
        'Free Throw': 0,
        '2-Pointer': 0,
        '3-Pointer': 0,
    }

    for row in cur:
        dct[row[1]] += 1

    labels = list(dct.keys())
    values = list(dct.values())

    axs[0].pie(values, labels=labels, autopct='%1.2f%%')
    axs[0].axis('equal')
    axs[0].set_title('First Basket Shot Type Distribution')

    cur.execute("SELECT FirstBuckets.points, ShotTypes.shot_type, FirstBuckets.team_id, Games.winner_id FROM FirstBuckets "
                "JOIN ShotTypes ON FirstBuckets.points = ShotTypes.points "
                "JOIN Games ON FirstBuckets.game_id = Games.game_id")
    
    tuples = []

    for row in cur:
        if row[2] == row[3]:
            tuples.append(row + ('Won',))
        if row[2] != row[3]:
            tuples.append(row + ('Lost',))

    df = pd.DataFrame(tuples, columns=['points', 'shot_type', 'team', 'winner', 'Outcome'])

    df.to_csv('basic_charts.csv')

    sb.histplot(data = df, y = df['shot_type'], hue = df['Outcome'], multiple='stack', palette= ['mediumseagreen', 'red'])

    axs[1].set_xlabel('Occurences in February 2023 Games')
    axs[1].set_ylabel('')
    axs[1].set_title('First Basket Shot Type vs. Game Outcome')
    fig.tight_layout()

    plt.show()

make_basic_charts(cur)

def make_shotdistance_graph(cur): 

    cur.execute("SELECT DISTINCT Games.game_id, FirstBuckets.team_id, Games.winner_id, FirstBuckets.shot_distance, FirstBuckets.points, Teams.team_name "
                "FROM FirstBuckets "
                "JOIN Games ON FirstBuckets.game_id = Games.game_id "
                "JOIN Teams ON FirstBuckets.team_id = Teams.team_id ")

    tuples = []

    for row in cur:
        if row[1] == row[2]:
            tuples.append(row + ('Won',))
        else:
            tuples.append(row + ('Lost',))


    df = pd.DataFrame(tuples)

    df.to_csv('shot_distance.csv')

    sb.scatterplot(data=df, x=0, y = 3, hue=6, palette= ['mediumseagreen', 'red'])

    plt.xlabel('Games in February 2023 (by Game ID)')
    plt.ylabel('Shot Distance (by ft.)')

    plt.title('First Basket Shot Distance vs. Game Outcome')
    plt.show()

make_shotdistance_graph(cur)

def make_shotchart(cur):
    cur.execute("SELECT FirstBuckets.xpos, FirstBuckets.ypos, FirstBuckets.game_id, FirstBuckets.team_id, Games.home_team_id FROM FirstBuckets JOIN Games ON FirstBuckets.game_id = Games.game_id")

    tuples = []

    for row in cur:
        if row[3] == row[4]:
            tuples.append(row + ('Home', ))
        if row[3] != row[4]:
            tuples.append(row + ('Away', ))

    ftpos_home = {'xpos': 20.21, 'ypos': 50}
    ftpos_away = {'xpos': 79.79, 'ypos': 50}

    df = pd.DataFrame(tuples, columns=['xpos', 'ypos', 'game_id', 'team_id', 'hometeam_id', 'Status'])

    df.to_csv('shot_chart.csv')

    pd.set_option('display.max_rows', 1000)

    df.loc[df['Status'] == 'Home', ['xpos', 'ypos']] = df.loc[df['Status'] == 'Home', ['xpos', 'ypos']].fillna(value=ftpos_home)
    df.loc[df['Status'] == 'Away', ['xpos', 'ypos']] = df.loc[df['Status'] == 'Away', ['xpos', 'ypos']].fillna(value=ftpos_away)

    sb.set(rc={"figure.figsize":(9.4, 5)})

    g = sb.scatterplot(x = 'xpos', y = 'ypos', s=80, hue = 'Status', data=df, palette=['#1D42BA', '#C8102E'])
    ax = plt.gca()

    ax.set_xticks([])
    ax.set_yticks([])
    plt.xlabel('94 ft.')
    plt.ylabel('50 ft.')
    plt.title('NBA First Basket (Made) Shot Chart')
    plt.show()

make_shotchart(cur)

def make_conversion_graph(cur):
    cur.execute("SELECT DISTINCT Games.day, Teams.team_name, FirstBuckets.team_id, Games.winner_id, Games.score_diff "
                "FROM Games JOIN FirstBuckets ON Games.game_id = FirstBuckets.game_id "
                "JOIN Teams ON Teams.team_id = FirstBuckets.team_id "  
                "ORDER BY Games.day ")
    
    tuples = []
    scorediffwinlist = []
    scoredifflostlist = []

    for row in cur:
        if row[2] == row[3]:
            tuples.append(row + ('Won',))
            scorediffwinlist.append(str(row[4]) + ":won")
        else:
            tuples.append(row + ('Lost',))
            scoredifflostlist.append(str(row[4]) + ":lost")

    df = pd.DataFrame(tuples, columns=['day', 'team', 'team_id', 'winner_id', 'Score Difference', 'Result'])

    sb.set(rc={"figure.figsize":(12, 7.5)})

    plot_order = df.sort_values(by='Score Difference', ascending=False)

    plot_order.to_csv('conversion_graph.csv')

    g = sb.scatterplot(data = plot_order, x = 'day', y = 'team', hue = 'Result', size = 'Score Difference', sizes=(20, 500), alpha=.95, palette=["#1D42BA", "#C8102E"], legend='brief')
    g.legend_.set_title(None)
    g.legend_.texts[0].set_text('Lost')
    g.legend_.texts[1].set_text('Won')
    g.legend_.get_frame().set_linewidth(0.0)
    g.legend_.get_frame().set_edgecolor('gray')
    g.legend_.get_frame().set_facecolor('white')
    g.legend_.get_frame().set_alpha(0.6)
    g.legend_.shadow = True
    
    plt.grid()
    plt.xlabel('Games in February 2023 (by date)')
    plt.ylabel('Team')
    plt.suptitle('Teams Ability to Win After Getting First Basket')
    plt.title('Size of circle is how much team won / lost by. The large gap in data is during All-Star Weekend.')
    plt.tight_layout()
    plt.grid()
    plt.show()

    lossdenom = len(scoredifflostlist)
    windenom = len(scorediffwinlist)

    scorewtotal = 0
    scoreltotal = 0

    for sdiff in scoredifflostlist:
        scoreltotal += int(sdiff.split(':')[0])

    for sdiff in scorediffwinlist:
        scorewtotal += int(sdiff.split(':')[0])

    print(f'Average score difference (win) when getting first basket: {round((scorewtotal / windenom), 2)}.')
    print(f'Average score difference (loss) when getting first basket: {round((scoreltotal / lossdenom), 2)}.')

make_conversion_graph(cur)