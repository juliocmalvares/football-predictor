#!/usr/bin/python3
import pandas
import json
import pathlib

class dataframe_generator(object):
    def __init__(self):
        self.files = list(pathlib.Path('../data').glob('*'))

    def gen_match(self):
        path = ''
        for i in self.files:
            if i.name == 'matches.json':
                path = i
        js = json.load(path.open())
        df = pandas.DataFrame(data=js).T
        return df

    def gen_statistics(self):
        path = ''
        for i in self.files:
            if i.name == 'statistics.json':
                path = i
        js = json.load(path.open())
        df = pandas.DataFrame(data=js).T
        return df

    def gen_news(self):
        path = ''
        for i in self.files:
            if i.name == 'news.json':
                path = i
        js = json.load(path.open())
        df = pandas.DataFrame(data=js).T
        return df
# df = pandas.DataFrame(data=js).T

# dt = dataframe_generator()
# df = dt.gen_news()
# print(df.head())