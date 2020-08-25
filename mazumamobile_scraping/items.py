# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MazumamobileScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # phone detail item
    phoneID = scrapy.Field()
    phoneName = scrapy.Field()
    phoneModel = scrapy.Field()
    phoneType = scrapy.Field()
    excellentPrice = scrapy.Field()
    goodPrice = scrapy.Field()
    poorPrice = scrapy.Field()
    faultyPrice = scrapy.Field()
    deadPrice = scrapy.Field()
    # image item
    images = scrapy.Field()
    image_urls = scrapy.Field()
    image_name = scrapy.Field()
    image_paths = scrapy.Field()



# class ImageItem(scrapy.Item):
#     images = scrapy.Field()
#     image_urls = scrapy.Field()
#     image_paths = scrapy.Field()
