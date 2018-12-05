# -*- coding: utf-8 -*-
import scrapy

from cat.items import CatItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/board/4']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        for i in range(10):
            yield scrapy.Request(url = 'http://maoyan.com/board/4?offset={}'.format(i * 10),
                                 headers=headers,
                                 method='GET',
                                 callback=self.parse)

    def parse(self, response):
        dd_list = response.selector.xpath('//dl[@class="board-wrapper"]/dd')
        for dd in dd_list:
            item = CatItem()
            item['movie'] = dd.xpath('.//p[@class="name"]/a/text()').extract_first()
            item['img'] = dd.xpath('./a/img/@data-src').extract_first()
            item['top'] = dd.xpath('./i/text()').extract_first()
            item['starring'] = dd.xpath('.//p[@class="star"]/text()').extract_first().strip()[3:]
            item['releasetime'] = dd.xpath('.//p[@class="releasetime"]/text()').extract_first().strip()[5:]
            item['score'] = ''.join(dd.xpath('.//p[@class="score"]//text()').extract()).strip()
            item['link'] = 'https://maoyan.com' + dd.xpath('.//p[@class="name"]/a/@href').extract_first().strip()

            yield item
