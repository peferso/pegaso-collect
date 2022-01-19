'''
Created on 8 ene. 2022
@author: pedfernandez
'''

import os
import logging
from bs4 import BeautifulSoup
import time
import pandas as pd
from pandas import DataFrame

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

def parse_for_prices(data_list, label):
    elements = set(data_list)
    if label in elements:
        index = data_list.index(label)
        returned_price = data_list[index + 1]
    else:
        returned_price = parse_for_ending_characters(data_list, '€')
    return returned_price

def parse_for_ending_characters(data_list, chars):
    for i in data_list:
        if len(i) > len(chars):
            if i[-len(chars):] == chars:
                value = i
                return value
            else:
                value = 'NULL'
        else:
            value = 'NULL'
    return value

def parse_for_exact_string(data_list, word):
    for i in data_list:
        if i == word:
            return 'TRUE'
        else:
            value = 'FALSE'
    return value

def parse_for_year(data_list):
    for i in data_list:
        if len(i) == 4 and i.isdigit():
            if 1900 <= int(i) <= 3000:
                return i
        else:
            value = 'NULL'
    return value

def create_data_frame(file, lists):

    time_start = time.time()
    logging.info('Start')

    cars = {
            'id':                 lists[0],
            'brand':              lists[1],
            'model':              lists[2],
            'price_c':            lists[3],
            'price_f':            lists[4],
            'kilometers':         lists[5],
            'power':              lists[6],
            'doors':              lists[7],
            'profesional_vendor': lists[8],
            'automatic_gearbox':  lists[9],
            'year':               lists[10],
            'source':             lists[11]
             }

    total_registers = len(lists[0])
    ic = 0
    for i in lists:
        if len(i) != total_registers:
            logging.error('Different number of registers in column \'' + str(list(cars.keys())[ic]) + '\'. It is ' + str(len(i)) + ' when it should be ' + str(total_registers) + '.')
            logging.error('\n' + str(i) + '\n' + str(lists[0]))
            exit()
        ic += 1

    df = DataFrame(cars, columns=['id',
                                  'brand',
                                  'model',
                                  'price_c',
                                  'price_f',
                                  'kilometers',
                                  'power',
                                  'doors',
                                  'profesional_vendor',
                                  'automatic_gearbox',
                                  'year',
                                  'source'
                                  ])

    logging.info('Exporting data frame as .csv file \'' + str(file) + '\'')
    df.to_csv(file, index=None, header=True)

    time_end = time.time()
    logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')

