# -*- coding: utf-8 -*-
import scrapy


class CruzeiroLinksSpider(scrapy.Spider):
    name = 'cruzeiro_links'
    start_urls = ['http://globoesporte.globo.com/futebol/times/cruzeiro/index/feed/pagina-1.ghtml/']
    links = []
    counter = 1
    def parse(self, response):
        dlinks = response.xpath('.//a[contains(@class, "feed-post-link")]/@href').extract()
        for l in dlinks:
            self.links.append(l)
        self.counter+=1
        yield scrapy.Request(
            url='http://globoesporte.globo.com/futebol/times/cruzeiro/index/feed/pagina-%i.ghtml/' % self.counter,
            callback=self.parse
        )
