#!/bin/bash

shopt -s expand_aliases

source ~/.profile_PEGASO

start_db

while `get_db_ip`=="null"
do
  sleep 2
done

cd ${PEGASO_COLLT_DIR%/*}

run.sh load.py

cd ${OLDPWD}

stop_db

sleep 180
