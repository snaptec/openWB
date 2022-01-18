#!/bin/bash
#
# Running with sudo
#
timestamp=`date +"%Y-%m-%d %H:%M:%S"`
if [ -f /var/www/html/openWB/ramdisk/debuguser ]; then
	echo "$timestamp cleanup.sh: Skipping logfile cleanup as senddebug.sh is collecting data." >> /var/www/html/openWB/ramdisk/openWB.log
else
	echo "$timestamp cleanup.sh: checking logfiles." >> /var/www/html/openWB/ramdisk/openWB.log
	find /var/www/html/openWB/ramdisk/ -name "*.log" -type f -exec /var/www/html/openWB/runs/cleanupf.sh {} \;
fi
