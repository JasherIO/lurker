# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Match(scrapy.Item):
    rnd = scrapy.Field()
    teamA = scrapy.Field()
    scoreA = scrapy.Field()
    teamB = scrapy.Field()
    scoreB = scrapy.Field()
    event = scrapy.Field()

class Placement(scrapy.Item):
    position = scrapy.Field()
    team = scrapy.Field()
    matchWins = scrapy.Field()
    matchLosses = scrapy.Field()
    gameWins = scrapy.Field()
    gameLosses = scrapy.Field()
    event = scrapy.Field()

class Player(scrapy.Item):
    name = scrapy.Field()
    displayName = scrapy.Field()
    platform = scrapy.Field()
    platformId = scrapy.Field()
    role = scrapy.Field()
    team = scrapy.Field()
    isCheckedIn = scrapy.Field()

class Rank(scrapy.Item):
    player = scrapy.Field()
    team = scrapy.Field()
    isCheckedIn = scrapy.Field()
    duel = scrapy.Field()
    doubles = scrapy.Field()
    standard = scrapy.Field()

class Team(scrapy.Item):
    name = scrapy.Field()
    full = scrapy.Field()
