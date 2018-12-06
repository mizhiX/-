# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class ZhancoolPipeline(object):
    def process_item(self, item, spider):
        return item


# 保存图片
class ZhancoolImagesPipeline(ImagesPipeline):

    # 返回图片文件名
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    # 判断图片下载请求是否成功(还没有到本地存盘)
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        # 如果成功就返回 if 失败就去掉
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item

    # 构造图片URL请求
    def get_media_requests(self, item, info):
        # 找到网址
        yield Request(item['preview_url'])
