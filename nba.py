from nba_api.live.nba.endpoints import playbyplay
from nba_api.live.nba.endpoints import boxscore
import time
import re

time.sleep(.600)

start_time = time.time()

october18 = '0022200001' # first game of the regular season october 18th, 2022
january1 = '022200547'
january31 = '0022200768'
february1 = '0022200770'
february28 = '0022200932'
march22 = '0022201092' # last game on march 22nd, 2023
#test

gameIdList = []
for id in range(int(february1), int(february28) + 1): # add game IDs to gamelist
    gameIdList.append("00" + str(id)) # have to add '00' here because integers don't allow leading 0's

firstbucketsdict = {}
firstbucketslist = []

for gameId in gameIdList:
    pbp = playbyplay.PlayByPlay(gameId)
    pbpdict = pbp.get_dict()
    
    box = boxscore.BoxScore(gameId)
    bdict = box.get_dict()

print(bdict)
#     hometeaminfo = (bdict.get('game').get('homeTeam').get('teamTricode'), bdict.get('game').get('homeTeam').get('score'))
#     awayteaminfo = (bdict.get('game').get('awayTeam').get('teamTricode'), bdict.get('game').get('awayTeam').get('score'))
    
#     if int(hometeaminfo[1]) > int(awayteaminfo[1]):
#         winningteam = hometeaminfo[0]
#         scorediff = int(hometeaminfo[1]) - int(awayteaminfo[1])
#         if scorediff > 1:
#             msg = f'{winningteam} beat {awayteaminfo[0]} by {scorediff} points.'
#         else:
#             msg = f'{winningteam} beat {awayteaminfo[0]} by {scorediff} point.'
#     else:
#         winningteam = awayteaminfo[0]
#         scorediff = int(awayteaminfo[1]) - int(hometeaminfo[1])
#         if scorediff > 1:
#             msg = f'{winningteam} beat {hometeaminfo[0]} by {scorediff} points.'
#         else:
#             msg = f'{winningteam} beat {hometeaminfo[0]} by {scorediff} point.'
                
#     actions = list(pbpdict['game']['actions'])
#     for action in actions:
#         if action['period'] == 1 and action['isFieldGoal'] == 1 and action['shotResult'] == 'Made':
#             firstbucketslist.append((msg, action['teamTricode'], action['description'], action['playerNameI'], action['clock'], action['subType'], action.get('shotDistance', 'Free Throw')))
#             break

# bothcounter = 0
# splitcounter = 0
# threeptbothcounter = 0
# threeptsplitcounter = 0
# fbplayerlist = []
# fbplayerdict = {}

# for firstbucketinfo in firstbucketslist:
#     # if firstbucketinfo[0][:3] == firstbucketinfo[1]:
#     #     bothcounter += 1
#     #     if '3 PTS' in firstbucketinfo[2]:
#     #         threeptbothcounter += 1
#     # else:
#     #     splitcounter += 1
#     #     if '3 PTS' in firstbucketinfo[2]:
#     #         threeptsplitcounter += 1

#     fbplayerlist.append(firstbucketinfo[3])

# for player in fbplayerlist:
#     if player in fbplayerdict:
#         fbplayerdict[player] += 1
#     else:
#         fbplayerdict[player] = 1  

# fbplayerdict = dict(sorted(fbplayerdict.items(), key=lambda x: x[1], reverse=True)) 

# print(f'The team that got the first bucket won {bothcounter} times and lost {splitcounter} times out of {bothcounter + splitcounter} games.')
# print(f'When the first bucket was a 3-pointer, that team won {threeptbothcounter} times and lost {threeptsplitcounter} times out of {threeptbothcounter + threeptsplitcounter} games.')
print("Process finished --- %s seconds ---" % (time.time() - start_time))