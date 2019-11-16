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
mqttvar["lp1/ChargeStatus"]=ladestatus
mqttvar["lp2/ChargeStatus"]=ladestatuss1
mqttvar["lp3/ChargeStatus"]=ladestatuss2
mqttvar["lp4/ChargeStatus"]=ladestatuslp4
mqttvar["lp5/ChargeStatus"]=ladestatuslp5
mqttvar["lp6/ChargeStatus"]=ladestatuslp6
mqttvar["lp7/ChargeStatus"]=ladestatuslp7
mqttvar["lp8/ChargeStatus"]=ladestatuslp8
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
mqttvar["Verbraucher/WhImportedNr1"]=verbraucher1_wh
mqttvar["Verbraucher/WhExportedNr1"]=verbraucher1_whe
mqttvar["Verbraucher/WNr2"]=verbraucher2_watt
mqttvar["Verbraucher/WhImportedNr2"]=verbraucher2_wh
mqttvar["Verbraucher/WhExportedNr2"]=verbraucher2_whe
mqttvar["evu/WhExported"]=einspeisungkwh
mqttvar["evu/WhImported"]=bezugkwh
mqttvar["housebattery/WhExported"]=speicherekwh
mqttvar["housebattery/WhImported"]=speicherikwh
mqttvar["pv/CounterTillStartPvCharging"]=pvcounter
mqttvar["pv/WhCounter"]=pvkwh
mqttvar["lp1/PfVPhase1"]=llpf1
mqttvar["lp1/PfPhase2"]=llpf2
mqttvar["lp1/PfPhase3"]=llpf3
mqttvar["lp1/ChargePointEnabled"]=lp1enabled
mqttvar["lp2/ChargePointEnabled"]=lp2enabled
mqttvar["lp3/ChargePointEnabled"]=lp3enabled
mqttvar["lp4/ChargePointEnabled"]=lp4enabled
mqttvar["lp5/ChargePointEnabled"]=lp5enabled
mqttvar["lp6/ChargePointEnabled"]=lp6enabled
mqttvar["lp7/ChargePointEnabled"]=lp7enabled
mqttvar["lp8/ChargePointEnabled"]=lp8enabled
mqttvar["evu/WAverage"]=glattwattbezug
mqttvar["strLastmanagementActive"]=lastregelungaktiv
mqttvar["lp6/W"]=llaktuelllp6
mqttvar["lp6/kWhCounter"]=llkwhlp6
mqttvar["lp6/APhase1"]=lla1lp6
mqttvar["lp6/APhase2"]=lla2lp6
mqttvar["lp6/APhase3"]=lla3lp6
mqttvar["lp6/VPhase1"]=llv1lp6
mqttvar["lp6/VPhase2"]=llv2lp6
mqttvar["lp6/VPhase3"]=llv3lp6
mqttvar["lp7/W"]=llaktuelllp7
mqttvar["lp7/kWhCounter"]=llkwhlp7
mqttvar["lp7/APhase1"]=lla1lp7
mqttvar["lp7/APhase2"]=lla2lp7
mqttvar["lp7/APhase3"]=lla3lp7
mqttvar["lp7/VPhase1"]=llv1lp7
mqttvar["lp7/VPhase2"]=llv2lp7
mqttvar["lp7/VPhase3"]=llv3lp7
mqttvar["lp8/W"]=llaktuelllp8
mqttvar["lp8/kWhCounter"]=llkwhlp8
mqttvar["lp8/APhase1"]=lla1lp8
mqttvar["lp8/APhase2"]=lla2lp8
mqttvar["lp8/APhase3"]=lla3lp8
mqttvar["lp8/VPhase1"]=llv1lp8
mqttvar["lp8/VPhase2"]=llv2lp8
mqttvar["lp8/VPhase3"]=llv3lp8
mqttvar["lp4/W"]=llaktuelllp4
mqttvar["lp4/kWhCounter"]=llkwhlp4
mqttvar["lp4/APhase1"]=lla1lp4
mqttvar["lp4/APhase2"]=lla2lp4
mqttvar["lp4/APhase3"]=lla3lp4
mqttvar["lp4/VPhase1"]=llv1lp4
mqttvar["lp4/VPhase2"]=llv2lp4
mqttvar["lp4/VPhase3"]=llv3lp4
mqttvar["lp5/W"]=llaktuelllp5
mqttvar["lp5/kWhCounter"]=llkwhlp5
mqttvar["lp5/APhase1"]=lla1lp5
mqttvar["lp5/APhase2"]=lla2lp5
mqttvar["lp5/APhase3"]=lla3lp5
mqttvar["lp5/VPhase1"]=llv1lp5
mqttvar["lp5/VPhase2"]=llv2lp5
mqttvar["lp5/VPhase3"]=llv3lp5
mqttvar["evu/ASchieflast"]=schieflast
mqttvar["evu/WPhase1"]=bezugw1
mqttvar["evu/WPhase2"]=bezugw2
mqttvar["evu/WPhase3"]=bezugw3
mqttvar["lp1/AConfigured"]=llsoll
mqttvar["lp2/AConfigured"]=llsolls1
mqttvar["lp3/AConfigured"]=llsolls2
mqttvar["lp4/AConfigured"]=llsolllp4
mqttvar["lp5/AConfigured"]=llsolllp5
mqttvar["lp6/AConfigured"]=llsolllp6
mqttvar["lp7/AConfigured"]=llsolllp7
mqttvar["lp8/AConfigured"]=llsolllp8
mqttvar["lp1/kWhActualCharged"]=aktgeladen
mqttvar["lp2/kWhActualCharged"]=aktgeladens1
mqttvar["lp3/kWhActualCharged"]=aktgeladens2
mqttvar["lp4/kWhActualCharged"]=aktgeladenlp4
mqttvar["lp5/kWhActualCharged"]=aktgeladenlp5
mqttvar["lp6/kWhActualCharged"]=aktgeladenlp6
mqttvar["lp7/kWhActualCharged"]=aktgeladenlp7
mqttvar["lp8/kWhActualCharged"]=aktgeladenlp8
mqttvar["lp1/boolPlugStat"]=plugstat
mqttvar["lp2/boolPlugStat"]=plugstats1
mqttvar["lp4/boolPlugStat"]=plugstatlp4
mqttvar["lp5/boolPlugStat"]=plugstatlp5
mqttvar["lp6/boolPlugStat"]=plugstatlp6
mqttvar["lp7/boolPlugStat"]=plugstatlp7
mqttvar["lp8/boolPlugStat"]=plugstatlp8
mqttvar["lp1/boolChargeStat"]=chargestat
mqttvar["lp2/boolChargeStat"]=chargestats1
mqttvar["lp4/boolChargeStat"]=chargestatlp4
mqttvar["lp5/boolChargeStat"]=chargestatlp5
mqttvar["lp6/boolChargeStat"]=chargestatlp6
mqttvar["lp7/boolChargeStat"]=chargestatlp7
mqttvar["lp8/boolChargeStat"]=chargestatlp8
mqttvar["lp1/kWhChargedSincePlugged"]=pluggedladungbishergeladen
mqttvar["lp2/kWhChargedSincePlugged"]=pluggedladungbishergeladenlp2
mqttvar["lp3/kWhChargedSincePlugged"]=pluggedladungbishergeladenlp3
mqttvar["lp4/kWhChargedSincePlugged"]=pluggedladungbishergeladenlp4
mqttvar["lp5/kWhChargedSincePlugged"]=pluggedladungbishergeladenlp5
mqttvar["lp6/kWhChargedSincePlugged"]=pluggedladungbishergeladenlp6
mqttvar["lp7/kWhChargedSincePlugged"]=pluggedladungbishergeladenlp7
mqttvar["lp8/kWhChargedSincePlugged"]=pluggedladungbishergeladenlp8


tempPubList=""
for mq in "${!mqttvar[@]}"; do
	declare o${mqttvar[$mq]}
	declare ${mqttvar[$mq]}
	tempnewname=${mqttvar[$mq]}

	tempoldname=o${mqttvar[$mq]}
	tempoldname=$(<ramdisk/mqtt"${mqttvar[$mq]}")
	tempnewname=$(<ramdisk/"${mqttvar[$mq]}")
	if [[ "$tempoldname" != "!$tempnewname" ]]; then
		tempPubList="${tempPubList}\nopenWB/${mq}=${tempnewname}"
		echo $tempnewname > ramdisk/mqtt${mqttvar[$mq]}
	fi
	#echo ${mqttvar[$mq]} $mq 
done

#echo "Publist:"
#echo -e $tempPubList

#echo "Running Python:"
echo -e $tempPubList | python3 runs/mqttpub.py -q 2 -r
