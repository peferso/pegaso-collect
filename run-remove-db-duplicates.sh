#!/bin/bash

shopt -s expand_aliases

source ~/.profile_PEGASO

$PEGASO_INFRA_DIR/Utilities/bash-scripts/find-and-export-db-ip.sh 2>1 | tee -a ${LOGFILE}

sleep 1.5

source ~/.profile_PEGASO

if [ $DBHOST == "null" ];
then
  echo 'The database is not available.' | tee -a ${LOGFILE} 
  echo 'Exiting.' | tee -a ${LOGFILE} 
  exit 1
else
  
  SCRIPTNAME=${0%.*} ; SCRIPTNAME=${SCRIPTNAME##*/}
  
  LOGFILE="${PEGASO_COLLT_DIR%/*}/logs/${SCRIPTNAME}_"`date "+%Y-%m-%d_%H-%M-%S"`.log

  echo 'Running '${0}'... Sending logs to '${LOGFILE}| tee -a ${LOGFILE}

  run_database_procedure < $PEGASO_INFRA_DIR/Utilities/sql/run_procedure_remove_rptd_itms.sql 2>1 | tee -a ${LOGFILE}

  echo Execution of $0 finished: `date "+%Y-%m-%d %H:%M:%S"` | tee -a ${LOGFILE}

fi



