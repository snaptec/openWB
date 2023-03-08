#!/bin/bash
TOKENFILE='/var/www/html/openWB/ramdisk/remotetoken'
token=$(<$TOKENFILE)
IFS=';' read -r token port user <<< "$token"
if [ "${#user}" -gt 5 ]; then
	user=$user
else
	user=getsupport
fi

sudo rm $TOKENFILE

/var/www/html/openWB/runs/startremotesupport.sh $token $port $user &>/dev/null & disown;
