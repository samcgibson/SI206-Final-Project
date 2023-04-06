import sqlite3
import json
import os
from collections import Counter

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'NBA.db')
cur = conn.cursor()

cur.execute("SELECT FirstBuckets.player_id, Players.player_name, FirstBuckets.shot_distance, FirstBuckets.points FROM FirstBuckets JOIN Players ON FirstBuckets.player_id = Players.player_id")

firstbucketlist = []
for row in cur:
    firstbucketlist.append(row[1])

firstbucketdict = dict(Counter(firstbucketlist))

sorted_dict = dict(sorted(firstbucketdict.items(), key=lambda x: x[1], reverse=True))
print(sorted_dict)