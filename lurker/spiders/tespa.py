# -*- coding: utf-8 -*-

# Usage: scrapy crawl tespa -a tournament="https://compete.tespa.org/tournament/78/phase/3/group/1"

# S1 Eastern: 'https://compete.tespa.org/tournament/80/phase/3/group/1'
# S1 Northern: 'https://compete.tespa.org/tournament/78/phase/3/group/1'
# S1 Southern: 'https://compete.tespa.org/tournament/79/phase/3/group/1'
# S1 Western: 'https://compete.tespa.org/tournament/81/phase/3/group/1'

# S2 Eastern: 'https://compete.tespa.org/tournament/119/phase/3/group/1'
# S1 Northern: 'https://compete.tespa.org/tournament/117/phase/3/group/1'
# S2 Southern: 'https://compete.tespa.org/tournament/118/phase/3/group/1'
# S2 Western: 'https://compete.tespa.org/tournament/120/phase/3/group/1'

import scrapy
from ..items import Match, Placement, Player, Team

# Standings
STANDINGS_SELECTOR = '#collapseGroup > table > tbody > tr'
POSITION_SELECTOR = 'td:nth-child(1)::text'
TEAM_SELECTOR = 'td:nth-child(2) > a::text'
TEAM_LINK_SELECTOR = 'td:nth-child(2) > a::attr(href)'
MATCH_SELECTOR = 'td:nth-child(3)::text'
GAME_SELECTOR = 'td:nth-child(4)::text'

# Rounds
ROUNDS_SELECTOR = '.compete-panel-groupRounds'
ROUND_TITLE_SELECTOR = '.compete-panel-heading > h4::text'
ROUND_MATCHES_SELECTOR = 'div > table > tbody'
TEAM_A_SELECTOR = 'tr:nth-child(1) > td > a > span::text'
SCORE_A_SELECTOR = 'tr:nth-child(1) > td > div::text'
TEAM_B_SELECTOR = 'tr:nth-child(2) > td > a > span::text'
SCORE_B_SELECTOR = 'tr:nth-child(2) > td > div::text'

# Team
NAME_SELECTOR = '#TeamView > div.compete-team__header > div.media > div.team-name > h3 > span::text'
FULL_SELECTOR = '#TeamView > div.compete-team__header > div.media > div.team-name > h4 > span::text'
PLAYERS_SELECTOR = '#TeamView > div.compete-table__wrapper.compete-table-responsive > table > tbody > tr'
PLAYER_ROLE_SELECTOR = 'td:nth-child(1)'
PLAYER_NAME_SELECTOR = 'td:nth-child(2)::text'
PLAYER_DISPLAY_SELECTOR = 'td:nth-child(3)::text'

class TespaSpider(scrapy.Spider):
    name = 'tespa'
    allowed_domains = ['compete.tespa.org']

    def start_requests(self):
        if hasattr(self, 'tournament'):
            yield scrapy.Request(self.tournament, self.parse)

    def parse(self, response):
        # Standings
        for row in response.css(STANDINGS_SELECTOR):
            position = row.css(POSITION_SELECTOR).extract_first(default='')
            
            team = row.css(TEAM_SELECTOR).extract_first(default='').strip()
            href = row.css(TEAM_LINK_SELECTOR).extract_first(default='')
            yield scrapy.Request(href, self.parse_team)
            
            match = row.css(MATCH_SELECTOR).extract_first(default='')
            [matchWins, matchLosses] = match.strip(' ').split('-')
            matchWins = matchWins.strip()
            matchLosses = matchLosses.strip()
            
            game = row.css(GAME_SELECTOR).extract_first(default='')
            [gameWins, gameLosses] = game.strip(' ').split('-')
            gameWins = gameWins.strip()
            gameLosses = gameLosses.strip()

            yield Placement(position=position, team=team, matchWins=matchWins, matchLosses=matchLosses, gameWins=gameWins, gameLosses=gameLosses)
        
        # Rounds
        for row in response.css(ROUNDS_SELECTOR):
            index = row.css(ROUND_TITLE_SELECTOR).extract_first(default='').strip().split(' ').pop()
            
            for r in row.css(ROUND_MATCHES_SELECTOR):
                teamA = r.css(TEAM_A_SELECTOR).extract_first(default='').strip()
                scoreA = r.css(SCORE_A_SELECTOR).extract_first(default='').strip()

                teamB = r.css(TEAM_B_SELECTOR).extract_first(default='').strip()
                scoreB = r.css(SCORE_B_SELECTOR).extract_first(default='').strip()
                
                yield Match(rnd=index, teamA=teamA, scoreA=scoreA, teamB=teamB, scoreB=scoreB)

    def parse_team(self, response):
        team = response.css(NAME_SELECTOR).extract_first(default='')
        full = response.css(FULL_SELECTOR).extract_first(default='')

        for row in response.css(PLAYERS_SELECTOR):
            name = row.css(PLAYER_NAME_SELECTOR).extract_first(default='').strip()
            displayName = row.css(PLAYER_DISPLAY_SELECTOR).extract_first(default='').strip()

            yield Player(name=name, displayName=displayName, team=team)
