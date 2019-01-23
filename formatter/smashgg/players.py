import csv
import json

players = []
with open('players.csv', 'r') as f:
  reader = csv.DictReader(f)
  completedTeamKey = next(x for x in reader.fieldnames if x.endswith("Completed Team"))
  incompletedTeamKey = next(x for x in reader.fieldnames if x.endswith("Incomplete Teams"))

  for row in reader:
    row['displayName'] = row['Short GamerTag']
    row['team'] = row[completedTeamKey]
    row['completedTeam'] = row[completedTeamKey]
    row['incompletedTeam'] = row[incompletedTeamKey].strip('ACCEPTED:').strip('OPEN_SPOT:').strip('INVITED:').strip(' ')
    row['steam'] = row['Steam Name']

    if row['Connect']:
      playerInfo = row['Connect'].strip('"').split(' ')
      platform = playerInfo[0].strip(':')
      platformId = playerInfo[1].strip('"').strip(',')

      if platform == 'psn':
        platform = 'ps'

      if platform == 'xboxlive':
        platform = 'xbox'

      row['platform'] = platform
      row['platformId'] = platformId

    players.append(row)

with open('cleaned.csv', 'wb') as f:
  fieldnames = ['displayName', 'team', 'completedTeam', 'incompletedTeam', 'steam', 'platform', 'platformId']
  writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')

  writer.writeheader()
  for player in players:
    writer.writerow(player)