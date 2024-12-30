#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
BACKUPDIR="$OPENWBBASEDIR/web/backup"
. "$OPENWBBASEDIR/helperFunctions.sh"

backup() {
	# $1: name for new backup file
	# remove old backup files
	openwbDebugLog MAIN 1 "deleting old backup files if present"
	rm "$BACKUPDIR/"*

	# tell mosquitto to store all retained topics in db now
	openwbDebugLog MAIN 1 "sending 'SIGUSR1' to mosquitto"
	sudo pkill --echo -SIGUSR1 mosquitto
	# give mosquitto some time to finish
	sleep 0.2

	# create backup file
	BACKUPFILE="$BACKUPDIR/$1"
	openwbDebugLog MAIN 0 "creating new backup file: $BACKUPFILE"
	sudo tar --verbose --create --gzip --file="$BACKUPFILE" \
		--exclude="$BACKUPDIR" \
		--exclude="$OPENWBBASEDIR/.git" \
		"$OPENWBBASEDIR/" "/var/lib/mosquitto/"
	openwbDebugLog MAIN 1 "setting permissions of new backup file"
	sudo chown pi:www-data "$BACKUPFILE"
	sudo chmod 664 "$BACKUPFILE"

	openwbDebugLog MAIN 0 "backup finished"
}

useExtendedFilename=$1
if ((useExtendedFilename == 1)); then
	FILENAME="openWB_backup_$(date +"%Y-%m-%d_%H:%M:%S").tar.gz"
else
	FILENAME="backup.tar.gz"
fi

openwbRunLoggingOutput backup "$FILENAME"
# return our filename for further processing
echo "$FILENAME"
