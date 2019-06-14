# -*- coding: utf-8 -*-
import os


def execute_links(time):
    os.chdir('crw_fbpred')
    os.system('scrapy crawl links')
    # os.system('scrapy runspider links.py -a time={}'.format(time))

def execute_news(file):
    # os.system('cd crw_fbpred')
    os.chdir('crw_fbpred')
    os.system('scrapy crawl news')
    # os.system('scrapy runspider news.py -a path_file={}'.format(file))


# execute_links('cruzeiro')
execute_news('links.csv')
