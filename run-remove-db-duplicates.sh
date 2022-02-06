#!/bin/bash

shopt -s expand_aliases

source ~/.profile_PEGASO

SCRIPTNAME=${0%.*} ; SCRIPTNAME=${SCRIPTNAME##*/}
LOGFILE="${PEGASO_COLLT_DIR%/*}/logs/${SCRIPTNAME}_"`date "+%Y-%m-%d_%H-%M-%S"`.log

echo 'Running '${0}'... Sending logs to '${LOGFILE}| tee -a ${LOGFILE}

run_database_procedure < $PEGASO_INFRA_DIR/Utilities/sql/run_procedure_remove_rptd_itms.sql | tee -a ${LOGFILE}

echo Execution of $0 finished: `date "+%Y-%m-%d %H:%M:%S"` | tee -a ${LOGFILE}

