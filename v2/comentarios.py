#!/usr/bin/python3
# -*- coding:utf-8 -*-
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import csv
import json

"""
procurar glbComentarios-lista-resposta e o atributo data-total-replaies
//ul[contains(@class, "glbComentarios-lista-resposta-todos")]/li
"""
def clearComment(element):
    print(">>> id:", element.get_attribute("data-comentario-id"))
    aux = {}
    aux['name'] = element.find_element_by_tag_name("strong").text  #(by=By.XPATH, value="//strong[contains(@class, 'glbComentarios-dados-usuario-nome')]").text
    aux['text'] = element.find_element_by_tag_name('p').text  #(by=By.XPATH, value="//p[contains(@class, 'glbComentarios-texto-comentario')]").text
    aux['date'] = element.find_element_by_tag_name("abbr").get_attribute("title")  #(by=By.XPATH, value="//abbr[contains(@itemprop, 'commentTime')]").get_attribute("title")
    aux['likes'] = element.find_elements_by_tag_name("button")[1].text  #(by=By.XPATH, value="//button[contains(@class, 'voted')]")[0].text
    aux['unlikes'] = element.find_elements_by_tag_name("button")[2].text #find_elements(by=By.XPATH, value="//button[contains(@class, 'voted')]")[1].text

    # replies = element.find_element_by_xpath(".//div[contains(@class, 'glbComentarios-lista-resposta')]").get_attribute("data-total-replies")
    # print(">>> replies: ", replies)
    print(aux)
    print("\n")
    return aux

def getComentarios():
    link = "https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/marques-comenta-sobre-rever-e-guga-e-ve-situacoes-bem-encaminhadas-no-atletico-mg.ghtml"

    opt = Options()
    # opt.add_argument("--headless") #tela minimizada
    driver = webdriver.Chrome(options=opt)
    driver.get(link)
    driver.implicitly_wait(time_to_wait=10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    button_carregar = driver.find_elements(by=By.XPATH, value="//button[contains(@class, 'glbComentarios-botao-mais')]")[0]
    # driver.execute_script('window.scrollTo({},{})'.format(str(button_carregar.location['x']), str(button_carregar.location['y'])))
    try:
        button_carregar.click()
    except selenium.common.exceptions.ElementNotInteractableException:
        print("call again")
        getComentarios()

    elements = driver.find_elements(by=By.XPATH, value = "//ul[contains(@class, 'glbComentarios-lista-todos')]/li")
    # elements = driver.find_elements_by_xpath(".//div[contains(@class, 'glbComentarios-conteudo')]")
    # elements = driver.find_elements_by_class_name("glbComentarios-conteudo")
    # print(len(elements))

    comentarios = {}
    count = 0

    for li in elements:
        comentarios[count] = clearComment(li)
        count += 1
    with open("comentarios.json", "w") as jsf:
            json.dump(comentarios, jsf, ensure_ascii=False, indent=4)

    driver.close()


getComentarios()