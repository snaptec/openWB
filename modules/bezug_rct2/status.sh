#!/bin/bash
MODULEDIR=$(cd "$(dirname "$0")" && pwd)
python3 "$MODULEDIR/rct_read_status.py" --ip="$bezug1_ip"
