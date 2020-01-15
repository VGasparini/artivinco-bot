import json
import time
import os
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import datetime
from bs4 import BeautifulSoup as BS


def get_info():
        with open('credential.json') as f:
                return json.load(f)

def login():
        username = browser.find_element_by_id('txtlogin')
        password = browser.find_element_by_id('txtsenha')
        username.send_keys(credencial['username'])
        password.send_keys(credencial['pass'])
        password.submit()
        return True

def set_date():
        global browser
        # initxt = str(datetime.now().day).zfill(2) + str(max(1,datetime.now().month-1)).zfill(2) + str(datetime.now().year)
        ini = browser.find_element_by_id('txtdataini')
        initxt = '08122019'
        ini.send_keys(initxt)
        fim = browser.find_element_by_id('txtdatafim')
        fimtxt = str(datetime.now().day).zfill(2) + str(datetime.now().month).zfill(2) + str(datetime.now().year)
        fim.send_keys(fimtxt)

        return

def get_data(url):
        global browser, logged
        browser.get(url)
        if not logged:
                logged = login()
        browser.get('http://intranet.artivinco.com.br/vds/StatusPedido.php')
        set_date()
        submit_button = browser.find_elements_by_xpath('//*[@id="ConsultaRapida4"]/fieldset[3]/div[1]/input')[0]
        submit_button.click()
        print("Filtrando...")
        time.sleep(120)
        # submit_button = browser.find_elements_by_xpath('//*[@id="GeraExcel"]')[0]
        # submit_button.click()
        print("Baixando...")
        table = browser.find_elements_by_xpath('//*[@id="StPedido"]/table')[0]
        with open('report.csv', 'w', newline='') as csvfile:
                wr = csv.writer(csvfile)
                for row in table.find_elements_by_css_selector('tr'):
                        wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])


credencial = get_info()
options = webdriver.ChromeOptions()
# options.headless = True
browser = webdriver.Chrome('./chromedriver',chrome_options = options)
browser.implicitly_wait(60)
logged = False
url = 'http://intranet.artivinco.com.br/index.php'
get_data(url)
time.sleep(10)
browser.quit()
