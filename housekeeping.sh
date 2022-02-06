#!/bin/bash

source ~/.profile_PEGASO

HTMLTARFILE=batch-html-files_`date "+%Y-%m-%d_%H-%M-%S"`.tar.gz
CSVTARFILE=batch-csv-files_`date "+%Y-%m-%d_%H-%M-%S"`.tar.gz
SQLTARFILE=batch-sql-files_`date "+%Y-%m-%d_%H-%M-%S"`.tar.gz
BCKDIR=~/Desktop/pegaso-backups/
HTMLBCKDIR=${BCKDIR}/raw-data/
CSVBCKDIR=${BCKDIR}/processed-data/
SQLBCKDIR=${BCKDIR}/sql-data/

cd ${PEGASO_COLLT_DIR}/raw-data

tar -czvf ${HTMLTARFILE} *.html

mkdir -p $HTMLBCKDIR

mv ${HTMLTARFILE} ${HTMLBCKDIR}/${HTMLTARFILE}

cd ${PEGASO_COLLT_DIR}/processed-data

tar -czvf ${CSVTARFILE} *.html

mkdir -p $CSVBCKDIR

mv ${CSVTARFILE} ${CSVBCKDIR}/${CSVTARFILE}

cd ${PEGASO_COLLT_DIR}/sql-data

tar -czvf ${SQLTARFILE} *.html

mkdir -p $SQLBCKDIR

mv ${SQLTARFILE} ${SQLBCKDIR}/${SQLTARFILE}

cd ${OLDPWD}

