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

log() {
	echo "[wr_solarview] $*" >>"$target/openWB.log"
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
	# Format:   {WR,Tag,Monat,Jahr,Stunde,Minute,KDY,KMT,KYR,KT0,PAC,UDC,IDC,UDCB,IDCB,UDCC,IDCC,UDCD,IDCD,UL1,IL1,UL2,IL2,UL3,IL3,TKK},Checksum
	# Beispiel: {01,09,09,2019,08,18,0000.0,00082,002617,00018691,00104,451,000.2,000,000.0,000,000.0,000,000.0,226,000.4,000,000.0,000,000.0,00},▒
	#
	# Bedeutung (siehe SolarView-Dokumentation):
	#  KDY= Tagesertrag (kWh)
	#  KMT= Monatsertrag (kWh)
	#  KYR= Jahresertrag (kWh)
	#  KT0= Gesamtertrag (kWh)
	#  PAC= Generatorleistung in W
	#  UDC, UDCB, UDCC, UDCD= Generator-Spannungen in Volt pro MPP-Tracker
	#  IDC, IDCB, IDCC, IDCD= Generator-Ströme in Ampere pro MPP-Tracker
	#  UL1, IL1= Netzspannung, Netzstrom Phase 1
	#  UL2, IL2= Netzspannung, Netzstrom Phase 2
	#  UL3, IL3= Netzspannung, Netzstrom Phase 3
	#  TKK= Temperatur Wechselrichter

	# Geschweifte Klammern und Checksumme entfernen
	values="${response#*\{}"
	values="${values%\}*}"

	# Werte auslesen und verarbeiten
	local LANG=C
	echo "$values" | while IFS=',' read -r WR Tag Monat Jahr Stunde Minute KDY KMT KYR KT0 PAC UDC IDC UDCB IDCB UDCC IDCC UDCD IDCD UL1 IL1 UL2 IL2 UL3 IL3 TKK
	do
		# Werte formatiert in Variablen speichern
		id="$WR"
		timestamp="$Jahr-$Monat-$Tag $Stunde:$Minute"
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
		grid1_voltage=$(      printf "%.0f" "$UL1")
		grid1_current=$(      printf "%.1f" "$IL1")
		grid2_voltage=$(      printf "%.0f" "$UL2")
		grid2_current=$(      printf "%.1f" "$IL2")
		grid3_voltage=$(      printf "%.0f" "$UL3")
		grid3_current=$(      printf "%.1f" "$IL3")
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
			log "Netz:"
			log "  Phase 1:"
			log "    Spannung: $grid1_voltage V"
			log "    Strom:    $grid1_current A"
			log "  Phase 2:"
			log "    Spannung: $grid2_voltage V"
			log "    Strom:    $grid2_current A"
			log "  Phase 3:"
			log "    Spannung: $grid3_voltage V"
			log "    Strom:    $grid3_current A"
		fi

		# Werte speichern
		echo "$power"        >"$target/pvwatt"
		echo "$energy_total" >"$target/pvkwh"
		echo "$energy_day"   >"$target/daily_pvkwh"
		echo "$energy_month" >"$target/monthly_pvkwh"
		echo "$energy_year"  >"$target/yearly_pvkwh"

		# Aktuelle Leistung an der Aufrufer zurückliefern
		echo "$power"
	done
}

# Sende-Kommando (siehe SolarView-Dokumentation); Beispiele:
# '00*': Gesamte Anlage
# '01*': Wechselrichter 1
# '02*': Wechselrichter 2
command="${1:-00*}"

power=$(request "$command")
echo "$power"