def parse_html_file(html, lists):

    time_start = time.time()
    logging.info('Start')

    l_id = lists[0]
    l_brand = lists[1]
    l_model = lists[2]
    l_price_c = lists[3]
    l_price_f = lists[4]
    l_kilometers = lists[5]
    l_power = lists[6]
    l_doors = lists[7]
    l_profesional_vendor = lists[8]
    l_automatic_gearbox = lists[9]
    l_year = lists[10]
    l_source = lists[11]

    parsed_html = BeautifulSoup(html, features="html.parser")
    items = parsed_html.body.find_all('div', attrs={'class': 'ma-AdCard-detail'})

    logging.info('Parsing a file containing ' + str(len(items)) + ' items.')

    name_separator_left = '<a class="ma-AdCard-titleLink" data-e2e="ma-AdCard-titleLink"'
    name_separator_right = '<'
    id_c = 0

    for advertise in items:

        id_c += 1

        # Extract name
        ad_contents = advertise.contents
        information = str(ad_contents[0]).split(name_separator_left)[-1].split('>')[1]
        name = information.split(name_separator_right)[0]
        brand = name.split('-', 1)[0].replace(' ', '')
        model = name.split('-', 1)[-1].replace(' ', '', 1)
        # Extract data
        if len(ad_contents) < 2:
            break
        else:
            information = str(ad_contents[1]).split('span class')
        ii = 0
        data_list = []
        for itm in information:
            data = itm.split('>')[1]
            data = data.split('<')[0]
            ii += 1
            data_list.append(data)

        price_c = parse_for_prices(data_list, 'Precio al contado')
        price_f = parse_for_prices(data_list, 'Precio financiado')
        kilometers = parse_for_ending_characters(data_list, 'kms')
        power = parse_for_ending_characters(data_list, 'CV')
        doors = parse_for_ending_characters(data_list, 'puertas')
        profesional_vendor = parse_for_exact_string(data_list, 'Profesional')
        automatic_gearbox = parse_for_exact_string(data_list, 'Automático')
        year = parse_for_year(data_list)

        if price_c != 'NULL':
            l_id.append(str(id_c) + str(html_file.split('/')[-1]))
            l_brand.append(brand.replace(' ', '').upper())
            l_model.append(model.upper())
            l_price_c.append(price_c.replace('.', '').replace('€', '').replace(' ', ''))
            l_price_f.append(price_f.replace('.', '').replace('€', '').replace(' ', ''))
            l_kilometers.append(kilometers.lower().replace('.', '').replace('kms', '').replace(' ', ''))
            l_power.append(power.lower().replace('.', '').replace('cv', '').replace(' ', ''))
            l_doors.append(doors.lower().replace('.', '').replace('puertas', '').replace(' ', ''))
            l_profesional_vendor.append(profesional_vendor)
            l_automatic_gearbox.append(automatic_gearbox)
            l_source.append(html_file.split('/')[-1])
            l_year.append(year)
            logging.info('Item ' + str(id_c) + ' parsed - \'' + name + '\'.' +
                         '\nbrand:               ' + str(l_brand[-1]) +
                         '\nmodel:               ' + str(l_model[-1]) +
                         '\nprice_c:             ' + str(l_price_c[-1]) +
                         '\nprice_f:             ' + str(l_price_f[-1]) +
                         '\nkilometers:          ' + str(l_kilometers[-1]) +
                         '\npower:               ' + str(l_power[-1]) +
                         '\ndoors:               ' + str(l_doors[-1]) +
                         '\nprofesional_vendor:  ' + str(l_profesional_vendor[-1]) +
                         '\nautomatic_gearbox:   ' + str(l_automatic_gearbox[-1]) +
                         '\nyear:                ' + str(l_year[-1]) +
                         '\nsource:              ' + str(l_source[-1]))
        else:
            logging.info('Item ' + str(id_c) + ' parsed - \'' + name + '\'.' +
                         '\nExcluded due to empty price.')

    logging.info('Grouping extracted data into columns...')

    lists = [
        l_id,
        l_brand,
        l_model,
        l_price_c,
        l_price_f,
        l_kilometers,
        l_power,
        l_doors,
        l_profesional_vendor,
        l_automatic_gearbox,
        l_year,
        l_source
    ]

    time_end = time.time()
    logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')

    return lists


# Variables
THIS_SCRIPT_PATH = os.environ['PEGASO_COLLT_DIR']
raw_data_folder = 'raw-data'
processed_data_folder = 'processed-data'
html_file = raw_data_folder + '/data_2022-01-08_16-39-37032217_1.html'

# Main

os.chdir(THIS_SCRIPT_PATH)

initial_checks(raw_data_folder)

initial_checks(processed_data_folder)

for html_file in os.listdir(raw_data_folder):

    f = open(raw_data_folder + '/' + html_file, 'r')

    processed_file = processed_data_folder + '/' + html_file.split('/')[-1].replace('.html', '.csv')

    html = f.read()

    l_id = []
    l_brand = []
    l_model = []
    l_price_c = []
    l_price_f = []
    l_kilometers = []
    l_power = []
    l_doors = []
    l_profesional_vendor = []
    l_automatic_gearbox = []
    l_year = []
    l_source = []

    lists = [
        l_id,
        l_brand,
        l_model,
        l_price_c,
        l_price_f,
        l_kilometers,
        l_power,
        l_doors,
        l_profesional_vendor,
        l_automatic_gearbox,
        l_year,
        l_source
    ]

    lists = parse_html_file(html, lists)

    f.close()

    create_data_frame(processed_file, lists)
