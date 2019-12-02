#!/bin/bash
#set -e
. openwb.conf

#TEST=echo

if [[ $debug == "2" ]]; then
    echo "Checking for MQTT bridge configs"
fi

# constant settings
mosquittoConfDir=/etc/mosquitto/conf.d
deleteFile=ramdisk/99-bridgesToDelete
sudo=sudo
waitTime=3

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

    #$TEST $sudo kill -HUP $process_id
    $TEST $sudo service mosquitto restart

    # wait some seconds to allow Mosquitto to fully come up again before rest of regel.sh starts publishing data
    echo "Waiting $waitTime seconds for Mosquitto to come up again before going ahead with rest of 'regel.sh' script"
    sleep $waitTime
}

###############
# main script #
###############
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
