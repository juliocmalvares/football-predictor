# -*- coding: utf-8 -*-
import scrapy


class CruzeiroLinksSpider(scrapy.Spider):
    name = 'cruzeiro_links'
    allowed_domains = ['https://globoesporte.globo.com/futebol/times/cruzeiro/index/feed/pagina-1.ghtml']
    start_urls = ['http://https://globoesporte.globo.com/futebol/times/cruzeiro/index/feed/pagina-1.ghtml/']

    def parse(self, response):
        pass
