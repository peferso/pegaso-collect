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
from utils import AWSNotifications


logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO)

aws = AWSNotifications()

SCRIPT = 'extract.py'

dw_s_t = os.popen('df -kh . | awk -F " " \'{print $4}\' | tail -1').read()
dw_s_t_pc = os.popen('df -kh . | awk -F " " \'{print $5}\' | tail -1').read()

aws.generate_json_event(SCRIPT, 'Start', 'The size available in the filesystem is ' + str(dw_s_t).replace('\n', '') +
                        ', ' + str(dw_s_t_pc).replace('\n', '') + ' used.')

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
    time.sleep(random.uniform(5, 7))
    full_height = browser.execute_script("return document.documentElement.scrollHeight")
    full_height_old = full_height
    reached_bottom = False
    while not reached_bottom:
        browser.execute_script('window.scrollTo(0,' + str(full_height / 2.0) + ')')
        time.sleep(random.uniform(5, 7))
        full_height = browser.execute_script("return document.documentElement.scrollHeight")
        print(full_height_old, full_height)
        if full_height_old == full_height:
            reached_bottom = True
        else:
            full_height_old = full_height
    browser.execute_script('window.scrollTo(0,' + str(0) + ')')
    total_scrolls = int(random.uniform(19, 26))
    for i in range(1, int(total_scrolls) + 1):
        wait_time = random.uniform(2, 3)
        height = int(full_height/float(total_scrolls)*i)
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
THIS_SCRIPT_PATH = os.environ['PEGASO_COLLT_DIR']
link = os.environ['URL']
driver_path = os.environ['CHROMEDRIVER_DIR']
execution_timestamp = datetime.datetime.now()
raw_data_folder = 'raw-data'
raw_file = raw_data_folder + '/data_' + str(execution_timestamp).replace(':', '-').replace('.', '').replace(' ', '_')

# Main
os.chdir(THIS_SCRIPT_PATH)

initial_checks(raw_data_folder)

new_browser = True

time_start = time.time()

time_last_br = time_start

for page_number in range(200, 0, -1):

    chrome_browser = webdriver.Chrome(driver_path)

    elapsed_time = time.time() - time_last_br

    if elapsed_time > 600:
        time_last_br = time.time()
        random.uniform(60, 300)

    go_to_link(chrome_browser, link + str(page_number))
    time.sleep(random.uniform(2, 5))

    if new_browser:
        accept_terms(chrome_browser)
        time.sleep(random.uniform(2, 5))
        new_browser = False

    scroll_down(chrome_browser)
    time.sleep(random.uniform(4, 6))

    printing_html(chrome_browser, raw_file + '_' + str(page_number) + '.html')
    time.sleep(random.uniform(2, 4))

    new_browser = True
    chrome_browser.close()

chrome_browser.close()

dw_s = os.popen('du -sh raw-data | awk -F " " \'{print $1}\'').read()
dw_s_t = os.popen('df -kh . | awk -F " " \'{print $4}\' | tail -1').read()
dw_s_t_pc = os.popen('df -kh . | awk -F " " \'{print $5}\' | tail -1').read()


aws.generate_json_event(SCRIPT, 'End', 'A total of ' + str(dw_s).replace('\n', '') +
                        ' data was downloaded. The size available in the filesystem is ' + str(dw_s_t).replace('\n', '') +
                        ', ' + str(dw_s_t_pc).replace('\n', '') + ' used.')
