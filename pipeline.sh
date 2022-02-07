#!/bin/bash

source ~/.profile_PEGASO

cd ${PEGASO_COLLT_DIR%/*}

mv *_*_INIT *_*_END_* logs/pipeline-logs

# ------------------------------------------------------- #

STEP=extract

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_INIT"

run.sh extract.py

EXIT=$?

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_END_${EXIT}"

# ------------------------------------------------------- #

STEP=process

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_INIT"

run.sh process.py

EXIT=$?

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_END_${EXIT}"

# ------------------------------------------------------- #

STEP=load

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_INIT"

run.sh load.py

EXIT=$?

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_END_${EXIT}"

# ------------------------------------------------------- #

STEP=remove-duplicates

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_INIT"

run-remove-db-duplicates.sh

EXIT=$?

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_END_${EXIT}"

# ------------------------------------------------------- #

STEP=housekeeping

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_INIT"

housekeeping.sh

EXIT=$?

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_END_${EXIT}"

cd ${OLDPWD}
