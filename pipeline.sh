#!/bin/bash

source ~/.profile_PEGASO

cd ${PEGASO_COLLT_DIR%/*}

# ------------------------------------------------------- #

STEP=extract

rm -rf ${STEP}_*_INIT ${STER}_*_END_*

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_INIT"

run.sh extract.py

EXIT=$?

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_END_${EXIT}"

# ------------------------------------------------------- #

STEP=process

rm -rf ${STEP}_*_INIT ${STER}_*_END_*

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_INIT"

run.sh process.py

EXIT=$?

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_END_${EXIT}"

# ------------------------------------------------------- #

STEP=load

rm -rf ${STEP}_*_INIT ${STER}_*_END_*

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_INIT"

run.sh load.py

EXIT=$?

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_END_${EXIT}"

# ------------------------------------------------------- #

STEP=remove-duplicates

rm -rf ${STEP}_*_INIT ${STER}_*_END_*

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_INIT"

run-remove-db-duplicates.sh

EXIT=$?

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_END_${EXIT}"

# ------------------------------------------------------- #

STEP=housekeeping

rm -rf ${STEP}_*_INIT ${STER}_*_END_*

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_INIT"

housekeeping.sh

EXIT=$?

touch "${STEP}_`date "+%Y-%m-%d_%H-%M-%S"`_END_${EXIT}"

cd ${OLDPWD}
