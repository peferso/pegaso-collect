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

rm -rf ./*.html

cd ${PEGASO_COLLT_DIR}/processed-data

tar -czvf ${CSVTARFILE} *.csv

mkdir -p $CSVBCKDIR

mv ${CSVTARFILE} ${CSVBCKDIR}/${CSVTARFILE}

rm -rf ./*.csv

cd ${PEGASO_COLLT_DIR}/sql-data

tar -czvf ${SQLTARFILE} ./*

mkdir -p $SQLBCKDIR

mv ${SQLTARFILE} ${SQLBCKDIR}/${SQLTARFILE}

rm -rf ./*

cd ${OLDPWD}

if [ `date +%u` -eq 6 ];
then

  cd ${PEGASO_COLLT_DIR%/*}/logs

  tar -czvf ${LOGTARFILE} *.log

  mkdir -p $LOGBCKDIR

  mv ${LOGTARFILE} ${LOGBCKDIR}/${LOGTARFILE}

  rm -rf ./*.log

  cd ${OLDPWD}

fi
