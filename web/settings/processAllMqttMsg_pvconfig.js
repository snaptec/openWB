/**
 * functions to setup pv charging parameters via MQTT-messages
 *
 * required function setInputValue and setToggleBtnGroup defined in main pvconfig.html
 *
 * @author Michael Ortenstein
 */

function processMessages(mqttmsg, mqttpayload) {
    var elementId = mqttmsg.substring(mqttmsg.lastIndexOf('/')+1);

	if ( mqttmsg == 'openWB/config/get/global/maxEVSECurrentAllowed' ) {
        setInputValue( $('#' + elementId), mqttpayload );
	}
	else if ( mqttmsg == 'openWB/config/get/pv/chargeSubmode' ) {
        // 0 = Einspeisung, 1 = Bezug, 2 = manueller Regelpunkt
        setToggleBtnGroup(elementId, mqttpayload);
	}
	else if ( mqttmsg == 'openWB/config/get/pv/regulationPoint' ) {
        if ( !isNaN(mqttpayload) && mqttpayload < 0 ) {
            // negative values are displayed by checkbox
            $('#regulationPointPosNeg').prop('checked', true);
            mqttpayload *= -1;
        }
        setInputValue( $('#' + elementId), mqttpayload );
	}
    else if ( mqttmsg == 'openWB/config/get/pv/minFeedinPowerBeforeStart' ) {
        console.log(elementId);
        console.log(mqttpayload);

        setInputValue( $('#' + elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/startDelay' ) {
        setInputValue( $('#' + elementId), mqttpayload );
	}
    else if ( mqttmsg == 'openWB/config/get/pv/maxPowerConsumptionBeforeStop' ) {
        setInputValue( $('#' + elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/stopDelay' ) {
        setInputValue( $('#' + elementId), mqttpayload );
    }
    else if ( mqttmsg.match( /^openwb\/config\/get\/pv\/lp\/[1-8]\/mincurrent$/i ) ) {
        var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
        setInputValue( $('#minCurrentLp' + index), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/boolAdaptiveCharging' ) {
        // 0 = ausgeschaltet, 1 = eingeschaltet
        setToggleBtnGroup(elementId, mqttpayload);
    }
    else if ( mqttmsg == 'openWB/config/get/pv/adaptiveChargingFactor' ) {
        setInputValue( $('#' + elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/nurpv70dynact' ) {
        // 0 = ausgeschaltet, 1 = eingeschaltet
        setToggleBtnGroup(elementId, mqttpayload);
    }
    else if ( mqttmsg == 'openWB/config/get/pv/nurpv70dynw' ) {
        setInputValue( $('#' + elementId), mqttpayload );
    }
    else if ( mqttmsg.match( /^openwb\/config\/get\/pv\/lp\/[1-8]\/minsocalwaystochargeto$/i ) ) {
        var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
        setInputValue( $('#' + elementId + 'Lp' + index), mqttpayload );
    }
    else if ( mqttmsg.match( /^openwb\/config\/get\/pv\/lp\/[1-8]\/minsocalwaystochargetocurrent$/i ) ) {
        var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
        setInputValue( $('#' + elementId + 'Lp' + index), mqttpayload );
    }
    else if ( mqttmsg.match( /^openwb\/config\/get\/pv\/lp\/[1-8]\/maxsoctochargeto$/i ) ) {
        var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
        setInputValue( $('#' + elementId + 'Lp' + index), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/priorityModeEVBattery' ) {
        // 0 = nicht anzeigen, 1 = anzeigen
        console.log(elementId);
        console.log(mqttpayload);

        setToggleBtnGroup(elementId, mqttpayload);
    }
    else if ( mqttmsg == 'openWB/config/get/pv/boolShowPriorityIconInTheme' ) {
        // 0 = nicht anzeigen, 1 = anzeigen
        console.log(elementId);
        console.log(mqttpayload);

        setToggleBtnGroup(elementId, mqttpayload);
    }
    else if ( mqttmsg == 'openWB/config/get/pv/minBatteryChargePowerAtEvPriority' ) {
        setInputValue( $('#' + elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/minBatteryDischargeSocAtBattPriority' ) {
        setInputValue( $('#' + elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/batteryDischargePowerAtBattPriority' ) {
        setInputValue( $('#' + elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/minCurrentMinPv' ) {
        setInputValue( $('#' + elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/socStartChargeAtMinPv' ) {
        setInputValue( $('#' + elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/socStopChargeAtMinPv' ) {
        setInputValue( $('#' + elementId), mqttpayload );
    }

}  // end processMessages
