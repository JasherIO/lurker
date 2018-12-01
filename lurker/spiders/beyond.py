# -*- coding: utf-8 -*-
import scrapy
from ..items import Player

# scrapy crawl beyond -a tournament="http://teambeyond.net/forum/tournaments/standings/160-astronauts-2000-rocket-league-3v3-1126-700pm-est/" -o entrants.csv
# scrapy crawl beyond -a tournament="http://teambeyond.net/forum/tournaments/standings/162-astronauts-1000-rocket-league-1v1-125-700pm-est/" -o entrants.csv
class BeyondSpider(scrapy.Spider):
    name = 'beyond'
    allowed_domains = ['teambeyond.net']

    def start_requests(self):
        if hasattr(self, 'tournament'):
            yield scrapy.Request(self.tournament, self.parse)
        
        if hasattr(self, 'team'):
            yield scrapy.Request(self.team, self.parse_team)

        return

    def parse(self, response):
        for href in response.css('.next a::attr(href)'):
            yield response.follow(href, self.parse)

        for href in response.css('.row2 td a::attr(href)'):
            yield response.follow(href, self.parse_team)

    def parse_team(self, response):
        team = response.css('.team-1 h3::text').extract_first(default='')

        for player in response.css('.row2'):
            displayName = player.xpath('td[1]//text()').extract_first(default='')
            platform = player.xpath('td[3]//@src').extract_first(default='')
            platformId = player.xpath('td[3]//text()').extract_first(default='').strip() or player.xpath('td[3]//div//text()').extract_first(default='').strip()
            
            yield Player(team=team, displayName=displayName, platform=platform, platformId=platformId)
