import scrapy
from scrapy.crawler import CrawlerProcess
import os


class LinkItem(scrapy.Item):
    link = scrapy.Field()

class TelegraphSpider(scrapy.Spider):
    name = 'telegraph'
    start_urls = ['https://www.telegraphindia.com/']
    custom_settings = {
        'FEED_FORMAT':'csv',
        'FEED_URI':'teleurl.csv',
        'overwrite':'True'
    }

    def parse(self, response):
        item = LinkItem()
        utr = response.xpath('//a/@href')
        for urls in utr:
            item['link'] = urls.extract()
            yield item

class IESpider(scrapy.Spider):
    name = 'indianexp'
    start_urls = ['https://indianexpress.com/']
    custom_settings = {
        'FEED_FORMAT':'csv',
        'FEED_URI':'ie.csv',
        'overwrite':'True'
    }

    def parse(self, response):
        item = LinkItem()
        utr = response.xpath('//a/@href')
        for urls in utr:
            item['link'] = urls.extract()
            yield item

class FreePressJournal(scrapy.Spider):
    name = 'freepress'
    start_urls = ['https://www.freepressjournal.in/']
    custom_settings = {
        'FEED_FORMAT':'csv',
        'FEED_URI':'fpj.csv',
        'overwrite':'True'
    }

    def parse(self, response):
        item = LinkItem()
        utr = response.xpath('//a/@href')
        for urls in utr:
            item['link'] = urls.extract()
            yield item

# class Tribune(scrapy.Spider):
#     name = 'tribune'
#     start_urls = ['https://www.tribuneindia.com/']
#     custom_settings = {
#         'FEED_FORMAT':'csv',
#         'FEED_URI':'tribune.csv',
#         'overwrite':'True'
#     }
#
#     def parse(self, response):
#         item = LinkItem()
#         utr = response.xpath('//a/@href')
#         for urls in utr:
#             item['link'] = urls.extract()
#             yield item
class HT(scrapy.Spider):
    name = 'HT'
    start_urls = ['https://www.hindustantimes.com/']
    custom_settings = {
        'FEED_FORMAT':'csv',
        'FEED_URI':'ht.csv',
        'overwrite':'True'
    }

    def parse(self, response):
        item = LinkItem()
        utr = response.xpath('//a/@href')
        for urls in utr:
            item['link'] = urls.extract()
            yield item

os.remove('fpj.csv')
os.remove('ie.csv')
os.remove('teleurl.csv')
os.remove('ht.csv')

process = CrawlerProcess()
process.crawl(TelegraphSpider)
process.crawl(IESpider)
process.crawl(FreePressJournal)
process.crawl(HT)
process.start()