#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

if [ -e "$OPENWBBASEDIR/web/ladelog" ]; then
	mkdir "$OPENWBBASEDIR/web/logging/data/ladelog"
	oldlog="${OPENWBBASEDIR}/web/ladelog"
	while IFS= read -r line
	do
		  #echo "$line"
		year=$(echo "$line" | cut -c 7-8 )
		month=$(echo "$line" | cut -c 4-5 )
		if [[ $year == "19" ]] ||  [[ $year == "20" ]]; then
			echo "$line" >> "${OPENWBBASEDIR}/web/logging/data/ladelog/20$year$month.csv "
		fi
	  done < "$oldlog"
	  rm "${OPENWBBASEDIR}/web/ladelog"
	  chown -R pi:pi "${OPENWBBASEDIR}/web/logging/data/ladelog/"
	  chmod 777 "${OPENWBBASEDIR}/web/logging/data/ladelog/*"
fi

# upgrade charge log data with costs
python3 "${OPENWBBASEDIR}/runs/upgradeChargeLogs.py" --price "$preisjekwh"
