# -*- coding: utf-8 -*-
import scrapy

# scrapy crawl tracker-network -o ranking.csv -a platform="steam" -a platformId="dappur"
class TrackerNetworkSpider(scrapy.Spider):
    name = 'tracker-network'
    allowed_domains = ['rocketleague.tracker.network']
    # start_urls = ['http://rocketleague.tracker.network/']

    def start_requests(self):
        platform = getattr(self, 'platform', None)
        platformId = getattr(self, 'platformId', None)
        if platform is None and platformId is None:
            return
        
        url = "https://rocketleague.tracker.network/profile/" + platform + "/" + platformId

        yield scrapy.Request(url, self.parse)

    
    def parse(self, response):
        error = response.css('body > div.container.content-container > div:nth-child(1) > div.alert.alert-danger.alert-dismissable').extract_first()
        if error:
            return

        yield {
            'doubles': response.css("#season-9 > table:nth-child(2) > tbody > tr:nth-child(2) > td:nth-child(4)::text").extract_first().strip()
            # 'standard': 'doubles': response.css("#season-9 > table:nth-child(2) > tbody > tr:nth-child(4) > td:nth-child(4)::text").extract_first().strip()
        }