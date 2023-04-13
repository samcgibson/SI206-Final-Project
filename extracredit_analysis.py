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

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'NYT.db')
cur = conn.cursor()

def make_charts(cur):
    cur.execute('SELECT SportsArticles.pub_date, SportsArticles.print_page, SportsArticles.word_count, PrintStatus.status '
                'FROM SportsArticles JOIN PrintStatus ON SportsArticles.print_status = PrintStatus.status_id')
    
    df = pd.DataFrame(cur, columns=['Day', 'page', 'Word Count', 'Print Status'])

    sb.scatterplot(data=df, x=df['Day'], y=df['Word Count'], hue=df['Print Status'])
    plt.title('NYT Sports Articles, Feb. 2023')
    plt.tight_layout()

    mean_printed = df[df['Print Status'] == 'Printed']['Word Count'].mean()
    mean_not_printed = df[df['Print Status'] != 'Printed']['Word Count'].mean()

    plt.axhline(mean_printed, linestyle='--', color='#4372C4')
    plt.axhline(mean_not_printed, linestyle='--', color='#ED7D32')

    plt.show()

make_charts(cur)
