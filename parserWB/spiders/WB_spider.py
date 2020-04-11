import scrapy
from datetime import datetime

from urllib.parse import urljoin
from parserWB.items import ParserwbItem


class WB_Spider(scrapy.Spider):
    name = "WB_parser"

    start_urls = [
        'https://www.wildberries.ru/catalog/obuv/zhenskaya/sabo-i-myuli/myuli',
    ]
    visited_urls = []

    def parse(self, response):
        if response.url not in self.visited_urls:
            self.visited_urls.append(response.url)
            # проходимся по всем товарам и открываем каждый из них
            for post_link in response.xpath(
                    '//a[@class="ref_goods_n_p j-open-full-product-card"]/@href').extract():
                url = urljoin(response.url, post_link)
                yield scrapy.Request(url, callback=self.parse_contents)

        # проходим по всем страницам с товарами
        next_page = response.css('a.next::attr(href)').get()
        next_page_url = response.urljoin(next_page)
        yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_contents(self, response):

        item = ParserwbItem()

        item['timestamp'] = datetime.today().timestamp()

        item['url'] = response.url

        item['RPC'] = response.url.split('/')[4]

        title = response.selector.xpath('//div[@class="brand-and-name j-product-title"]/span/text()').extract()
        item['title'] = title[0] + "/" + title[1]

        item['brand'] = response.selector.xpath(
            '//div[@class="brand-and-name j-product-title"]/span[@class="brand"]/text()').get()

        item['section'] = response.selector.xpath(
            '//ul[@class="bread-crumbs"]/li[@class="secondary"]/a/span/text()').extract()

        price_data = {}
        price_data['current'] = response.selector.xpath(
            '//div[@class="final-price-block"]/span[@class="final-cost"]/text()').get()
        price_data['original'] = response.selector.xpath(
            '//del[@class="c-text-base"]/text()').get()
        price_data['sale_tag'] = response.selector.xpath(
            '//div[@class="discount-tooltipster-content"]/p[2]/span/text()').get()
        item['price_data'] = price_data

        stock = {}
        stock['is_stock'] = True  # выдает товары только те, которые есть в наличии
        stock['count'] = None  # не встретил такие товары, которые заканчивались
        item['stock'] = stock

        assets = {}
        assets['main_image'] = response.selector.xpath('//img[@class="MagicZoomFullSizeImage"]/@src').get()
        assets['set_images'] = set(response.selector.xpath('//ul[@class="carousel"]/li/a/img/@src').extract())
        assets['view360'] = response.selector.xpath(
            '//a[@class="disabledZoom thumb_3d j-carousel-v360"]/img/@src').get()
        assets['video'] = response.selector.xpath('//video[@class="vjs-tech"]/@src').get()
        item['assets'] = assets

        metadata = {}
        metadata['__description'] = response.selector.xpath(
            '//div[@class="i-composition-v1 j-collapsable-composition i-collapsable-v1"]/span/text()').get()
        metadata['АРТИКУЛ'] = response.selector.xpath(
            '//div[@class="product-content-v1"]//div[@class="article"]/span/text()').get()
        item['metadata'] = metadata
        yield item

        #          "marketing_tags": [], # {list of str}список тэгов, напрмер ['Популярный', 'Акция', 'Подарок']
