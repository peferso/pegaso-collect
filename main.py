'''
Created on 3 ene. 2022
@author: pedfernandez
'''

from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.common.by import By  # for locating elements
import time
import datetime
import pandas as pd
from pandas import DataFrame

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

link = "https://www.milanuncios.com/coches-de-segunda-mano/?demanda=n&orden=date&fromSearch=1"
execution_timestamp = datetime.datetime.now()

print('Execution starts:', execution_timestamp)

def accept_terms(browser):
    button_class = 'sui-AtomButton sui-AtomButton--primary sui-AtomButton--solid sui-AtomButton--center '
    browser.find_element_by_class_name(button_class).click()

chrome_browser = webdriver.Chrome('/home/pietari/chromedriver/chromedriver')
chrome_browser.implicitly_wait(10)

chrome_browser.get(link)
time.sleep(2.5)

accept_terms(chrome_browser)
time.sleep(2.5)

print('Execution finished', datetime.datetime.now())

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