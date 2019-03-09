# -*- coding: utf-8 -*-
import scrapy


class CruzeiroLinksSpider(scrapy.Spider):
    name = 'cruzeiro_links'
    start_urls = ['https://globoesporte.globo.com/futebol/times/cruzeiro/index/feed/pagina-1.ghtml']
    links = []
    counter = 1
    arch = 'cruzeiro_links.csv'
    def parse(self, response):
        dlinks = response.xpath('.//a[contains(@class, "feed-post-link")]/@href').extract()
        for l in dlinks:
            self.links.append(l)
        self.counter+=1
        print(" >>> COUNTER:", self.counter)

        if self.counter % 10 == 0:
            fl = open(self.arch, 'a+')
            for link in self.links:
                fl.write(link + ',\n')
            self.links.clear()
            fl.close()
        yield scrapy.Request(
            url='https://globoesporte.globo.com/futebol/times/cruzeiro/index/feed/pagina-%i.ghtml' % self.counter,
            callback=self.parse
        )
