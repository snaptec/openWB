#!/bin/sh

#
# OpenWB-Modul für die Anbindung von SolarView über den integrierten TCP-Server
# Details zur API: https://solarview.info/solarview-fb_Installieren.pdf
#

. /var/www/html/openWB/openwb.conf

# Checks
if [ -z "$solarview_hostname" ]; then
  echo "Missing required variable 'solarview_hostname'" >&2
  return 1
fi
if [ "${solarview_port}" ]; then
  if [ "$solarview_port" -lt 1 ] || [ "$solarview_port" -gt 65535 ]; then
    echo "Invalid value '$solarview_port' for variable 'solarview_port'" >&2
    return 1
  fi
fi


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

  [ "$debug" -ne 0 ] && echo "Raw response: $response"
  #
  # Format:   {WR,Tag,Monat,Jahr,Stunde,Minute,KDY,KMT,KYR,KT0,PAC,UDC,IDC,UDCB,IDCB,UDCC,IDCC,UL1,IL1,UL2,IL2,UL3,IL3,TKK},Checksum
  # Beispiel: {01,05,09,2019,06,25,0000.0,00038,002574,00018647,00000,037,000.0,000,000.0,000,000.0,227,000.0,00},F
  #
  # Bedeutung (siehe SolarView-Dokumentation):
  #  KDY= Tagesertrag (kWh)
  #  KMT= Monatsertrag (kWh)
  #  KYR= Jahresertrag (kWh)
  #  KT0= Gesamtertrag (kWh)
  #  PAC= Generatorleistung in W
  #  UDC, UDCB, UDCC= Generator-Spannungen in Volt pro MPP-Tracker
  #  IDC, IDCB, IDCC= Generator-Ströme in Ampere pro MPP-Tracker
  #  UL1, IL1= Netzspannung, Netzstrom Phase 1
  #  UL2, IL2= Netzspannung, Netzstrom Phase 2
  #  UL3, IL3= Netzspannung, Netzstrom Phase 3
  #  TKK= Temperatur Wechselrichter

  # Geschweifte Klammern und Checksumme entfernen
  values="${response#*\{}"
  values="${values%\}*}"

  # Werte auslesen und verarbeiten
  local LANG=C
  local IFS=','
  echo "$values" | while read -r WR Tag Monat Jahr Stunde Minute KDY KMT KYR KT0 PAC UDC IDC UDCB IDCB UDCC IDCC UL1 IL1 UL2 IL2 UL3 IL3 TKK
  do

    # Werte formatiert in Variablen speichern
    id="$WR"
    timestamp="$Jahr-$Monat-$Tag $Stunde:$Minute"
    power=$(printf %.0f "$PAC")
    # Sonderbehandlung: Aufbereitung der Leistung für D0-Einspeisung (21*) und D0-Bezug (22*)
    #  PAC = '-0357' bedeutet: 357 W Bezug, 0 W Einspeisung
    #  PAC =  '0246' bedeutet: 0 W Bezug, 246 W Einspeisung
    [ "$command" = '21*' ] && [ "$power" -lt 0 ] && power=0
    if [ "$command" = '22*' ]; then
      [ "$power" -gt 0 ] && power=0
      [ "$power" -lt 0 ] && power=$(expr -1 \* "$power")
    fi
    energy_day=$(printf "%.1f" "$KDY")
    energy_month=$(printf "%.0f" "$KMT")
    energy_year=$(printf "%.0f" "$KYR")
    energy_total=$(printf "%.0f" "$KT0")
    mpptracker1_voltage=$(printf "%.0f" "$UDC")
    mpptracker1_current=$(printf "%.1f" "$IDC")
    mpptracker2_voltage=$(printf "%.0f" "$UDCB")
    mpptracker2_current=$(printf "%.1f" "$IDCB")
    mpptracker3_voltage=$(printf "%.0f" "$UDCC")
    mpptracker3_current=$(printf "%.1f" "$IDCC")
    grid1_voltage=$(printf "%.0f" "$UL1")
    grid1_current=$(printf "%.1f" "$IL1")
    # Bei einphasigen Wechselrichtern fehlen die Werte von Phase 2 und 3 in der Response.
    # Auf der Variable 'IL1' steht dann die Temperatur und alle nachfolgenden Variablen sind unbelegt
    if [ "$IL2" ]; then
      grid2_voltage=$(printf "%.0f" "$UL2")
      grid2_current=$(printf "%.1f" "$IL2")
      grid3_voltage=$(printf "%.0f" "$UL3")
      grid3_current=$(printf "%.1f" "$IL3")
      temperature=$(printf "%.0f" "$TKK")
    else
      temperature=$(printf "%.0f" "$IL2")
    fi

    if [ "$debug" -ne 0 ]; then
      # Werte ausgeben
      echo "ID: $id"
      echo "Zeitpunkt: $timestamp"
      echo "Temperatur: $temperature °C"
      echo "Leistung: $power W"
      echo "Energie:"
      echo "  Tag:    $energy_day kWh"
      echo "  Monat:  $energy_month kWh"
      echo "  Jahr:   $energy_year kWh"
      echo "  Gesamt: $energy_total kWh"
      echo "Generator-MPP-Tracker-1"
      echo "  Spannung: $mpptracker1_voltage V"
      echo "  Strom:    $mpptracker1_current A"
      echo "Generator-MPP-Tracker-2"
      echo "  Spannung: $mpptracker2_voltage V"
      echo "  Strom:    $mpptracker2_current A"
      echo "Generator-MPP-Tracker-3"
      echo "  Spannung: $mpptracker3_voltage V"
      echo "  Strom:    $mpptracker3_current A"
      echo "Netz:"
      echo "  Phase 1:"
      echo "    Spannung: $grid1_voltage V"
      echo "    Strom:    $grid1_current A"
      if [ "$grid2_voltage" ] || [ "$grid2_current" ]; then
        echo "  Phase 2:"
        [ "$grid2_voltage" ] && echo "    Spannung: $grid2_voltage V"
        [ "$grid2_current" ] && echo "    Strom:    $grid2_current A"
      fi
      if [ "$grid3_voltage" ] || [ "$grid3_current" ]; then
        echo "  Phase 3:"
        [ "$grid3_voltage" ] && echo "    Spannung: $grid3_voltage V"
       [ "$grid3_current" ] && echo "    Strom:    $grid3_current A"
      fi
    fi

    # Werte speichern
    [ "$2" ] && echo "$energy_day"          >"/var/www/html/openWB/ramdisk/$2"
    [ "$3" ] && echo "$energy_month"        >"/var/www/html/openWB/ramdisk/$3"
    [ "$4" ] && echo "$energy_year"         >"/var/www/html/openWB/ramdisk/$4"
    [ "$5" ] && echo "$energy_total"        >"/var/www/html/openWB/ramdisk/$5"
    [ "$6" ] && echo "$power"               >"/var/www/html/openWB/ramdisk/$6"
    [ "$7" ] && echo "$mpptracker1_current" >"/var/www/html/openWB/ramdisk/$7"
    [ "$8" ] && echo "$mpptracker2_current" >"/var/www/html/openWB/ramdisk/$8"
    [ "$9" ] && echo "$mpptracker3_current" >"/var/www/html/openWB/ramdisk/$9"
  done
}

echo
echo Wechselrichter Gesamt
echo ---------------------
request '00*' 'daily_pvkwhk' 'monthly_pvkwhk' 'yearly_pvkwhk' 'pvkwhk' 'pvwatt'

echo
echo Wechselrichter 1
echo ----------------
request '01*' 'daily_pvkwhk1' 'monthly_pvkwhk1' 'yearly_pvkwhk1' 'pvkwhk1' 'pvwatt1' 'pva1' 'pva2' 'pva3'

echo
echo Wechselrichter 2
echo ----------------
request '02*' 'daily_pvkwhk2' 'monthly_pvkwhk2' 'yearly_pvkwhk2' 'pvkwhk2' 'pvwatt2' 'pva1' 'pva2' 'pva3'

echo
echo D0-Einspeisung
echo --------------
request '21*' '' '' '' 'einspeisungkwh' ''

echo
echo D0-Bezug
echo --------
request '22*' '' '' '' 'bezugkwh' 'bezugwatt'
