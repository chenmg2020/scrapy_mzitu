# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from ..items import MzituImgsItem


class MzituSpider(scrapy.Spider):
    name = 'mzitu'
    allowed_domains = ['mzitu.com']
    start_urls = ['https://mzitu.com/']
    domain = "https://mzitu.com/"

    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }

    def parse(self, response):
        # 获取首页所有需要链接
        all_urls = response.xpath("//ul[@id='pins']/li/a/@href")
        for url in all_urls:
            topic_url = parse.urljoin(self.domain, url.extract())
            yield scrapy.http.Request(url=topic_url, callback=self.parse_topic)
        next_page = response.xpath("//a[@class='next page-numbers']/@href").extract()
        # 获取下一页
        if next_page:
            next_url = parse.urljoin(self.domain, next_page[0])
            next_url_flag = int(next_url.split('/')[-2])
            # 爬到第几页
            if next_url_flag <= 1:
                yield scrapy.http.Request(url=next_url, callback=self.parse)

    def parse_topic(self, response):
        img_url = response.xpath("//div[@class='main-image']/p/a/img/@src").extract()[0]
        img_alt = response.xpath("//div[@class='main-image']/p/a/img/@alt").extract()[0]
        next_img_url = response.xpath("//div[@class='pagenavi']/a/@href").extract()[-1]
        next_img_url_flag = response.xpath("//div[@class='pagenavi']/a/span/text()").extract()[-1]
        next_img_url_flag2 = int(next_img_url.split('/')[-1])
        if img_url:
            item = MzituImgsItem()
            item['image_urls'] = img_url
            item['category'] = img_alt
            yield item
        # 每个主题爬几张
        if '下一页' in next_img_url_flag and next_img_url_flag2 <= 2:
            yield scrapy.http.Request(url=next_img_url, callback=self.parse_topic)




