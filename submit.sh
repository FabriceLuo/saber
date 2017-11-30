#! /bin/sh
#
# submit.sh
# Copyright (C) 2017 mike <mike@debian-dev>
#
# Distributed under terms of the MIT license.
#

COMMIT_FILE_NAME=`uuid | cut -d '-' -f 1`
COMMIT_FILE_PATH="/tmp/${COMMIT_FILE_NAME}.scm"

rm -f "${COMMIT_FILE_PATH}"
vim "${COMMIT_FILE_PATH}"

svn commit --file "${COMMIT_FILE_PATH}"

if [[ $? -eq 0 ]];then
    echo "commit success"
    rm -f "${COMMIT_FILE_PATH}"
else
    echo "commit failed"
fi
