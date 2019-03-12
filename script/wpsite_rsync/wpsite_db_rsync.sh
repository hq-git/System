#!/bin/bash

# Sync DB from local to remote host
# Need add below privileges with visudo
# Defaults:  devuser  !requiretty
# devuser   ALL=(root) NOPASSWD:bin/rm -rf /tmp/*.sql.gz
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
Site_ROOT=/data/web/$SRC_HOST/
Back_dir=/tmp
DB_file=$Back_dir/${Date}_${SRC_HOST}.sql.gz

# Export DB
echo ">> Export DB ..."
cd $Site_ROOT
wp db export --add-drop-table - |gzip > $DB_file

# Rsync DB from local to remote host
echo ">> Rsync DB file to $DST_HOST:$Back_dir/ ..."
/usr/bin/rsync -av --progress $DB_file $DST_HOST:$Back_dir/

# Import DB
echo ">> Import DB ..."
ssh devuser@$DST_HOST <<EOF
set -x
cd $Site_ROOT
zcat $DB_file | wp db import -
sudo /bin/rm -rf $DB_file
EOF
