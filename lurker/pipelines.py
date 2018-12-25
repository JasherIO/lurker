# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
import validators
from items import Match, Player, Rank

def strip(item):
    for key in item.keys():
        if isinstance(item[key], str):
            item[key] = item[key].strip()

class PlayerPipeline(object):
    def open_spider(self, spider):
        fields_to_export = ['name', 'displayName', 'team', 'platform', 'platformId', 'role']
        f = open('players.csv', 'wb')
        self.exporter = CsvItemExporter(f, fields_to_export=fields_to_export)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        # self.exporter.file.close()

    def process_item(self, item, spider):
        if isinstance(item, Player):
            self.exporter.export_item(item)

        return item

class RankPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, Rank):
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

        return item
