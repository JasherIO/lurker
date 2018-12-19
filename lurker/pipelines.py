# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from items import Match, Player, Rank
import validators

def strip(item):
    for key in item.keys():
        if isinstance(item[key], str):
            item[key] = item[key].strip()

class PlayerPipeline(object):
    def clean(self, item):
        if not 'platform' in item or not 'platformId' in item:
            return item
        
        p = item['platform'].split('/').pop()

        if p == "Steam20.png":
            item['platform'] = "steam"
        
        if p == "PS20.png":
            item['platform'] = "ps"
        
        if validators.url(item['platformId']):
            item['platformId'] = item['platformId'].strip('/').split('/').pop()

    def process_item(self, item, spider):
        if isinstance(item, Player):
            strip(item)
            self.clean(item)

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
