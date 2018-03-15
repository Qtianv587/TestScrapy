import scrapy


class ClimateItem(scrapy.Item):
    name = scrapy.Field()
    temp = scrapy.Field()
    time = scrapy.Field()
    prep = scrapy.Field()
    climate = scrapy.Field()
    wind_speed = scrapy.Field()
    wind_dire = scrapy.Field()
    air_pres = scrapy.Field()
    relative_hum = scrapy.Field()
    cloud = scrapy.Field()
    visibility = scrapy.Field()
    day_climate = scrapy.Field()
    climate_code = scrapy.Field()
