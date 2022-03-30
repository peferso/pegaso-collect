#!/bin/bash

build_event () {
  STEP=$1
  MSG=$2
  cp event-remove-duplicates-skel.json event-remove-duplicates.json
  TIME=`date "+%Y-%m-%d %H:%M:%N"`
  SCRIPT=`basename $0`
  REPL_MSG=`echo "s/XXMSGXX/${MSG}/"`
  REPL_STEP=`echo "s/XXSTEPXX/${STEP}/"`
  REPL_TIME=`echo "s/XXTIMEXX/${TIME}/"`
  REPL_SCRIPT=`echo "s/XXSCRIPTXX/${SCRIPT}/"`
  sed -i "$REPL_MSG" event-remove-duplicates.json
  sed -i "$REPL_STEP" event-remove-duplicates.json
  sed -i "$REPL_TIME" event-remove-duplicates.json
  sed -i "$REPL_SCRIPT" event-remove-duplicates.json
}

remove_duplicates () {
  
  SCRIPTNAME=${0%.*} ; SCRIPTNAME=${SCRIPTNAME##*/}
  
  LOGFILE="${PEGASO_COLLT_DIR%/*}/logs/${SCRIPTNAME}_"`date "+%Y-%m-%d_%H-%M-%S"`.log

  echo 'Running '${0}'... Sending logs to '${LOGFILE}| tee -a ${LOGFILE}

  NUMREGBFORE=`run_database_procedure < query.sql 2>/dev/null`

  build_event "Start" "Table raw_data has $NUMREGBFORE registers before deleting duplicates."

  aws events put-events --profile ec2Manager --entries file://event-remove-duplicates.json

  run_database_procedure < $PEGASO_INFRA_DIR/Utilities/sql/run_procedure_remove_rptd_itms.sql 2>1 | tee -a ${LOGFILE}

  NUMREGAFTER=`run_database_procedure < query.sql 2>/dev/null`
  
  build_event "Start" "Table raw_data has $NUMREGAFTER registers after deleting duplicates. A total of $((NUMREGBFORE-NUMREGAFTER)) registers were deleted"

  aws events put-events --profile ec2Manager --entries file://event-remove-duplicates.json
  
  echo Execution of $0 finished: `date "+%Y-%m-%d %H:%M:%S"` | tee -a ${LOGFILE}

}
 
shopt -s expand_aliases

source ~/.profile_PEGASO

$PEGASO_INFRA_DIR/Utilities/bash-scripts/find-and-export-db-ip.sh 2>1 | tee -a ${LOGFILE}

source ~/.profile_PEGASO

if [ $DBHOST == "null" ];
then

  echo 'The database is not available.' | tee -a ${LOGFILE} 
  echo 'Starting' | tee -a ${LOGFILE} 
 
  start_db

  sleep 180

  source ~/.profile_PEGASO
  
  remove_duplicates

  stop_db

  echo 'Stopping' | tee -a ${LOGFILE} 

else

  remove_duplicates

fi

