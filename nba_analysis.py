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

sb.set_theme(style="white")

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'NBA.db')
cur = conn.cursor()


def make_conversion_graph(cur):
    cur.execute("SELECT DISTINCT Games.day, Teams.team_name, FirstBuckets.team_id, Games.winner_id, Games.score_diff "
                "FROM Games JOIN FirstBuckets ON Games.game_id = FirstBuckets.game_id "
                "JOIN Teams ON Teams.team_id = FirstBuckets.team_id "  
                "ORDER BY Games.day ")
    tuples = []

    for row in cur:
        if row[2] == row[3]:
            tuples.append(row + ('Won',))
        else:
            tuples.append(row + ('Lost',))

    df = pd.DataFrame(tuples, columns=['day', 'team', 'team_id', 'winner_id', 'Score Difference', 'Result'])

    g = sb.scatterplot(data = df, x = 'day', y = 'team', hue = 'Result', size = 'Score Difference', sizes=(20, 300), alpha=.75, palette="muted", legend='brief')
    sb.move_legend(
        g, "lower center",
        bbox_to_anchor=(.5, .975), ncol=3, title=None, frameon=False,
)
    plt.xlabel('Games in February 2023 (by date)')
    plt.ylabel('Team')

    plt.grid()
    plt.show()

make_conversion_graph(cur)

def make_shotdistance_graph(cur):

    cur.execute("SELECT DISTINCT Players.player_name, Games.game_id, FirstBuckets.team_id, Games.winner_id, FirstBuckets.shot_distance, FirstBuckets.points, Teams.team_name "
                "FROM FirstBuckets JOIN Players ON FirstBuckets.player_id = Players.player_id "
                "JOIN Games ON FirstBuckets.game_id = Games.game_id "
                "JOIN Teams ON FirstBuckets.team_id = Teams.team_id ")

    tuples = []

    for row in cur:
        if row[2] == row[3]:
            tuples.append(row + ('Won',))
        else:
            tuples.append(row + ('Lost',))


    df = pd.DataFrame(tuples)

    sb.scatterplot(data=df, x=1, y = 4, hue=7, palette= ['mediumseagreen', 'orangered'])

    plt.xlabel('Games in February 2023 (by Game ID)')
    plt.ylabel('Shot Distance (by ft.)')

    plt.title('First Basket Shot Distance vs. Game Outcome')
    plt.show()

make_shotdistance_graph(cur)