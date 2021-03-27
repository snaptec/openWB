#!/bin/bash
#set -e
. /var/www/html/openWB/loadconfig.sh

cd /var/www/html/openWB

#TEST=echo

if [[ $debug == "2" ]]; then
    echo "Checking for MQTT bridge configs"
fi

# constant settings
mosquittoConfDir=/etc/mosquitto/conf.d
deleteFile=ramdisk/99-bridgesToDelete
sudo=sudo

# perform the actual installation of a single config
function InstallConfig {
    configToInstall=$1
    configFileNameToInstall=${configToInstall#ramdisk/}
    echo "Installing or updating bridge config '$configToInstall' in Mosquitto '$mosquittoConfDir'";
    $TEST $sudo mv -v $configToInstall $mosquittoConfDir/$configFileNameToInstall
    $TEST $sudo chown mosquitto.www-data $mosquittoConfDir/$configFileNameToInstall
    $TEST $sudo chmod 0660 $mosquittoConfDir/$configFileNameToInstall
}

# tell Mosquitto to re-read its configuration
function TriggerMosquittoConfigRead {
    #process_id=`/bin/ps aux | grep "mosquitto" | grep -v "grep" | awk '{print $2}'`
    if [[ $debug == "1" ]]; then
        echo "Restarting Mosquitto server to trigger re-read of changed bridge config (SIGHUP would not remove deleted bridges)"
    fi

    # $TEST $sudo kill -HUP $process_id
    # $TEST $sudo service mosquitto restart
    # sometimes the ports where still blocked on restart causing mosquitto to fail!
    $TEST $sudo service mosquitto reload
}

###############
# main script #
###############
if [[ $debug == "1" ]]; then
    echo "**** MQTT configuration starting at `date` ****"
fi
anyConfigChanged="0"

# handle bridges to delete
if [ -f $deleteFile ]; then
    for currentConfig in $(<$deleteFile); do
        if [[ $debug == "1" ]]; then
            echo "Removing bridge '$currentConfig'"
        fi
        $TEST $sudo rm -v $currentConfig
        anyConfigChanged="1"
    done

    $TEST $sudo rm -v $deleteFile
#else
    # echo "No bridges to be deleted"
fi

# handle bridges to install
for currentConfig in ramdisk/99-bridge-*; do
    if [ -f "$currentConfig" ]; then
        if [[ $debug == "1" ]]; then
            echo "Found bridge config '$currentConfig' for installation or update in Mosquitto '$mosquittoConfDir'"
        fi
        InstallConfig $currentConfig
        anyConfigChanged="1"
    fi
done

if [ "$anyConfigChanged" != "0" ]; then
    TriggerMosquittoConfigRead
#else
    # echo "No bridges to be installed/updated"
fi
#force pushing all values in broker
timeout 3 mosquitto_sub -v -h localhost -t "openWB/#" > /tmp/mqttvars
while read line; do
	if [[ $line == *"openWB"* ]];then
		value=$(echo -e $line | awk '{print $2;}')
		name=$(echo -e $line | awk '{print $1;}')
		mosquitto_pub -r -t $name -m $value
	fi
done < /tmp/mqttvars
if [[ $debug == "1" ]]; then
    echo "**** MQTT configuration done at `date` ****"
fi
