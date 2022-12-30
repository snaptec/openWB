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

# sets variables necessary due to inconsistent naming
powerLp1=$(<ramdisk/llaktuell)
powerLp2=$(<ramdisk/llaktuells1)
powerLp3=$(<ramdisk/llaktuells2)
powerLp4=$(<ramdisk/llaktuelllp4)
powerLp5=$(<ramdisk/llaktuelllp5)
powerLp6=$(<ramdisk/llaktuelllp6)
powerLp7=$(<ramdisk/llaktuelllp7)
powerLp8=$(<ramdisk/llaktuelllp8)
isConfiguredLp1="1"
isConfiguredLp2=$lastmanagement
isConfiguredLp3=$lastmanagements2
isConfiguredLp4=$lastmanagementlp4
isConfiguredLp5=$lastmanagementlp5
isConfiguredLp6=$lastmanagementlp6
isConfiguredLp7=$lastmanagementlp7
isConfiguredLp8=$lastmanagementlp8

# process current time
timeOfDay=$(date +%H:%M)
dayOfWeek=$(date +%u)  # 1 = Montag
second=$(date +%S)

# values used for status flag:
# 0 = standby
# 1 = waiting for autolock
# 2 = autolock performed
# 3 = auto-unlock performed

if [ "$second" -lt "10" ]; then
	# once a minute at new minute check if (un)lock-time is up

	for chargePoint in {1..8}
	do
		variableConfiguredLpName="isConfiguredLp${chargePoint}"  # name of variable for lp configured
		if [ "${!variableConfiguredLpName}" = "1" ]; then
			# charge point is configured, so process it
			statusFlagFilename="/var/www/html/openWB/ramdisk/autolockstatuslp${chargePoint}"  # name autolock status file
			lpFilename="/var/www/html/openWB/ramdisk/lp${chargePoint}enabled"  # name lp enable file
			locktimeSettingName="lockTimeLp${chargePoint}_${dayOfWeek}"  # name of variable of lock time for today

			if [ -z "${!locktimeSettingName}" ]; then
				# variable is not defined in config file (or empty)
				lockTime=""  # so set the lock time to empty string
			else
				lockTime="${!locktimeSettingName}"  # get the lock time from config file
			fi

			# now process the settings...
			lpenabled=$(<$lpFilename)  # read ramdisk value for lp enabled
			statusFlag=$(<$statusFlagFilename)  # read flag from ramdisk
			if [ "$lpenabled" = "1" ] && [ $timeOfDay = "$lockTime" ] && [ $statusFlag != "1" ]; then
				# if the charge point is enabled and auto lock time is now
				# and flag not already set, set flag "waiting for autolock"
				mqttTopic="openWB/set/lp/$chargePoint/AutolockStatus"
				mosquitto_pub -r -t $mqttTopic -m 1
			fi
		fi
	done
fi

function checkDisableLp {
	powerVarName="powerLp${chargePoint}"
	if [ "$waitUntilFinished" = "off" ] || [ "${!powerVarName}" -lt "200" ]; then
		# autolock is not configured to wait until finished or charge point not charging, so disable charge point
		mqttTopic="openWB/set/lp/$chargePoint/ChargePointEnabled"
		mosquitto_pub -r -t $mqttTopic -m 0
		# and set flag "autolock performed"
		mqttTopic="openWB/set/lp/$chargePoint/AutolockStatus"
		mosquitto_pub -r -t $mqttTopic -m 2
	fi
}

for chargePoint in {1..8}
do
	# every 10 seconds check if flag is set to disable charge point
	# or if unlock time is up
	variableConfiguredLpName="isConfiguredLp${chargePoint}"  # name of variable for lp configured
	statusFlagFilename="/var/www/html/openWB/ramdisk/autolockstatuslp${chargePoint}"  # name autolock status file
	if [ "${!variableConfiguredLpName}" = "1" ]; then
		# charge point is configured, so process it
		statusFlag=$(<$statusFlagFilename)  # read ramdisk value for autolock wait flag

		# check all settings if any time is configured for lp to set flag for icon in theme
		isAutolockConfigured=false
		for day in {1..7}
		do
			# check for configured lock time
			locktimeSettingName="lockTimeLp${chargePoint}_${day}"  # name variable: lock time for the given day
			if [ -n "${!locktimeSettingName}" ]; then
				# locktime is set to a non empty string
				isAutolockConfigured=true
				break  # exit loop
			fi
			# check for configured unlock time
			unlocktimeSettingName="unlockTimeLp${chargePoint}_${day}"  # name variable: unlock time for the given day
			if [ -n "${!unlocktimeSettingName}" ]; then
				# unlocktime is set to a non empty string
				isAutolockConfigured=true
				break  # exit loop
			fi
		done

		configuredFlagFilename="/var/www/html/openWB/ramdisk/autolockconfiguredlp${chargePoint}"  # name of file for flag: autolock configured
		if $isAutolockConfigured ; then
			echo "1" > $configuredFlagFilename  # set flag in ramdisk
		else
			echo "0" > $configuredFlagFilename  # set flag in ramdisk
			if [ "$statusFlag" != "0" ]; then			
				# and set flag "standby" id not already set
				mqttTopic="openWB/set/lp/$chargePoint/AutolockStatus"
				mosquitto_pub -r -t $mqttTopic -m 0
			fi
		fi

		locktimeSettingName="lockTimeLp${chargePoint}_${dayOfWeek}"  # name variable: unlock time for today
		unlocktimeSettingName="unlockTimeLp${chargePoint}_${dayOfWeek}"  # name variable: unlock time for today
		waitUntilFinishedName="waitUntilFinishedBoxLp${chargePoint}"  # name checkbox-value-variable: wait autolock until finished charging yes/no

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
		if [ "$statusFlag" = "1" ]; then
			# charge point waiting for lock
			if [ $timeOfDay = "$unlockTime" ]; then
				# but auto unlock time is now
				# set flag back to "standby"
				mqttTopic="openWB/set/lp/$chargePoint/AutolockStatus"
				mosquitto_pub -r -t $mqttTopic -m 0
			else
				if [ $statusFlag != "2" ]; then
					# charge point waiting for auto lock
					# check if charge point still busy to lock
					checkDisableLp
				fi
			fi
		elif [ $timeOfDay = "$unlockTime" ] && [ $statusFlag != "3" ]; then
			# charge point not waiting for lock and not already unlocked
			# but unlock time is now, so enable charge point
			mqttTopic="openWB/set/lp/$chargePoint/ChargePointEnabled"
			mosquitto_pub -r -t $mqttTopic -m 1
			# and set flag "auto-unlock performed"
			mqttTopic="openWB/set/lp/$chargePoint/AutolockStatus"
			mosquitto_pub -r -t $mqttTopic -m 3
		fi
	fi
done
