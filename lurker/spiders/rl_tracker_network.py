
# -*- coding: utf-8 -*-
import scrapy
from ..items import Player, Rank
import csv
import json

import logging

ERROR_SELECTOR = 'body > div.container.content-container > div:nth-child(1) > div.alert.alert-danger.alert-dismissable'
RANKS_SELECTOR = '#season-9 > table:nth-child(2) > tbody > tr'
RANK_NAME_SELECTOR = 'td:nth-child(2)::text'
RANK_MMR_SELECTOR = 'td:nth-child(4)::text'

def toUrl(player):
    return "https://rocketleague.tracker.network/profile/" + player['platform'] + "/" + player['platformId']

# scrapy crawl rl-tracker-network -a entrantsFile="entrants.csv"
class RlTrackerNetworkSpider(scrapy.Spider):
    name = 'rl-tracker-network'
    allowed_domains = ['rocketleague.tracker.network']

    def start_requests(self):

        if not hasattr(self, 'entrantsFile'):
            return

        if self.entrantsFile.endswith('.csv'):

            with open(self.entrantsFile, 'r') as csvfile:
                for obj in csv.DictReader(csvfile):
                    request = scrapy.Request(toUrl(obj), self.parse)
                    request.meta['player'] = obj
                    yield request
            
        if self.entrantsFile.endswith('.json'):
            with open(self.entrantsFile, 'r') as jsonfile:
                for obj in json.load(jsonfile):
                    request = scrapy.Request(toUrl(obj), self.parse)
                    request.meta['player'] = obj
                    yield request

        if self.entrantsFile.endswith('.jl'):
            with open(self.entrantsFile, 'r') as jlfile:
                for line in jlfile:
                    obj = json.loads(line)
                    request = scrapy.Request(toUrl(obj), self.parse)
                    request.meta['player'] = obj
                    yield request

        return
        
    def parse(self, response):
        item = Rank(player=response.meta['player']['displayName'], team=response.meta['player']['team'])

        error = response.css(ERROR_SELECTOR).extract_first()
        if not error:
            for rank in response.css(RANKS_SELECTOR):
                name = rank.css(RANK_NAME_SELECTOR).extract_first(default='').strip()
                mmr = rank.css(RANK_MMR_SELECTOR).extract_first(default='').strip()
                
                if name == 'Ranked Duel 1v1':
                    item['duel'] = mmr
                elif name == 'Ranked Doubles 2v2':
                    item['doubles'] = mmr
                elif name == 'Ranked Standard 3v3':
                    item['standard'] = mmr

        yield item