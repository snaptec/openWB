#!/bin/bash

declare -A mqttvar
mqttvar["evu/APhase1"]=bezuga1
mqttvar["evu/APhase2"]=bezuga2
mqttvar["evu/APhase3"]=bezuga3
mqttvar["evu/VPhase1"]=evuv1
mqttvar["evu/VPhase2"]=evuv2
mqttvar["evu/VPhase3"]=evuv3
mqttvar["evu/Hz"]=evuhz
mqttvar["evu/PfPhase1"]=evupf1
mqttvar["evu/PfPhase2"]=evupf2
mqttvar["evu/PfPhase3"]=evupf3
mqttvar["lp2/VPhase1"]=llvs11
mqttvar["lp2/VPhase2"]=llvs12
mqttvar["lp2/VPhase3"]=llvs13
mqttvar["lp1/VPhase1"]=llv1
mqttvar["lp1/VPhase2"]=llv2
mqttvar["lp1/VPhase3"]=llv3
mqttvar["lp3/VPhase1"]=llvs21
mqttvar["lp3/VPhase2"]=llvs22
mqttvar["lp3/VPhase3"]=llvs23
mqttvar["lp2/APhase1"]=llas11
mqttvar["lp2/APhase2"]=llas12
mqttvar["lp2/APhase3"]=llas13
mqttvar["lp3/APhase1"]=llas21
mqttvar["lp3/APhase2"]=llas22
mqttvar["lp3/APhase3"]=llas23
mqttvar["lp1/APhase1"]=lla1
mqttvar["lp1/APhase2"]=lla2
mqttvar["lp1/APhase3"]=lla3
mqttvar["lp1/kWhCounter"]=llkwh
mqttvar["lp2/kWhCounter"]=llkwhs1
mqttvar["lp3/kWhCounter"]=llkwhs2
mqttvar["Verbraucher/WNr1"]=verbraucher1_watt
mqttvar["Verbraucher/WhImportNr1"]=verbraucher1_wh
mqttvar["Verbraucher/WhExportNr1"]=verbraucher1_whe
mqttvar["Verbraucher/WNr2"]=verbraucher2_watt
mqttvar["Verbraucher/WhImportNr2"]=verbraucher2_wh
mqttvar["Verbraucher/WhExportNr2"]=verbraucher2_whe
mqttvar["evu/WhExported"]=einspeisungkwh
mqttvar["evu/WhImported"]=bezugkwh
mqttvar["housebattery/WhExported"]=speicherekwh
mqttvar["housebattery/WhImported"]=speicherikwh
mqttvar["pv/CounterTillStartPvCharging"]=pvcounter
mqttvar["pv/Whcounter"]=pvkwh
mqttvar["lp1/PfVPhase1"]=llpf1
mqttvar["lp1/PfPhase2"]=llpf2
mqttvar["lp1/PfPhase3"]=llpf3








mqttvar["evu/ASchieflast"]=schieflast
mqttvar["evu/WPhase1"]=bezugw1
mqttvar["evu/WPhase2"]=bezugw2
mqttvar["evu/WPhase3"]=bezugw3
for mq in "${!mqttvar[@]}"; do
	declare o${mqttvar[$mq]}
	declare ${mqttvar[$mq]}
	tempnewname=${mqttvar[$mq]}

	tempoldname=o${mqttvar[$mq]}
	tempoldname=$(<ramdisk/mqtt"${mqttvar[$mq]}")
	tempnewname=$(<ramdisk/"${mqttvar[$mq]}")
	if [[ "$tempoldname" != "$tempnewname" ]]; then
		mosquitto_pub -t openWB/$mq -r -m "$tempnewname"
		#echo "neu  $mq $tempnewname"
		echo $tempnewname > ramdisk/mqtt${mqttvar[$mq]}
	fi
	#echo ${mqttvar[$mq]} $mq 
done






