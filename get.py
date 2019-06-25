#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Opção para abrir driver sem interface
opt = Options()
opt.add_argument("--headless")

driver = webdriver.Chrome(options=opt)
driver.get('https://veja.abril.com.br/placar/campeonato-brasileiro/atletico-mg-e-botafogo-01122018/');
x = driver.find_element_by_id('game-stats');

print(x.text)
print(x.get_attribute('innerHTML'))
