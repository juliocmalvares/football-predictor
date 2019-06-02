# -*- coding: utf-8 -*-
import scrapy
import csv
import json
class News(scrapy.Spider):
    name = 'news'
    start_urls = ['https://globoesporte.globo.com/futebol/times/cruzeiro/ao-vivo/paginas-heroicas-e-imortais.ghtml']
    counter = 1
    path_file = ''
    urls = []
    first_time = True

    def populate(self):
        self.urls = open(self.path_file, 'r').read().split(',')
        # with open(self.path_file, 'r') as fl:
        #     reader = csv.reader(fl, delimiter=',')
        #     for lin in reader:
        #         self.urls.append(lin)
    
    def parse(self, response):
        if self.first_time:
            self.populate()
            self.first_time = False
            self.start_urls[0] = self.urls[0]

        time = response.xpath('.//a[contains(@class, "header-editoria--link")]/text()').extract_first()
        title = response.xpath('//div[contains(@class, "title")]/meta/@content').extract()
        author = response.xpath('//p[contains(@class, "content-publication-data__from")]/@title').extract()
        text = response.xpath('//p[contains(@class, "content-text__container")]/text()').extract()
        
        data = {'time':time, 'title':title, 'author':author, 'text':text}
        
        with open(str(self.counter)+'.json', 'w') as jsf:
            json.dump(data, jsf)
            self.counter+=1
        yield scrapy.Request(
            url=str(self.urls.pop(0)),
            callback=self.parse
        )
        
