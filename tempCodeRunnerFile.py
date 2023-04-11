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

    sb.histplot(data = df, y = df['shot_type'], hue = 'Outcome', multiple= 'stack', palette= ['mediumseagreen', 'red'])

    axs[1].set_xlabel('Occurences in February 2023 Games')
    axs[1].set_ylabel('')
    axs[1].set_title('First Basket Shot Type vs. Game Outcome')
    fig.tight_layout()

    plt.show()

make_basic_charts(cur)