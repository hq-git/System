#!/bin/bash

# Sync files from local to remote host
# Author: HaoQiang at 20190222

if [ $# -lt 2 ]; then
	echo "Wrong number of arguments !"
	echo "Usage: bash $0 Site_domain Dest_IP [-t]"
	echo "Site_domain	Which site we want to sync data"
	echo "Dest_IP		The IP of remote host"
	echo "-t --dry-run  perform a trial run with no changes made"
	exit 1
fi

Site_domain=$1
#Sync_folder=/data/web/$Site_domain/sites/all/files/
Sync_folder=/data/web/$Site_domain/
Dest_IP=$2
Option="-av --progress --exclude=wp-config.php"

if [ $3 ]; then
	if [ $3 = "-t" ]; then
		Option=$Option" --dry-run"
	fi
fi
rsync_command="/usr/bin/rsync $Option $Sync_folder* $Dest_IP:$Sync_folder"

while [ 1 != 2 ]; do
	echo "Will run the command -> $rsync_command"
	echo -n "Please confirm [y/n]:"
	read choice
	# convert input to lower case
	choice=`echo $choice| tr [A-Z] [a-z]`
	if [ $choice == "y" ]; then
		break
	elif [ $choice == "n" ]; then
		exit 1
	fi
done
echo "Start syncing ..."
${rsync_command}
