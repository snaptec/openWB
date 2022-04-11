#!/bin/bash
OPENWBBASEDIR=$(cd $(dirname "${BASH_SOURCE[0]}")/../.. && pwd)

#datenauslesung erfolgt im PV Modul
cat "$OPENWBBASEDIR/ramdisk/wattbezug"
