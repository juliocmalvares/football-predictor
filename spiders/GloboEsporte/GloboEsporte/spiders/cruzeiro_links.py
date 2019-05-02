# -*- coding: utf-8 -*-
import scrapy
import hashlib

class CruzeiroLinksSpider(scrapy.Spider):
	name = 'cruzeiro_links'
	start_urls = ['https://globoesporte.globo.com/futebol/times/cruzeiro/index/feed/pagina-1.ghtml']
	links = []
	counter = 1
	arch = 'cruzeiro_links.csv'
	links_available = []
	first_time = True

	def populate(self):
		try:
			purelinks = open(self.arch, 'r').read().split(',\n')
		except:
			return
		for link in purelinks:
			if link not in self.links_available:
				self.links_available.append(hashlib.sha1(bytes(link, 'utf-8')).hexdigest())
		

	def parse(self, response):
		if self.first_time:
			self.populate()
			self.first_time = False			
		dlinks = response.xpath('.//a[contains(@class, "feed-post-link")]/@href').extract()
		for l in dlinks:
			self.links.append(l)
		self.counter+=1
		print(" >>> Counter:", self.counter)

		if self.counter % 10 == 0:
			fl = open(self.arch, 'a+')
			for link in self.links:
				if hashlib.sha1(bytes(link, 'utf-8')).hexdigest() not in self.links_available:
					fl.write(link + ',\n')
					self.links_available.append(hashlib.sha1(bytes(link, 'utf-8')).hexdigest())
				else:
					print(">>> Link já existente")
			self.links.clear()
			fl.close()
		yield scrapy.Request(
			url='https://globoesporte.globo.com/futebol/times/cruzeiro/index/feed/pagina-%i.ghtml' % self.counter,
			callback=self.parse
		)
