'''
Created on 18 ene. 2022
@author: pedfernandez
'''

import logging
import time
import datetime
import os
import pandas as pd


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

def scan_csv_files(data_folder):
    time_start = time.time()
    logging.info('Start')
    ic = 0
    list_of_files = []
    for i in os.listdir(data_folder):
        ext = i.split('.')[-1]
        if ext == 'csv':
            ic += 1
            logging.info('File ' + str(ic) + ': \'' + str(i) + '\'')
            list_of_files.append(i)
    time_end = time.time()
    logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')
    return list_of_files

def generate_sql_inserts(file, sql_folder):
    time_start = time.time()
    logging.info('Start')
    batch_date = file.split('_')[1]
    batch_page = file.split('.')[0].split('_')[-1]
    d_folder = sql_folder + '/' + batch_date
    if not os.path.exists(d_folder):
        logging.warning('Folder ' + d_folder + ' does not exist: creating...')
        os.makedirs(d_folder)
    else:
        logging.info('Folder \'' + d_folder + '\' exists: not creating.')
    df = pd.read_csv(file)
    f = open(d_folder + '/' + batch_page + '.sql', 'w+')
    print('USE pegaso_db;', file=f, sep="','", end='\n')
    for index, row in df.iterrows():
        print('INSERT INTO raw_data VALUES (\'' +
              row['id'],
              row['brand'],
              row['model'],
              row['price_c'],
              row['price_f'],
              row['kilometers'],
              row['profesional_vendor'],
              row['automatic_gearbox'],
              row['year'],
              row['source'],
              batch_date +
              '\');', file=f, sep="','", end='\n')
    f.close()
    # id,brand,model,price_c,price_f,kilometers,power,doors,profesional_vendor,automatic_gearbox,year,source
    time_end = time.time()
    logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')


# Variables
THIS_SCRIPT_PATH = os.environ['PEGASO_COLLT_DIR']
execution_timestamp = datetime.datetime.now()
csv_data_folder = 'processed-data'
sql_data_folder = 'sql-data'

# Main
os.chdir(THIS_SCRIPT_PATH)

initial_checks(sql_data_folder)

csv_files = scan_csv_files(csv_data_folder)

for csv_f in csv_files:

    generate_sql_inserts(csv_data_folder + '/' + csv_f, sql_data_folder)
