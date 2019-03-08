#!/bin/bash

# Sync DB from local to remote host
# Need add below privileges with visudo
# Defaults:  devuser  !requiretty
# devuser   ALL=(root) NOPASSWD:bin/rm -rf /tmp/*.sql.gz
# Author: HaoQiang at 20190222

if [ $# -lt 2 ]; then
	echo "Wrong number of arguments !"
	echo "Usage: bash $0 Site_domain Dest_IP"
	echo "Site_domain	Which site we want to sync data"
	echo "Dest_IP		The IP of remote host"
	exit 1
fi

Date=`date +%Y%m%d-%H%M%S`
Site_domain=$1
Site_ROOT=/data/web/$Site_domain/
Back_dir=/tmp
DB_file=$Back_dir/${Date}_${Site_domain}.sql.gz
Dest_IP=$2

# Export DB
echo "Step1: Export DB ..."
cd $Site_ROOT
wp db export --add-drop-table - |gzip > $DB_file

# Rsync DB from local to remote host
echo "Step2: Rsync DB file to $Dest_IP:$Back_dir/ ..."
/usr/bin/rsync -av --progress $DB_file $Dest_IP:$Back_dir/

# Import DB
echo "Step3: Import DB ..."
ssh devuser@$Dest_IP <<EOF
set -x
cd $Site_ROOT
zcat $DB_file | wp db import -
sudo /bin/rm -rf $DB_file
EOF
