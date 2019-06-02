#-*- encoding: utf8 -*-
#/usr/bin/python3

import csv
import json
import os
import numpy as np

class IO(object):
    def __init__(self):
        self.path = os.getcwd()
        self.broken = False
        self.ejson = json.encoder
        self.djson = json.decoder

    def __reader_csv(self, path, data):
        pass
    def __writer_csv(self, path, data):
        pass
    def __reader_json(self, path, data):
        pass
    def __writer_csv(self, path, data):
        pass
    
    def database_from_csv(self, path):
        pass
    
    def database_from_json(self, path):
        pass

    def csv_from_database(self, path, database):
        pass
    
    def json_from_database(self, path, database, broken):
        pass

    def write_log(self, path):
        pass