# -*- coding: utf-8 -*-
import scrapy
import hashlib
import scrapy
import hashlib

class Links(scrapy.Spider):
	name = 'links'
	time = '' # -a time='time' para passar o parâmetro
	start_urls = ['https://globoesporte.globo.com/futebol/times/{}/index/feed/pagina-1.ghtml'.format(time)]
	links = []
	counter = 1
	file = 'cruzeiro_links.csv'
	links_available = []
	first_time = True
	base_link = 'https://globoesporte.globo.com/futebol/times/%s' % time

	def populate(self):
		try:
			purelinks = open(self.file, 'r').read().split(',\n')
		except:
			return
		for link in purelinks:
			if link not in self.links_available:
				self.links_available.append(hashlib.sha1(bytes(link, 'utf-8')).hexdigest())
		
#globoesporte.globo.com/futebol/times/time
	def parse(self, response):

		if self.first_time:
			self.populate()
			self.first_time = False			
		dlinks = response.xpath('.//a[contains(@class, "feed-post-link")]/@href').extract()
		for l in dlinks:
			self.links.append(l)
		self.counter+=1
		# print(" >>> Counter:", self.counter)
		if self.counter % 10 == 0:
			fl = open(self.file, 'a+')
			for link in self.links:
				if (hashlib.sha1(bytes(link, 'utf-8')).hexdigest() not in self.links_available) and (self.base_link in link):
					print(">>>",link, "\n>>>", self.base_link)
					fl.write(link + ',\n')
					self.links_available.append(hashlib.sha1(bytes(link, 'utf-8')).hexdigest())
			self.links.clear()
			fl.close()
		yield scrapy.Request(
			url='https://globoesporte.globo.com/futebol/times/cruzeiro/index/feed/pagina-%i.ghtml' % self.counter,
			callback=self.parse
		)


#response.xpath('.//a[contains(@class, "header-editoria--link")]/text()').extract_first() Time
#response.xpath('//div[contains(@class, "title")]/a/text()').extract_first() Time modo 2


# response.xpath('//div[contains(@class, "title")]/meta/@content').extract() Titulo e subtitulo

#response.xpath('//p[contains(@class, "content-publication-data__from")]/@title').extract()   Autor

#response.xpath('//p[contains(@class, "content-text__container")]/text()').extract() Texto

