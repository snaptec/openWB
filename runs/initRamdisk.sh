#!/bin/bash
# Ramdisk mit initialen Werten befüllen nach Neustart

initRamdisk(){
	RamdiskPath="/var/www/html/openWB/ramdisk"
	echo "Initializing Ramdisk $RamdiskPath"

	# Logfiles erstellen
	if [[ ! -L $RamdiskPath/openWB.log ]]; then
		ln -s /var/log/openWB.log $RamdiskPath/openWB.log
	fi
	echo "**** REBOOT ****" >> $RamdiskPath/mqtt.log
	echo "**** REBOOT ****" >> $RamdiskPath/ladestatus.log
	echo "**** REBOOT ****" >> $RamdiskPath/soc.log
	echo "**** REBOOT ****" >> $RamdiskPath/rfid.log
	echo "**** REBOOT ****" >> $RamdiskPath/nurpv.log
	echo "**** REBOOT ****" >> $RamdiskPath/cleanup.log
	echo "**** REBOOT ****" >> $RamdiskPath/smarthome.log
	echo "**** REBOOT ****" >> $RamdiskPath/isss.log

	echo "$bootmodus" > $RamdiskPath/lademodus

	# Ladepunkte
	# Variablen noch nicht einheitlich benannt, daher individuelle Zeilen
	echo 0 > $RamdiskPath/errcounterextopenwb
	echo 0 > $RamdiskPath/pluggedin
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
	echo 0 > $RamdiskPath/ladestart
	echo 0 > $RamdiskPath/ladestarts1
	echo 0 > $RamdiskPath/ladestarts2
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
	echo 0 > $RamdiskPath/pluggedladungbishergeladenlp1
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
	echo 0 > $RamdiskPath/llaktuell
	echo 0 > $RamdiskPath/llaktuells1
	echo 0 > $RamdiskPath/llaktuells2
	echo 0 > $RamdiskPath/llaktuelllp4
	echo 0 > $RamdiskPath/llaktuelllp5
	echo 0 > $RamdiskPath/llaktuelllp6
	echo 0 > $RamdiskPath/llaktuelllp7
	echo 0 > $RamdiskPath/llaktuelllp8
	echo 0 > $RamdiskPath/nachtladen2state
	echo 0 > $RamdiskPath/nachtladen2states1
	echo 0 > $RamdiskPath/nachtladenstate
	echo 0 > $RamdiskPath/nachtladenstates1
	echo 0 > $RamdiskPath/pluggedtimerlp1
	echo 0 > $RamdiskPath/pluggedtimerlp2
	echo 0 > $RamdiskPath/pluggedtimerlp3
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
	echo 0 > $RamdiskPath/ladungdurchziel
	echo 0 > $RamdiskPath/extcpulp1
	echo 20000 > $RamdiskPath/soctimer
	echo 20000 > $RamdiskPath/soctimer1
	echo 28 > $RamdiskPath/evsemodbustimer
	touch $RamdiskPath/llog
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
	echo 0 > $RamdiskPath/smarthome_device_minhaus_1
	echo 0 > $RamdiskPath/smarthome_device_minhaus_2
	echo 0 > $RamdiskPath/smarthome_device_minhaus_3
	echo 0 > $RamdiskPath/smarthome_device_minhaus_4
	echo 0 > $RamdiskPath/smarthome_device_minhaus_5
	echo 0 > $RamdiskPath/smarthome_device_minhaus_6
	echo 0 > $RamdiskPath/smarthome_device_minhaus_7
	echo 0 > $RamdiskPath/smarthome_device_minhaus_8
	echo 0 > $RamdiskPath/smarthome_device_minhaus_9
	echo 0 > $RamdiskPath/smarthome_device_manual_1
	echo 0 > $RamdiskPath/smarthome_device_manual_2
	echo 0 > $RamdiskPath/smarthome_device_manual_3
	echo 0 > $RamdiskPath/smarthome_device_manual_4
	echo 0 > $RamdiskPath/smarthome_device_manual_5
	echo 0 > $RamdiskPath/smarthome_device_manual_6
	echo 0 > $RamdiskPath/smarthome_device_manual_7
	echo 0 > $RamdiskPath/smarthome_device_manual_8
	echo 0 > $RamdiskPath/smarthome_device_manual_9
	echo 0 > $RamdiskPath/smarthome_device_manual_control_1
	echo 0 > $RamdiskPath/smarthome_device_manual_control_2
	echo 0 > $RamdiskPath/smarthome_device_manual_control_3
	echo 0 > $RamdiskPath/smarthome_device_manual_control_4
	echo 0 > $RamdiskPath/smarthome_device_manual_control_5
	echo 0 > $RamdiskPath/smarthome_device_manual_control_6
	echo 0 > $RamdiskPath/smarthome_device_manual_control_7
	echo 0 > $RamdiskPath/smarthome_device_manual_control_8
	echo 0 > $RamdiskPath/smarthome_device_manual_control_9
	echo 0 > $RamdiskPath/smarthomehandlermaxbatterypower
	echo 0 > $RamdiskPath/smarthomehandlerloglevel

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
	echo 0 > $RamdiskPath/pvcounter
	echo 0 > $RamdiskPath/pvecounter
	echo 0 > $RamdiskPath/pvkwh
	echo 0 > $RamdiskPath/pvkwhk
	echo 0 > $RamdiskPath/pvkwhk1
	echo 0 > $RamdiskPath/pvkwhk2
	echo 0 > $RamdiskPath/pv1vorhanden
	echo 0 > $RamdiskPath/pv2vorhanden
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
	echo -1 > $RamdiskPath/mqttdurchslp2
	echo -1 > $RamdiskPath/mqttdurchslp3
	echo -1 > $RamdiskPath/mqttgelrlp1
	echo -1 > $RamdiskPath/mqttgelrlp2
	echo -1 > $RamdiskPath/mqttgelrlp3
	echo -1 > $RamdiskPath/mqttladeleistunglp1
	echo -1 > $RamdiskPath/mqttladeleistungs1
	echo -1 > $RamdiskPath/mqttladeleistungs2
	echo -1 > $RamdiskPath/mqttlastchargestat
	echo -1 > $RamdiskPath/mqttlastchargestats1
	echo -1 > $RamdiskPath/mqttlastladestatus
	echo -1 > $RamdiskPath/mqttlastplugstat
	echo -1 > $RamdiskPath/mqttlastplugstats1
	echo -1 > $RamdiskPath/mqttpv1vorhanden
	echo -1 > $RamdiskPath/mqttpv2vorhanden
	echo -1 > $RamdiskPath/mqttetprovidermaxprice
	echo -1 > $RamdiskPath/mqttetproviderprice
	echo -1 > $RamdiskPath/mqttlademkwhs1
	echo -1 > $RamdiskPath/mqttlademkwhs2
	echo -1 > $RamdiskPath/mqttllsolls1
	echo -1 > $RamdiskPath/mqttllsolls2
	echo -1 > $RamdiskPath/mqttsoc1
	echo -1 > $RamdiskPath/mqttspeicherleistung
	echo -1 > $RamdiskPath/mqttspeichervorhanden
	echo -1 > $RamdiskPath/mqttlastmanagement
	echo -1 > $RamdiskPath/mqttlastmanagements1
	echo -1 > $RamdiskPath/mqttlastmanagements2
	echo -1 > $RamdiskPath/mqttlastmanagementlp4
	echo -1 > $RamdiskPath/mqttlastmanagementlp5
	echo -1 > $RamdiskPath/mqttlastmanagementlp6
	echo -1 > $RamdiskPath/mqttlastmanagementlp7
	echo -1 > $RamdiskPath/mqttlastmanagementlp8
	echo -1 > $RamdiskPath/mqttspeichersoc
	echo -1 > $RamdiskPath/mqttrfidlasttag
	echo -1 > $RamdiskPath/mqttrfidlp1
	echo -1 > $RamdiskPath/mqttrfidlp2

	# rfid
	echo "$rfidlist" > $RamdiskPath/rfidlist
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
	echo "$verbraucher1_name" > $RamdiskPath/verbraucher1_name
	echo "$verbraucher2_name" > $RamdiskPath/verbraucher2_name
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
	touch $RamdiskPath/ladestophooklp1aktiv # benötigt damit der Ladestopp-WebHook nicht beim Neustart auslöst
	touch $RamdiskPath/abgesteckthooklp1aktiv # benötigt damit der Abgesteckt-WebHook nicht beim Neustart auslöst

	# standard socket
	echo 0 > $RamdiskPath/socketa
	echo 0 > $RamdiskPath/socketv
	echo 0 > $RamdiskPath/socketp
	echo 0 > $RamdiskPath/socketpf
	echo 0 > $RamdiskPath/socketkwh
	echo 0 > $RamdiskPath/socketApproved
	echo 0 > $RamdiskPath/socketActivated
	echo 0 > $RamdiskPath/socketActivationRequested
	echo "unknown" > $RamdiskPath/isss_mode
	
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
	touch $RamdiskPath/etprovidergraphlist
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
			"restzeitlp${i}::0" \
			"autolockstatuslp${i}::0" \
			"autolockconfiguredlp${i}::0" \
			"lp${i}sofortll:openWB/config/get/sofort/lp/${i}/current:10" \
			"rfidlp${i}::0" \
			"boolstopchargeafterdisclp${i}::0" \
			"mqttstopchargeafterdisclp${i}::-1" \
			"mqttzielladenaktivlp${i}::-1" \
			"mqttmsmoduslp${i}::-1" \
			"mqttlp${i}name::Lp${i}" \
			"mqttdisplaylp${i}max::-1" \
			"mqttautolockstatuslp${i}::-1" \
			"mqttautolockconfiguredlp${i}::-1"
		do
			IFS=':' read -r -a tuple <<< "$f"
			currentRamdiskFile="$RamdiskPath/${tuple[0]}"
			if ! [ -f "$currentRamdiskFile" ]; then
				if [[ -n ${tuple[1]} ]]; then
					mqttValue=$(timeout 1 mosquitto_sub -C 1 -t "${tuple[1]}")
					if [[ -n "$mqttValue" ]]; then
						echo "'$currentRamdiskFile' missing: Setting from MQTT topic '${tuple[0]}' to value '$mqttValue'"
						echo "$mqttValue" > "$currentRamdiskFile"
					else
						echo "'$currentRamdiskFile' missing: MQTT topic '${tuple[0]}' can also not provide any value: Setting to default of '${tuple[2]}'"
						echo "${tuple[2]}" > "$currentRamdiskFile"
					fi
				else
					echo "'$currentRamdiskFile' missing: no MQTT topic set: Setting to default of '${tuple[2]}'"
					echo "${tuple[2]}" > "$currentRamdiskFile"
				fi
			fi
		done
	done

	# init other files
	for f in \
		"mqttCp1Configured:-1" \
		"mqttRandomSleepValue:-1" \
		"mqttabschaltuberschuss:-1" \
		"mqttabschaltverzoegerung:-1" \
		"mqttadaptfaktor:-1" \
		"mqttadaptpv:-1" \
		"mqttaktgeladen:-1" \
		"mqttaktgeladens1:-1" \
		"mqttaktgeladens2:-1" \
		"mqttdailychargelp1:-1" \
		"mqttdailychargelp2:-1" \
		"mqttdailychargelp3:-1" \
		"mqttdatenschutzack:-1" \
		"mqttdisplayevumax:-1" \
		"mqttdisplayhausanzeigen:-1" \
		"mqttdisplayhausmax:-1" \
		"mqttdisplaypvmax:-1" \
		"mqttdisplayspeichermax:-1" \
		"mqttdurchslp1:-1" \
		"mqtteinschaltverzoegerung:-1" \
		"mqttetprovideraktiv:-1" \
		"mqttetprovider:notset" \
		"mqttlp1etbasedcharging:-1" \
		"mqttlp2etbasedcharging:-1" \
		"mqttlp3etbasedcharging:-1" \
		"mqttlp4etbasedcharging:-1" \
		"mqttlp5etbasedcharging:-1" \
		"mqttlp6etbasedcharging:-1" \
		"mqttlp7etbasedcharging:-1" \
		"mqttlp8etbasedcharging:-1" \
		"mqttevuglaettungakt:-1" \
		"mqtthausverbrauch:-1" \
		"mqtthausverbrauchstat:-1" \
		"mqttheutegeladen:-1" \
		"mqtthook1_aktiv:-1" \
		"mqtthook2_aktiv:-1" \
		"mqtthook3_aktiv:-1" \
		"mqttlademkwh:-1" \
		"mqttlademkwhlp4:-1" \
		"mqttlademkwhlp5:-1" \
		"mqttlademkwhlp6:-1" \
		"mqttlademkwhlp7:-1" \
		"mqttlademkwhlp8:-1" \
		"mqttlademstat:-1" \
		"mqttlademstatlp4:-1" \
		"mqttlademstatlp5:-1" \
		"mqttlademstatlp6:-1" \
		"mqttlademstatlp7:-1" \
		"mqttlademstatlp8:-1" \
		"mqttlademstats1:-1" \
		"mqttlademstats2:-1" \
		"mqttlastlademodus:-1" \
		"mqttmaximalstromstaerke:-1" \
		"mqttmaxnurpvsoclp1:-1" \
		"mqttmindestuberschuss:-1" \
		"mqttminimalalp2pv:-1" \
		"mqttminimalampv:-1" \
		"mqttminimalapv:-1" \
		"mqttminimalstromstaerke:-1" \
		"mqttminnurpvsocll:-1" \
		"mqttminnurpvsoclp1:-1" \
		"mqttnachtladen:-1" \
		"mqttnachtladens1:-1" \
		"mqttnlakt_minpv:-1" \
		"mqttnlakt_nurpv:-1" \
		"mqttnlakt_sofort:-1" \
		"mqttnlakt_standby:-1" \
		"mqttnurpv70dynact:-1" \
		"mqttnurpv70dynw:-1" \
		"mqttoffsetpv:-1" \
		"mqttpreisjekwh:-1" \
		"mqttpvbezugeinspeisung:-1" \
		"mqttpvwatt:-1" \
		"mqttrestzeitlp1:-1" \
		"mqttrestzeitlp2:-1" \
		"mqttrestzeitlp3:-1" \
		"mqttrfidakt:-1" \
		"mqttsoc1vorhanden:-1" \
		"mqttsoc:-1" \
		"mqttsocvorhanden:-1" \
		"mqttsofortsoclp1:-1" \
		"mqttsofortsoclp2:-1" \
		"mqttsofortsocstatlp1:-1" \
		"mqttsofortsocstatlp2:-1" \
		"mqttspeichermaxwatt:-1" \
		"mqttspeicherpveinbeziehen:-1" \
		"mqttspeicherpvui:-1" \
		"mqttspeichersochystminpv:-1" \
		"mqttspeichersocminpv:-1" \
		"mqttspeichersocnurpv:-1" \
		"mqttspeicherwattnurpv:-1" \
		"mqttstopchargepvatpercentlp1:-1" \
		"mqttstopchargepvatpercentlp2:-1" \
		"mqttstopchargepvpercentagelp1:-1" \
		"mqttstopchargepvpercentagelp2:-1" \
		"mqttu1p3paktiv:-1" \
		"mqttu1p3pminundpv:-1" \
		"mqttu1p3pnl:-1" \
		"mqttu1p3pnurpv:-1" \
		"mqttu1p3psofort:-1" \
		"mqttu1p3pstandby:-1" \
		"mqttupdateinprogress:-1" \
		"mqttverbraucher1_aktiv:-1" \
		"mqttverbraucher1_name:notset" \
		"mqttverbraucher2_aktiv:-1" \
		"mqttverbraucher2_name:notset" \
		"mqttversion:-1" \
		"mqttwattbezug:-1" \
		"mqttwizzarddone:-1"
	do
		IFS=':' read -r -a tuple <<< "$f"
		currentRamdiskFile="$RamdiskPath/${tuple[0]}"
		if ! [ -f "$currentRamdiskFile" ]; then
			if [[ -n "${tuple[1]}" ]]; then
				echo "'${tuple[0]}' missing: Setting to provided default value '${tuple[1]}'"
				echo "${tuple[1]}" > "$currentRamdiskFile"
			else
				echo "'${tuple[0]}' missing: No default value provided. Setting to 0."
				echo 0 > "$currentRamdiskFile"
			fi
		fi
	done

	# read values from mosquitto and store them to ramdisk for smarthomehandler.py
	ra='^-?[0-9]+$'
	importtemp=$(timeout 1 mosquitto_sub -t openWB/config/get/SmartHome/maxBatteryPower)
	if ! [[ $importtemp =~ $ra ]] ; then
		importtemp="0"
	fi
	echo $importtemp > $RamdiskPath/smarthomehandlermaxbatterypower

	sudo chmod 777 $RamdiskPath/*

	echo "Trigger update of logfiles..."
	python3 /var/www/html/openWB/runs/csvcalc.py --input /var/www/html/openWB/web/logging/data/daily/ --output /var/www/html/openWB/web/logging/data/v001/ --partial /var/www/html/openWB/ramdisk/ --mode M >> /var/www/html/openWB/ramdisk/csvcalc.log 2>&1 &
	echo "Ramdisk init done."
}
