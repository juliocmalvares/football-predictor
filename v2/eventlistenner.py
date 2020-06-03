#!/usr/bin/python3
# -*- coding:utf-8 -*-

from selenium.webdriver.support.events import AbstractEventListener
from selenium import webdriver
class Listenner(AbstractEventListener):

    def after_navigate_to(self, url, driver):
        print(">>> Acessed", url)
        driver.implicitly_wait(time_to_wait=10)
        print(">> wait for 10 seconds")

    def after_click(self, url, driver):
        pass