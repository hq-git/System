#!/bin/bash

SRC_HOST=learning.edanzediting.com
DST_HOST=learning.liwenbianji.cn

# Sync code from SRC to DST
echo "Step1: Sync code from $SRC_HOST to $DST_HOST:"
/bin/sh ./wpsite_code_rsync.sh $SRC_HOST $DST_HOST
sleep 3

# Sync database from SRC to DST
echo "Step2: Sync DB from $SRC_HOST to $DST_HOST:"
/bin/sh ./wpsite_db_rsync.sh $SRC_HOST $DST_HOST
