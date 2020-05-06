#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo
import json
import pprocess
import argparse
import logging
import pathlib

############ Configurations ############
logging.basicConfig(filename="debug.log", filemode="w", level=logging.DEBUG)
####################################

# client = pymongo.MongoClient(
#     "mongodb+srv://fbpred:fbpred@fbpred-9mob3.mongodb.net/fbpred?retryWrites=true&w=majority")

# collection = client['fbpred']['news']


class DataLoader(object):
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(
                "mongodb+srv://fbpred:fbpred@fbpred-9mob3.mongodb.net/fbpred?retryWrites=true&w=majority")
            print(">>> Connected to database")
        except:
            print("Error on connect to database")
        self.collection = None

    def download_data(self):
        p = pathlib.Path("backup_data.json")
        new_data = {}
        old_data = {}
        if p.exists():
            old_data = data = json.load(p.open())
            self.collection = self.client['fbpred']['news']
            cursor = self.collection.find(
                {"ratings": {"$gt": 0}, "id": {"$nin": list(data.keys())}})
            print("> Founded ", cursor.count(), " new tuples.")
            for i in cursor:
                i.pop("_id")
                new_data[i["id"]] = i
            for i in new_data.keys():
                old_data[i] = new_data[i]
            print(">>> A Backup file as created.", len(data), "samples.")
            self.__toJSON(old_data)
            return old_data
        else:
            self.collection = self.client['fbpred']['news']
            cursor = self.collection.find({"ratings": {"$gt": 0}})
            print("> Founded", cursor.count(), "tuples.")
            for i in cursor:
                i.pop("_id")
                new_data[int(i['id'])] = i
            print(">>> A Backup file as created.")
            self.__toJSON(new_data)
            return new_data

    def __toJSON(self, dic, pathname='backup_data.json'):
        with open(pathname, 'w') as jsf:
            json.dump(dic, jsf, indent=4, ensure_ascii=False)

    def loadJSON(self):
        js = json.load(open("backup_data.json", 'r'))
        return js

    def pprocess(self, dic, stw=True, stm=True):
        pp = pprocess.preprocessing()

        if stw == True and stm == True:
            print(">>> Processing text and title in removing stopwords and stemming.")
            for i in dic.keys():
                pp.applystw(dic[i], 'title', 'process_title')
                pp.applystw(dic[i], 'text', 'process_text')
                pp.applystem(dic[i], 'process_text', "process_text")
                pp.applystem(dic[i], 'process_title', "process_title")
        elif stw == True and stm == False:
            print(">>> Processing text and title in removing stopwords.")
            for i in dic.keys():
                pp.applystw(dic[i], 'title', 'process_title')
                pp.applystw(dic[i], 'text', 'process_text')
        elif stw == False and stm == True:
            print(">>> Processing text and title in stemming.")
            for i in dic.keys():
                pp.applystem(dic[i], 'process_text', "process_text")
                pp.applystem(dic[i], 'process_title', "process_title")
        self.__toJSON(dic)


def get_args():
    parser = argparse.ArgumentParser("LoadData")

    parser.add_argument("-a", "--download-all", action="store_true",
                        default=False, help="Download all data")
    parser.add_argument("-stw", "--clean-stw", action="store_true",
                        default=False, help="Clean stopwords from text and title")
    parser.add_argument("-stm", "--clean-stm", action="store_true",
                        default=False, help="Apply stemmer from text and title")
    parser.add_argument("-y", "--yes-all", action="store_true",
                        default=False, help="Download all and clean")
    parser.add_argument("-l", "--load-data", action="store_true",
                        default=False, help="Load data from existing file")
    return parser.parse_args()

def main():
    args = get_args()
    loader = DataLoader()
    data = {}

    if args.download_all:
        data = loader.download_data()
    if args.load_data:
        data = loader.loadJSON()
    if args.clean_stw:
        if data == {}:
            raise RuntimeError("You need to load or download data first")
        loader.pprocess(data, stw=True, stm=False)
    if args.clean_stm:
        if data == {}:
            raise RuntimeError("You need to load or download data first")
        loader.pprocess(data, stw=False, stm=True)
    if args.yes_all:
        data = loader.download_data()
        loader.pprocess(data)
    
    print(">>> All jobs done.")
    return data


if __name__ == "__main__":
    data = main()

# d = data()
# d.download_data()
# print(dados)
