#!/bin/bash

# Sync files from local to remote host
# Author: HaoQiang at 20190222

if [ $# -lt 2 ]; then
	echo "Wrong number of arguments !"
	echo "Usage: bash $0 SRC_HOST DST_HOST [-t]"
	echo "SRC_HOST	The local site which we want to sync data from"
	echo "DST_HOST	The IP or hostname of the remote host"
	echo "-t --dry-run  perform a trial run with no changes made"
	exit 1
fi

SRC_HOST=$1
DST_HOST=$2
Option="-av --progress --exclude=wp-config.php"
Sync_folder=/data/web/$SRC_HOST/
#Sync_folder=/data/web/$SRC_HOST/sites/all/files/

# Generate the rsync command
if [ $3 ]; then
	if [ $3 = "-t" ]; then
		Option=$Option" --dry-run"
	fi
fi
rsync_command="/usr/bin/rsync $Option $Sync_folder* $DST_HOST:$Sync_folder"

# Confirm whether to run the command
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

# Run sync process
echo "Start syncing ..."
${rsync_command}
