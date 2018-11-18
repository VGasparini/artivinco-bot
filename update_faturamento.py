from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json
import time


def get_info():
    with open('credential.json') as f:
        return json.load(f)

def login():
    username = browser.find_element_by_id('username')
    password = browser.find_element_by_id('password')
    username.send_keys(credencial['username'])
    password.send_keys(credencial['pass'])
    password.submit()
    return True

def get_data(url):
    global browser, logged
    browser.get(url)
    if not logged:
        logged = login()
    browser.find_element_by_name('csvsetup').click()
    select = Select(browser.find_element_by_id('xf'))
    select.select_by_value('csv')
    browser.find_element_by_name('export').click()


credencial = get_info()
browser = webdriver.Chrome()
browser.implicitly_wait(30)
logged = False
url = 'https://artivinco.force.com/00O36000006ufjR'
get_data(url)
time.sleep(15)
browser.quit()