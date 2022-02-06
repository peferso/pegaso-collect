#!/bin/bash

source ~/.profile_PEGASO

cd ${PEGASO_COLLT_DIR%/*}

run.sh process.py

cd ${OLDPWD}
