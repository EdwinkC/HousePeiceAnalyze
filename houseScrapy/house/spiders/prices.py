# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import HouseItem


class PricesSpider(scrapy.Spider):
    name = 'houses'
    allowed_domains = ['www.anjuke.com']
    # start_urls = ['https://www.anjuke.com/fangjia/yixianchengshi2010/']
    # start_urls = ['https://www.anjuke.com/fangjia/quanguo2019/']

    def __init__(self, city='quanguo', year='2019', *args, **kwargs):
        super(PricesSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.anjuke.com/fangjia/%s%s/'%(city, year)]
        print(self.start_urls)


    def parse(self, response):
      
        le = LinkExtractor(restrict_css='div.switch-year-ajkcomp.clearfix')
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_houses)



    def parse_houses(self, response):
        
        sel = response.css('div.avger.clearfix div.fjlist-wrap.clearfix:first-child ul')
        for p in sel.xpath('./li/a'):
            house = HouseItem()
            house['name'] = p.xpath('./b/text()').extract_first()
            house['date'] = p.xpath('./b/text()').re_first('\d+')
            house['price'] = p.xpath('./span/text()').extract_first()
            house['rating'] = p.xpath('./em/text()').extract_first()
            yield house
