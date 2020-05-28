#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk
from joblib import Parallel, delayed
import time
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer

class preprocessing(object):
    def __init__(self, jobs=-2, language='portuguese'):
        self.__jobs = jobs
        self.__language = language
        self.__stopwords = nltk.corpus.stopwords.words(self.__language)
        if self.__language == 'portuguese':
            self.__stemmer = nltk.stem.RSLPStemmer()
        else:
            self.__stemmer = nltk.stem.SnowballStemmer(self.__language)

    def __stringer(self, lista):
        text = ''
        for words in lista:
            if words != '':
                text += words + ' '
        text.replace(" ,", ",")
        text.replace("  ", " ")
        return text

    def __stremover(self, sentence):
        sentence = nltk.word_tokenize(sentence.lower())
        sentence = self.__stringer(
            [p for p in sentence if p not in self.__stopwords])
        return (sentence)

    def __stem(self, sentence):
        sentence = nltk.word_tokenize(sentence.lower())
        sentence = [str(self.__stemmer.stem(p)) for p in sentence]
        return self.__stringer(sentence)

    def applystw(self, df, entrada, saida):
        tkn = nltk.tokenize.SpaceTokenizer()
        dados_entrada = tkn.tokenize(df[entrada])
        result = Parallel(n_jobs=self.__jobs, backend='loky')(
            delayed(self.__stremover)(elem) for elem in (dados_entrada))
        df[saida] = self.__stringer(result)

    def applystem(self, df, entrada, saida):
        tkn = nltk.tokenize.SpaceTokenizer()
        dados_entrada = tkn.tokenize(df[entrada])
        result = Parallel(n_jobs=self.__jobs, backend='loky')(
            delayed(self.__stem)(elem) for elem in (dados_entrada))
        df[saida] = self.__stringer(result)

    def tfidf(self, df, entrada):
        vectorizer = TfidfVectorizer(encoding="utf-8")
        transformer = TfidfTransformer(smooth_idf=False)

        corpus = [df[i][entrada] for i in df.keys()]
        classes = [df[i]["avaliations"]["aval_1"] for i in df.keys()]
        vector = vectorizer.fit_transform(corpus)
        tfidf = transformer.fit_transform(vector)
        return tfidf, classes


    def toPickle(self, df, name):
        df.to_pickle(name)

    def fromPickle(self, path):
        df = pandas.read_pickle(path)
        return df

# import load
# import pprocess
# data = load.DataLoader().download_data()
# proc = pprocess.preprocessing()
# tfidf, classes = proc.tfidf(data, "text")
