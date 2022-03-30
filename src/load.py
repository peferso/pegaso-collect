'''
Created on 18 ene. 2022
@author: pedfernandez
'''

import logging
import time
import datetime
import os
import json
import pandas as pd
import pymysql
import subprocess
import hashlib
from utils import AWSOperations, AWSNotifications

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

def get_monday_of_week_date(input_batch_date):
    xd = input_batch_date.split('-')
    dt = datetime.datetime(int(xd[0]), int(xd[1]), int(xd[2]), 0, 0, 0)
    last_monday = dt + datetime.timedelta(days=-dt.weekday(), weeks=0)
    last_monday = str(last_monday).split(' ')[0]
    return last_monday

def generate_sql_inserts(file, sql_folder):
    time_start = time.time()
    logging.info('Start')
    batch_date = file.split('_')[1]
    logical_batch_date = get_monday_of_week_date(file.split('_')[1])
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
        text = str(row['brand']).replace(' ', '').upper() + \
               str(row['model']).replace(' ', '').upper() + \
               str(row['price_c']).replace(' ', '').upper() + \
               str(row['price_f']).replace(' ', '').upper() + \
               str(row['kilometers']).replace(' ', '').upper() + \
               str(row['power']).replace(' ', '').upper() + \
               str(row['doors']).replace(' ', '').upper() + \
               str(row['profesional_vendor']).replace(' ', '').upper() + \
               str(row['automatic_gearbox']).replace(' ', '').upper() + \
               str(row['year']).replace(' ', '').upper()
        hashed_cols = hashlib.sha3_256(text.encode()).hexdigest()
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
              str(hashed_cols) + '\',\'' + \
              str(logical_batch_date) + '\');'
        query = query.replace("'nan'", "NULL")
        print(query, file=f)
    f.close()

    # id,brand,model,price_c,price_f,kilometers,power,doors,profesional_vendor,automatic_gearbox,year,source
    time_end = time.time()
    logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')

def check_db_disk_usage():
    time_start = time.time()
    logging.info('Start')
    aws.start_database_ec2_if_stopped()
    ip = aws.get_database_public_ip()
    SSH_KEYS_DIR    = os.environ['SSH_KEYS_DIR']
    SSH_KEY_APPLCTN = os.environ['SSH_KEY_APPLCTN']
    ssh = 'ssh -i ' + str(SSH_KEYS_DIR) + '/' + str(SSH_KEY_APPLCTN) + \
          ' -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ec2-user@' + str(ip)
    cmd_1 = ' "df -k" 2>/dev/null | grep /dev/xvda1 | awk -F " " \'{ print $3 }\' '
    cmd_2 = ' "df -k" 2>/dev/null | grep /dev/xvda1 | awk -F " " \'{ print $4 }\' '
    cmd_3 = ' "df -k" 2>/dev/null | grep /dev/xvda1 | awk -F " " \'{ print $5 }\' '
    root_fs_disk_used = str(round(int(str(os.popen(ssh + cmd_1).read()).replace('\n', ''))/1000, 2))
    root_fs_disk_avmb = str(round(int(str(os.popen(ssh + cmd_2).read()).replace('\n', ''))/1000, 2))
    root_fs_disk_avpc = str(os.popen(ssh + cmd_3).read()).replace('\n', '')
    logging.info('Amount of root db disk used (MB)      ' + root_fs_disk_used)
    logging.info('Amount of root db disk available (MB) ' + root_fs_disk_avmb)
    logging.info('Amount of root db disk available (%)  ' + root_fs_disk_avpc)
    time_end = time.time()
    logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')
    return root_fs_disk_used, root_fs_disk_avmb, root_fs_disk_avpc

def connect_to_database(aws):
    time_start = time.time()
    logging.info('Start')

    aws.start_database_ec2_if_stopped()

    ip = aws.get_database_public_ip()

    ready = False
    while not ready:
        try:
            logging.info('Trying to connect...')
            connection = pymysql.connect(host=ip,
                                         user=os.environ['DBUSER'],
                                         passwd=os.environ['DBPASS'],
                                         db="pegaso_db",
                                         charset='utf8')
        except pymysql.err.OperationalError as msg:
            logging.warning("Unable to connect" + str(msg))
            logging.warning("Waiting 120 seconds for graceful start.")
            time.sleep(120)
            ready = False
        else:
            logging.info("The database is up. Proceeding")
            ready = True

    ready = False
    while not ready:
        try:
            query='select * from global_statistics;'
            logging.info('Trying to run a select query: \'' + query + '\'')
            connection.cursor().execute(query)
            connection.commit()
        except pymysql.err.OperationalError as msg:
            logging.warning("Unable to make select" + str(msg))
            logging.warning("Waiting 120 seconds for graceful startup.")
            time.sleep(120)
            ready = False
        else:
            logging.info("The database is ready. Proceeding")
            ready = True

    time_end = time.time()
    logging.info('End. Elapsed time: ' + str(time_end - time_start) + ' seconds.')
    return connection

