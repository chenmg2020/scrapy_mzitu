# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class ScrapyTestPipeline(object):
    def process_item(self, item, spider):
        return item


class MzituImgDownloadPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        default_headers = {
            'referer': 'https://www.mzitu.com/',
        }
        yield Request(item['image_urls'], headers=default_headers, meta={"item_category": item['category'],
                                                                         "item_url": item['image_urls']})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        category = request.meta['item_category']
        image_guid = request.meta['item_url'].split('/')[-1]
        return '%s/%s' % (category, image_guid)


