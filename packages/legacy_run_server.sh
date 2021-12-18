#!/bin/bash
# This script will start the "legacy run server". If it is already running, it is stopped and restarted.

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
legacy_run_python_file="$SCRIPT_DIR/legacy_run_server.py"

pkill -f "$legacy_run_python_file"
status=$?
counter=0
if [ $status != 1 ]
then
	echo "Server is already running. Killing old instance."
	while true
	do
		pgrep -f "$legacy_run_python_file" > /dev/null
		status=$?
		if [ $status == 1 ]
		then
			echo "Old process successfully terminated."
			break
		fi
		if [ $counter == 100 ]
		then
			echo "Old process still alive after 10 seconds. Attempt force kill"
			pkill --signal 9 -f "$legacy_run_python_file"
		fi
		if [ $counter == 200 ]
		then
			echo "old process still alive after 20 seconds. Giving up."
			exit
		fi
		sleep .1
		((counter++))
	done
fi
echo "Starting legacy run server"
# This script *might* have been called for user "root" (e.g. when called from atreboot.sh). However we always want to
# run the server as user "pi", so that the socket file is always accessible for other scripts running as that user.
# (and of course because such scripts should not run as root in general)
(
	sudo -u pi python3 "$legacy_run_python_file" 2>&1 | while read -r line
	do
		# Multiple processes are writing to `openWB.log`, so we can't just write to that file all the time. Instead we
		# only open, write and close the file on each new line
		echo "$line" >> $SCRIPT_DIR/../ramdisk/openWB.log
	done
) &
