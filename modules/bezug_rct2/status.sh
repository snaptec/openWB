#!/bin/bash
MODULEDIR=$(cd "$(dirname "$0")" && pwd)
timeout -k 9 10 python3 "$MODULEDIR/rct_read_status.py" --ip="$bezug1_ip"