# -*- coding: utf-8 -*-
import json

import scrapy

from zhancool.items import ZhancoolItem


class CoolSpider(scrapy.Spider):
    name = 'cool'
    allowed_domains = ['hellorf.com']
    start_urls = ['http://www.hellorf.com/']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://www.hellorf.com/image/search?q=%E7%BD%91%E7%AB%99',
            'Host': 'api.hellorf.com'
        }
        for i in range(10):
            data = {'page': '%d' % (i + 1),
                    'keyword': "网站"}
            yield scrapy.FormRequest(url='https://api.hellorf.com/hellorf/image/search?page=%d' % (i + 1),
                                     headers=headers,
                                     formdata=data,
                                     method='POST',
                                     callback=self.parse)

    def parse(self, response):
        json_result = json.loads(response.text)
        data_lsit = json_result['data']['data']
        for data in data_lsit:
            item = ZhancoolItem()
            item['item_id'] = data.get('_id', '')
            item['title'] = data.get('title', '')
            item['preview_url'] = data.get('preview_url', '')
            yield item
