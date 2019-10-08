import bs4
import pandas as pd
from bs4 import BeautifulSoup as soup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import re
import time

#extrae part numbers de un csv, en amazon lo mas recomendable es buscar partnumber+brand
items = []
data = pd.read_csv(r"C:\Users\Maximiliano\Desktop\numerosparte.csv",squeeze=True)
for parte in data:
    items.append(str(parte))
    
class EBayBot(object):
    def __init__(self, items):
        self.ebay_url = "https://www.ebay.com/"
        self.items = items
        self.profile = webdriver.FirefoxProfile()
        self.options = Options()
        #se tiene que cambiar el path de geckodriver de acuerdo al archivo de cada uno
        self.driver = webdriver.Firefox(executable_path=r'C:\Users\Maximiliano\Downloads\geckodriver-v0.25.0-win64\geckodriver.exe',
                                        firefox_profile=self.profile,
                                        options=self.options)
        self.driver.get(self.ebay_url)
        self.html = self.driver.page_source
        self.sopita = soup(self.html, 'html.parser')
    def search_items(self):
        urls = []
        for item in self.items:
            print(f"Buscando {item}...")
            self.driver.get(self.ebay_url)
            
            search_input = self.driver.find_element_by_id("gh-ac")
            search_input.send_keys(item)

            time.sleep(2)
            
            search_button = self.driver.find_element_by_id('gh-btn')
            search_button.click()

            time.sleep(2)
            
            first_result = self.driver.find_element_by_class_name('s-item__image')
            first_result.click()
            
            time.sleep(5)
            
            final_url = self.driver.current_url
            urls.append(final_url)
            
            print(self.driver.current_url)
            
            
ebay_bot = EBayBot(items)
ebay_bot.search_items()


