#!/bin/bash
OPENWB_BASE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
RAMDISK_DIR="$OPENWB_BASE_DIR/ramdisk"
LOG_FILE="$RAMDISK_DIR/remote_support.log"

re='^[0-9]+$'
if ! [[ $2 =~ $re ]]; then
	port=2223
else
	port=$2
fi

echo "sshpass -p '$1' ssh -tt -o 'StrictHostKeyChecking=no' -o 'ServerAliveInterval 60' -R '$port:localhost:22' 'getsupport@remotesupport.openwb.de' &" >>"$LOG_FILE"
sshpass -p "$1" ssh -tt -o "StrictHostKeyChecking=no" -o "ServerAliveInterval 60" -R "$port:localhost:22" "getsupport@remotesupport.openwb.de" &
echo $! >"$RAMDISK_DIR/remote_support_pid"
