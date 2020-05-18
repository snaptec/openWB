#!/bin/bash

# echo $#
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
# echo $OPENWBBASEDIR


case $1 in
	2)
		# second charge point
		tintervallladen=$(( soc_teslalp2_intervallladen * 6 ))
		tintervall=$(( soc_teslalp2_intervall * 6 ))
		teslatimer=$(<$OPENWBBASEDIR/ramdisk/soctimer1)
		ladeleistung=$(<$OPENWBBASEDIR/ramdisk/llaktuells1)
		soctimerfile="$OPENWBBASEDIR/ramdisk/soctimer1"
		socfile="$OPENWBBASEDIR/ramdisk/soc1"
		username=$soc_teslalp2_username
		password=$soc_teslalp2_password
		carnumber=$soc_teslalp2_carnumber
		;;
	*)
		# defaults to first charge point for backward compatibility
		tintervallladen=$(( soc_tesla_intervallladen * 6 ))
		tintervall=$(( soc_tesla_intervall * 6 ))
		teslatimer=$(<$OPENWBBASEDIR/ramdisk/soctimer)
		ladeleistung=$(<$OPENWBBASEDIR/ramdisk/llaktuell)
		soctimerfile="$OPENWBBASEDIR/ramdisk/soctimer"
		socfile="$OPENWBBASEDIR/ramdisk/soc"
		username=$soc_tesla_username
		password=$soc_tesla_password
		carnumber=$soc_tesla_carnumber
		;;
esac

getAndWriteSoc(){
	re='^-?[0-9]+$'
	soclevel=$(sudo python $OPENWBBASEDIR/modules/soc_tesla/tsoc.py $username $password $carnumber | jq .battery_level)
	if  [[ $soclevel =~ $re ]] ; then
		if (( $soclevel != 0 )) ; then
			echo $soclevel > $socfile
			# echo "$soclevel > $socfile"
		fi
	fi
	echo 0 > $soctimerfile
	# echo "0 > $soctimerfile"
}

incrementTimer(){
	teslatimer=$((teslatimer+1))
	echo $teslatimer > $soctimerfile
	# echo "$teslatimer > $soctimerfile"
}

if (( ladeleistung > 1000 )); then
	if (( teslatimer < tintervallladen )); then
		# echo "$teslatimer < $tintervallladen"
		incrementTimer
	else
		getAndWriteSoc
	fi
else
	if (( teslatimer < tintervall )); then
		# echo "$teslatimer < $tintervall"
		incrementTimer
	else
		getAndWriteSoc
	fi
fi
