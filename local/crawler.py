from utils import export_to_csv

from datetime import datetime, timedelta
import time

from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup

from selenium import webdriver
import seleniumrequests

from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, browser, user):
        self.browser = browser
        self.logged = False
        self.user = user
        self.table_ita = ''
        self.table_srv = ''
        self.table_raw = ''
        self.tables = ''

    def login(self):
        try:
            username = self.browser.find_element_by_id("txtlogin")
            secret = self.browser.find_element_by_id("txtsenha")

            username.send_keys(self.user.username)
            secret.send_keys(self.user.secret)
            secret.submit()

            self.logged = True
        except:
            pass

    def url(self, path):
        return "http://intranet.artivinco.com.br/" + path

    def post(self, data, url):
        return self.browser.request('POST', self.url(url), data=data)

    def build_data(self):
        today = datetime.now()
        past = today - timedelta(days=30)
        future = today + timedelta(days=10)

        data = {
            'DtInicio' : past.strftime("%Y-%m-%d"),
            'DtFim' : future.strftime("%Y-%m-%d"),
            'cliente' : 0,
            'representante' : 0,
            'supervisor' : 'undefined',
            'PRODUTO' : '',
            'NumPedido' : '',
        }

        return data
    
    def change(self, idx):
        option = self.browser.find_element_by_xpath('//*[@id="BDados"]/option[{}]'.format(idx)).click()
        time.sleep(5)
        return

    def run(self, idx):
        if not self.logged:
            self.browser.get(self.url(""))
            self.login()
        post_data = self.build_data()
        self.change(idx)
        r = self.browser.request('POST', self.url("vds/RelStatusPedido.php"), data = post_data)
        html = r.text
        soup = BeautifulSoup(html)
        self.table_raw = html
        self.table = soup.find("table")
        return