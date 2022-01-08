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

def initial_checks(data_folder):
    time_start = time.time()
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
    time_end = time.time()
    logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')

def go_to_link(browser, url):
    time_start = time.time()
    logging.info('Start')
    logging.info('Going to page: \'' + url + '\'')
    browser.get(url)
    time_end = time.time()
    logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')

def accept_terms(browser):
    time_start = time.time()
    logging.info('Start')
    button_xpath = '//*[@id="app"]/div[2]/div[1]/div/div/div/footer/div/button[2]'
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, button_xpath))
    ).click()
    time_end = time.time()
    logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')

def scroll_down(browser):
    time_start = time.time()
    logging.info('Start')
    full_height = browser.execute_script("return document.documentElement.scrollHeight")
    total_scrolls = 20.0
    for i in range(1, int(total_scrolls)):
        wait_time = random.uniform(8, 12)
        height = int(full_height/total_scrolls*i)
        logging.info('Scrolling to height (' + str(i) + ' of ' + str(int(total_scrolls)) + ') ' + str(height) + ' and waiting ' + str(wait_time) + ' seconds.')
        browser.execute_script('window.scrollTo(0,' + str(height) + ')')
        time.sleep(wait_time)
    time_end = time.time()
    logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')

def printing_html(browser, outfile):
    time_start = time.time()
    logging.info('Start')
    logging.info('Getting page source...')
    html = browser.page_source
    logging.info('Writing to file: ' + outfile)
    f = open(outfile, 'w')
    f.write(html)
    time_end = time.time()
    logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')

# Variables
THIS_SCRIPT_PATH = '/home/pietari/PycharmProjects/cars/pegaso-collect'
link = "https://www.milanuncios.com/coches-de-segunda-mano/?demanda=n&orden=date&fromSearch=1"
execution_timestamp = datetime.datetime.now()
raw_data_folder = 'raw-data'
raw_file = raw_data_folder + '/data_' + str(execution_timestamp).replace(':', '-').replace('.', '').replace(' ', '_')

# Main
os.chdir(THIS_SCRIPT_PATH)

chrome_browser = webdriver.Chrome('/home/pietari/chromedriver/chromedriver')

initial_checks(raw_data_folder)

go_to_link(chrome_browser, link)
time.sleep(random.uniform(2, 5))

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