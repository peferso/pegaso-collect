'''
Created on 3 ene. 2022
@author: pedfernandez
'''

import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By  # for locating elements
import time
import datetime
import random
import os
#from selenium.webdriver.chrome.service import Service
#import pandas as pd
#from pandas import DataFrame

logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO)

'''
def run_collection(driver):
    path_element = []
    links = []
    path_element = driver.find_elements_by_class_name("item-info-container")
    links = driver.find_elements_by_class_name("item-link")
    print('len(path_element)', len(path_element))
    print('len(links)', len(links))

    if len(path_element) == 0:
        sys.exit('Error: getting empty list of web element.\nMaybe the element was not found')

    for iart in range(1, len(path_element) + 1):
        print('\n =============== \nItem', iart)
        path_element = driver.find_elements_by_class_name("item-info-container")
        links = driver.find_elements_by_class_name("item-link")
        result = path_element[iart - 1].text
        self.id = self.id + 1
        self.get_entry_provide_values(result)
        link = links[iart - 1]
        self.get_links_provide_values(driver, link)

        if (self.id == 1):
            self.oldestitemname = self.listnames[0]
        else:
            if (self.oldestitemname == self.listnames[-1]):
                self.stopnow = True
                self.last_article = iart
            else:
                continue
'''

def initial_checks(data_folder):
    logging.info('Start')
    if not os.path.exists(data_folder):
        logging.warning('Folder ' + data_folder + 'does not exist: creating...')
        os.makedirs(data_folder)
    else:
        logging.info('Folder \'' + data_folder + '\' exists: not creating.')
        logging.info('Folder \'' + data_folder + '\' contains the following files:')
        ic = 0
        for i in os.listdir(data_folder):
            ic += 1
            logging.info('File ' + str(ic) + ': \'' + str(i) + '\'')
    logging.info('End')

def accept_terms(browser):
    logging.info('Start')
    button_xpath = '//*[@id="app"]/div[2]/div[1]/div/div/div/footer/div/button[2]'
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, button_xpath))
    ).click()
    logging.info('End')

def scroll_down(browser):
    logging.info('Start')
    browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    logging.info('End')

def printing_html(browser, outfile):
    logging.info('Start')
    logging.info('Getting page source...')
    html = browser.page_source
    logging.info('Writing to file: ' + outfile)
    f = open(outfile, 'w')
    f.write(html)
    logging.info('End')

# Variables
link = "https://www.milanuncios.com/coches-de-segunda-mano/?demanda=n&orden=date&fromSearch=1"
execution_timestamp = datetime.datetime.now()
project_folder = os.getcwd()
raw_data_folder = 'pegaso-collect/raw-data'
raw_file = raw_data_folder + '/data_' + str(execution_timestamp).replace(':', '-').replace('.', '').replace(' ', '_')

chrome_browser = webdriver.Chrome('/home/pietari/chromedriver/chromedriver')

initial_checks(raw_data_folder)

chrome_browser.get(link)
time.sleep(random.uniform(8, 12))

accept_terms(chrome_browser)
time.sleep(random.uniform(2, 5))

scroll_down(chrome_browser)
time.sleep(random.uniform(8, 12))

printing_html(chrome_browser, raw_file + '_1.html')
time.sleep(random.uniform(2, 4))

'''path_element = chrome_browser.find_elements(By.CLASS_NAME, "ma-AdList")
print(len(path_element))
print(path_element.__class__)
print(path_element[0])
html = driver.page_source
time.sleep(2)
print(html)
#driver.quit()


try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
parsed_html = BeautifulSoup(html, features="html.parser")
print(parsed_html.body.find('div', attrs={'class':'ma-AdList'}).text)


print('FIN')
'''
'''
import time
import pandas as pd
from pandas import DataFrame
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import os
import datetime
import requests

ts = datetime.datetime.now()

url = 'https://www.milanuncios.com/coches-de-segunda-mano/?demanda=n&orden=date&fromSearch=1'

# This will yield only the HTML code
response = requests.get(url)

print(response.text)

print(dir(response))

print(response.headers)

print(response.status_code)

exit()

'''

'''
url = 'https://www.milanuncios.com/coches-de-segunda-mano/?demanda=n&orden=date&fromSearch=1'

response = urllib.request.urlopen(url)
webContent = response.read().decode('UTF-8')

#TODO
# Add to cheatsheet how to print a timestamp
# 1. Navigate to the project local folder with a terminal
# 2. Make sure that the repository exists 
# https://stackoverflow.com/questions/25947059/git-clone-repository-not-found/57117454#57117454 comentar que necesité poner password a la key ssh para clonar repositorio privado
# 3. Get wd in python

'''
'''
f = open('pegaso-collect/raw-data/ma-data-' + ts.isoformat() + '.html', 'w')
f.write(response.text)
f.close()
project_folder = os.getcwd()
raw_data_folder = 'pegaso-collect/raw-data'
file = project_folder + '/' + raw_data_folder + '/' + 'ma-data-2022-01-04T00:34:57.965655.html'
f = open(file, 'r')
html = f.read()
parsed_html = BeautifulSoup(html, features="html.parser")
#print(parsed_html.body.find('div', attrs={'class':'ma-AdCard-detail'}).text)
#print( parsed_html.find_all("'class':'ma-AdCard-detail'") )

for foo in parsed_html.find_all('div', attrs={'class': 'ma-AdCard'}):
    print('here' + foo.text)

'''