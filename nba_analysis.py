import sqlite3
import json
import os
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd

sb.set()

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'NBA.db')
cur = conn.cursor()

# cur.execute("SELECT FirstBuckets.player_id, Players.player_name, FirstBuckets.shot_distance, FirstBuckets.points, FirstBuckets.team_id FROM FirstBuckets JOIN Players ON FirstBuckets.player_id = Players.player_id")

# firstbucketlist = []
# for row in cur:
#     print(row)
#     firstbucketlist.append((row[1], row[2]))

# firstbucketdict = dict(firstbucketlist)

cur.execute("SELECT DISTINCT Players.player_name, Games.game_id, FirstBuckets.team_id, Games.winner_id, FirstBuckets.shot_distance, FirstBuckets.points, Teams.team_name "
            "FROM FirstBuckets JOIN Players ON FirstBuckets.player_id = Players.player_id "
            "JOIN Games ON FirstBuckets.game_id = Games.game_id "
            "JOIN Teams ON FirstBuckets.team_id = Teams.team_id ")

tuples = []

for row in cur:
    if row[2] == row[3]:
        tuples.append(row + ('won',))
    else:
        tuples.append(row + ('lost',))

# print(tuples)



# firstbucketdict = dict(Counter(firstbucketlist))

# sorted_dict = dict(sorted(firstbucketdict.items(), key=lambda x: x[1], reverse=True))

df = pd.DataFrame(tuples)

sb.lineplot(data=df, x=1, y = 4, hue=7)

plt.show()
