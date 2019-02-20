
# -*- coding: utf-8 -*-
import scrapy
from ..items import Player, Rank
import csv
import json

import logging

ERROR_SELECTOR = 'body > div.container.content-container > div:nth-child(1) > div.alert.alert-danger.alert-dismissable'
RANKS_SELECTOR = '#season-10 > table:nth-child(2) > tbody > tr'
# RANKS_SELECTOR = '#season-9 > table > tbody > tr'
RANK_NAME_SELECTOR = 'td:nth-child(2)::text'
RANK_MMR_SELECTOR = 'td:nth-child(4)::text'

# scrapy crawl rl-tracker-network -a file="file.csv"
class RlTrackerNetworkSpider(scrapy.Spider):
    name = 'rl-tracker-network'
    allowed_domains = ['rocketleague.tracker.network']

    def start_requests(self):

        if not hasattr(self, 'file'):
            return

        with open(self.file, 'r') as csvfile:
            for obj in csv.DictReader(csvfile):

                hasTeam = ('team' in obj) and obj['team']
                hasPlatform = ('platform' in obj) and obj['platform']
                hasPlatformId = ('platformId' in obj) and obj['platformId']
                hasSteam = ('steam' in obj) and obj['steam']

                if hasPlatform and hasPlatformId:
                    platform = obj['platform']
                    platformId = obj['platformId']

                elif hasSteam:
                    platform = 'steam'
                    platformId = obj['steam']

                elif not (hasTeam and hasPlatform and hasPlatformId):
                    continue

                url = "https://rocketleague.tracker.network/profile/{}/{}".format(platform, platformId)
                request = scrapy.Request(url, self.parse)
                request.meta['player'] = obj['displayName']
                request.meta['team'] = obj['team']
                request.meta['isCheckedIn'] = obj['isCheckedIn'] if ('isCheckedIn' in obj) else ''
                yield request
            
        return
        
    def parse(self, response):
        item = Rank(player=response.meta['player'], team=response.meta['team'], isCheckedIn=response.meta['isCheckedIn'])

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