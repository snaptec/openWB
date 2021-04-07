#!/bin/bash
if [ ! -f /var/www/html/openWB/ramdisk/debuguser ]; then
	find /var/www/html/openWB/ramdisk/* -name "*.log" -type f -exec /var/www/html/openWB/runs/cleanupf.sh {} \;
else
	echo "Skipping logfile cleanup as senddebug.sh is collecting data." >> /var/www/html/openWB/ramdisk/openwb.log
fi
