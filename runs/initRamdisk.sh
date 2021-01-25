#!/bin/bash
# Ramdisk mit initialen Werten befüllen nach Neustart

initRamdisk(){
	RamdiskPath="/var/www/html/openWB/ramdisk"
	echo "Initializing Ramdisk $RamdiskPath"

	# Logfiles erstellen
	ln -s /var/log/openWB.log $RamdiskPath/openWB.log
	echo "**** REBOOT ****" > $RamdiskPath/mqtt.log
	echo "**** REBOOT ****" > $RamdiskPath/ladestatus.log
	echo "**** REBOOT ****" > $RamdiskPath/soc.log
	echo "**** REBOOT ****" > $RamdiskPath/rfid.log
	echo "**** REBOOT ****" > $RamdiskPath/nurpv.log
	echo "**** REBOOT ****" > $RamdiskPath/cleanup.log
	echo "**** REBOOT ****" > $RamdiskPath/smarthome.log


	echo $bootmodus > $RamdiskPath/lademodus

	# Ladepunkte
	# Variablen noch nicht einheitlich benannt, daher individuelle Zeilen
	echo "nicht angefragt" > $RamdiskPath/evsedintestlp1
	echo "nicht angefragt" > $RamdiskPath/evsedintestlp2
	echo "nicht angefragt" > $RamdiskPath/evsedintestlp3
	echo 0 > $RamdiskPath/restzeitlp1m
	echo 0 > $RamdiskPath/restzeitlp2m
	echo 0 > $RamdiskPath/restzeitlp3m
	echo 0 > $RamdiskPath/aktgeladen
	echo 0 > $RamdiskPath/aktgeladens1
	echo 0 > $RamdiskPath/aktgeladens2
	echo 0 > $RamdiskPath/aktgeladenlp4
	echo 0 > $RamdiskPath/aktgeladenlp5
	echo 0 > $RamdiskPath/aktgeladenlp6
	echo 0 > $RamdiskPath/aktgeladenlp7
	echo 0 > $RamdiskPath/aktgeladenlp8
	echo 0 > $RamdiskPath/chargestat
	echo 0 > $RamdiskPath/chargestats1
	echo 0 > $RamdiskPath/chargestatlp3
	echo 0 > $RamdiskPath/chargestatlp4
	echo 0 > $RamdiskPath/chargestatlp5
	echo 0 > $RamdiskPath/chargestatlp6
	echo 0 > $RamdiskPath/chargestatlp7
	echo 0 > $RamdiskPath/chargestatlp8
	echo 0 > $RamdiskPath/ladestatus
	echo 0 > $RamdiskPath/ladestatuss1
	echo 0 > $RamdiskPath/ladestatuss2
	echo 0 > $RamdiskPath/ladestatuslp4
	echo 0 > $RamdiskPath/ladestatuslp5
	echo 0 > $RamdiskPath/ladestatuslp6
	echo 0 > $RamdiskPath/ladestatuslp7
	echo 0 > $RamdiskPath/ladestatuslp8
	echo 0 > $RamdiskPath/gelrlp1
	echo 0 > $RamdiskPath/gelrlp2
	echo 0 > $RamdiskPath/gelrlp3
	echo 0 > $RamdiskPath/ladeleistunglp4
	echo 0 > $RamdiskPath/ladeleistunglp5
	echo 0 > $RamdiskPath/ladeleistunglp6
	echo 0 > $RamdiskPath/ladeleistunglp7
	echo 0 > $RamdiskPath/ladeleistunglp8
	echo 0 > $RamdiskPath/ladungaktivlp1
	echo 0 > $RamdiskPath/ladungaktivlp2
	echo 0 > $RamdiskPath/ladungaktivlp3
	echo 0 > $RamdiskPath/lla1
	echo 0 > $RamdiskPath/llas11
	echo 0 > $RamdiskPath/llas21
	echo 0 > $RamdiskPath/lla1lp4
	echo 0 > $RamdiskPath/lla1lp5
	echo 0 > $RamdiskPath/lla1lp6
	echo 0 > $RamdiskPath/lla1lp7
	echo 0 > $RamdiskPath/lla1lp8
	echo 0 > $RamdiskPath/lla2
	echo 0 > $RamdiskPath/llas12
	echo 0 > $RamdiskPath/llas22
	echo 0 > $RamdiskPath/lla2lp4
	echo 0 > $RamdiskPath/lla2lp5
	echo 0 > $RamdiskPath/lla2lp6
	echo 0 > $RamdiskPath/lla2lp7
	echo 0 > $RamdiskPath/lla2lp8
	echo 0 > $RamdiskPath/lla3
	echo 0 > $RamdiskPath/llas13
	echo 0 > $RamdiskPath/llas23
	echo 0 > $RamdiskPath/lla3lp4
	echo 0 > $RamdiskPath/lla3lp5
	echo 0 > $RamdiskPath/lla3lp6
	echo 0 > $RamdiskPath/lla3lp7
	echo 0 > $RamdiskPath/lla3lp8
	echo 0 > $RamdiskPath/llkwh
	echo 0 > $RamdiskPath/llkwhs1
	echo 0 > $RamdiskPath/llkwhs2
	echo 0 > $RamdiskPath/llkwhlp4
	echo 0 > $RamdiskPath/llkwhlp5
	echo 0 > $RamdiskPath/llkwhlp6
	echo 0 > $RamdiskPath/llkwhlp7
	echo 0 > $RamdiskPath/llkwhlp8
	echo 0 > $RamdiskPath/llsoll
	echo 0 > $RamdiskPath/llsolls1
	echo 0 > $RamdiskPath/llsolls2
	echo 0 > $RamdiskPath/llsolllp4
	echo 0 > $RamdiskPath/llsolllp5
	echo 0 > $RamdiskPath/llsolllp6
	echo 0 > $RamdiskPath/llsolllp7
	echo 0 > $RamdiskPath/llsolllp8
	echo 0 > $RamdiskPath/llv1
	echo 0 > $RamdiskPath/llvs11
	echo 0 > $RamdiskPath/llvs21
	echo 0 > $RamdiskPath/llv1lp4
	echo 0 > $RamdiskPath/llv1lp5
	echo 0 > $RamdiskPath/llv1lp6
	echo 0 > $RamdiskPath/llv1lp7
	echo 0 > $RamdiskPath/llv1lp8
	echo 0 > $RamdiskPath/llv2
	echo 0 > $RamdiskPath/llvs12
	echo 0 > $RamdiskPath/llvs22
	echo 0 > $RamdiskPath/llv2lp4
	echo 0 > $RamdiskPath/llv2lp5
	echo 0 > $RamdiskPath/llv2lp6
	echo 0 > $RamdiskPath/llv2lp7
	echo 0 > $RamdiskPath/llv2lp8
	echo 0 > $RamdiskPath/llv3
	echo 0 > $RamdiskPath/llvs13
	echo 0 > $RamdiskPath/llvs23
	echo 0 > $RamdiskPath/llv3lp4
	echo 0 > $RamdiskPath/llv3lp5
	echo 0 > $RamdiskPath/llv3lp6
	echo 0 > $RamdiskPath/llv3lp7
	echo 0 > $RamdiskPath/llv3lp8
	echo 0 > $RamdiskPath/pluggedladungbishergeladen
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp2
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp3
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp4
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp5
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp6
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp7
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp8
	echo 0 > $RamdiskPath/plugstat
	echo 0 > $RamdiskPath/plugstats1
	echo 0 > $RamdiskPath/plugstatlp3
	echo 0 > $RamdiskPath/plugstatlp4
	echo 0 > $RamdiskPath/plugstatlp5
	echo 0 > $RamdiskPath/plugstatlp6
	echo 0 > $RamdiskPath/plugstatlp7
	echo 0 > $RamdiskPath/plugstatlp8
	echo 0 > $RamdiskPath/llaltnv
	echo 0 > $RamdiskPath/llhz
	echo 0 > $RamdiskPath/llkombiniert
	echo 0 > $RamdiskPath/llkwhges
	echo 0 > $RamdiskPath/llpf1
	echo 0 > $RamdiskPath/llpf2
	echo 0 > $RamdiskPath/llpf3
	echo 1 > $RamdiskPath/llaktuell
	echo 1 > $RamdiskPath/llaktuells1
	echo 1 > $RamdiskPath/llaktuells2
	echo 1 > $RamdiskPath/llaktuelllp4
	echo 1 > $RamdiskPath/llaktuelllp5
	echo 1 > $RamdiskPath/llaktuelllp6
	echo 1 > $RamdiskPath/llaktuelllp7
	echo 1 > $RamdiskPath/llaktuelllp8
	echo 0 > $RamdiskPath/nachtladen2state
	echo 0 > $RamdiskPath/nachtladen2states1
	echo 0 > $RamdiskPath/nachtladenstate
	echo 0 > $RamdiskPath/nachtladenstates1
	echo 0 > $RamdiskPath/pluggedtimer1
	echo 0 > $RamdiskPath/pluggedtimer2
	echo 0 > $RamdiskPath/progevsedinlp1
	echo 0 > $RamdiskPath/progevsedinlp12000
	echo 0 > $RamdiskPath/progevsedinlp12007
	echo 0 > $RamdiskPath/progevsedinlp2
	echo 0 > $RamdiskPath/progevsedinlp22000
	echo 0 > $RamdiskPath/progevsedinlp22007
	echo 0 > $RamdiskPath/cpulp1counter
	echo 0 > $RamdiskPath/soc
	echo 0 > $RamdiskPath/soc-live.graph
	echo 0 > $RamdiskPath/soc.graph
	echo 0 > $RamdiskPath/soc1
	echo 0 > $RamdiskPath/soc1vorhanden
	echo 0 > $RamdiskPath/tmpsoc
	echo 0 > $RamdiskPath/tmpsoc1
	echo 0 > $RamdiskPath/zielladenkorrektura
	echo 20000 > $RamdiskPath/soctimer
	echo 20000 > $RamdiskPath/soctimer1
	echo 28 > $RamdiskPath/evsemodbustimer
	touch $RamdiskPath/llog1
	touch $RamdiskPath/llogs1
	touch $RamdiskPath/llogs2

	# SmartHome 2.0
	echo 0 > $RamdiskPath/device1_temp0
	echo 0 > $RamdiskPath/device1_temp1
	echo 0 > $RamdiskPath/device1_temp2
	echo 0 > $RamdiskPath/device1_wh
	echo 0 > $RamdiskPath/device2_temp0
	echo 0 > $RamdiskPath/device2_temp1
	echo 0 > $RamdiskPath/device2_temp2
	echo 0 > $RamdiskPath/device2_wh
	echo 0 > $RamdiskPath/device3_wh
	echo 0 > $RamdiskPath/device4_wh
	echo 0 > $RamdiskPath/device5_wh
	echo 0 > $RamdiskPath/device6_wh
	echo 0 > $RamdiskPath/device7_wh
	echo 0 > $RamdiskPath/device8_wh
	echo 0 > $RamdiskPath/device9_wh
	echo 0 > $RamdiskPath/smarthome_device_manual_1
	echo 0 > $RamdiskPath/smarthome_device_manual_2
	echo 0 > $RamdiskPath/smarthome_device_manual_3
	echo 0 > $RamdiskPath/smarthome_device_manual_4
	echo 0 > $RamdiskPath/smarthome_device_manual_5
	echo 0 > $RamdiskPath/smarthome_device_manual_6
	echo 0 > $RamdiskPath/smarthome_device_manual_7
	echo 0 > $RamdiskPath/smarthome_device_manual_8
	echo 0 > $RamdiskPath/smarthome_device_manual_9

	# evu
	echo 0 > $RamdiskPath/bezuga1
	echo 0 > $RamdiskPath/bezuga2
	echo 0 > $RamdiskPath/bezuga3
	echo 0 > $RamdiskPath/bezugkwh
	echo 0 > $RamdiskPath/bezugw1
	echo 0 > $RamdiskPath/bezugw2
	echo 0 > $RamdiskPath/bezugw3
	echo 0 > $RamdiskPath/einspeisungkwh
	echo 0 > $RamdiskPath/evu-live.graph
	echo 0 > $RamdiskPath/evu.graph
	echo 0 > $RamdiskPath/evuhz
	echo 0 > $RamdiskPath/evupf1
	echo 0 > $RamdiskPath/evupf2
	echo 0 > $RamdiskPath/evupf3
	echo 0 > $RamdiskPath/evuv1
	echo 0 > $RamdiskPath/evuv2
	echo 0 > $RamdiskPath/evuv3
	echo 0 > $RamdiskPath/wattbezug

	# pv
	echo 0 > $RamdiskPath/daily_pvkwhk
	echo 0 > $RamdiskPath/daily_pvkwhk1
	echo 0 > $RamdiskPath/daily_pvkwhk2
	echo 0 > $RamdiskPath/monthly_pvkwhk
	echo 0 > $RamdiskPath/monthly_pvkwhk1
	echo 0 > $RamdiskPath/monthly_pvkwhk2
	echo 0 > $RamdiskPath/nurpv70dynstatus
	echo 0 > $RamdiskPath/pv-live.graph
	echo 0 > $RamdiskPath/pv.graph
	echo 0 > $RamdiskPath/pv1watt
	echo 0 > $RamdiskPath/pv2a1
	echo 0 > $RamdiskPath/pv2a2
	echo 0 > $RamdiskPath/pv2a3
	echo 0 > $RamdiskPath/pv2kwh
	echo 0 > $RamdiskPath/pv2watt
	echo 0 > $RamdiskPath/pv2watt
	echo 0 > $RamdiskPath/pvcounter
	echo 0 > $RamdiskPath/pvecounter
	echo 0 > $RamdiskPath/pvkwh
	echo 0 > $RamdiskPath/pvkwhk
	echo 0 > $RamdiskPath/pvkwhk1
	echo 0 > $RamdiskPath/pvkwhk2
	echo 0 > $RamdiskPath/pvvorhanden
	echo 0 > $RamdiskPath/pvwatt
	echo 0 > $RamdiskPath/pvwatt1
	echo 0 > $RamdiskPath/pvwatt2
	echo 0 > $RamdiskPath/yearly_pvkwhk
	echo 0 > $RamdiskPath/yearly_pvkwhk1
	echo 0 > $RamdiskPath/yearly_pvkwhk2

	# bat
	echo 0 > $RamdiskPath/speicher
	echo 0 > $RamdiskPath/speicherekwh
	echo 0 > $RamdiskPath/speicherikwh
	echo 0 > $RamdiskPath/speicherleistung
	echo 0 > $RamdiskPath/speicherleistung1
	echo 0 > $RamdiskPath/speicherleistung2
	echo 0 > $RamdiskPath/speichersoc
	echo 0 > $RamdiskPath/speichersoc2

	# temp mqtt
	echo 0 > $RamdiskPath/mqttdurchslp2
	echo 0 > $RamdiskPath/mqttdurchslp3
	echo 0 > $RamdiskPath/mqttgelrlp1
	echo 0 > $RamdiskPath/mqttgelrlp2
	echo 0 > $RamdiskPath/mqttgelrlp3
	echo 0 > $RamdiskPath/mqttladeleistunglp1
	echo 0 > $RamdiskPath/mqttladeleistungs1
	echo 0 > $RamdiskPath/mqttladeleistungs2
	echo 0 > $RamdiskPath/mqttlastchargestat
	echo 0 > $RamdiskPath/mqttlastchargestats1
	echo 0 > $RamdiskPath/mqttlastladestatus
	echo 0 > $RamdiskPath/mqttlastplugstat
	echo 0 > $RamdiskPath/mqttlastplugstats1
	echo 0 > $RamdiskPath/mqttpvvorhanden
	echo 1 > $RamdiskPath/mqttetprovidermaxprice
	echo 1 > $RamdiskPath/mqttetproviderprice
	echo 1 > $RamdiskPath/mqttlademkwhs1
	echo 1 > $RamdiskPath/mqttlademkwhs2
	echo 1 > $RamdiskPath/mqttllsolls1
	echo 1 > $RamdiskPath/mqttllsolls2
	echo 1 > $RamdiskPath/mqttsoc1
	echo 2 > $RamdiskPath/mqttspeicherleistung
	echo 2 > $RamdiskPath/mqttspeichervorhanden
	echo 3 > $RamdiskPath/mqttlastmanagement
	echo 3 > $RamdiskPath/mqttlastmanagements1
	echo 3 > $RamdiskPath/mqttlastmanagements2
	echo 3 > $RamdiskPath/mqttlastmanagementlp4
	echo 3 > $RamdiskPath/mqttlastmanagementlp5
	echo 3 > $RamdiskPath/mqttlastmanagementlp6
	echo 3 > $RamdiskPath/mqttlastmanagementlp7
	echo 3 > $RamdiskPath/mqttlastmanagementlp8
	echo 3 > $RamdiskPath/mqttspeichersoc

	# rfid
	echo $rfidlist > $RamdiskPath/rfidlist
	echo 0 > $RamdiskPath/mqttrfidlasttag
	echo 0 > $RamdiskPath/mqttrfidlp1
	echo 0 > $RamdiskPath/mqttrfidlp2
	echo 0 > $RamdiskPath/rfidlasttag
	echo 0 > $RamdiskPath/rfidlp1
	echo 0 > $RamdiskPath/rfidlp2
	echo 0 > $RamdiskPath/readtag

	# SmartHome 1.0
	echo 0 > $RamdiskPath/hook1akt
	echo 0 > $RamdiskPath/hook1einschaltverzcounter
	echo 0 > $RamdiskPath/hook2akt
	echo 0 > $RamdiskPath/hook2einschaltverzcounter
	echo 0 > $RamdiskPath/hook3akt
	echo $verbraucher1_name > $RamdiskPath/verbraucher1_name
	echo $verbraucher2_name > $RamdiskPath/verbraucher2_name
	echo 0 > $RamdiskPath/daily_verbraucher1ekwh
	echo 0 > $RamdiskPath/daily_verbraucher1ikwh
	echo 0 > $RamdiskPath/daily_verbraucher2ekwh
	echo 0 > $RamdiskPath/daily_verbraucher2ikwh
	echo 0 > $RamdiskPath/daily_verbraucher3ikwh
	echo 0 > $RamdiskPath/verbraucher1_watt
	echo 0 > $RamdiskPath/verbraucher1_wh
	echo 0 > $RamdiskPath/verbraucher1_whe
	echo 0 > $RamdiskPath/verbraucher1vorhanden
	echo 0 > $RamdiskPath/verbraucher2_watt
	echo 0 > $RamdiskPath/verbraucher2_wh
	echo 0 > $RamdiskPath/verbraucher2_whe
	echo 0 > $RamdiskPath/verbraucher2vorhanden
	echo 0 > $RamdiskPath/verbraucher3_watt
	echo 0 > $RamdiskPath/verbraucher3_wh
	echo 0 > $RamdiskPath/verbraucher3vorhanden

	# diverse Dateien
	echo 0 > $RamdiskPath/AllowedTotalCurrentPerPhase
	echo 0 > $RamdiskPath/ChargingVehiclesOnL1
	echo 0 > $RamdiskPath/ChargingVehiclesOnL2
	echo 0 > $RamdiskPath/ChargingVehiclesOnL3
	echo 0 > $RamdiskPath/TotalCurrentConsumptionOnL1
	echo 0 > $RamdiskPath/TotalCurrentConsumptionOnL2
	echo 0 > $RamdiskPath/TotalCurrentConsumptionOnL3
	echo 0 > $RamdiskPath/autolocktimer
	echo 0 > $RamdiskPath/blockall
	echo 0 > $RamdiskPath/date-live.graph
	echo 0 > $RamdiskPath/date.graph
	echo 0 > $RamdiskPath/devicetotal_watt
	echo 0 > $RamdiskPath/etprovidermaxprice
	echo 0 > $RamdiskPath/etproviderprice
	echo 0 > $RamdiskPath/ev-live.graph
	echo 0 > $RamdiskPath/ev.graph
	echo 0 > $RamdiskPath/evseausgelesen
	echo 0 > $RamdiskPath/glattwattbezug
	echo 0 > $RamdiskPath/hausverbrauch
	echo 0 > $RamdiskPath/ipaddress
	echo 0 > $RamdiskPath/ledstatus
	echo 0 > $RamdiskPath/netzschutz
	echo 0 > $RamdiskPath/randomSleepValue
	echo 0 > $RamdiskPath/renewmqtt
	echo 0 > $RamdiskPath/rseaktiv
	echo 0 > $RamdiskPath/rsestatus
	echo 0 > $RamdiskPath/schieflast
	echo 0 > $RamdiskPath/u1p3pstat
	echo 0 > $RamdiskPath/uhcounter
	echo 0 > $RamdiskPath/urcounter
	echo 1 > $RamdiskPath/anzahlphasen
	echo 1 > $RamdiskPath/bootinprogress
	echo 1 > $RamdiskPath/execdisplay
	echo 4 > $RamdiskPath/graphtimer

	# temporäre Zwischenspeicher für z. B. Kostal Plenticore, da
	# bei Anschluss von Speicher und Energiemanager direkt am WR
	# alle Werte im Modul des Wechselrichters aus den Registern
	# gelesen werden, um einen zeitlich zusammenhängenden Datensatz
	# zu bekommen. Im jeweiligen Modul Speicher/Bezug werden
	# die Werte dann in die ramdisk für die weitere globale
	# Verarbeitung geschrieben.
	# Bezug/Einspeisung
	echo 0 > $RamdiskPath/temp_wattbezug
	# Gesamte AC-Leistung des Speichers am WR 1 + 2
	echo 0 > $RamdiskPath/temp_peicherleistung
	# AC-Leistung des Speichers am WR 1
	echo 0 > $RamdiskPath/temp_peicherleistung1
	# AC-Leistung des Speichers am WR 2
	echo 0 > $RamdiskPath/temp_peicherleistung2
	# SoC des Speichers am WR 1
	echo 0 > $RamdiskPath/temp_speichersoc
	# Strom auf den jeweiligen Phasen
	echo 0 > $RamdiskPath/temp_bezuga1
	echo 0 > $RamdiskPath/temp_bezuga2
	echo 0 > $RamdiskPath/temp_bezuga3
	# Netzfrequenz
	echo 0 > $RamdiskPath/temp_evuhz
	# Leistung auf den jeweiligen Phasen
	echo 0 > $RamdiskPath/temp_bezugw1
	echo 0 > $RamdiskPath/temp_bezugw2
	echo 0 > $RamdiskPath/temp_bezugw3
	# Spannung auf den jeweiligen Phasen
	echo 0 > $RamdiskPath/temp_evuv1
	echo 0 > $RamdiskPath/temp_evuv2
	echo 0 > $RamdiskPath/temp_evuv3
	# Wirkfaktor, wird aus historischen Gründen je Phase geschrieben
	echo 0 > $RamdiskPath/temp_evupf1
	echo 0 > $RamdiskPath/temp_evupf2
	echo 0 > $RamdiskPath/temp_evupf3

	# init common files for lp1 to lp8
	# "<ramdiskFileName>:<MqttTopic>:<defaultValue>"
	# <Mqtt-Topic> is optional and request to broker will be skipped if empty
	for i in $(seq 1 8);
	do
		for f in \
			"pluggedladunglp${i}startkwh:openWB/lp/${i}/plugStartkWh:0" \
			"pluggedladungaktlp${i}:openWB/lp/${i}/pluggedladungakt:0" \
			"lp${i}phasen::0" \
			"lp${i}enabled::1" \
			"restzeitlp${i}::--" \
			"autolockstatuslp${i}::0" \
			"autolockconfiguredlp${i}::0" \
			"lp${i}sofortll::10" \
			"rfidlp${i}::0" \
			"boolstopchargeafterdisclp${i}::0" \
			"mqttzielladenaktivlp${i}::0" \
			"mqttmsmoduslp${i}::0" \
			"mqttlp${i}name::Lp${i}" \
			"mqttdisplaylp${i}max::22000" \
			"mqttautolockstatuslp${i}::0" \
			"mqttautolockconfiguredlp${i}::0"
		do
			IFS=':' read -r -a tuple <<< "$f"
			currentRamdiskFileVar="\"$RamdiskPath/${tuple[0]}\""
			eval currentRamdiskFile=\$$currentRamdiskFileVar
			if ! [ -f $currentRamdiskFile ]; then
				if [[ ! -z ${tuple[1]} ]]; then
					mqttValue=$(timeout 1 mosquitto_sub -C 1 -t ${tuple[1]})
					if [[ ! -z "$mqttValue" ]]; then
						echo "'$currentRamdiskFile' missing: Setting from MQTT topic '${tuple[0]}' to value '$mqttValue'"
						echo "$mqttValue" > $currentRamdiskFile
					else
						echo "'$currentRamdiskFile' missing: MQTT topic '${tuple[0]}' can also not provide any value: Setting to default of '${tuple[2]}'"
						echo ${tuple[2]} > $currentRamdiskFile
					fi
				else
					echo "'$currentRamdiskFile' missing: no MQTT topic set: Setting to default of '${tuple[2]}'"
					echo ${tuple[2]} > $currentRamdiskFile
				fi
			fi
		done
	done

	# init other files
	for f in \
		"mqttCp1Configured:1" \
		"mqttRandomSleepValue:0" \
		"mqttabschaltuberschuss:0" \
		"mqttabschaltverzoegerung:0" \
		"mqttadaptfaktor:0" \
		"mqttadaptpv:0" \
		"mqttaktgeladen:0" \
		"mqttaktgeladens1:0" \
		"mqttaktgeladens2:0" \
		"mqttdailychargelp1:0" \
		"mqttdailychargelp2:0" \
		"mqttdailychargelp3:0" \
		"mqttdatenschutzack:0" \
		"mqttdisplayevumax:10000" \
		"mqttdisplayhausanzeigen:1" \
		"mqttdisplayhausmax:11000" \
		"mqttdisplaypvmax:10000" \
		"mqttdisplayspeichermax:5000" \
		"mqttdurchslp1:17" \
		"mqtteinschaltverzoegerung:0" \
		"mqttetprovideraktiv:0" \
		"mqttevuglaettungakt:0" \
		"mqtthausverbrauch:0" \
		"mqtthausverbrauchstat:1" \
		"mqttheutegeladen:1" \
		"mqtthook1_aktiv:0" \
		"mqtthook2_aktiv:0" \
		"mqtthook3_aktiv:0" \
		"mqttlademkwh:0" \
		"mqttlademkwhlp4:0" \
		"mqttlademkwhlp5:0" \
		"mqttlademkwhlp6:0" \
		"mqttlademkwhlp7:0" \
		"mqttlademkwhlp8:0" \
		"mqttlademstat:0" \
		"mqttlademstatlp4:0" \
		"mqttlademstatlp5:0" \
		"mqttlademstatlp6:0" \
		"mqttlademstatlp7:0" \
		"mqttlademstatlp8:0" \
		"mqttlademstats1:0" \
		"mqttlademstats2:0" \
		"mqttlastlademodus:3" \
		"mqttmaximalstromstaerke:32" \
		"mqttmaxnurpvsoclp1:100" \
		"mqttmindestuberschuss:0" \
		"mqttminimalalp2pv:6" \
		"mqttminimalampv:6" \
		"mqttminimalapv:6" \
		"mqttminimalstromstaerke:6" \
		"mqttminnurpvsocll:6" \
		"mqttminnurpvsoclp1:0" \
		"mqttnachtladen:0" \
		"mqttnachtladens1:0" \
		"mqttnlakt_minpv:0" \
		"mqttnlakt_nurpv:0" \
		"mqttnlakt_sofort:0" \
		"mqttnlakt_standby:0" \
		"mqttnurpv70dynact:0" \
		"mqttnurpv70dynw:0" \
		"mqttoffsetpv:0" \
		"mqttpreisjekwh:0.30" \
		"mqttpvbezugeinspeisung:0" \
		"mqttpvwatt:0" \
		"mqttrestzeitlp1:0" \
		"mqttrestzeitlp2:0" \
		"mqttrestzeitlp3:0" \
		"mqttrfidakt:0" \
		"mqttsoc1vorhanden:0" \
		"mqttsoc:0" \
		"mqttsocvorhanden:0" \
		"mqttsofortsoclp1:100" \
		"mqttsofortsoclp2:100" \
		"mqttsofortsocstatlp1:100" \
		"mqttsofortsocstatlp2:100" \
		"mqttspeichermaxwatt:0" \
		"mqttspeicherpveinbeziehen:0" \
		"mqttspeicherpvui:1" \
		"mqttspeichersochystminpv:0" \
		"mqttspeichersocminpv:0" \
		"mqttspeichersocnurpv:0" \
		"mqttspeicherwattnurpv:0" \
		"mqttstopchargepvatpercentlp1:100" \
		"mqttstopchargepvatpercentlp2:100" \
		"mqttstopchargepvpercentagelp1:100" \
		"mqttstopchargepvpercentagelp2:100" \
		"mqttu1p3paktiv:0" \
		"mqttu1p3pminundpv:0" \
		"mqttu1p3pnl:0" \
		"mqttu1p3pnurpv:0" \
		"mqttu1p3psofort:0" \
		"mqttu1p3pstandby:0" \
		"mqttupdateinprogress:0" \
		"mqttverbraucher1_aktiv:0" \
		"mqttverbraucher1_name:Verbraucher 1" \
		"mqttverbraucher2_aktiv:0" \
		"mqttverbraucher2_name:Verbraucher 2" \
		"mqttversion:0" \
		"mqttwattbezug:0" \
		"mqttwizzarddone:0"
	do
		IFS=':' read -r -a tuple <<< "$f"
		currentRamdiskFileVar="\"$RamdiskPath/${tuple[0]}\""
		eval currentRamdiskFile=\$$currentRamdiskFileVar
		if ! [ -f $currentRamdiskFile ]; then
			if [[ ! -z "${tuple[1]}" ]]; then
				echo "'${tuple[0]}' missing: Setting to provided default value '${tuple[1]}'"
				echo "${tuple[1]}" > $currentRamdiskFile
			else
				echo "'${tuple[0]}' missing: No default value provided. Setting to 0."
				echo 0 > $currentRamdiskFile
			fi
		fi
	done

	sudo chmod 777 $RamdiskPath/*

	echo "Ramdisk init done."
}
