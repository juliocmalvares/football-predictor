#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json


def clear(text):
    for i in range(10):
        text = text.replace("  ", " ", -1)
        text = text.replace(" .", ".", -1)
        text = text.replace(" ,", ",", -1)
        text = text.replace(" ;", ";", -1)
    text = text.replace("/", "", -1)

    return text


jsfinal = {}
with open("news.json", 'r') as jsf:
    js = json.load(jsf)
    for i in js:
        try:
            js[i]["text"] = clear(js[i]["text"])
            jsfinal[i] = js[i]
            jsfinal[i]["ratings"] = 0
            jsfinal[i]["avaliations"] = {0:'', 1:'', 2:''}
        except:
            print("Error on key", i)
print(jsfinal["12924"])

with open("bd.json", "w") as jsf:
    json.dump(jsfinal, jsf, ensure_ascii=False, indent=4)