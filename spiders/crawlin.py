import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader

from ..items import RcrawlItem



class RestuarantSpider(scrapy.Spider):
    name = "restaurant"

    def start_requests(self):
        urls = ['https://www.restaurantbusinessonline.com/top-100-independents?year=2014#data-table',
                'https://www.restaurantbusinessonline.com/top-100-independents?year=2015#data-table',
                'https://www.restaurantbusinessonline.com/top-100-independents?year=2016#data-table',
                'https://www.restaurantbusinessonline.com/top-100-independents?year=2017#data-table',
                'https://www.restaurantbusinessonline.com/top-100-independents?year=2018#data-table',
                'https://www.restaurantbusinessonline.com/top-100-independents?year=2019#data-table',
                'https://www.restaurantbusinessonline.com/top-100-independents?year=2020#data-table',
                ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for biz in response.css('div.table-responsive tr'):
            item = RcrawlItem()
            item['Name'] = biz.css('a::text').get()
            item['Sales'] = biz.css('td.text-right::text').re(r'\$\d+,\d+,\d+')
            item['AvgCheck'] = biz.css('td.text-right::text').re(r'\$\d+[^,]$')
            item['City'] = biz.css('td::text').re(r'^[a-zA-Z]+\s*[a-zA-Z]+(?!.)*[a-zA-Z]+\s*[a-zA-Z]+(?!.)')
            item['State'] = biz.css('td::text').re(r'^[A-Z]+[a-z]*[.]+[A-Z]*[.]*')

            yield item