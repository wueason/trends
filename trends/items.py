# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TrendsItem(Item):
    name = Field()
    category = Field()

class TrendsRankingItem(Item):
    category = Field()
    date = Field()
    ageRange = Field()
    rank = Field()
    keyword = Field()
    searches = Field()
    changeRate = Field()
    isNew = Field()
    trend = Field()
    percentage = Field()
