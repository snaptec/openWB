#!/bin/bash
OPENWB_BASE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
RAMDISK_DIR="$OPENWB_BASE_DIR/ramdisk"
LOG_FILE="$RAMDISK_DIR/remote_support.log"
TOKEN_FILE="$RAMDISK_DIR/remote_support_token"

token=$(<"$TOKEN_FILE")
IFS=';' read -r token port user <<<"$token"
if [ "${#user}" -lt 6 ]; then
	user=getsupport
fi
echo "removing token file" >>"$LOG_FILE"
sudo rm "$TOKEN_FILE"
echo "starting ssh tunnel" >> "$LOG_FILE"
"$OPENWB_BASE_DIR/runs/remoteSupport/startRemoteSupport.sh" "$token" "$port" "$user" &>/dev/null &
disown
