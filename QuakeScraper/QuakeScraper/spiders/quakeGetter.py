import scrapy


class QuakegetterSpider(scrapy.Spider):
    name = 'quakeGetter'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        pass
