#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
BACKUPDIR="$OPENWBBASEDIR/web/backup"
. "$OPENWBBASEDIR/helperFunctions.sh"

backup() {
	openwbDebugLog MAIN 0 "creating new backup: $FILENAME"
	# remove old backup files
	openwbDebugLog MAIN 1 "deleting old backup files if present"
	rm "$BACKUPDIR/"*
	BACKUPFILE="$BACKUPDIR/$FILENAME"

	# tell mosquitto to store all retained topics in db now
	openwbDebugLog MAIN 1 "sending 'SIGUSR1' to mosquitto"
	sudo pkill -e -SIGUSR1 mosquitto
	# give mosquitto some time to finish
	sleep 0.2

	# create backup file
	openwbDebugLog MAIN 1 "creating new backup file: $BACKUPFILE"
	sudo tar --exclude="$BACKUPDIR" --exclude="$OPENWBBASEDIR/.git" -czf "$BACKUPFILE" "$OPENWBBASEDIR/" "/var/lib/mosquitto/"
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
