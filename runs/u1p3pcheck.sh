#!/bin/bash

if [[ "$1" == "1" ]]; then
	if [[ $evsecon == "modbusevse" ]]; then
		sudo python runs/trigopen.py
	fi
	if [[ $evsecon == "ipevse" ]]; then
		sudo python runs/u1p3premote.py $evseiplp1 $u1p3plp2id 1
	fi
	if [[ $evsecon == "extopenwb" ]]; then
		mosquitto_pub -r -t openWB/set/isss/U1p3p -h $chargep1ip -m "1"
	fi
	if [[ $lastmanagement == 1 && $evsecons1 == "ipevse" && $u1p3plp2aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp2 $u1p3plp2id 1
	fi
	if [[ $lastmanagement == 1 && $evsecons1 == "extopenwb" ]]; then
		mosquitto_pub -r -t openWB/set/isss/U1p3p -h $chargep2ip -m "1"
	fi
	if [[ $lastmanagements2 == 1 && $evsecons2 == "extopenwb" ]]; then
		mosquitto_pub -r -t openWB/set/isss/U1p3p -h $chargep3ip -m "1"
	fi

	if [[ $lastmanagements2 == 1 && $evsecons2 == "ipevse" && $u1p3plp3aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp3 $u1p3plp3id 1
	fi
	if [[ $lastmanagementlp4 == 1 && $evseconlp4 == "ipevse" && $u1p3plp4aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp4 $u1p3plp4id 1
	fi
	if [[ $lastmanagementlp5 == 1 && $evseconlp5 == "ipevse" && $u1p3plp5aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp5 $u1p3plp5id 1
	fi
	if [[ $lastmanagementlp6 == 1 && $evseconlp6 == "ipevse" && $u1p3plp6aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp6 $u1p3plp6id 1
	fi
	if [[ $lastmanagementlp7 == 1 && $evseconlp7 == "ipevse" && $u1p3plp7aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp7 $u1p3plp7id 1
	fi
	if [[ $lastmanagementlp8 == 1 && $evseconlp8 == "ipevse" && $u1p3plp8aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp8 $u1p3plp8id 1
	fi
	echo 1 > ramdisk/u1p3pstat
fi
if [[ "$1" == "3" ]]; then
	if [[ $evsecon == "modbusevse" ]]; then
		sudo python runs/trigclose.py
	fi
	if [[ $evsecon == "extopenwb" ]]; then
		mosquitto_pub -r -t openWB/set/isss/U1p3p -h $chargep1ip -m "3"
	fi
	if [[ $lastmanagement == 1 && $evsecons1 == "extopenwb" ]]; then
		mosquitto_pub -r -t openWB/set/isss/U1p3p -h $chargep2ip -m "3"
	fi
	if [[ $lastmanagements2 == 1 && $evsecons2 == "extopenwb" ]]; then
		mosquitto_pub -r -t openWB/set/isss/U1p3p -h $chargep3ip -m "3"
	fi
	if [[ $evsecon == "ipevse" ]]; then
		sudo python runs/u1p3premote.py $evseiplp1 $u1p3plp2id 3
	fi
	if [[ $lastmanagement == 1 && $evsecons1 == "ipevse" && $u1p3plp2aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp2 $u1p3plp2id 3
	fi
	if [[ $lastmanagements2 == 1 && $evsecons2 == "ipevse" && $u1p3plp3aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp3 $u1p3plp3id 3
	fi
	if [[ $lastmanagementlp4 == 1 && $evseconlp4 == "ipevse" && $u1p3plp4aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp4 $u1p3plp4id 3
	fi
	if [[ $lastmanagementlp5 == 1 && $evseconlp5 == "ipevse" && $u1p3plp5aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp5 $u1p3plp5id 3
	fi
	if [[ $lastmanagementlp6 == 1 && $evseconlp6 == "ipevse" && $u1p3plp6aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp6 $u1p3plp6id 3
	fi
	if [[ $lastmanagementlp7 == 1 && $evseconlp7 == "ipevse" && $u1p3plp7aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp7 $u1p3plp7id 3
	fi
	if [[ $lastmanagementlp8 == 1 && $evseconlp8 == "ipevse" && $u1p3plp8aktiv == "1" ]]; then
		sudo python runs/u1p3premote.py $evseiplp8 $u1p3plp8id 3
	fi
	echo 3 > ramdisk/u1p3pstat
fi
if [[ "$1" == "stop" ]]; then
	if [[ $evsecon == "modbusevse" ]]; then
		oldll=$(<ramdisk/llsoll)
		echo $oldll > ramdisk/tmpllsoll
		runs/set-current.sh 0 m
	fi
	if [[ $evsecon == "extopenwb" ]]; then
		mosquitto_pub -r -t openWB/set/isss/Current -h $chargep1ip -m "0"
		oldll=$(<ramdisk/llsoll)
		echo $oldll > ramdisk/tmpllsoll
	fi
	if [[ $lastmanagement == 1 && $evsecons1 == "extopenwb" ]]; then
		oldlls1=$(<ramdisk/llsolls1)
		echo $oldlls1 > ramdisk/tmpllsolls1
		mosquitto_pub -r -t openWB/set/isss/Current -h $chargep2ip -m "0"
	fi
	if [[ $lastmanagements2 == 1 && $evsecons2 == "extopenwb" ]]; then
		oldlls2=$(<ramdisk/llsolls2)
		echo $oldlls2 > ramdisk/tmpllsolls2
		mosquitto_pub -r -t openWB/set/isss/Current -h $chargep3ip -m "0"
	fi

	if [[ $evsecon == "ipevse" ]]; then
		oldll=$(<ramdisk/llsoll)
		echo $oldll > ramdisk/tmpllsoll
		runs/set-current.sh 0 m
	fi
	if [[ $lastmanagement == 1 && $evsecons1 == "modbusevse" && $u1p3plp2aktiv == "1" ]]; then
		oldlls1=$(<ramdisk/llsolls1)
		echo $oldlls1 > ramdisk/tmpllsolls1
		runs/set-current.sh 0 s1
	fi
	if [[ $lastmanagement == 1 && $evsecons1 == "ipevse" && $u1p3plp2aktiv == "1" ]]; then
		oldlls1=$(<ramdisk/llsolls1)
		echo $oldlls1 > ramdisk/tmpllsolls1
		runs/set-current.sh 0 s1
	fi
	if [[ $lastmanagements2 == 1 && $evsecons2 == "ipevse" && $u1p3plp3aktiv == "1" ]]; then
		oldlls2=$(<ramdisk/llsolls2)
		echo $oldlls2 > ramdisk/tmpllsolls2
		runs/set-current.sh 0 s2
	fi
	if [[ $lastmanagementlp4 == 1 && $evseconlp4 == "ipevse" && $u1p3plp4aktiv == "1" ]]; then
		oldlllp4=$(<ramdisk/llsolllp4)
		echo $oldlllp4 > ramdisk/tmpllsolllp4
		runs/set-current.sh 0 lp4
	fi
	if [[ $lastmanagementlp5 == 1 && $evseconlp5 == "ipevse" && $u1p3plp5aktiv == "1" ]]; then
		oldlllp5=$(<ramdisk/llsolllp5)
		echo $oldlllp5 > ramdisk/tmpllsolllp5
		runs/set-current.sh 0 lp5
	fi
	if [[ $lastmanagementlp6 == 1 && $evseconlp6 == "ipevse" && $u1p3plp6aktiv == "1" ]]; then
		oldlllp6=$(<ramdisk/llsolllp6)
		echo $oldlllp6 > ramdisk/tmpllsolllp6
		runs/set-current.sh 0 lp6
	fi
	if [[ $lastmanagementlp7 == 1 && $evseconlp7 == "ipevse" && $u1p3plp7aktiv == "1" ]]; then
		oldlllp7=$(<ramdisk/llsolllp7)
		echo $oldlllp7 > ramdisk/tmpllsolllp7
		runs/set-current.sh 0 lp7
	fi
	if [[ $lastmanagementlp8 == 1 && $evseconlp8 == "ipevse" && $u1p3plp8aktiv == "1" ]]; then
		oldlllp8=$(<ramdisk/llsolllp8)
		echo $oldlllp8 > ramdisk/tmpllsolllp8
		runs/set-current.sh 0 lp8
	fi
fi

if [[ "$1" == "start" ]]; then
	if [[ $evsecon == "modbusevse" ]]; then
		oldll=$(<ramdisk/tmpllsoll)
		runs/set-current.sh $oldll m
	fi
	if [[ $evsecon == "ipevse" ]]; then
		oldll=$(<ramdisk/tmpllsoll)
		runs/set-current.sh $oldll m
	fi
	if [[ $evsecon == "extopenwb" ]]; then
		oldll=$(<ramdisk/tmpllsoll)
		mosquitto_pub -r -t openWB/set/isss/Current -h $chargep1ip -m "$oldll"
	fi
	if [[ $lastmanagement == 1 && $evsecons1 == "extopenwb" ]]; then
		oldlls1=$(<ramdisk/tmpllsolls1)
		mosquitto_pub -r -t openWB/set/isss/Current -h $chargep2ip -m "$oldlls1"
	fi
	if [[ $lastmanagements2 == 1 && $evsecons2 == "extopenwb" ]]; then
		oldlls2=$(<ramdisk/tmpllsolls2)
		mosquitto_pub -r -t openWB/set/isss/Current -h $chargep3ip -m "$oldlls1"
	fi

	if [[ $lastmanagement == 1 && $evsecons1 == "modbusevse" && $u1p3plp2aktiv == "1" ]]; then
		oldlls1=$(<ramdisk/tmpllsolls1)
		runs/set-current.sh $oldlls1 s1
	fi

	if [[ $lastmanagement == 1 && $evsecons1 == "ipevse" && $u1p3plp2aktiv == "1" ]]; then
		oldlls1=$(<ramdisk/tmpllsolls1)
		runs/set-current.sh $oldlls1 s1
	fi
	if [[ $lastmanagements2 == 1 && $evsecons2 == "ipevse" && $u1p3plp3aktiv == "1" ]]; then
		oldlls2=$(<ramdisk/tmpllsolls2)
		runs/set-current.sh $oldlls2 s2
	fi
	if [[ $lastmanagementlp4 == 1 && $evseconlp4 == "ipevse" && $u1p3plp4aktiv == "1" ]]; then
		oldlllp4=$(<ramdisk/tmpllsolllp4)
		runs/set-current.sh $oldlllp4 lp4
	fi
	if [[ $lastmanagementlp5 == 1 && $evseconlp5 == "ipevse" && $u1p3plp5aktiv == "1" ]]; then
		oldlllp5=$(<ramdisk/tmpllsolllp5)
		runs/set-current.sh $oldlllp5 lp5
	fi
	if [[ $lastmanagementlp6 == 1 && $evseconlp6 == "ipevse" && $u1p3plp6aktiv == "1" ]]; then
		oldlllp6=$(<ramdisk/tmpllsolllp6)
		runs/set-current.sh $oldlllp6 lp6
	fi
	if [[ $lastmanagementlp7 == 1 && $evseconlp7 == "ipevse" && $u1p3plp7aktiv == "1" ]]; then
		oldlllp7=$(<ramdisk/tmpllsolllp7)
		runs/set-current.sh $oldlllp7 lp7
	fi
	if [[ $lastmanagementlp8 == 1 && $evseconlp8 == "ipevse" && $u1p3plp8aktiv == "1" ]]; then
		oldlllp8=$(<ramdisk/tmpllsolllp8)
		runs/set-current.sh $oldlllp8 lp8
	fi
fi
if [[ "$1" == "startslow" ]]; then
	if [[ $evsecon == "modbusevse" ]]; then
		runs/set-current.sh $minimalapv m
	fi
	if [[ $evsecon == "extopenwb" ]]; then
		mosquitto_pub -r -t openWB/set/isss/Current -h $chargep1ip -m "$minimalapv"
	fi
	if [[ $lastmanagement == 1 && $evsecons1 == "extopenwb" ]]; then
		mosquitto_pub -r -t openWB/set/isss/Current -h $chargep2ip -m "$minimalapv"
	fi
	if [[ $lastmanagements2 == 1 && $evsecons2 == "extopenwb" ]]; then
		mosquitto_pub -r -t openWB/set/isss/Current -h $chargep3ip -m "$minimalapv"
	fi

	if [[ $evsecon == "ipevse" ]]; then
		runs/set-current.sh $minimalapv m
	fi
	if [[ $lastmanagement == 1 && $evsecons1 == "modbusevse" && $u1p3plp2aktiv == "1" ]]; then
		runs/set-current.sh $minimalapv s1
	fi
	if [[ $lastmanagement == 1 && $evsecons1 == "ipevse" && $u1p3plp2aktiv == "1" ]]; then
		runs/set-current.sh $minimalapv s1
	fi
	if [[ $lastmanagements2 == 1 && $evsecons2 == "ipevse" && $u1p3plp3aktiv == "1" ]]; then
		runs/set-current.sh $minimalapv s2
	fi
	if [[ $lastmanagementlp4 == 1 && $evseconlp4 == "ipevse" && $u1p3plp4aktiv == "1" ]]; then
		runs/set-current.sh $minimalapv lp4
	fi
	if [[ $lastmanagementlp5 == 1 && $evseconlp5 == "ipevse" && $u1p3plp5aktiv == "1" ]]; then
		runs/set-current.sh $minimalapv lp5
	fi
	if [[ $lastmanagementlp6 == 1 && $evseconlp6 == "ipevse" && $u1p3plp6aktiv == "1" ]]; then
		runs/set-current.sh $minimalapv lp6
	fi
	if [[ $lastmanagementlp7 == 1 && $evseconlp7 == "ipevse" && $u1p3plp7aktiv == "1" ]]; then
		runs/set-current.sh $minimalapv lp7
	fi
	if [[ $lastmanagementlp8 == 1 && $evseconlp8 == "ipevse" && $u1p3plp8aktiv == "1" ]]; then
		runs/set-current.sh $minimalapv lp8
	fi
fi
