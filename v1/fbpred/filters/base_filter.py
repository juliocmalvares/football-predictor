#-*- encoding: utf8 -*-
#/usr/bin/python3

from abc import ABCMeta, abstractmethod

class Filter(object, metaclass=ABCMeta):
    def __init__(self):
        self.aplicator = None
        self.jobs = 4
    
    @abstractmethod
    def aplication(self, elem):
        pass