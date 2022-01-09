import os
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame

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

def create_data_frame(lists):
    print('creating the data frame\n ...')
    cars = {
            'id':                 lists[0],
            'price_c':            lists[1],
            'price_f':            lists[2],
            'kilometers':         lists[3],
            'power':              lists[4],
            'doors':              lists[5],
            'profesional_vendor': lists[6],
            'automatic_gearbox':  lists[7],
            'source':             lists[8]
             }
    for i in lists:
        print('length', len(i))

    df = DataFrame(cars, columns=['id',
                                  'price_c',
                                  'price_f',
                                  'kilometers',
                                  'power',
                                  'doors',
                                  'profesional_vendor',
                                  'automatic_gearbox',
                                  'source'
                                  ])

    print('exporting data frame\n ...')
    export_csv = df.to_csv(r'test.csv', index=None, header=True)

    print('let us print a few lines of the data frame\n ...')
    print(df.head())

# Variables
THIS_SCRIPT_PATH = '/home/pietari/PycharmProjects/cars/pegaso-collect'
raw_data_folder = 'raw-data'
html_file = raw_data_folder + '/data_2022-01-08_16-39-37032217_1.html'

# Main

os.chdir(THIS_SCRIPT_PATH)

f = open(html_file, 'r')
html = f.read()
parsed_html = BeautifulSoup(html, features="html.parser")
items = parsed_html.body.find_all('div', attrs={'class':'ma-AdCard-detail'})
print('There are ' + str(len(items)) + ' ads in this file.')

l_id = []
l_price_c = []
l_price_f = []
l_kilometers = []
l_power = []
l_doors = []
l_profesional_vendor = []
l_automatic_gearbox = []
l_source = []

name_separator_left = '<a class="ma-AdCard-titleLink" data-e2e="ma-AdCard-titleLink"'
name_separator_right = '<'

id_c = 0

for advertise in items:
    id_c += 1
    ad_contents = advertise.contents
    information = str(ad_contents[0]).split(name_separator_left)[-1].split('>')[1]
    name = information.split(name_separator_right)[0]
    brand = name.split('-')[0].replace(' ', '')
    model = name.split('-')[-1].replace(' ', '', 1)

    information = str(ad_contents[1]).split('span class')
    ii = 0
    data_list = []
    for itm in information:
        data = itm.split('>')[1]
        data = data.split('<')[0]
        ii += 1
        data_list.append(data)
    print(set(data_list))

    price_c = parse_for_prices(data_list, 'Precio al contado')
    price_f = parse_for_prices(data_list, 'Precio financiado')
    kilometers = parse_for_ending_characters(data_list, 'kms')
    power = parse_for_ending_characters(data_list, 'CV')
    doors = parse_for_ending_characters(data_list, 'puertas')
    profesional_vendor = parse_for_exact_string(data_list, 'Profesional')
    automatic_gearbox = parse_for_exact_string(data_list, 'Automático')

    l_id.append(str(id_c) + str(html_file.split('/')[-1]))
    l_price_c.append(price_c)
    l_price_f.append(price_f)
    l_kilometers.append(kilometers)
    l_power.append(power)
    l_doors.append(doors)
    l_profesional_vendor.append(profesional_vendor)
    l_automatic_gearbox.append(automatic_gearbox)
    l_source.append(html_file.split('/')[-1])

    print()
    print('name: ', name)
    print('Brand: ' + brand)
    print('Model: ' + model)
    print('km: ' + kilometers)
    print('profesional_vendor: ' + profesional_vendor)
    print('year: ' + data_list[7])
    print('power: ' + power)
    print('doors: ' + doors)
    print('automatic_gearbox: ' + automatic_gearbox)
    print('price (cash): ' + price_c)
    print('price (financed): ' + price_f)

f.close()

lists = [
    l_id,
    l_price_c,
    l_price_f,
    l_kilometers,
    l_power,
    l_doors,
    l_profesional_vendor,
    l_automatic_gearbox,
    l_source
]
create_data_frame(lists)