# -*- coding: utf-8 -*-
import scrapy


class StatSpider(scrapy.Spider):
    name = 'stat'
    start_urls = ['https://veja.abril.com.br/placar/campeonato-brasileiro/cruzeiro-e-gremio-14042018/']

    def parse(self, response):
        pass
