#!/usr/bin/python3
#-*- encoding:utf-8 -*-
import json
import pathlib
import html.parser

class JsonCorrect(object):
    def __init__(self):
        self.path = ''
        self.files = []
        self.dump = json.dump
        self.data = {}
        self.teams = json.load(open('teams.json'))
    
    def populate(self, path):
        self.path = path
        self.files = list(pathlib.Path('.').glob(self.path + '/*.json'))
    
    def union_matches(self):
        for i in self.files:
            js = json.load(i.open())
            id = js.pop('id')
            for i in self.teams.keys():
                if js['id_winner'] == int(i):
                    js['id_winner'] = self.teams[i]
                if js['id_home_team'] == int(i):
                    js['id_home_team'] = self.teams[i]
                if js['id_visiting_team'] == int(i):
                    js['id_visiting_team'] = self.teams[i]
            self.data[id] = js
        return self.data
    
    def union_statistics(self):
        for i in self.files:
            js = json.load(i.open())
            id = js.pop('id')
            for i in self.teams.keys():
                if js['team_id'] == int(i):
                    js['team_id'] = self.teams[i]
            self.data[id] = js
        return self.data
    
    def union_news(self):
        parser = html.parser.HTMLParser()
        
        for i in self.files:
            js = json.load(i.open())
            id = js.pop('id')
            for i in self.teams.keys():
                if js['team_id'] == int(i):
                    js['team_id'] = self.teams[i]
            js['title'] = parser.unescape(js['title'])
            js['text'] = parser.unescape(js['text'])
            self.data[id] = js
        return self.data
    
    def clear(self):
        self.files.clear()
        self.data.clear()
        self.path = ''
        
    def write(self, path):
        with open(path, 'w') as jsf:
            self.dump(self.data, jsf, indent=4, ensure_ascii=False)
            
# js = JsonCorrect()
# js.populate('matches')
# js.union_matches()
# js.write('matches.json')
# js.clear()

# js.populate('statistics')
# js.union_statistics()
# js.write('statistics.json')
# js.clear()

# js.populate('news')
# js.union_news()
# js.write('news.json')
# js.clear()

def spliter_parentese(text):
    aux = ''
    passou = False
    for i in text:
        if i == '[' or passou:
            if i == '[':
                passou = True
            aux += i
    aux = aux.replace('[', '')
    aux = aux.replace(']', '')
    return aux

def text_cleanner(text):
    text = text.replace('é', 'e')
    text = text.replace('thl', 'tl')
    text = text.replace('á', 'a')
    text = text.replace('ê', 'e')
    text = text.replace('ã', 'a')
    text = text.replace('ó', 'o')
    text = text.replace(' ', '-')
    text = text.lower()
    return text

class CleanerWiki(object):
    def __init__(self, path):
        self.path = path
        self.tx = open(path, 'r+').read()
        self.dat = list()
        for i in self.tx.split('---'):
            i = i.replace('\n', '')
            aux = i.split(';')
            del aux[0]
            d = {
                'data': aux[0],
                'mandant': aux[1],
                'placar': aux[2],
                'visitant': aux[3],
                'publico': aux[4],
                'renda': aux[5]
            }
            self.dat.append(d)
    
    def data_redefinition(self):
        for i in self.dat:
            data = i['data']
            data = spliter_parentese(data)
            dia = int(data.split(' ')[0])
            if dia < 10:
                dia = '0' + str(dia)
            
            mes = 0
            if data.split(' ')[-1].lower() == 'janeiro':
                mes = '01'
            elif data.split(' ')[-1].lower() == 'fevereiro':
                mes = '02'
            elif data.split(' ')[-1].lower() == 'março':
                mes = '03'
            elif data.split(' ')[-1].lower() == 'abril':
                mes = '04'
            elif data.split(' ')[-1].lower() == 'maio':
                mes = '05'
            elif data.split(' ')[-1].lower() == 'junho':
                mes = '06'
            elif data.split(' ')[-1].lower() == 'julho':
                mes = '07'
            elif data.split(' ')[-1].lower() == 'agosto':
                mes = '08'
            elif data.split(' ')[-1].lower() == 'setembro':
                mes = '09'
            elif data.split(' ')[-1].lower() == 'outubro':
                mes = 10
            elif data.split(' ')[-1].lower() == 'novembro':
                mes = 11
            elif data.split(' ')[-1].lower() == 'dezembro':
                mes = 12
            data = str(dia) + '/' + str(mes) + '/2018'
            i['data'] = data
            
    def team_redefinition(self):
        for i in self.dat:
            team_m = i['mandant'].split('=')[-1]
            team_v = i['visitant'].split('=')[-1]
            
            team_m = team_m.replace('{', '')
            team_m = team_m.replace('}', '')
            team_v = team_v.replace('{', '')
            team_v = team_v.replace('}', '')
            
            team_m = text_cleanner(team_m)
            team_v = text_cleanner(team_v)
            if team_m == 'internacional-rs':
                team_m = 'internacional'
            if team_v == 'internacional-rs':
                team_v = 'internacional'
            
            # print(team_m, team_v)
            i['mandant'] = team_m
            i['visitant'] = team_v
    
    def placar_redefinition(self):
        for i in self.dat:
            placar = i['placar']
            placar = placar.split('=')[-1].replace(' ', '')
            i['placar'] = placar
            golsm, golsv = 0, 0
            golsm = int(placar.split(',')[0])
            golsv = int(placar.split(',')[1])
            if golsm > golsv:
                i['vencedor'] = i['mandant']
            elif golsv > golsm:
                i['vencedor'] = i['visitant']
            else:
                i['vencedor'] = 'empate'
                
    def publico_redefinition(self):
        for i in self.dat:
            publico = i['publico']
            publico = publico.split("=")[-1]
            publico = publico.replace(' ', '')
            i['publico'] = publico
            
    def renda_redefinition(self):
        for i in self.dat:
            renda = i['renda']
            renda = renda.replace('}', '')
            renda = renda.split('=')[-1]
            if renda[0] == ' ':
                renda = renda.replace(' ', '', 1)
            i['renda'] = renda
    
    def writer(self):
        import csv
        with open('games.csv', 'w') as csvf:
            wr = csv.writer(csvf, delimiter=';')
            for i in self.dat:
                wr.writerow([i['data'], i['mandant'], i['visitant'], i['vencedor'], i['placar'], i['renda'], i['publico']])
            
c = CleanerWiki('games.txt')
c.data_redefinition()
c.team_redefinition()
c.placar_redefinition()
c.publico_redefinition()
c.renda_redefinition()
# print(c.dat)
c.writer()
for i in c.dat:
    print(i)