# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PbfcrwalItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    text = scrapy.Field()
    pass
