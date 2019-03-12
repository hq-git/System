#!/bin/bash

SRC_HOST=learning.edanzediting.com
DST_HOST=learning.liwenbianji.cn

# Sync code from SRC to DST
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "Step1 >> Sync code from $SRC_HOST to $DST_HOST"
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
/bin/bash ./wpsite_code_rsync.sh $SRC_HOST $DST_HOST
echo
sleep 1

# If above command execute failed, just exit the script.
if [ $? -ne 0 ]; then
    echo "Step1 failed, exit ..."
    exit 1
fi

# Sync database from SRC to DST
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "Step2 >> Sync DB from $SRC_HOST to $DST_HOST"
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
/bin/bash ./wpsite_db_rsync.sh $SRC_HOST $DST_HOST
