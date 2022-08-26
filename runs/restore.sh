#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
SOURCEFILE="$OPENWBBASEDIR/web/tools/upload/backup.tar.gz"
WORKINGDIR="/home/pi/openwb_restore"
MOSQUITTODIR="/var/lib/mosquitto"
LOGFILE="$OPENWBBASEDIR/web/tools/upload/restore.log"

{
	echo "$(date +"%Y-%m-%d %H:%M:%S") Restore of backup started..."
	echo "****************************************"
	echo "Step 1: setting flag 'update in progress' and wait for control loop to finish"
	echo 1 > "$OPENWBBASEDIR/ramdisk/updateinprogress"
	# Wait for regulation loop(s) and cron jobs to end, but with timeout in case a script hangs
	pgrep -f "$OPENWBBASEDIR/(regel\\.sh|runs/cron5min\\.sh|runs/cronnightly\\.sh)$" | \
		timeout 15 xargs -n1 -I'{}' tail -f --pid="{}" /dev/null
	echo "****************************************"
	echo "Step 2: creating working directory \"$WORKINGDIR\""
	mkdir -p "$WORKINGDIR"
	echo "****************************************"
	echo "Step 3: extracting archive to working dir \"$WORKINGDIR\"..."
	if ! sudo tar -vxf "$SOURCEFILE" -C "$WORKINGDIR"; then
		echo "something went wrong! aborting restore"
		echo "Wiederherstellung fehlgeschlagen! Bitte Protokolldateien prüfen." >"$RAMDISKDIR/lastregelungaktiv"
		echo 0 > "$OPENWBBASEDIR/ramdisk/updateinprogress"
		exit 1
	fi
	echo "****************************************"
	echo "Step 4: replacing old files..."
	mv -v -f "${WORKINGDIR}${OPENWBBASEDIR}/." "${OPENWBBASEDIR}/"
	echo "****************************************"
	echo "Step 5: restoring mosquitto db..."
	sudo systemctl stop mosquitto.service
	sleep 2
	sudo mv -v -f "${WORKINGDIR}${MOSQUITTODIR}/mosquitto.db" "$MOSQUITTODIR/mosquitto.db"
	echo "****************************************"
	echo "Step 6: cleanup after restore..."
	sudo rm "$SOURCEFILE"
	sudo rm -R "$WORKINGDIR"
	echo "****************************************"
	echo "$(date +"%Y-%m-%d %H:%M:%S") End: Restore finished."
	echo "rebooting"
	"$OPENWBBASEDIR/runs/reboot.sh"
	echo "****************************************"
} >"$LOGFILE" 2>&1
