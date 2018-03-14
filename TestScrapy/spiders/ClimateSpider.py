import scrapy
from TestScrapy.ClimateItems import ClimateItem


class ClimateSpider(scrapy.Spider):
    name = "ClimateSpider"
    allowed_domains = ["wunderground.com"]
    start_urls = ["https://www.wunderground.com/hourly/cn/lai-chi-van/IMACAU9?cm_ven=localwx_hour"]

    def parse(self, response):
        item = ClimateItem()
        for box in response.xpath('//html//body//app//*[@id="hourly-forecast-table"]/tbody//tr'):
            item['name'] = box.xpath('//*[@id="inner-content"]/div[1]/div/div/city-header/div/div/a[1]/text()').extract()[0].strip()
            item['lat'] = box.xpath('//*[@id="inner-content"]/div[1]/div/div/city-header/div/span/strong[2]/text()').extract()[0] + "N"
            item['lng'] = box.xpath('//*[@id="inner-content"]/div[1]/div/div/city-header/div/span/strong[3]/text()').extract()[0] + "E"
            ap = box.xpath('./td[1]/ng-saw-cell-parser/div/span/text()[2]').extract()[0].strip()
            item['time'] = box.xpath('./td[1]/ng-saw-cell-parser/div/span/text()[1]').extract()[0] + ap
            temp_f = box.xpath('./td[3]/ng-saw-cell-parser/div/span/text()').extract()[0].split(' ')[0]
            temp_c = (float(temp_f) - 32.0) * 5 / 9
            item['temp'] = round(temp_c, 2)
            prep_in = box.xpath('./td[6]/ng-saw-cell-parser/div/span/a/text()').extract()[0].split(' ')[0]
            item['prep'] = round(float(prep_in) * 25.40, 2)
            yield item
