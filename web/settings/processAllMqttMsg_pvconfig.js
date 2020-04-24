/**
 * functions to setup pv charging parameters via MQTT-messages
 *
 * required function setInputValue defined in main html
 *
 * @author Michael Ortenstein
 */

function processMessages(mqttmsg, mqttpayload) {
    var elementId = '#' + mqttmsg.substring(mqttmsg.lastIndexOf('/')+1);

    console.log('received '+mqttmsg+' = '+mqttpayload+'    id = '+elementId);

	if ( mqttmsg == 'openWB/config/get/global/maxEVSECurrentAllowed' ) {
        setInputValue( $(elementId), mqttpayload );
	}
	else if ( mqttmsg == 'openWB/config/get/pv/chargeSubmode' ) {
        // 0 = Einspeisung, 1 = Bezug, 2 = manueller Regelpunkt
        switch ( mqttpayload ) {
            case '0':
                $('#optionFeedIn').prop('checked', true);
                $('#optionFeedIn').closest('label').addClass("active");
                $('#optionConsume').prop('checked', false);
                $('#optionConsume').closest('label').removeClass("active");
                $('#optionManual').prop('checked', false);
                $('#optionManual').closest('label').removeClass("active");
                break;
            case '1':
                $('#optionFeedIn').prop('checked', false);
                $('#optionFeedIn').closest('label').removeClass("active");
                $('#optionConsume').prop('checked', true);
                $('#optionConsume').closest('label').addClass("active");
                $('#optionManual').prop('checked', false);
                $('#optionManual').closest('label').removeClass("active");
                break;
            case '2':
                $('#optionFeedIn').prop('checked', false);
                $('#optionFeedIn').closest('label').removeClass("active");
                $('#optionConsume').prop('checked', false);
                $('#optionConsume').closest('label').removeClass("active");
                $('#optionManual').prop('checked', true);
                $('#optionManual').closest('label').addClass("active");
                break;
        }
	}
	else if ( mqttmsg == 'openWB/config/get/pv/regulationPoint' ) {
        setInputValue( $(elementId), mqttpayload );
	}
    else if ( mqttmsg == 'openWB/config/get/pv/minFeedinPowerBeforeStart' ) {
        setInputValue( $(elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/startDelay' ) {
        setInputValue( $(elementId), mqttpayload );
	}
    else if ( mqttmsg == 'openWB/config/get/pv/maxPowerConsumptionBeforeStop' ) {
        setInputValue( $(elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/stopDelay' ) {
        setInputValue( $(elementId), mqttpayload );
    }
    else if ( mqttmsg.match( /^openwb\/config\/get\/pv\/lp\/[1-8]\/mincurrent$/i ) ) {
        var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
        setInputValue( $('#minCurrentLp' + index), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/boolAdaptiveCharging' ) {
        // 0 = ausgeschaltet, 1 = eingeschaltet
        switch ( mqttpayload ) {
            case '0':
                $('#adaptiveChargingOff').prop('checked', true);
                $('#adaptiveChargingOff').closest('label').addClass("active");
                $('#adaptiveChargingOn').prop('checked', false);
                $('#adaptiveChargingOn').closest('label').removeClass("active");
                break;
            case '1':
                $('#adaptiveChargingOff').prop('checked', false);
                $('#adaptiveChargingOff').closest('label').removeClass("active");
                $('#adaptiveChargingOn').prop('checked', true);
                $('#adaptiveChargingOn').closest('label').addClass("active");
                break;
        }
    }
    else if ( mqttmsg == 'openWB/config/get/pv/adaptiveChargingFactor' ) {
        setInputValue( $(elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/nurpv70dynact' ) {
        // 0 = ausgeschaltet, 1 = eingeschaltet
        switch ( mqttpayload ) {
            case '0':
                $('#nurpv70dynactOff').prop('checked', true);
                $('#nurpv70dynactOff').closest('label').addClass("active");
                $('#nurpv70dynactOn').prop('checked', false);
                $('#nurpv70dynactOn').closest('label').removeClass("active");
                break;
            case '1':
                $('#nurpv70dynactOff').prop('checked', false);
                $('#nurpv70dynactOff').closest('label').removeClass("active");
                $('#nurpv70dynactOn').prop('checked', true);
                $('#nurpv70dynactOn').closest('label').addClass("active");
                break;
        }
    }
    else if ( mqttmsg == 'openWB/config/get/pv/nurpv70dynw' ) {
        setInputValue( $(elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/minSocAlwaysToChargeTo' ) {
        setInputValue( $(elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/minSocAlwaysToChargeToCurrent' ) {
        setInputValue( $(elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/boolShowPriorityIconInTheme' ) {
        // 0 = nicht anzeigen, 1 = anzeigen
        switch ( mqttpayload ) {
            case '0':
                $('#hidePriority').prop('checked', true);
                $('#hidePriority').closest('label').addClass("active");
                $('#showPriority').prop('checked', false);
                $('#showPriority').closest('label').removeClass("active");
                break;
            case '1':
                $('#hidePriority').prop('checked', false);
                $('#hidePriority').closest('label').removeClass("active");
                $('#showPriority').prop('checked', true);
                $('#showPriority').closest('label').addClass("active");
                break;
        }
    }
    else if ( mqttmsg == 'openWB/config/get/pv/minBatteryChargePowerAtEvPriority' ) {
        setInputValue( $(elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/minBatteryDischargeSocAtBattPriority' ) {
        setInputValue( $(elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/batteryDischargePowerAtBattPriority' ) {
        setInputValue( $(elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/minCurrentMinPv' ) {
        setInputValue( $(elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/socStartChargeAtMinPv' ) {
        setInputValue( $(elementId), mqttpayload );
    }
    else if ( mqttmsg == 'openWB/config/get/pv/socStopChargeAtMinPv' ) {
        setInputValue( $(elementId), mqttpayload );
    }

}  // end processMessages
