#!/bin/bash

find /var/www/html/openWB/ramdisk/* -name "*.log" -type f -exec /var/www/html/openWB/runs/cleanupf.sh {} \;

