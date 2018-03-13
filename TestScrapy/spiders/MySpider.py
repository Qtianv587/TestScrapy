import scrapy
from TestScrapy.CourseItems import CourseItem


class MySpider(scrapy.Spider):
    name = "MySpider"
    allowed_domains = ["imooc.com"]
    start_urls = ["http://www.imooc.com/course/list"]

    def parse(self, response):
        item = CourseItem()
        for box in response.xpath('//div[@class="moco-course-wrap"]/a[@target="_self"]'):
            item['url'] = 'http://www.imooc.com' + box.xpath(".//@href").extract()[0]
            item['title'] = box.xpath('.//img/@alt').extract()[0].strip()
            item['image_url'] = box.xpath('.//@src').extract()[0]
            item['student'] = box.xpath('.//span/text()').extract()[0].strip()[:-3]
            item['introduction'] = box.xpath('.//p/text()').extract()[0].strip()
            yield item
