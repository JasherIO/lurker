import csv
import json

MAX_PLAYERS = 5

with open('ranks.csv', 'r') as csvfile:
  players = list(csv.DictReader(csvfile, delimiter=','))

teams = {}
for player in players:
  team = player['team']
  name = player['player']
  mmr = player['standard']

  if team in teams:

    for i in range(MAX_PLAYERS):
      p = 'player{}'.format(i+1)

      if p not in teams[team]:
        teams[team][p] = name
        teams[team][p + 'MMR'] = mmr
        break
  
  else:

    teams[team] = {
      'team': team,
      'player1': name,
      'player1MMR': mmr
    }


l = []
for key in teams:
  l.append(teams[key])

with open('post.json', 'w') as jsonfile:
  json.dump(l, jsonfile, indent=2)

# with open('post.csv', 'w') as csvfile:
#   fieldnames = ['team', 'player1', 'player1MMR', 'player2', 'player2MMR', 'player3', 'player3MMR']
#   writer = csv.DictWriter(csvfile, l)