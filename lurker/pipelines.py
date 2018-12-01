# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import validators
from items import Player

class PlayerPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, Player):
            p = item['platform'].split('/').pop()

            if p == "Steam20.png":
                item['platform'] = "steam"
            
            if p == "PS20.png":
                item['platform'] = "ps"
            
            if validators.url(item['platformId']):
                item['platformId'] = item['platformId'].strip('/').split('/').pop()

        return item
