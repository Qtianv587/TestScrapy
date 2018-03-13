#!/usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy

class XiaoHuarSpider(scrapy.spiders.Spider):
    name = "xiaohuar"
    allowed_domains = ["xiaohuar.com"]
    start_urls = [
        "http://www.xiaohuar.com/hua/",
    ]

    def parse(self, response):
        print("+++++++")
        print(response)
        print("+++++++")
        # print(response, type(response))
        # from scrapy.http.response.html import HtmlResponse
        # print(response.body_as_unicode())

        current_url = response.url
        body = response.body
        unicode_body = response.body_as_unicode()