'''
Created on 18 ene. 2022
@author: pedfernandez
'''

import logging
import time
import datetime
import os
import pandas as pd
import pymysql
import subprocess


logging.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO)

def load_environment():
    subprocess.run(["source",
                    "~/.profile_PEGASO"], shell=True)

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
    # TODO
    # Replace 'nan' por NULL
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
    print('USE pegaso_db;', file=f, sep="','")
    for index, row in df.iterrows():
        query = 'INSERT INTO raw_data VALUES (\'' + \
              str(row['id']) + '\',\'' + \
              str(row['brand']) + '\',\'' + \
              str(row['model']) + '\',\'' + \
              str(row['price_c']) + '\',\'' + \
              str(row['price_f']) + '\',\'' + \
              str(row['kilometers']) + '\',\'' + \
              str(row['power']) + '\',\'' + \
              str(row['doors']) + '\',\'' + \
              str(row['profesional_vendor']) + '\',\'' + \
              str(row['automatic_gearbox']) + '\',\'' + \
              str(row['year']) + '\',\'' + \
              str(row['source']) + '\',\'' + \
              str(batch_date) + '\');'
        query = query.replace("'nan'", "NULL")
        print(query, file=f)
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

load_environment()

initial_checks(sql_data_folder)

csv_files = scan_csv_files(csv_data_folder)

for csv_f in csv_files:

    generate_sql_inserts(csv_data_folder + '/' + csv_f, sql_data_folder)

connection = pymysql.connect(host=os.environ['DBHOST'],
                             user=os.environ['DBUSER'],
                             passwd=os.environ['DBPASS'],
                             #db="pegaso_db",
                             charset='utf8')

ib = 0

for batch_date in os.listdir(sql_data_folder):

    ib += 1

    logging.info('Iterating batch \'' + batch_date + '\' (' + str(ib) + ' of ' + str(len(os.listdir(sql_data_folder))) + ').')

    iq = 0

    for query_file in os.listdir(sql_data_folder + '/' + batch_date):

        iq += 1

        logging.info(' + Executing query file \'' + query_file + '\' (' + str(iq) + ' of ' + str(len(os.listdir(sql_data_folder + '/' + batch_date))) + ').')

        file = open(sql_data_folder + '/' + batch_date + '/' + query_file, 'r')
        sql_file = file.read()
        file.close()

        sql_commands = sql_file.split(';\n')

        con_cursor = connection.cursor()

        for command in sql_commands:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            if command != '':
                try:
                    con_cursor.execute(command)
                    connection.commit()
                except pymysql.err.OperationalError as msg:
                    logging.warning(" ++ Command skipped: " + str(msg))
                    print(command)

        con_cursor.close()

        logging.info(' + Finished query file \'' + query_file + '\' (' + str(iq) + ' of ' + str(len(os.listdir(sql_data_folder + '/' + batch_date))) + ').')

connection.close()