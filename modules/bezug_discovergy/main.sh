#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
python "$SCRIPT_DIR/discovergy.py" "$discovergyuser" "$discovergypass" "$discovergyevuid"
cat /var/www/html/openWB/ramdisk/wattbezug
