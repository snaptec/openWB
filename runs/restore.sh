#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SOURCEFILE="$OPENWBBASEDIR/web/tools/upload/backup.tar.gz"
WORKINGDIR="/home/pi/openwb_restore"
LOGFILE="$OPENWBBASEDIR/web/tools/upload/restore.log"

{
	echo "$(date +"%Y-%m-%d %H:%M:%S") Restore of backup started..."
	echo "****************************************"
	echo "Step 1: creating working directory \"$WORKINGDIR\""
	mkdir -p "$WORKINGDIR"
	echo "****************************************"
	echo "Step 2: extracting archive to working dir \"$WORKINGDIR\"..."
	sudo tar -vxf "$SOURCEFILE" -C "$WORKINGDIR"
	echo "****************************************"
	echo "Step 3: replacing old files..."
	cp -v -R -p "${WORKINGDIR}${OPENWBBASEDIR}/." "${OPENWBBASEDIR}R/"
	echo "****************************************"
	echo "Step 4: restoring mosquitto db..."
	sudo systemctl stop mosquitto.service
	sleep 2
	sudo cp -v -p "$WORKINGDIR/var/lib/mosquitto/mosquitto.db" "/var/lib/mosquitto/mosquitto.db"
	sudo systemctl start mosquitto.service
	echo "****************************************"
	echo "Step 5: cleanup after restore..."
	sudo rm "$SOURCEFILE"
	sudo rm -R "$WORKINGDIR"
	echo "****************************************"
	echo "$(date +"%Y-%m-%d %H:%M:%S") End: Restore finished."
	echo "****************************************"
} >"$LOGFILE" 2>&1
