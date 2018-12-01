# -*- coding: utf-8 -*-
import scrapy
from ..items import Player, Rank
import validators

ERROR_SELECTOR = 'body > div.container.content-container > div:nth-child(1) > div.alert.alert-danger.alert-dismissable'
DUEL_SELECTOR = '#season-9 > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(4)::text'
DOUBLES_SELECTOR = '#season-9 > table:nth-child(2) > tbody > tr:nth-child(2) > td:nth-child(4)::text'
STANDARD_SELECTOR = '#season-9 > table:nth-child(2) > tbody > tr:nth-child(3) > td:nth-child(4)::text'

# scrapy crawl beyond -o teams.csv -a url="http://teambeyond.net/forum/tournaments/standings/160-astronauts-2000-rocket-league-3v3-1126-700pm-est/"
# scrapy crawl beyond -o teams.csv -a url="http://teambeyond.net/forum/tournaments/standings/162-astronauts-1000-rocket-league-1v1-125-700pm-est/"
class BeyondSpider(scrapy.Spider):
    name = 'beyond'
    allowed_domains = ['teambeyond.net', 'rocketleague.tracker.network']
    # start_urls = ['http://teambeyond.net/']

    def start_requests(self):
        url = getattr(self, 'url', None)
        if url is None:
            return
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for href in response.css('.next a::attr(href)'):
            yield response.follow(href, self.parse)

        for href in response.css('.row2 td a::attr(href)'):
            yield response.follow(href, self.parse_team)

    def parse_team(self, response):
        team = response.css('.team-1 h3::text').extract_first(default='').strip()

        for player in response.css('.row2'):
            displayName = player.xpath('td[1]//text()').extract_first(default='').strip()
            platform = player.xpath('td[3]//@src').extract_first(default='').strip()
            platformId = player.xpath('td[3]//text()').extract_first(default='').strip() or player.xpath('td[3]//div//text()').extract_first(default='').strip()

            p = platform.split('/').pop()
            if p == "Steam20.png":
                platform = "steam"
            if p == "PS20.png":
                platform = "ps"
            
            if validators.url(platformId):
                platformId = platformId.strip('/').split('/').pop()
            
            item = Player(team=team, displayName=displayName, platform=platform, platformId=platformId)

            url = "https://rocketleague.tracker.network/profile/" + platform + "/" + platformId
            request = scrapy.Request(url, self.parse_ranking)
            request.meta['item'] = item
            yield request

    def parse_ranking(self, response):
        item = response.meta['item']

        error = response.css(ERROR_SELECTOR).extract_first()
        if not error:
            # https://stackoverflow.com/questions/2953746/python-parse-comma-separated-number-into-int
            duelStr = response.css(DUEL_SELECTOR).extract_first(default='').strip().replace(',', '')
            item['duel'] = int(duelStr) if duelStr else ''

            doublesStr = response.css(DOUBLES_SELECTOR).extract_first(default='').strip().replace(',', '')
            item['doubles'] = int(doublesStr) if doublesStr else ''

            standardStr = response.css(STANDARD_SELECTOR).extract_first(default='').strip().replace(',', '')
            item['standard'] = int(standardStr) if standardStr else ''

        yield item
