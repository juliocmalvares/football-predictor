#!/usr/bin/python3
# -*- coding:utf-8 -*-
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os
import csv
import json

"""
procurar glbComentarios-lista-resposta e o atributo data-total-replaies
//ul[contains(@class, "glbComentarios-lista-resposta-todos")]/li
"""

def teste():
    return

def clearSubComment(element):
    aux = {}
    aux['name'] = element.find_element_by_tag_name("strong").text  #(by=By.XPATH, value="//strong[contains(@class, 'glbComentarios-dados-usuario-nome')]").text
    # print(aux['name'])
    aux['text'] = element.find_element_by_tag_name("p").text  #(by=By.XPATH, value="//p[contains(@class, 'glbComentarios-texto-comentario')]").text
    aux['date'] = element.find_element_by_tag_name("abbr").get_attribute("title")  #(by=By.XPATH, value="//abbr[contains(@itemprop, 'commentTime')]").get_attribute("title")
    aux['likes'] = element.find_elements_by_tag_name("button")[1].text  #(by=By.XPATH, value="//button[contains(@class, 'voted')]")[0].text
    aux['unlikes'] = element.find_elements_by_tag_name("button")[2].text #find_elements(by=By.XPATH, value="//button[contains(@class, 'voted')]")[1].text
    print(aux, '\n')
    return aux

def clearComment(driver, element):
    aux = {}
    aux['name'] = element.find_element_by_tag_name("strong").text  #(by=By.XPATH, value="//strong[contains(@class, 'glbComentarios-dados-usuario-nome')]").text
    aux['text'] = element.find_element_by_tag_name('p').text  #(by=By.XPATH, value="//p[contains(@class, 'glbComentarios-texto-comentario')]").text
    
    if aux['text']  == '':
        return {}

    aux['date'] = element.find_element_by_tag_name("abbr").get_attribute("title")  #(by=By.XPATH, value="//abbr[contains(@itemprop, 'commentTime')]").get_attribute("title")
    aux['likes'] = element.find_elements_by_tag_name("button")[1].text  #(by=By.XPATH, value="//button[contains(@class, 'voted')]")[0].text
    aux['unlikes'] = element.find_elements_by_tag_name("button")[2].text #find_elements(by=By.XPATH, value="//button[contains(@class, 'voted')]")[1].text
    aux['replies'] = []
    # replies = element.find_element_by_xpath(".//div[contains(@class, 'glbComentarios-lista-resposta')]").get_attribute("data-total-replies")
    
    
    replies = None
    n_replies = int(element.get_attribute("data-comentario-qtd_replies"))
    aux['n_replies'] = n_replies
    if n_replies > 0:
        # if n_replies > 2:
        #     # scroller = element.find_elements_by_tag_name("button")[2]
        #     # driver.execute_script("arguments[0].scrollIntoView();", scroller)
        #     bt_mais = element.find_element_by_class_name("glbComentarios-lista-bt-paginar")
        #     try:
        #         bt_mais.click()
        #     except:
        #         print("Unclicable")
        #         return aux

        replies = element.find_elements_by_tag_name("li")#find_elements_by_xpath("//div[contains(@class, 'glbComentarios-lista-resposta')]/li")
        for i in replies:
            aux['replies'].append(clearSubComment(i))
    else:
        return aux

    # if n_replies > 0:
    #     if n_replies > 2:
    #         bt_mais = element.find_elements_by_tag_name("button")[3]
    #         driver.execute_script("arguments[0].scrollIntoView();", bt_mais)
    #         bt_mais.click()
    #         print ("Position confirmed and clicked")
    #     # driver.implicitly_wait(10)
    #     replies = element.find_elements_by_tag_name("li")
    #     for i in replies:
    #         aux['replies'].append(clearSubComment(i))


    # print(aux)
    # print("\n")
    return aux

def getComentarios():
    link = "https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/marques-comenta-sobre-rever-e-guga-e-ve-situacoes-bem-encaminhadas-no-atletico-mg.ghtml"

    opt = Options()
    opt.add_argument("-window-size=1920,1080")
    # opt.add_argument("--headless") #tela minimizada
    driver = webdriver.Chrome(options=opt)
    driver.get(link)
    driver.implicitly_wait(time_to_wait=10)
    element_aux = driver.find_elements_by_xpath("//a[contains(@class, 'entities__list-itemLink')]")[0]
    
    driver.execute_script("arguments[0].scrollIntoView();", element_aux)
    button_carregar = driver.find_elements(by=By.XPATH, value="//button[contains(@class, 'glbComentarios-botao-mais')]")[0]

    try:
        button_carregar.click()
    except:
        print("call again")
        driver.close()
        getComentarios()

    elements = driver.find_elements(by=By.XPATH, value = "//ul[contains(@class, 'glbComentarios-lista-todos')]/li")
    # elements = driver.find_elements_by_tag_name("li")
    print(">>> ", len(elements), "items")
    # elements = driver.find_elements_by_xpath(".//div[contains(@class, 'glbComentarios-conteudo')]")
    # elements = driver.find_elements_by_class_name("glbComentarios-conteudo")
    # print(len(elements))

    # btn_mais = driver.find_elements_by_class_name("button.glbComentarios-lista-bt-paginar")
    # print(len(btn_mais))
    # for i in btn_mais:
    #     i.click()
    #     print("Clicked")
    comentarios = {}
    count = 0




    spam_buttons = driver.find_elements(by=By.XPATH, value = "//button[contains(@class, 'glbComentarios-lista-bt-paginar')]")
    print("Tamanho antes",len(spam_buttons))
    spam_buttons = [p for p in spam_buttons if p.is_displayed()]
    print("Tamanho dps",len(spam_buttons))
    print(">>> buttons pag: ", len(spam_buttons))
    for bt in spam_buttons:
        driver.execute_script("arguments[0].scrollIntoView();", bt)
        try:
            bt.click()
            print("Clicked")
        except:
            print("Error")






    for li in elements:
        coment = clearComment(driver, li)
        if coment != {}:
            comentarios[count] = coment
            count += 1
    with open("comentarios.json", "w") as jsf:
            json.dump(comentarios, jsf, ensure_ascii=False, indent=4)

    driver.close()


getComentarios()