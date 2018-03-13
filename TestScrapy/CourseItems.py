import scrapy


class CourseItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    introduction = scrapy.Field()
    student = scrapy.Field()
