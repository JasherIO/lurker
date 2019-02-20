# -*- coding: utf-8 -*-

# Usage: scrapy crawl beyond -a url="https://teambeyond.net/forum/tournaments/164-astronauts-2000-rocket-league-3v3-1217-700pm-est/standings/"

import scrapy
import validators
from ..items import Player

import logging

TEAMS_SELECTOR = '#ipsTabs_elTourneyTabs_standings_panel > div > div > table > tbody > tr > td > a::attr(href)'
TEAM_ROWS_SELECTOR = '#ipsTabs_elTourneyTabs_standings_panel > div > div > table > tbody > tr'
TEAM_LINK_SELECTOR = 'td > a::attr(href)'
TEAM_CHECKED_IN_SELECTOR_1 = 'td:nth-child(6) > div::text'
TEAM_CHECKED_IN_SELECTOR_2 = 'td:nth-child(7) > div::text'
TEAM_NAME_SELECTOR = '#ipsLayout_mainArea > section > div:nth-child(1) > div.title-section > h3::text'
PLAYERS_SELECTOR = '#ipsTabs_elTeamTabs_details_panel > div > div > table > tbody > tr'
PLAYER_DISPLAY_NAME_SELECTOR = 'td:nth-child(1) > a::text'
PLAYER_STEAM_SELECTOR = 'td:nth-child(3) > div > span > img::attr(src)'
PLAYER_PS_SELECTOR = 'td:nth-child(3) > span > img::attr(src)'
PLAYER_STEAM_ID_SELECTOR = 'td:nth-child(3) > div > ul > li > ul > li > a::text'
PLAYER_PS_ID_SELECTOR = 'td:nth-child(3)::text'

STEAM_PICTURE = 'https://teambeyond.net/forum/uploads/set_resources_2/a6a2e7cb1d0d4e506cc9e64a9611c0f2_Steam20.png'
PS_PICTURE = 'https://teambeyond.net/forum/uploads/set_resources_2/a6a2e7cb1d0d4e506cc9e64a9611c0f2_PS20.png'

class BeyondSpider(scrapy.Spider):
    name = 'beyond'
    allowed_domains = ['teambeyond.net']

    def start_requests(self):
        if hasattr(self, 'url'):
            yield scrapy.Request(self.url, self.parse)

        return

    def parse(self, response):
        for row in response.css(TEAM_ROWS_SELECTOR):
            href = row.css(TEAM_LINK_SELECTOR).extract_first(default='')
            text = row.css(TEAM_CHECKED_IN_SELECTOR_1).extract_first(default='').strip() or row.css(TEAM_CHECKED_IN_SELECTOR_2).extract_first(default='').strip()
            isCheckedIn = True if text == "Checked In" else False

            request = scrapy.Request(href, self.parse_team)
            request.meta['isCheckedIn'] = isCheckedIn
            yield request

    def parse_team(self, response):
        team = response.css(TEAM_NAME_SELECTOR).extract_first(default='')

        for player in response.css(PLAYERS_SELECTOR):
            displayName = player.css(PLAYER_DISPLAY_NAME_SELECTOR).extract_first(default='').strip()
            platform = player.css(PLAYER_STEAM_SELECTOR).extract_first(default='') or player.css(PLAYER_PS_SELECTOR).extract_first(default='')
            platformId = player.css(PLAYER_STEAM_ID_SELECTOR).extract_first(default='').strip() or player.css(PLAYER_PS_ID_SELECTOR).extract().pop().strip()
            
            if platform == STEAM_PICTURE:
                platform = "steam"
            
            if platform == PS_PICTURE:
                platform = "ps"
            
            if validators.url(platformId) or platformId.find('steamcommunity') > -1:
                platformId = platformId.strip('/').split('/').pop()

            yield Player(team=team, displayName=displayName, platform=platform, platformId=platformId, isCheckedIn=response.meta['isCheckedIn'])
