# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.wait import WebDriverWait
# opt = Options()
# opt.add_argument("--headless")
# driver = webdriver.Chrome(options=opt)
# driver.get("https://globoesporte.globo.com/futebol/times/flamengo/index/feed/pagina-6.ghtml")



# beg = time.time()
# r = http.request("GET", "https://globoesporte.globo.com/futebol/times/atletico-mg/index/feed/pagina-5.ghtml")
# end = time.time()
# end - beg



import urllib3
from lxml import html
import time

http_requester = urllib3.PoolManager()
beg = time.time()
request = http_requester.request("GET", "https://globoesporte.globo.com/futebol/times/atletico-mg/index/feed/pagina-5.ghtml")
end = time.time()
print("Tempo de request: ", end-beg)
root = html.fromstring(request.data)
elements = root.xpath(".//a[contains(@class, 'feed-post-link')]")
for i in elements:
    print(i.attrib['href'])