# Variables
THIS_SCRIPT_PATH = os.environ['PEGASO_COLLT_DIR']
execution_timestamp = datetime.datetime.now()
csv_data_folder = 'processed-data'
sql_data_folder = 'sql-data'
mode = 'GENERATE_SQL_FILES'

# Main
os.chdir(THIS_SCRIPT_PATH)

load_environment()

initial_checks(sql_data_folder)

csv_files = scan_csv_files(csv_data_folder)

if mode == 'GENERATE_SQL_FILES':
    for csv_f in csv_files:
        generate_sql_inserts(csv_data_folder + '/' + csv_f, sql_data_folder)

logging.info('Retrieving initial database state...')

aws = AWSOperations()

ec2_info_dict = aws.retrieve_aws_ec2_info()

INIT_DB_STATE = ec2_info_dict['insSt']

d_used, d_avmb, d_avpc = check_db_disk_usage()

SCRIPT = 'load.py'
aws_n = AWSNotifications()
aws_n.generate_json_event(SCRIPT, 'Start', 'Preparing to inject sql queries. ' +
                          'The database initial state is ' + str(INIT_DB_STATE) + '. ' +
                          'Disk usage info in root volume -> MB used: ' + str(d_used) + '.' +
                          ' MB available: ' + str(d_avmb) + ' (' + str(d_avpc) + ').')

logging.info('Initial database state is: ' + INIT_DB_STATE)

connection = connect_to_database(aws)

ib = 0

nq_s = 0
nq_f_o = 0
nq_f_pk = 0

for batch_date in os.listdir(sql_data_folder):

    ib += 1

    logging.info('Iterating batch \'' + batch_date + '\' (' + str(ib) + ' of ' + str(len(os.listdir(sql_data_folder))) + ').')

    iq = 0

    for query_file in os.listdir(sql_data_folder + '/' + batch_date):

        iq += 1

        time_start_q = time.time()

        logging.info(' + Executing query file \'' + query_file + '\' (' + str(iq) + ' of ' + str(len(os.listdir(sql_data_folder + '/' + batch_date))) + ').' + ' [batch \'' + batch_date + '\' (' + str(ib) + ' of ' + str(len(os.listdir(sql_data_folder))) + ')]')

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
                    nq_f_o += 1
                except pymysql.err.IntegrityError as msg:
                    logging.warning(" ++ Command skipped: " + str(msg))
                    print(command)
                    nq_f_pk += 1
                except pymysql.err as msg:
                    logging.Error(" ++ Command skipped: " + str(msg))
                    print(command)
                    nq_f_pk += 1
                else:
                    logging.info(" ++ Command executed: " + str(command))
                    nq_s += 1

        con_cursor.close()

        time_end_q = time.time()

        logging.info(' + Finished query file \'' + query_file + '\' (' + str(iq) + ' of ' + str(len(os.listdir(sql_data_folder + '/' + batch_date))) + ').' + ' ' + str(time_end_q - time_start_q) + ' seconds elapsed.' + ' [batch \'' + batch_date + '\' (' + str(ib) + ' of ' + str(len(os.listdir(sql_data_folder))) + ')]')

connection.close()

ec2_info_dict = aws.retrieve_aws_ec2_info()

d_used, d_avmb, d_avpc = check_db_disk_usage()

aws_n.generate_json_event(SCRIPT, 'End', 'The data load has finished. The database final state is ' + str(ec2_info_dict['insSt']) + '.' +
                          'A total of ' + str(nq_s + nq_f_o + nq_f_pk) + ' were executed, ' +
                          str(nq_s) + ' were OK, ' + str(nq_f_pk) + ' failed due to primary key, ' + str(nq_f_o) + ' for other reasons. ' +
                          'The queries can be tracked by batch date(s): ' +
                          str(os.listdir(sql_data_folder)).replace('[', '').replace(']', '').replace('\'', '').replace('\"', '') +
                          '. Disk usage info in root volume -> MB used: ' + str(d_used) + '.' +
                          ' MB available: ' + str(d_avmb) + ' (' + str(d_avpc) + ').')

if INIT_DB_STATE.lower() == 'stopped':

    logging.warning("Stopping database instance to leave it in initial state...")

    aws.stop_database_ec2_if_running()

    logging.warning("Stopped.")
