#!/usr/bin/python3
# -*- coding:utf-8 -*-
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from eventlistenner import Listenner
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support import expected_conditions


import os
import csv
import json
from joblib import Parallel, delayed
from tqdm import tqdm

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
    # print(aux, '\n')
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
        replies = element.find_elements_by_tag_name("li")#find_elements_by_xpath("//div[contains(@class, 'glbComentarios-lista-resposta')]/li")
        for i in replies:
            aux['replies'].append(clearSubComment(i))

    return aux

def getComentarios(crawled_link):
    link = crawled_link
    opt = Options()
    opt.add_argument("-window-size=1920,1080") #seting size of window
    # opt.add_argument("--headless") #tela minimizada
    listenner = Listenner() #invoking my listenner
    driver = EventFiringWebDriver(webdriver.Chrome(options=opt), listenner) #joining the driver with the listenner

    driver.get(link)

    """
        In the code snippet below, we use a DOM element as a "scapegoat" to position the screen in the place we would like,
         due to the fact that the website's comments tab is only invoked when positioning the screen in place.
    """
    element_aux = driver.find_elements_by_xpath("//div[contains(@class, 'entities')]")[0]
    driver.execute_script("arguments[0].scrollIntoView();", element_aux)
    
    """
        In the excerpt below, we use WebDriverWait together with ExceptConditions to wait for the desired element to be visible in the DOM before just clicking!
        The element is the "Load all comments" button
    """
    load_button = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'glbComentarios-botao-mais')]")))
    load_button.click()

    """
        Here we invoke all the elements that contain comments and set the variables to receive them
    """
    elements = driver.find_elements(by=By.XPATH, value = "//ul[contains(@class, 'glbComentarios-lista-todos')]/li")
    comentarios = {}
    count = 0

    """
    The excerpt below is necessary because, when a comment has more than three replies, the site inserts a button to load all replies.
    Thus, they are not visible in the DOM and the click is necessary.
    We look for everyone, we clean the ones that are unnecessary for us (the invisible ones on the screen that are part of the 
    favorite comments, we work in the tab of all comments) and we make the clicks.
    """
    spam_buttons = driver.find_elements(by=By.XPATH, value = "//button[contains(@class, 'glbComentarios-lista-bt-paginar')]")
    spam_buttons = [p for p in spam_buttons if p.is_displayed()]
    
    for bt in spam_buttons:
        driver.execute_script("arguments[0].scrollIntoView();", bt)
        bt.click()

    """
    Then, we just invoke the clearComment function for all elements finded.
    """
    for li in elements:
        coment = clearComment(driver, li)
        if coment != {}:
            comentarios[count] = coment
            count += 1
    
    driver.quit()
    return comentarios

def get(links):
    links = links

    coments = dict(Parallel(n_jobs=4, backend='threading')(
        delayed(getComentarios)(link) for link in tqdm(links)))
    with open("comentarios.json", "w") as jsf:
            json.dump(coments, jsf, ensure_ascii=False, indent=4)

links = [
    "https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/marques-comenta-sobre-rever-e-guga-e-ve-situacoes-bem-encaminhadas-no-atletico-mg.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/atletico-mg-ostenta-otimos-numeros-na-libertadores-nesta-decada-e-compoe-top-3-no-brasil.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/sombra-para-ricardo-oliveira-atacante-do-cerro-porteno-entra-na-mira-do-atletico-mg.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/atletico-mg-repete-formula-na-contratacao-de-guga-e-prepara-terreno-para-negociar-emerson.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/blanco-evita-dar-prazo-para-voltar-ao-atletico-mg-mas-projeta-2019-sem-lesoes-e-pensa-em-jogar-com-elias.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/leo-silva-vai-estender-contrato-ate-junho-sequencia-fora-de-campo-esta-engatilhada-no-atletico-mg.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/presidente-ve-elenco-do-atletico-mg-na-conta-do-cha-e-esconde-estrategia-para-atrair-investidores.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/convocado-para-o-sul-americano-sub-20-emerson-perdera-pre-temporada-e-inicio-do-mineiro.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/barcelona-e-betis-conversam-por-transferencia-emerson-do-atletico-mg-diz-radio-espanhola.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/com-56-jogos-luan-tem-segundo-ano-mais-atuante-pelo-atletico-mg-mas-fica-sem-titulo-pela-1a-vez.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/presidente-do-atletico-mg-esclarece-declaracao-sobre-a-sul-americana-e-comenta-sobre-processos-a-torcedores-do-galo.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/barca-do-atletico-mg-apostas-da-era-gallo-lideram-lista-de-dispensa-denilson-e-o-mais-votado.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/sette-camara-avalia-primeiro-ano-no-atletico-mg-mais-dificil-do-que-imaginava-e-faz-balanco-positivo.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/com-moral-marques-tem-missao-de-findar-sina-na-direcao-de-futebol-do-atletico-mg-pos-maluf.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/atletico-mg-ja-conhece-possiveis-rivais-na-segunda-fase-da-libertadores-restam-duas-vagas.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/apos-tentar-contratar-diretor-de-futebol-presidente-do-atletico-mg-confirma-sequencia-de-marques.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/ricardo-oliveira-alcanca-feito-pelo-atletico-mg-faz-autocritica-e-fala-sobre-competitividade-aos-38-anos.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/danilo-analisa-ano-na-ponte-mira-nova-chance-no-atletico-mg-mas-aguarda-definicao-de-futuro.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/no-radar-do-atletico-mg-para-2019-zagueiro-maicon-pode-trocar-a-turquia-pelo-futebol-arabe.ghtml",
"https://globoesporte.globo.com/futebol/times/atletico-mg/noticia/atletico-mg-busca-parcerias-para-futuro-estadio-grana-do-shopping-se-aproxima-de-r-300-milhoes.ghtml"
]
coments = {}
for i in links:
    coments.update(getComentarios(i))
with open("comentarios.json", "w") as jsf:
    json.dump(coments, jsf, ensure_ascii=False, indent=4)
# get(links)