import scrapy


class ClimateItem(scrapy.Item):
    name = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    temp = scrapy.Field()
    time = scrapy.Field()
    prep = scrapy.Field()
