#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########## Melhorias ####################
# melhorar o path de arquivos
# fazer verificação de existencia de arquivo

############ Imports ############
import argparse
import pathlib
import json
import logging
import time
from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.by import By
import os
import csv
import sys
import urllib3
from lxml import html
from joblib import Parallel, delayed
from tqdm import tqdm
from helpmessage import help_message


####################################
teams = {
    1: "sao-paulo",
    2: "vasco",
    3: "atletico-mg",
    4: "ceara",
    5: "corinthians",
    6: "fluminense",
    7: "parana-clube",
    8: "palmeiras",
    9: "sport",
    10: "vitoria",
    11: "bahia",
    12: "botafogo",
    13: "flamengo",
    14: "cruzeiro",
    15: "chapecoense",
    16: "internacional",
    17: "gremio",
    18: "athletico-pr",
    19: "america-mg",
    20: "santos",
    21: "empate"
}
############ Configurations ############
logging.basicConfig(filename="debug.log", filemode="w", level=logging.DEBUG)
####################################


class Crawler:
    def __init__(self, team, dataLimit_init=None, dataLimit_end=None, qtPublic=None, backend="urllib"):
        '''
        qtPublic = quantidade de publicações a serem baixadas;
        dataLimit_init = data limite da ultima publicação a ser baixada
        backend = em que plataforma o crawler vai fazer request (urllib ou selenium)
        '''
        if not self.exists_path("links"):
            os.mkdir('links')
        self.crawled_team = team
        self.teams = {
            1: "sao-paulo",
            2: "vasco",
            3: "atletico-mg",
            4: "ceara",
            5: "corinthians",
            6: "fluminense",
            7: "parana-clube",
            8: "palmeiras",
            9: "sport",
            10: "vitoria",
            11: "bahia",
            12: "botafogo",
            13: "flamengo",
            14: "cruzeiro",
            15: "chapecoense",
            16: "internacional",
            17: "gremio",
            18: "athletico-pr",
            19: "america-mg",
            20: "santos",
            21: "empate"
        }
        self.crawled_links = []
        self.real_links = []
        self.initial_link = "https://globoesporte.globo.com/futebol/times/myteam/index/feed/pagina-npage.ghtml"
        self.base_link = "https://globoesporte.globo.com/futebol/times/myteam"
        self.driver = None
        if dataLimit_init != None:
            self.data_limite_init = time.mktime(datetime.strptime(
                str(dataLimit_init), "%d/%m/%Y").timetuple())
            self.data_limite_end = time.mktime(datetime.strptime(
                str(dataLimit_end), "%d/%m/%Y").timetuple())
            self.flag_data_control = True
            self.auxdata = dataLimit_init
        else:
            self.data_limite_init = None
            self.flag_data_control = False
        self.counter_links = qtPublic
        self.backend = backend
        self.urlcrawler = urllib3.PoolManager(num_pools=50, maxsize=10)
        self.urls_to_visit = None
        self.counter_news = 0

    def __control_url(self):
        if self.crawled_team == "athletico-pr" or self.crawled_team == "parana-clube":
            self.initial_link = self.initial_link.replace(
                "https://globoesporte.globo.com/futebol/times", "https://globoesporte.globo.com/pr/futebol/times")
            self.base_link = "https://globoesporte.globo.com/pr/futebol/times"
        elif self.crawled_team == "bahia" or self.crawled_team == "vitoria":
            self.initial_link = self.initial_link.replace(
                "https://globoesporte.globo.com/futebol/times", "https://globoesporte.globo.com/ba/futebol/times")
            self.base_link = "https://globoesporte.globo.com/ba/futebol/times"
        elif self.crawled_team == "ceara":
            self.initial_link = self.initial_link.replace(
                "https://globoesporte.globo.com/futebol/times", "https://globoesporte.globo.com/ce/futebol/times")
            self.base_link = "https://globoesporte.globo.com/ce/futebol/times"
        elif self.crawled_team == "chapecoense":
            self.initial_link = self.initial_link.replace(
                "https://globoesporte.globo.com/futebol/times", "https://globoesporte.globo.com/sc/futebol/times")
            self.base_link = "https://globoesporte.globo.com/sc/futebol/times"
        elif self.crawled_team == "internacional" or self.crawled_team == "gremio":
            self.initial_link = self.initial_link.replace(
                "https://globoesporte.globo.com/futebol/times", "https://globoesporte.globo.com/rs/futebol/times")
            self.base_link = "https://globoesporte.globo.com/rs/futebol/times"
        elif self.crawled_team == "santos":
            self.initial_link = self.initial_link.replace(
                "https://globoesporte.globo.com/futebol/times", "https://globoesporte.globo.com/sp/santos-e-regiao/futebol/times")
            self.base_link = "https://globoesporte.globo.com/sp/santos-e-regiao/futebol/times"
        elif self.crawled_team == "sport":
            self.initial_link = self.initial_link.replace(
                "https://globoesporte.globo.com/futebol/times", "https://globoesporte.globo.com/pe/futebol/times")
            self.base_link = "https://globoesporte.globo.com/pe/futebol/times"

    def exists_path(self, pathname):
        p = pathlib.Path("./" + pathname)
        logging.debug("The path returns " + str(p.exists()) +
                      " in exists_path function for the " + pathname + " path.")
        return p.exists()

    def set_team(self, team):
        self.crawled_team = team

    def exists_file(self, filename):
        return pathlib.Path("./" + filename).is_file()

    def __clear_links(self, pages):
        for i in pages:
            if self.base_link not in i:
                pages.remove(i)
        return pages

    def data_control(self):
        if self.data_limite_init != None:
            if len(self.crawled_links) > 0:
                link_request = self.urlcrawler.request(
                    "GET", self.crawled_links[-1])
            else:
                return False
            root = html.fromstring(link_request.data)
            try:
                date = root.xpath(
                    ".//time[contains(@itemprop, 'datePublished')]")[0]
                data_publicacao = time.mktime(datetime.strptime(
                    str(date.text.split(" ")[1]), "%d/%m/%Y").timetuple())
                self.urlcrawler.clear()
                link_request.close()
            except:
                return False
            # print(">>> Date: ",date.text, data_publicacao > self.data_limite_init)
            # print("> Data control: ",data_publicacao, self.data_limite_init, self.data_limite_end, self.data_limite_end > data_publicacao > self.data_limite_init)
            print(":>>Control Full")
            print("::Data_public: ", data_publicacao)
            print("::Data init/end, cond", self.data_limite_init, self.data_limite_end, self.data_limite_end > data_publicacao > self.data_limite_init, '\n')
            return self.data_limite_end > data_publicacao > self.data_limite_init
        return False

    def data_control_aux(self):
        if self.data_limite_init != None:
            if len(self.crawled_links) > 0:
                link_request = self.urlcrawler.request(
                    "GET", self.crawled_links[-1])
            else:
                return False
            root = html.fromstring(link_request.data)
            try:
                date = root.xpath(
                    ".//time[contains(@itemprop, 'datePublished')]")[0]
                data_publicacao = time.mktime(datetime.strptime(
                    str(date.text.split(" ")[1]), "%d/%m/%Y").timetuple())
                self.urlcrawler.clear()
                link_request.close()
            except:
                return False
            # print(">>> Date: ",date.text, data_publicacao > self.data_limite_init)
            # print("> Data control aux: ",data_publicacao, self.data_limite_init, self.data_limite_end, data_publicacao > self.data_limite_init)
            print(";>>Control aux")
            print(";;Data_public: ", data_publicacao)
            print(";;Data init/end, cond", self.data_limite_init, self.data_limite_end, data_publicacao > self.data_limite_init, '\n')
            return data_publicacao > self.data_limite_init
        return False


    def get_links_with_urllib(self):
        os.chdir("links")
        if self.exists_file(self.crawled_team.replace("-", "_") + ".csv"):
            resp = input("Arquivo de links já existente, sobrescrever? (s/n) ")
            if resp == "s" or resp == "S":
                os.remove(self.crawled_team.replace("-", "_") + ".csv")
            else:
                os.chdir("..")
                return

        self.__control_url()
        self.initial_link = self.initial_link.replace(
            "myteam", self.crawled_team)
        self.base_link = self.base_link.replace("myteam", self.crawled_team)

        '''
        control with data
        '''
        if self.flag_data_control:
            cont_link = 1
            while True:
                
                link_get = self.initial_link.replace("npage", str(cont_link))
                print(">> Visited:", link_get)
                beg = time.time()
                request = self.urlcrawler.request("GET", link_get)
                end = time.time()
                print(">>>: Tempo de requisição urllib3: ", end-beg, link_get, request.status)
                

                if request.status == 200:
                    # print('Request 200')
                    tree = html.fromstring(request.data)
                    pages = tree.xpath(
                        ".//a[contains(@class, 'feed-post-link')]")
                    # print(pages[0].values())
                    for i in pages:
                        if self.base_link in i.values()[0]:
                            self.crawled_links.append(i.values()[0])
                    if self.data_control():
                        for i in pages:
                            if self.base_link in i.values()[0]:
                                self.real_links.append(i.values()[0])
                    logging.debug(
                        "Crawled " + str(len(self.crawled_links)) + " links.")
                    cont_link += 1
                    # print(cont_link)
                else:
                    cont_link += 1
                    logging.debug("Error on page " + request.geturl())
                
                if self.data_control() == False and self.data_control_aux() == False:
                    break
                self.urlcrawler.clear()
        else:
            if self.counter_links == None:
                self.counter_links = 10
                print(">>> Baixando 10 páginas de links [Padrão]")
            else:
                print(">>> Baixando ", self.counter_links, " páginas de links!")
            for i in range(1, self.counter_links):
                link_get = self.initial_link.replace("npage", str(i))
                print(">> Link:", link_get)
                beg = time.time()
                request = self.urlcrawler.request("GET", link_get)
                end = time.time()
                # print(">>>: Tempo de requisição urllib3: ", float(end - beg))
                if request.status == 200:
                    tree = html.fromstring(request.data)
                    pages = tree.xpath(
                        ".//a[contains(@class, 'feed-post-link')]")
                    # print(pages[0].values())
                    for i in pages:
                        if self.base_link in i.values()[0]:
                            self.crawled_links.append(i.values()[0])
                    # request.close() VERIFICAR
                    logging.debug(
                        "Crawled " + str(len(self.crawled_links)) + " links.")
                else:
                    logging.debug("Error on page " + request.geturl())

        with open(self.crawled_team.replace("-", "_") + ".csv", 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            for i in self.real_links:
                writer.writerow([i])
        print("Crawled ", len(self.real_links))
        os.chdir("..")
        # self.crawled_links.clear()
        # self.real_links.clear()

    def __populate_urlstovisit(self):
        os.chdir("links")
        self.urls_to_visit = []
        arquivos = list(pathlib.Path('.').glob("*.csv"))
        # print(arquivos)
        for i in arquivos:
            # print("Abrindo ", i.name)
            logging.debug("Abrindo arquivo " + i.name)
            with i.open("r") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                for i in reader:
                    self.urls_to_visit.append(i[0])
        os.chdir("..")
        return

    def __stringer(self, lista):
        text = ''
        for words in lista:
            text += words + ' '
        return text

    def __getnew(self, link):
        request = None
        if self.urlcrawler != None:
            try:
                request = self.urlcrawler.request("GET", link)
            except:
                logging.debug("Error on link " + str(link))
            if request == None:
                print("Request nula")
                return
            if request.status == 200:
                tree = html.fromstring(request.data)
                info = dict()
                try:
                    info["time"] = (tree.xpath(
                        ".//a[contains(@class, 'header-editoria--link')]")[0]).text
                    info["date"] = tree.xpath(
                        ".//time[contains(@itemprop, 'datePublished')]/text()")[0]
                    info["title"] = self.__stringer(tree.xpath(
                        "//div[contains(@class, 'title')]/meta/@content"))
                    info["author"] = tree.xpath(
                        "//p[contains(@class, 'content-publication-data__from')]/@title")[0]
                    info["text"] = self.__stringer(tree.xpath(
                        "//p[contains(@class, 'content-text__container')]/text()"))
                    info["url"] = request.geturl()
                    logging.debug(
                        "Informations crawled successfully " + info["url"])
                except:
                    logging.debug(
                        "Exception ocurred on link " + request.geturl())
                self.urlcrawler.clear()
                request.close()
                try:
                    with open(info['time'].replace("-", "_") + "_" + str(self.counter_news) + ".json", "w") as jsf:
                        json.dump(info, jsf, indent=4, ensure_ascii=False)
                        self.counter_news += 1
                except:
                    print("Exception")


    def get_news_with_urllib(self, parallel=True):
        self.__populate_urlstovisit()
        news = []
        os.chdir("news")
        #Fazer a verificação do paralelo
        Parallel(n_jobs=4, backend="threading")(
            delayed(self.__getnew)(elem) for elem in tqdm(self.urls_to_visit))
        os.chdir("..")
        self.__correction_json_news()

    def __cleartext(self, text):
        for i in range(10):
            text = text.replace("  ", " ", -1)
            text = text.replace(" .", ".", -1)
            text = text.replace(" ,", ",", -1)
            text = text.replace(" ;", ";", -1)
        text = text.replace("/", "", -1)
        return text

    def __correction_aux(self):
        jsfinal = {}
        with open("news.json", 'r') as jsf:
            js = json.load(jsf)
            for i in js:
                try:
                    js[i]["text"] = self.__cleartext(js[i]["text"])
                    jsfinal[i] = js[i]
                    jsfinal[i]["ratings"] = 0
                    jsfinal[i]["avaliations"] = {0:'', 1:'', 2:''}
                except:
                    print("Error on key", i)
        with open("bd.json", "w") as jsf:
            json.dump(jsfinal, jsf, ensure_ascii=False, indent=4)

    def __correction_json_news(self):
        os.chdir("news")
        arquivos = sorted(pathlib.Path(".").glob("*.json"))
        news = {}
        for i in arquivos:
            js = json.load(i.open())
            news[(i.name.split("_")[-1]).split(".")[0]] = js
            js["time"] = js["time"].lower()
            js["time"] = js["time"].replace("é", "e")
            js["time"] = js["time"].replace("ê", "e")
            js["time"] = js["time"].replace("á", "a")
            js["time"] = js["time"].replace("ó", "o")
            js["time"] = js["time"].replace(" ", "_")
            js["time"] = js["time"].replace("-", "_")
            js["time"] = js["time"].replace("ã", "a")

        os.chdir("..")
        with open("news.json", "w") as jsf:
            json.dump(news, jsf, indent=4, ensure_ascii=False)
        self.__correction_aux()

    def download_all(self, data_control=False, data_init=None, data_end=None, npublic=None):
        path = pathlib.Path("./links")
        if path.exists() and path.is_dir():
            arqs = list(path.glob("*"))
            for i in arqs:
                i.unlink()
            path.rmdir()
            os.mkdir("links")

        if data_control == False:
            return
        else:
            for i in self.teams.keys():
                self.__init__(team=self.teams[i],
                              dataLimit_init=data_init, dataLimit_end=data_end, qtPublic=npublic)
                self.get_links_with_urllib()


def get_args():
    """
    Get arguments
    """
    parser = argparse.ArgumentParser("GloboEsporteWebCrawler", description="A news crawler and GloboEsporte website links", epilog=help_message, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-a", "--download-all", action="store_true",
                        default=False, help="Download all news from all teams.")
    parser.add_argument("-n", "--download-news", action="store_true",
                        default=False, help="Download all news from existing links.")
    parser.add_argument("-y", "--year", action="store_true",
                        default=False, help="Set year of the competition.")
    parser.add_argument("data_init", nargs="?", const="str")
    parser.add_argument("data_end", nargs="?", const="str")
    # parser.add_argument("-h", "--help", action='help', help = help_message)
    return parser.parse_args()


def main():
    args = get_args()
    crawler = Crawler(teams[1])
    # crawler.correction_json_news()
    # print(args.data_init, args.data_end)
    if args.download_all:
        if args.data_init == None:
            print("Download all option")
            crawler.download_all(npublic=20)
        else:
            if args.data_init != None and args.data_end != None:
                print(">>> Downloading with data")
                crawler.download_all(data_control=True, data_init=args.data_init, data_end=args.data_end)
            else:
                raise Exception("You need to provide two datas.")

    if args.download_news:
        print(":>>> Download news from existing links")
        crawler.get_news_with_urllib()


if __name__ == "__main__":
    main()

