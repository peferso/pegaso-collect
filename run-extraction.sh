#!/bin/bash

source ~/.profile_PEGASO

cd ${PEGASO_COLLT_DIR%/*}

run.sh extract.py

cd ${OLDPWD}
