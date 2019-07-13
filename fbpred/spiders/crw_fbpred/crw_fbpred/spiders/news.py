# -*- coding: utf-8 -*-
import scrapy
import os
import json
import time
from datetime import datetime

class NewsSpider(scrapy.Spider):
    name = 'news'
    start_urls = ['https://globoesporte.globo.com/futebol/times/cruzeiro/ao-vivo/paginas-heroicas-e-imortais.ghtml']
    counter = 1
    path_file = ''
    urls = []
    first_time = True
    date = '10/08/2018'

    def populate(self):
        self.urls = open('links.csv', 'r').read().split(',')
        os.system('mkdir -p Dados')
        os.chdir("Dados")
        # with open(self.path_file, 'r') as fl:
        #     reader = csv.reader(fl, delimiter=',')
        #     for lin in reader:
        #         self.urls.append(lin)
    
    def date_correction(self, date):
        first = time.mktime(datetime.strptime(str(date), '%d/%m/%Y' ).timetuple())
        end = time.mktime(datetime.strptime(str(self.date), '%d/%m/%Y' ).timetuple())
        return end >= first

    def parse(self, response):
        if self.first_time:
            self.populate()
            self.first_time = False
            self.start_urls[0] = self.urls[0]


        date = response.xpath('.//time[contains(@itemprop, "datePublished")]/text()').extract_first()
        
        if self.date_correction(date):
            continue
        else:
            continue

        time = response.xpath('.//a[contains(@class, "header-editoria--link")]/text()').extract_first()
        title = response.xpath('//div[contains(@class, "title")]/meta/@content').extract().encode().decode('utf-8')
        author = response.xpath('//p[contains(@class, "content-publication-data__from")]/@title').extract()
        text = response.xpath('//p[contains(@class, "content-text__container")]/text()').extract()
        
        text = [p.encode().decode('utf-8') for p in text]
        
        
        # data = {'time':time, 'title':title, 'author':author, 'text':text}
        
        yield{
            'time': time,
            'title': title,
            'author': author,
            'text': text,
            'date': date,
            'id': self.counter
        }
        self.counter += 1
        # with open(str(self.counter)+'.json', 'w') as jsf:
        #     json.dump(data, jsf)
        #     self.counter+=1

        yield scrapy.Request(
            url=str(self.urls.pop(0)),
            callback=self.parse
        )
        
