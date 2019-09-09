#!/bin/sh

#
# OpenWB-Modul für die Anbindung von SolarView über den integrierten TCP-Server
# Details zur API: https://solarview.info/solarview-fb_Installieren.pdf
#

openwb_home=/var/www/html/openWB
target="$openwb_home/ramdisk"

. "$openwb_home/openwb.conf"

# Checks
if [ -z "$solarview_hostname" ]; then
  >&2 echo "Missing required variable 'solarview_hostname'"
  return 1
fi
if [ "${solarview_port}" ]; then
  if [ "$solarview_port" -lt 1 ] || [ "$solarview_port" -gt 65535 ]; then
    >&2 echo "Invalid value '$solarview_port' for variable 'solarview_port'"
    return 1
  fi
fi

command_bezug='22*'
command_einspeisung='21*'

request() {
  command="$1"
  port="${solarview_port:-15000}"
  timeout="${solarview_timeout:-1}"

  response=$(echo "$command" | nc -w "$timeout" "$solarview_hostname" "$port")
  return_code="$?"
  if [ "$return_code" -ne 0 ]; then
    >&2 echo "Error: request to SolarView failed. Details: return-code: '$return_code', host: '$solarview_hostname', port: '$port', timeout: '$timeout'"
    return "$return_code"
  fi

  [ "$debug" -ne 0 ] && >&2 echo "Raw response: $response"
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
      >&2 echo "ID: $id"
      >&2 echo "Zeitpunkt: $timestamp"
      >&2 echo "Temperatur: $temperature °C"
      >&2 echo "Leistung: $power W"
      >&2 echo "Energie:"
      >&2 echo "  Tag:    $energy_day Wh"
      >&2 echo "  Monat:  $energy_month Wh"
      >&2 echo "  Jahr:   $energy_year Wh"
      >&2 echo "  Gesamt: $energy_total Wh"
      >&2 echo "Generator-MPP-Tracker-1"
      >&2 echo "  Spannung: $mpptracker1_voltage V"
      >&2 echo "  Strom:    $mpptracker1_current A"
      >&2 echo "Generator-MPP-Tracker-2"
      >&2 echo "  Spannung: $mpptracker2_voltage V"
      >&2 echo "  Strom:    $mpptracker2_current A"
      >&2 echo "Generator-MPP-Tracker-3"
      >&2 echo "  Spannung: $mpptracker3_voltage V"
      >&2 echo "  Strom:    $mpptracker3_current A"
      >&2 echo "Generator-MPP-Tracker-4"
      >&2 echo "  Spannung: $mpptracker4_voltage V"
      >&2 echo "  Strom:    $mpptracker4_current A"
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
