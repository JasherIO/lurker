# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
import validators
import csv
from items import Match, Placement, Player, Rank
import logging

def strip(item):
    for key in item.keys():
        if isinstance(item[key], str):
            item[key] = item[key].strip()

def get(obj, key, default=''):
    return obj[key] if key in obj else default

class MatchPipeline(object):
    def open_spider(self, spider):
        if spider.name != 'tespa':
            return
        
        fields_to_export = ['rnd', 'teamA', 'scoreA', 'teamB', 'scoreB']
        f = open('matches.csv', 'wb')
        self.exporter = CsvItemExporter(f, fields_to_export=fields_to_export)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        if spider.name != 'tespa':
            return

        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        if spider.name != 'tespa':
            return item

        if not isinstance(item, Match):
            return item
            
        self.exporter.export_item(item)
        return item

class PlacementPipeline(object):
    def open_spider(self, spider):
        if spider.name != 'tespa':
            return
        
        fields_to_export = ['position', 'team', 'matchWins', 'matchLosses', 'gameWins', 'gameLosses']
        f = open('placements.csv', 'wb')
        self.exporter = CsvItemExporter(f, fields_to_export=fields_to_export)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        if spider.name != 'tespa':
            return

        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        if spider.name != 'tespa':
            return item

        if not isinstance(item, Placement):
            return item
            
        self.exporter.export_item(item)
        return item

class PlayerPipeline(object):
    def open_spider(self, spider):
        if spider.name == 'rl-tracker-network':
            return
        
        fields_to_export = ['displayName', 'team', 'platform', 'platformId', 'isCheckedIn']
        f = open('players.csv', 'wb')
        self.exporter = CsvItemExporter(f, fields_to_export=fields_to_export)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        if spider.name == 'rl-tracker-network':
            return

        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        if spider.name == 'rl-tracker-network':
            return item

        if not isinstance(item, Player):
            return item
            
        self.exporter.export_item(item)
        return item

MAX_PLAYERS = 5
class RankPipeline(object):
    def open_spider(self, spider):
        if not spider.name == 'rl-tracker-network':
            return

        self.teams = {}

    def close_spider(self, spider):
        if not spider.name == 'rl-tracker-network':
            return
        
        l = []
        for key in self.teams:
            l.append(self.teams[key])

        fieldnames = [
            'team',
            'isCheckedIn',
            'player1',
            'player2',
            'player3',
            'player4',
            'player5',
            'player1Duel',
            'player1Doubles',
            'player1Standard',
            'player2Duel',
            'player2Doubles',
            'player2Standard',
            'player3Duel',
            'player3Doubles',
            'player3Standard',
            'player4Duel',
            'player4Doubles',
            'player4Standard',
            'player5Duel',
            'player5Doubles',
            'player5Standard'
        ]

        with open('ranks.csv', 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in l:
                writer.writerow(row)

    def process_item(self, item, spider):
        if not spider.name == 'rl-tracker-network':
            return item

        if not isinstance(item, Rank):
            return item


        strip(item)
        
        if 'duel' in item:
            duelStr = item['duel'].strip().replace(',', '')
            item['duel'] = int(duelStr) if duelStr else ''

        if 'doubles' in item:
            doublesStr = item['doubles'].strip().replace(',', '')
            item['doubles'] = int(doublesStr) if doublesStr else ''

        if 'standard' in item:
            standardStr = item['standard'].strip().replace(',', '')
            item['standard'] = int(standardStr) if standardStr else ''


        team = item['team']
        if team in self.teams:

            for i in range(MAX_PLAYERS):
                p = 'player{}'.format(i+1)

                if p not in self.teams[team]:
                    self.teams[team][p] = get(item, 'player')
                    self.teams[team][p + 'Duel'] = get(item, 'duel')
                    self.teams[team][p + 'Doubles'] = get(item, 'doubles')
                    self.teams[team][p + 'Standard'] = get(item, 'standard')
                    break
        
        else:

            self.teams[team] = {
                'team': team,
                'isCheckedIn': get(item, 'isCheckedIn'),
                'player1': get(item, 'player'),
                'player1Duel': get(item, 'duel'),
                'player1Doubles': get(item, 'doubles'),
                'player1Standard': get(item, 'standard')
            }

        return item
