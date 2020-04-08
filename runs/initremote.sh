#!/bin/bash
token=$(</var/www/html/openWB/ramdisk/remotetoken)
/var/www/html/openWB/runs/startremotesupport.sh $token  &>/dev/null & disown;

