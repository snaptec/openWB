#!/bin/bash

if [ -n "$bezug1_ip" ]; then
  opt=""
else
  echo "$0 Debughilfe bezug1_ip parameter not supplied use 192.168.208.63"
  bezug1_ip=192.168.208.63
  opt=" -v"
fi
#
#   
timeout -k 9 10 python3 /var/www/html/openWB/modules/bezug_rct2/rct_read_status.py $opt --ip=$bezug1_ip



