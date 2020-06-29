#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk
from joblib import Parallel, delayed
import time
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import spacy
from torchnlp.encoders.text import SpacyEncoder
from tqdm import tqdm


class preprocessing(object):
    def __init__(self, jobs=-2, language='portuguese'):
        self.__jobs = jobs
        self.__language = language
        self.stopwords = nltk.corpus.stopwords.words(self.__language)
        if self.__language == 'portuguese':
            self.stemmer = nltk.stem.RSLPStemmer()
        else:
            self.stemmer = nltk.stem.SnowballStemmer(self.__language)

    def stringer(self, lista):
        text = ''
        for words in lista:
            if words != '':
                text += words + ' '
        text.replace(" ,", ",")
        text.replace("  ", " ")
        return text

    def stremover(self, sentence):
        sentence = nltk.word_tokenize(sentence.lower())
        sentence = self.stringer(
            [p for p in sentence if p not in self.stopwords])
        return (sentence)

    def stem(self, sentence):
        sentence = nltk.word_tokenize(sentence.lower())
        sentence = [str(self.stemmer.stem(p)) for p in sentence]
        return self.stringer(sentence)

    def applystw(self, dados):
        dados_entrada = dados
        result = Parallel(n_jobs=self.__jobs, backend='loky')(
            delayed(self.stremover)(elem) for elem in tqdm(dados_entrada))
        # df[saida] = self.__stringer(result)
        return result

    def applystem(self, dados):
        dados_entrada = dados
        result = Parallel(n_jobs=self.__jobs, backend='loky')(
            delayed(self.stem)(elem) for elem in tqdm(dados_entrada))
        return result

    def tfidf(self, df, entrada):
        vectorizer = TfidfVectorizer(encoding="utf-8")
        transformer = TfidfTransformer(smooth_idf=False)

        corpus = [df[i][entrada] for i in df.keys()]
        classes = [df[i]["avaliations"]["aval_1"] for i in df.keys()]
        vector = vectorizer.fit_transform(corpus)
        tfidf = transformer.fit_transform(vector)
        return tfidf, classes

    def spacy(self, df, entrada, encoder=None):
        encoder = encoder
        corpus = [df[i][entrada] for i in df.keys()]
        print("Removendo StopWords")
        corpus = self.applystw(corpus)
        print("Radicalizando palavras")
        corpus = self.applystem(corpus)
        
        # print("corpus: ", corpus[:5])
        if encoder == None:
            encoder = SpacyEncoder(corpus)

        encoded_text = list()
        print("Creating tensors")
        for i in tqdm(range(len(corpus))):
            encoded_text.append(encoder.encode(corpus[i]))
        classes = [df[i]["avaliations"]["aval_1"] for i in df.keys()]
        # class_names = ["positiva", "negativa", "nfutebol", "neutra"]
        
        for i in range(len(classes)):
            if classes[i] == 'neutra':
                classes[i] = 0
            elif classes[i] == "positiva":
                classes[i] = 1
            elif classes[i] == "negativa":
                classes[i] = 2
            elif classes[i] == "nfutebol":
                classes[i] = 3
            else:
                classes[i] = -1

        return encoded_text, classes


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
