#-*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod

class Classifier(object, metaclass=ABCMeta):
    def __init__(self):
        self.data = None
        self.miscel = []
        self.retrospective = False
    
    @abstractmethod
    def training(self, equations):
        pass
    
    @abstractmethod
    def fit(self, equations, iterations):
        pass
    
    @abstractmethod
    def retrospective_analysis(self, equations):
        pass
    
    @abstractmethod
    def predict(self, sample):
        pass
