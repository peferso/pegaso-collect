#!/bin/bash

source ~/.profile_PEGASO

cd ${PEGASO_COLLT_DIR%/*}

source bin/activate

SCRIPTNAME=${0%.*}
SCRIPTNAME=${SCRIPTNAME##*/}

LOGFILE="logs/${SCRIPTNAME}_"`date "+%Y-%m-%d_%H-%M-%S"`.log

python3 src/load.py > ${LOGFILE} 2>&1 

echo "\n"Execution of $0 finished: `date "+%Y-%m-%d %H:%M:%S"` > ${LOGFILE}

cd ${OLDPWD}
