# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ParserwbPipeline(object):
    def process_item(self, item, spider):
        price_data = item['price_data']
        price_data['current'] = price_data['current'].strip()
        if price_data['original'] == None:
            price_data['original'] = price_data['current']
        else:
            price_data['original'] = price_data['original'].strip()
        return item
