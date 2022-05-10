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
	setTimeout(function(){
		publish( "0", "openWB/set/system/reloadDisplay" );
		// wait again to give the broker some time and avoid a reload loop
		setTimeout(function(){
			location.reload();
		}, 2000);
	}, 2000);
}

function handlevar(mqttmsg, mqttpayload) {
	// console.log("Topic: "+mqttmsg+" Message: "+mqttpayload);
	// receives all messages and calls respective function to process them
	if ( mqttmsg.match( /^openwb\/system\//i) ) { processSystemMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/lp\//i) ) { processChargepointMessages(mqttmsg, mqttpayload); }
}  // end handlevar

function processSystemMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/system
	// called by handlevar
	if ( mqttmsg == 'openWB/system/reloadDisplay' ) {
		if( mqttpayload == '1' ){
			reloadDisplay();
		}
	}
	// else if ( mqttmsg == 'openWB/system/parentWB' ) {
	// 	console.log("received parent openwb url: " + mqttpayload);
	// }
	// else if ( mqttmsg == 'openWB/system/parentCPlp1' ) {
	// 	console.log("received index for lp1 on parent openwb: " + mqttpayload);
	// }
	// else if ( mqttmsg == 'openWB/system/parentCPlp2' ) {
	// 	console.log("received index for lp2 on parent openwb: " + mqttpayload);
	// }
}

function processChargepointMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/system
	// called by handlevar
	if ( mqttmsg == 'openWB/lp/2/boolChargePointConfigured' ) {
		console.log("received configured for local lp2: " + mqttpayload)
	}
	else if ( mqttmsg == 'openWB/lp/1/%Soc' ) {
		var lp1s = mqttpayload;
		gaugelp1s.set(lp1s);
		$("#lp1st").html(mqttpayload + "%");
	}
	else if ( mqttmsg == 'openWB/lp/1/W' ) {
		var lp1w = mqttpayload;
		gaugelp1.set(lp1w);
		if ( lp1w > 999 ) {
			lp1w= lp1w / 1000;
			$("#lp1t").html(lp1w.toFixed(2) + " kW");
		} else {
			$("#lp1t").html(mqttpayload + " W");
		}
	}
	else if (mqttmsg == 'openWB/lp/1/boolSocConfigured' ) {
		if ( mqttpayload == 1 ) {
			$("#lp1s").removeClass("hide");
			$("#lp1st").removeClass("hide");
		} else {
			$("#lp1s").addClass("hide");
			$("#lp1st").addClass("hide");
		}
	}
	else if ( mqttmsg == 'openWB/lp/1/boolPlugStat' ) {
		if ( mqttpayload == 1 ) {
			$("#lp1plugstat").removeClass('hide');
		} else {
			$("#lp1plugstat").addClass('hide');
		}
	}
	else if ( mqttmsg == 'openWB/lp/1/boolChargeStat' ) {
		if ( mqttpayload == 1 ) {
			$("#lp1plugstat").removeClass('text-warning').addClass('text-success');
		} else {
			$("#lp1plugstat").removeClass('text-success').addClass('text-warning');
		}
	}
	else if ( mqttmsg == 'openWB/lp/1/ChargePointEnabled' ) {
		var lp1enabled = mqttpayload;
		if(lp1enabled == 1){
			$("#lp1enabled").removeClass("hide");
			$("#lp1disabled").addClass("hide");
		} else {
			$("#lp1enabled").addClass("hide");
			$("#lp1disabled").removeClass("hide");
		}
	}

}
