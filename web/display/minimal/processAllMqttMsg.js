/**
 * Functions to update graph and gui values via MQTT-messages
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 * @author Lutz Bender
 */

function reloadDisplay() {
	/** @function reloadDisplay
	 * triggers a reload of the current page
	 */
	// wait some seconds to allow other instances receive this message
	console.log("reloading display...");
	setTimeout(function () {
		publish("0", "openWB/set/system/reloadDisplay");
		// wait again to give the broker some time and avoid a reload loop
		setTimeout(function () {
			location.reload();
		}, 2000);
	}, 2000);
}

function handlevar(mqttmsg, mqttpayload) {
	// console.log("Topic: "+mqttmsg+" Message: "+mqttpayload);
	// receives all messages and calls respective function to process them
	if (mqttmsg.match(/^openwb\/system\//i)) { processSystemMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/lp\//i)) { processChargepointMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/global\/awattar\//i)) { processETMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/config\/get\/sofort\//i)) { processChargeNowMessages(mqttmsg, mqttpayload); }
}  // end handlevar

function processSystemMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/system
	// called by handlevar
	if (mqttmsg == 'openWB/system/reloadDisplay') {
		if (mqttpayload == '1') {
			reloadDisplay();
		}
	} else if (mqttmsg == 'openWB/system/priceForKWh') {
		let tmpValue = mqttpayload * 100;
		if (defaultPrice != tmpValue) {
			defaultPrice = tmpValue;
			updateMainPriceLabels();
		}
	} else if (mqttmsg == 'openWB/system/parentWB') {
		if (parentWB != mqttpayload) {
			parentWB = mqttpayload;
			connectToParent();
		}
	} else if (mqttmsg == 'openWB/system/parentCPlp1') {
		if (parentCP[0] != mqttpayload) {
			parentCP[0] = mqttpayload;
		}
	} else if (mqttmsg == 'openWB/system/parentCPlp2') {
		if (parentCP[1] != mqttpayload) {
			parentCP[1] = mqttpayload;
		}
	}
}

function processETMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/global/awattar
	// called by handlevar
	if ( mqttmsg == 'openWB/global/awattar/ActualPriceForCharging' ) {
		etCurrentPrice = parseFloat(mqttpayload)
		updateMainPriceLabels();
	} else if ( mqttmsg == 'openWB/global/awattar/pricelist' ) {
		etPriceList = mqttpayload;
		priceChart.update();
	} else if ( mqttmsg == 'openWB/global/awattar/MaxPriceForCharging' ) {
		// if we are an external openWB and have sent an update within the last 20 seconds
		// or we are just changing the value -> ignore it
		if (Date.now() - 20000 > etParentGlobalPriceUpdated && ! maxPriceDelayTimers[0]  && ! maxPriceDelayTimers[1]) {
			if (etMaxPriceGlobal != mqttpayload) {
				etMaxPriceGlobal = mqttpayload;
				updateMainPriceLabels();
				updateSetPriceLabels();
			}
		}
	} else if ( mqttmsg == 'openWB/global/awattar/boolAwattarEnabled' ) {
		if (etEnabled != mqttpayload) {
			etEnabled = mqttpayload;
			updateMainPriceLabels();
			updateSetPriceLabels();
		}
	}
}

function processChargepointMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/system
	// called by handlevar

	// check if topic contains subgroup like /lp/1/
	// last part of topic after /
	var topic = mqttmsg.substring(mqttmsg.lastIndexOf('/') + 1);
	var index = mqttmsg.match(/(\w+)\/(\d\d?)\//)[2];
	if (index != null && index <= configuredChargePoints) {
		if (topic == '%Soc') {
			eval("gaugelp" + index + "s.set(mqttpayload)");
			$('#lp' + index + 'st').html(mqttpayload + "%");
		} else if (topic == 'W') {
			var lpw = mqttpayload / 1000;
			if (eval("displaylp" + index + "max") > 999) {
				eval("gaugelp" + index + ".set(lpw)");
			} else {
				eval("gaugelp" + index + ".set(mqttpayload)");
			}
			if (mqttpayload > 999) {
				$('#lp' + index + 't').html(lpw.toFixed(1) + " kW");
			} else {
				$('#lp' + index + 't').html(mqttpayload + " W");
			}
		} else if (topic == 'boolSocConfigured') {
			if (mqttpayload == 1) {
				$('#lp' + index + 's').removeClass("hide");
				$('#lp' + index + 'st').removeClass("hide");
			} else {
				$('#lp' + index + 's').addClass("hide");
				$('#lp' + index + 'st').addClass("hide");
			}
		} else if (topic == 'boolPlugStat') {
			if (mqttpayload == 1) {
				$('#lp' + index + 'plugstat').removeClass('hide');
			} else {
				$('#lp' + index + 'plugstat').addClass('hide');
			}
		} else if (topic == 'boolChargeStat') {
			if (mqttpayload == 1) {
				$('#lp' + index + 'plugstat').removeClass('text-warning').addClass('text-success');
			} else {
				$('#lp' + index + 'plugstat').removeClass('text-success').addClass('text-warning');
			}
		} else if (topic == 'ChargePointEnabled') {
			if (mqttpayload == 1) {
				$('#lp' + index + 'enabled').removeClass("hide");
				$('#lp' + index + 'disabled').addClass("hide");
			} else {
				$('#lp' + index + 'enabled').addClass("hide");
				$('#lp' + index + 'disabled').removeClass("hide");
			}
		}
	}
}

function processChargeNowMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/system
	// called by handlevar

	// check if topic contains subgroup like /lp/1/
	// last part of topic after /

	var topic = mqttmsg.substring(mqttmsg.lastIndexOf('/') + 1);
	var index = mqttmsg.match(/(\w+)\/(\d\d?)\//)[2];
	if (index != null) {
		imm = index - 1;
		if (topic == 'etBasedCharging') {
			if (etModes[imm] != mqttpayload) {
				etModes[imm] = mqttpayload;
				updateMainPriceLabels();
				updateSetPriceLabels();
			}
		} else if  (topic == 'etChargeMaxPrice') {
			// if we are an external openWB and have sent an update within the last 20 seconds
			// or we are just changing the value -> ignore it
			if (Date.now() - 20000 > etParentLocalPriceUpdated[imm] && ! maxPriceDelayTimers[imm]) {
				if (etMaxPricesLocal[imm] != mqttpayload) {
					etMaxPricesLocal[imm] = mqttpayload;
					updateMainPriceLabels();
					updateSetPriceLabels();
				}
			}
		}
	}
}
