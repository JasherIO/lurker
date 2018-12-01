# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LurkerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Team(scrapy.Item):
    name = scrapy.Field()

class Player(scrapy.Item):
    name = scrapy.Field()
    displayName = scrapy.Field()
    platform = scrapy.Field()
    platformId = scrapy.Field()
    team = scrapy.Field()

class Rank(scrapy.Item):
    player = scrapy.Field()
    duel = scrapy.Field()
    doubles = scrapy.Field()
    standard = scrapy.Field()