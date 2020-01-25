#!/bin/bash
set -eo pipefail

#####
#
#  File: processautolock.sh
#
#  Copyright 2020 Michael Ortenstein
#
#  This file is part of openWB.
#
#     openWB is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     openWB is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with openWB.  If not, see <https://www.gnu.org/licenses/>.
#
#####

cd /var/www/html/openWB/
# read config file
. openwb.conf

# process autolock
second=$(( $(date +%S) + 1 ))  # make sure, second is never 0.
# sets variables necessary due to inconsistent naming
chargeStatusLp1=$(<ramdisk/mqttchargestat)
chargeStatusLp2=$(<ramdisk/mqttchargestats1)
chargeStatusLp3=$(<ramdisk/mqttchargestatlp3)
chargeStatusLp4=$(<ramdisk/mqttchargestatlp4)
chargeStatusLp5=$(<ramdisk/mqttchargestatlp5)
chargeStatusLp6=$(<ramdisk/mqttchargestatlp6)
chargeStatusLp7=$(<ramdisk/mqttchargestatlp7)
chargeStatusLp8=$(<ramdisk/mqttchargestatlp8)

# some stuff
timeOfDay=$(date +%H:%M)
dayOfWeek=$(date +%u)  # 1 = Montag

# autolocktimer=$(<ramdisk/autolocktimer)
if [ "$second" -lt "59" ]; then
	# once a minute at new minute check if (un)lock-time is up

	echo "processing check at ${second}"

	for chargePoint in {1..8}
	do
		flagFilename="/var/www/html/openWB/ramdisk/waitautolocklp${chargePoint}"  # name of variable for lp wait-to-lock
	    lpFilename="/var/www/html/openWB/ramdisk/mqttlp${chargePoint}enabled"  # name of variable for lpenable
	    locktimeSettingName="lockTimeLp${chargePoint}_${dayOfWeek}"  # name of variable of lock time for today

	    if [ -z "${!locktimeSettingName}" ]; then
	        # variable is not defined in config file (or empty)
	        lockTime=""  # so set the lock time to empty string
	    else
	        lockTime="${!locktimeSettingName}"  # get the lock time from config file
	    fi

	    # now process the settings...
	    lpenabled=$(<$lpFilename)  # read ramdisk value for lp enabled
	    now=$(date +'%Y-%m-%d %H:%M:%S');  # timestamp just for logging
	    if [ "$lpenabled" = "1" ]; then
			echo "LP${chargePoint} is enabled"
			# if the charge point is enabled, check for auto disabling
			if [ $timeOfDay = "$lockTime" ]; then
				echo "locktime for LP${chargePoint} is up"
				# auto lock time is now, set flag
				echo "1" > $flagFilename
			fi
		fi
	done
fi

function checkDisableLp {
    powerVarName="chargeStatusLp${chargePoint}"
    if [ "${!powerVarName}" = "0" ]; then
        # charge point not charging
        # delete wait-to-lock-flag
        echo "0" > $flagFilename
        # and disable charge point
        mqttTopic="openWB/set/lp$chargePoint/ChargePointEnabled"
        mosquitto_pub -r -t $mqttTopic -m 0
        echo "${now} auto-disabled charge point #${chargePoint}"
    else
        echo "${now} no auto-disable charge point #${chargePoint}, still charging: ${!powerVarName} W"
    fi
}

for chargePoint in {1..8}
do
    # every 10 seconds check if flag is set to disable charge point
    # or if unlock time is up
    flagFilename="/var/www/html/openWB/ramdisk/waitautolocklp${chargePoint}"  # name of variable for lp wait-to-lock
    unlocktimeSettingName="unlockTimeLp${chargePoint}_${dayOfWeek}"  # name variable of unlock time for today
    waitUntilFinishedName="waitUntilFinishedBoxLp${chargePoint}"  # name variable of checkbox value

    if [ -z "${!unlocktimeSettingName}" ]; then
        # variable is not defined in settings (or empty)
        unlockTime=""  # so set the unlock time to empty string
    else
        unlockTime="${!unlocktimeSettingName}"  # get the unlock time from setting
    fi

    if [ -z "${!waitUntilFinishedName}" ]; then
        # variable is not defined in settings (or empty)
        waitUntilFinished="off"  # so set the value to 'dont wait'
    else
        waitUntilFinished="${!waitUntilFinishedName}"  # get the checkbox-value from setting
    fi

    # now process the settings...
    now=$(date +'%Y-%m-%d %H:%M:%S');  # timestamp just for logging
    waitFlag=$(<$flagFilename)  # read ramdisk value for autolock wait flag
    if [ "$waitFlag" = "1" ]; then
        # charge point waiting for lock
        echo "${now} charge point #${chargePoint} waiting for lock"
        if [ $time = "$unlockTime" ]; then
            # but auto unlock time is now, so delete possible wait-to-lock-flag
            echo "${now} unlock time for charge point #${chargePoint}: disable wait for lock"
            echo "0" > $flagFilename
        else
            # unlock time not now and waiting for auto lock
            # check if charge point still busy to lock
            checkDisableLp
        fi
    fi
    if [ $timeOfDay = "$unlockTime" ]; then
        # unlock time is now, so enable charge point
        mqttTopic="openWB/set/lp$chargePoint/ChargePointEnabled"
        mosquitto_pub -r -t $mqttTopic -m 1
        echo "${now} auto-enabled charge point #${chargePoint}"
    fi
done
