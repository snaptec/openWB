#!/bin/bash
if [ -f /var/www/html/openWB/ramdisk/debuguser ]; then
	timestamp=`date +"%Y-%m-%d %H:%M:%S"`
	echo "$timestamp cleanup.sh: Skipping logfile cleanup as senddebug.sh is collecting data." >> /var/www/html/openWB/ramdisk/openwb.log
else
	find /var/www/html/openWB/ramdisk/ -name "*.log" -type f -exec /var/www/html/openWB/runs/cleanupf.sh {} \;
fi
