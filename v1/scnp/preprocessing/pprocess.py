import nltk
from joblib import Parallel, delayed
import time
import pandas


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
            text += words + ' '
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
        result = Parallel(n_jobs=self.__jobs, backend='loky', verbose=10)(
            delayed(self.__stremover)(elem) for elem in df[entrada])
        df[saida] = result

    def applystem(self, df, entrada, saida):
        result = Parallel(n_jobs=self.__jobs, backend='loky', verbose=10)(
            delayed(self.__stem)(elem) for elem in df[entrada])
        df[saida] = result

    def toPickle(self, df, name):
        df.to_pickle(name)

    def fromPickle(self, path):
        df = pandas.read_pickle(path)
        return df