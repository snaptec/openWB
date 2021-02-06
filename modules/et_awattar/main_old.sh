#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"

# for testing from cli
# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "et_awattar: seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
fi

# abort if we try to use unset variables
set -o nounset

if [[ "$awattarlocation" == "de" ]]; then
	awadata=$(curl -s https://api.awattar.de/v1/marketdata)
fi
if [[ "$awattarlocation" == "at" ]]; then
	awadata=$(curl -s https://api.awattar.at/v1/marketdata)
fi

if [ -f $RAMDISKDIR/awattarstarthours ]; then
	rm $RAMDISKDIR/awattarstarthours
fi
start=$(echo $awadata | jq '.data[].start_timestamp')
while IFS= read -r line; do
	date +"%H" -d @$((line/1000)) >> $RAMDISKDIR/awattarstarthours
done <<< "$start"

if [ -f $RAMDISKDIR/awattarendhours ]; then
	rm $RAMDISKDIR/awattarendhours
fi
end=$(echo $awadata | jq '.data[].end_timestamp')
while IFS= read -r line; do
	date +"%H" -d @$((line/1000)) >> $RAMDISKDIR/awattarendhours
done <<< "$end"

if [ -f $RAMDISKDIR/etproviderpricelist ]; then
	rm $RAMDISKDIR/etproviderpricelist
fi
actual=0
price=$(echo $awadata | jq '.data[].marketprice')
if [[ "$awattarlocation" == "de" ]]; then
	while IFS= read -r line; do
		if ((actual == 0 )); then
			echo "scale=2;$line * 100 / 1000 * 1.19" | bc -l > $RAMDISKDIR/etproviderprice
			actual=1
			actualprice=$(<$RAMDISKDIR/etproviderprice)
		fi
		echo "scale=2;$line * 100 / 1000 * 1.19" | bc -l >> $RAMDISKDIR/etproviderpricelist
	done <<< "$price"
fi
if [[ "$awattarlocation" == "at" ]]; then
	while IFS= read -r line; do
		if ((actual == 0 )); then
			echo "scale=2;$line * 100 / 1000 * 1.20" | bc -l > $RAMDISKDIR/etproviderprice
			actual=1
			actualprice=$(<$RAMDISKDIR/etproviderprice)
		fi
		echo "scale=2;$line * 100 / 1000 * 1.20" | bc -l >> $RAMDISKDIR/etproviderpricelist
	done <<< "$price"
fi
paste -d "," $RAMDISKDIR/awattarstarthours $RAMDISKDIR/etproviderpricelist > $RAMDISKDIR/etprovidergraphlist
mosquitto_pub -r -t openWB/global/awattar/pricelist -m "$(cat $RAMDISKDIR/etprovidergraphlist)"
