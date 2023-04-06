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

cur.execute("SELECT FirstBuckets.player_id, Players.player_name, FirstBuckets.shot_distance, FirstBuckets.points FROM FirstBuckets JOIN Players ON FirstBuckets.player_id = Players.player_id")

firstbucketlist = []
for row in cur:
    firstbucketlist.append((row[1], row[2]))

firstbucketdict = dict(firstbucketlist)

print(firstbucketdict)

# firstbucketdict = dict(Counter(firstbucketlist))

# sorted_dict = dict(sorted(firstbucketdict.items(), key=lambda x: x[1], reverse=True))

# my_df = pd.DataFrame(firstbucketdict.items())
# sb.scatterplot(x=0, y=1, data=my_df)

# plt.show()
