# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserwbItem(scrapy.Item):
    timestamp = scrapy.Field()
    RPC = scrapy.Field(serializator = str)
    url = scrapy.Field(serializator = str)
    title = scrapy.Field(serializator = str)
    marketing_tags = scrapy.Field(serializator = list) #
    brand = scrapy.Field(serializator = str)
    section = scrapy.Field(serializator = list)
    price_data = scrapy.Field()
    stock = scrapy.Field()
    assets = scrapy.Field()
    metadata = scrapy.Field()
