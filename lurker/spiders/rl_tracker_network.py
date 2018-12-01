
# -*- coding: utf-8 -*-
import scrapy
from ..items import Player, Rank
import csv
import json

import logging

ERROR_SELECTOR = 'body > div.container.content-container > div:nth-child(1) > div.alert.alert-danger.alert-dismissable'
DUEL_SELECTOR = '#season-9 > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(4)::text'
DOUBLES_SELECTOR = '#season-9 > table:nth-child(2) > tbody > tr:nth-child(2) > td:nth-child(4)::text'
STANDARD_SELECTOR = '#season-9 > table:nth-child(2) > tbody > tr:nth-child(3) > td:nth-child(4)::text'

def toUrl(player):
    return "https://rocketleague.tracker.network/profile/" + player['platform'] + "/" + player['platformId']

# scrapy crawl rl-tracker-network -a entrantsFile="entrants.csv" -o ranks.jl
# scrapy crawl rl-tracker-network -a entrantsFile="entrants.json" -o ranks.jl
# scrapy crawl rl-tracker-network -a entrantsFile="entrants.jl" -o ranks.jl
class RlTrackerNetworkSpider(scrapy.Spider):
    name = 'rl-tracker-network'
    allowed_domains = ['rocketleague.tracker.network']

    def start_requests(self):
        if not hasattr(self, 'entrantsFile'):
            return

        if self.entrantsFile.endswith('.csv'):
            with open(self.entrantsFile) as csvfile:
                for obj in csv.DictReader(csvfile):
                    request = scrapy.Request(toUrl(obj), self.parse)
                    request.meta['player'] = obj
                    yield request
            
        if self.entrantsFile.endswith('.json'):
            with open(self.entrantsFile) as jsonfile:
                for obj in json.load(jsonfile):
                    request = scrapy.Request(toUrl(obj), self.parse)
                    request.meta['player'] = obj
                    yield request

        if self.entrantsFile.endswith('.jl'):
            with open(self.entrantsFile) as jlfile:
                for line in jlfile:
                    obj = json.loads(line)
                    request = scrapy.Request(toUrl(obj), self.parse)
                    request.meta['player'] = obj
                    yield request

        return
        
    def parse(self, response):
        item = Rank(player=response.meta['player'])

        error = response.css(ERROR_SELECTOR).extract_first()
        if not error:
            item['duel'] = response.css(DUEL_SELECTOR).extract_first(default='')
            item['doubles'] = response.css(DOUBLES_SELECTOR).extract_first(default='')
            item['standard'] = response.css(STANDARD_SELECTOR).extract_first(default='')

        yield item