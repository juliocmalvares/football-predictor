#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo
import json

client = pymongo.MongoClient(
	"mongodb+srv://fbpred:fbpred@fbpred-9mob3.mongodb.net/fbpred?retryWrites=true&w=majority")

collection = client['fbpred']['news']


for i in range(19741):
	js = collection.find_one({"id": str(i)})
	counter = 0
	try:
		if js['ratings'] == 0:
			if js['avaliations']['aval_1'] != '':
				counter += 1
			if js['avaliations']['aval_2'] != '':
				counter += 1
			if js['avaliations']['aval_3'] != '':
				counter += 1
		if counter > 0:
			print(">>> ratings: ", js['ratings'], " Counter: ",
				  counter, " avals: ", js['avaliations'])
			collection.update_one({"id": str(i)}, {"$set": {"ratings": counter}})
		else:
			print(">>> Sem modificação")
	except:
		print("Exception ocurred")
# dados = None
# with open("bd.json", "r") as jsf:
# 	dados = json.load(jsf)

# for i in dados:
# 	js = dados[i]
# 	js["id"] = i
# 	js.pop('avaliations')
# 	js['avaliations'] = {"aval_1": "", "aval_2":"", "aval_3":""}
# 	collection.insert_one(js)


# print(js)
# print(dados["1"])
