#!/bin/bash

source ~/.profile_PEGASO

RAWTARFILE=batch-raw-files_`date "+%Y-%m-%d_%H-%M-%S"`.tar.gz
CSVTARFILE=batch-csv-files_`date "+%Y-%m-%d_%H-%M-%S"`.tar.gz
SQLTARFILE=batch-sql-files_`date "+%Y-%m-%d_%H-%M-%S"`.tar.gz
LOGTARFILE=batch-log-files_`date "+%Y-%m-%d_%H-%M-%S"`.tar.gz
BCKDIR=~/Desktop/pegaso-backups/
RAWBCKDIR=${BCKDIR}/raw-data/
CSVBCKDIR=${BCKDIR}/processed-data/
SQLBCKDIR=${BCKDIR}/sql-data/
LOGBCKDIR=${BCKDIR}/logs/

cd ${PEGASO_COLLT_DIR}/raw-data

tar -czvf ${RAWTARFILE} *.html

mkdir -p $RAWBCKDIR

mv ${RAWTARFILE} ${RAWBCKDIR}/${RAWTARFILE}

cd ${PEGASO_COLLT_DIR}/processed-data

tar -czvf ${CSVTARFILE} *.csv

mkdir -p $CSVBCKDIR

mv ${CSVTARFILE} ${CSVBCKDIR}/${CSVTARFILE}

cd ${PEGASO_COLLT_DIR}/sql-data

tar -czvf ${SQLTARFILE} *.sql

mkdir -p $SQLBCKDIR

mv ${SQLTARFILE} ${SQLBCKDIR}/${SQLTARFILE}

cd ${OLDPWD}

cd ${PEGASO_COLLT_DIR%/*}/logs

tar -czvf ${LOGTARFILE} *.log

mkdir -p $LOGBCKDIR

mv ${LOGTARFILE} ${LOGBCKDIR}/${LOGTARFILE}

cd ${OLDPWD}

