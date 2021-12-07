#!/bin/bash

variable=$(curl --silent --digest -u customer:$wrsunwavespw http://$wrsunwavesip/data/ajax.txt?CAN=1)
count=0
IFS=";"

for v in $variable
do
	if (( count == 1 ));then
		pvwatt=$(echo ${v//[!0-9]/})
		pvwatt=$(echo "$pvwatt*-1" |bc)
		echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
		echo $pvwatt 
	fi
	if (( count == 16 ));then
		echo $(echo "$v*1000" | bc) > /var/www/html/openWB/ramdisk/pvkwh
	fi

	count=$((count+1))
done
