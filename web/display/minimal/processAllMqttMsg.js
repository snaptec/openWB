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
}  // end handlevar

function processSystemMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/system
	// called by handlevar
	if (mqttmsg == 'openWB/system/reloadDisplay') {
		if (mqttpayload == '1') {
			reloadDisplay();
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
	if (index != null) {
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
