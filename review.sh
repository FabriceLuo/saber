#! /bin/sh
#
# review.sh
# Copyright (C) 2017 mike <mike@debian-dev>
#
# Distributed under terms of the MIT license.
#

REVIEW_FILE_NAME=`uuid | cut -d '-' -f 1`
REVIEW_FILE_PATH="/tmp/${REVIEW_FILE_NAME}.rif"

# update work directory
#svn update || echo "update vcs failed" && exit 1

## generate patch file


## generate review info
#vim "${REVIEW_FILE_PATH}"

## confirm info to review
#cat "${REVIEW_FILE_PATH}"

## commit review
#review_summary=""
#review_description=""
#review_test=""
#review_bug=""
#review_peoplea=""

#review_patch=""
#review_patch_dir=""

main() {
    echo "review tools"
    while getopts "?h" option
    do
        case $option in
            h|?)
                echo "help info:";;
            *)
                echo "unimplemented option:${option}"
                exit 1;;
        esac
    done
}

main $@
