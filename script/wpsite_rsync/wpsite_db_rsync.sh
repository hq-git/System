#!/bin/bash

# Sync DB from local to remote host
# Author: HaoQiang at 20190222

if [ $# -lt 2 ]; then
	echo "Wrong number of arguments !"
	echo "Usage: bash $0 SRC_HOST DST_HOST"
        echo "SRC_HOST  The local site which we want to sync data from"
        echo "DST_HOST  The IP or hostname of the remote host"
	exit 1
fi

Date=`date +%Y%m%d-%H%M%S`
SRC_HOST=$1
DST_HOST=$2
SRC_SITE_ROOT=/data/web/$SRC_HOST/
DST_SITE_ROOT=/data/web/$DST_HOST/
Back_dir=/tmp
DB_file=$Back_dir/${Date}_${SRC_HOST}.sql.gz

# Export DB
echo "@@>> Export DB ..."
cd $SRC_SITE_ROOT
wp db export --add-drop-table - |gzip > $DB_file

# Rsync DB from local to remote host
echo 
echo "@@>> Rsync DB file to $DST_HOST:$Back_dir/ ..."
/usr/bin/rsync -av --progress $DB_file $DST_HOST:$Back_dir/
/bin/rm -rf $DB_file

# Import DB
echo
echo "@@>> Import DB ..."
ssh devuser@$DST_HOST <<EOF
cd $DST_SITE_ROOT
/bin/zcat $DB_file | wp db import -
/bin/rm -rf $DB_file
EOF
