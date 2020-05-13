#!/bin/bash
code=$1
hook=${1:1:1}
action=${1:0:1}

if (( code == 11 )); then
	curl -s --connect-timeout 5 $hook1ein_url > ./ramdisk/hookmsg
fi
if (( code == 12 )); then
	curl -s --connect-timeout 5 $hook2ein_url > ./ramdisk/hookmsg
fi
if (( code == 13 )); then
	curl -s --connect-timeout 5 $hook3ein_url > ./ramdisk/hookmsg
fi
if (( code == 01 )); then
	curl -s --connect-timeout 5 $hook1aus_url > ./ramdisk/hookmsg
fi
if (( code == 02 )); then
	curl -s --connect-timeout 5 $hook2aus_url > ./ramdisk/hookmsg
fi
if (( code == 03 )); then
	curl -s --connect-timeout 5 $hook3aus_url > ./ramdisk/hookmsg
fi

cat ./ramdisk/hookmsg >> ./ramdisk/ladestatus.log
if (( action == 0 )); then
	rm ./ramdisk/hook$hookaktiv
	echo 0 > ./ramdisk/hook$hookaktiv

	echo "Hook $hook Manuell deaktiviert" >> ./ramdisk/ladestatus.log

fi
if (( action == 1 )); then
	touch ./ramdisk/hook$hookaktiv
	echo 1 > ./ramdisk/hook$hookaktiv
	echo "Hook $hook Manuell aktiviert" >> ./ramdisk/ladestatus.log

fi
