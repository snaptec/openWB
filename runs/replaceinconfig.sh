#!/bin/bash
OPENWBBASEDIR=$(cd $(dirname "${BASH_SOURCE[0]}")/.. && pwd)
CONFIG_FILE="$OPENWBBASEDIR/openwb.conf"

for i in {9..1}
do
	[[ -e "$CONFIG_FILE.$i" ]] && mv "$CONFIG_FILE.$i" "$CONFIG_FILE.$((i+1))"
done
# Do not move openwb.conf, so that it remains readable during the short moment where it is replaced.
# Use link instead, then let sed overwrite the original link
ln "$CONFIG_FILE" "$CONFIG_FILE.1"
sed -i "s,$1.*,$1$2,g" "$CONFIG_FILE"
