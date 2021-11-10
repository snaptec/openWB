#!/bin/sh

#
# OpenWB-Modul für die Anbindung von SolarView über den integrierten TCP-Server
# Details zur API: https://solarview.info/solarview-fb_Installieren.pdf
#

openwb_home=/var/www/html/openWB
target="$openwb_home/ramdisk"

# Checks
if [ -z "$solarview_hostname" ]; then
	log "Missing required variable 'solarview_hostname'"
	return 1
fi
if [ "${solarview_port}" ]; then
	if [ "$solarview_port" -lt 1 ] || [ "$solarview_port" -gt 65535 ]; then
		log "Invalid value '$solarview_port' for variable 'solarview_port'"
		return 1
	fi
fi

command_bezug='22*'
command_einspeisung='21*'

log() {
	echo "[bezug_solarview] $*" >>"$target/openWB.log"
}

request() {
	command="$1"
	port="${solarview_port:-15000}"
	timeout="${solarview_timeout:-1}"

	response=$(echo "$command" | nc -w "$timeout" "$solarview_hostname" "$port")
	return_code="$?"
	if [ "$return_code" -ne 0 ]; then
		log "Error: request to SolarView failed. Details: return-code: '$return_code', host: '$solarview_hostname', port: '$port', timeout: '$timeout'"
		return "$return_code"
	fi

	[ "$debug" -ne 0 ] && log "Raw response: $response"
	#
	# Format:    {WR,Tag,Monat,Jahr,Stunde,Minute,KDY,KMT,KYR,KT0,PAC,UDC,IDC,UDCB,IDCB,UDCC,IDCC,UDCD,IDCD,TKK},Checksum
	# Beispiele: {22,09,09,2019,10,37,0001.2,00024,000903,00007817,01365,000,000.0,000,000.0,000,000.0,000,000.0,00},:
	#            {21,09,09,2019,10,37,0002.3,00141,004233,00029525,01365,000,000.0,000,000.0,000,000.0,000,000.0,00},;
	#
	# Bedeutung (siehe SolarView-Dokumentation):
	#  KDY= Tagesertrag (kWh)
	#  KMT= Monatsertrag (kWh)
	#  KYR= Jahresertrag (kWh)
	#  KT0= Gesamtertrag (kWh)
	#  PAC= Generatorleistung in W
	#  UDC, UDCB, UDCC, UDCD= Generator-Spannungen in Volt pro MPP-Tracker
	#  IDC, IDCB, IDCC, IDCD= Generator-Ströme in Ampere pro MPP-Tracker
	#  TKK= Temperatur Wechselrichter

	# Geschweifte Klammern und Checksumme entfernen
	values="${response#*\{}"
	values="${values%\}*}"

	# Werte auslesen und verarbeiten
	local LANG=C
	echo "$values" | while IFS=',' read -r WR Tag Monat Jahr Stunde Minute KDY KMT KYR KT0 PAC UDC IDC UDCB IDCB UDCC IDCC UDCD IDCD TKK
	do
		# Werte formatiert in Variablen speichern
		id="$WR"
		timestamp="$Jahr-$Monat-$Tag $Stunde:$Minute"
		#  PAC = '-0357' bedeutet: 357 W Bezug, 0 W Einspeisung
		#  PAC =  '0246' bedeutet: 0 W Bezug, 246 W Einspeisung
		power=$(       awk "BEGIN{print   -1 * $PAC}")
		energy_day=$(  awk "BEGIN{print 1000 * $KDY}")
		energy_month=$(awk "BEGIN{print 1000 * $KMT}")
		energy_year=$( awk "BEGIN{print 1000 * $KYR}")
		energy_total=$(awk "BEGIN{print 1000 * $KT0}")
		mpptracker1_voltage=$(printf "%.0f" "$UDC")
		mpptracker1_current=$(printf "%.1f" "$IDC")
		mpptracker2_voltage=$(printf "%.0f" "$UDCB")
		mpptracker2_current=$(printf "%.1f" "$IDCB")
		mpptracker3_voltage=$(printf "%.0f" "$UDCC")
		mpptracker3_current=$(printf "%.1f" "$IDCC")
		mpptracker4_voltage=$(printf "%.0f" "$UDCD")
		mpptracker4_current=$(printf "%.1f" "$IDCD")
		temperature=$(        printf "%.0f" "$TKK")

		if [ "$debug" -ne 0 ]; then
			# Werte ausgeben
			log "ID: $id"
			log "Zeitpunkt: $timestamp"
			log "Temperatur: $temperature °C"
			log "Leistung: $power W"
			log "Energie:"
			log "  Tag:    $energy_day Wh"
			log "  Monat:  $energy_month Wh"
			log "  Jahr:   $energy_year Wh"
			log "  Gesamt: $energy_total Wh"
			log "Generator-MPP-Tracker-1"
			log "  Spannung: $mpptracker1_voltage V"
			log "  Strom:    $mpptracker1_current A"
			log "Generator-MPP-Tracker-2"
			log "  Spannung: $mpptracker2_voltage V"
			log "  Strom:    $mpptracker2_current A"
			log "Generator-MPP-Tracker-3"
			log "  Spannung: $mpptracker3_voltage V"
			log "  Strom:    $mpptracker3_current A"
			log "Generator-MPP-Tracker-4"
			log "  Spannung: $mpptracker4_voltage V"
			log "  Strom:    $mpptracker4_current A"
		fi

		# Werte speichern
		if [ "$command" = "$command_einspeisung" ]; then
			echo "$energy_total"  >"$target/einspeisungkwh"
		elif [ "$command" = "$command_bezug" ]; then
			echo "$power"         >"$target/wattbezug"
			echo "$energy_total"  >"$target/bezugkwh"
			echo "$grid1_current" >"$target/bezuga1"
			echo "$grid2_current" >"$target/bezuga2"
			echo "$grid3_current" >"$target/bezuga3"
			echo "$grid1_voltage" >"$target/evuv1"
			echo "$grid2_voltage" >"$target/evuv2"
			echo "$grid3_voltage" >"$target/evuv3"
		fi

		# Aktuelle Leistung an der Aufrufer zurückliefern
		echo "$power"
	done
}

request "$command_einspeisung" >/dev/null
power=$(request "$command_bezug")

echo "$power"
