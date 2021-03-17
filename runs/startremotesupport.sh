#!/bin/bash
re='^[0-9]+$'
if ! [[ $2 =~ $re ]] ; then
	port=2223
else
	port=$2
fi
sshpass -p $1 ssh -tt -o StrictHostKeyChecking=no  -o "ServerAliveInterval 60" -R $port:localhost:22 getsupport@remotesupport.openwb.de &

echo $! > /var/www/html/openWB/ramdisk/remotesupportpid
