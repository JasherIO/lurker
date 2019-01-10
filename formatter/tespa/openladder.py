import csv

placements = []
with open('openladder.csv', 'r') as f:
  reader = csv.DictReader(f)

  for row in reader:
    if row['region'] == 'East':
      row['region'] = 'Eastern'
    if row['region'] == 'North':
      row['region'] = 'Northern'
    if row['region'] == 'South':
      row['region'] = 'Southern'
    if row['region'] == 'West':
      row['region'] = 'Western'

    placements.append(row)

with open('openladder.wiki', 'w') as f:
  lines = '{| class="wikitable"\n'
  lines += '! Rank\n'
  lines += '! Team\n'
  lines += '! Rating\n'
  lines += '! Region\n'

  for placement in placements:
    lines += '|- align="center"\n'
    lines += '|{} ||{} ||{} || {}\n'.format(placement['rank'], placement['team'], placement['rating'], placement['region'])

  lines += '|}'

  f.write(lines)

