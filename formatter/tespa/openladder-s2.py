import csv

placements = []
with open('openladder.csv', 'r') as f:
  reader = csv.DictReader(f)

  for row in reader:
    placements.append(row)

with open('openladder.wiki', 'w') as f:
  lines = '{| class="wikitable"\n'
  lines += '! Rank\n'
  lines += '! Team\n'
  lines += '! Rating\n'
  lines += '! Record\n'

  for placement in placements:
    lines += '|- align="center"\n'
    lines += '|{} ||{} ||{} || {}\n'.format(placement['rank'], placement['team'], placement['rating'], placement['rating'])

  lines += '|}'

  f.write(lines)

