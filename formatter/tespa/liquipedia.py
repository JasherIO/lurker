import csv

# Placements
placements = []
with open('placements.csv', 'r') as f:
  reader = csv.DictReader(f)
  for row in reader:
    
    difference = int(row['gameWins']) - int(row['gameLosses'])
    if difference >= 0:
      difference = '+{}'.format(difference)

    placement = '{{GroupTableSlot|{{teamTable/'
    placement += row['team'] + '}}|'
    placement += 'place={}|'.format(row['position'])
    placement += 'win_m={}|'.format(row['matchWins'])
    placement += 'lose_m={}|'.format(row['matchLosses'])
    placement += 'win_g={}|'.format(row['gameWins'])
    placement += 'lose_g={}|'.format(row['gameLosses'])
    placement += 'diff={}'.format(difference)
    placement += '}}\n'

    placements.append(placement)

with open('placements.wiki', 'w') as f:
  f.write('{{GroupTableStart|Regular Season |width=350px|finished=}}\n')
  
  for placement in placements:
    f.write(placement)
  
  f.write('{{GroupTableEnd}}\n')

# Rounds and Cross Table
rounds = {}
with open('matches.csv', 'r') as f:
  reader = csv.DictReader(f)
  for row in reader:
    
    rnd = row['rnd']
    if rnd in rounds:
      rounds[rnd].append(row)
    else:
      rounds[rnd] = [row]
      
keys = map(lambda x: str(x), sorted(map(lambda x: int(x), rounds.keys())))

with open('rounds.wiki', 'w') as f:
  for key in keys:
    lines = '=====Round {}=====\n'.format(key)
    lines += '{{MatchSection|Round ' + key + '}}\n'
    lines += '{{MatchList\n'
    lines += '|hide=false|width=360px|title=Round {} Matches\n'.format(key)

    for (index, match) in enumerate(rounds[key]):
      lines += '|match{}='.format(index+1)
      lines += '{{MatchMaps\n'

      if (index+1) == 1:
        lines += '|date=October 10, 2017 - 17:00 {{Abbr/PDT}}\n'
        lines += '|finished=true\n'

      lines += '|team1={} '.format(match['teamA'])
      lines += '|games1={} '.format(match['scoreA'])
      lines += '|team2={} '.format(match['teamB'])
      lines += '|games2={} '.format(match['scoreB'])

      winner = '1' if int(match['scoreA']) > int(match['scoreB']) else '2'

      lines += '|winner={} '.format(winner)

      lines += '}}\n'

    lines += '}}\n'
    lines += '{{box|end}}\n\n' if key == '7' else '{{box|break|padding=2em}}\n\n'
  
    f.write(lines)
