/**
 * Functions to update graph and gui values via MQTT-messages
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

function getCol(matrix, col){
	var column = [];
	for(var i=0; i<matrix.length; i++){
		column.push(matrix[i][col]);
	}
	return column;
}

function convertToKw(dataColum) {
	var convertedDataColumn = [];
	dataColum.forEach((value) => {
		convertedDataColumn.push(value / 1000);
	});
	return convertedDataColumn;
}

function handlevar(mqttmsg, mqttpayload) {
	// receives all messages and calls respective function to process them
	if ( mqttmsg.match( /^openwb\/graph\//i ) ) { processGraphMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/evu\//i) ) { processEvuMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/global\//i) ) { processGlobalMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/housebattery\//i) ) { processHousebatteryMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/system\//i) ) { processSystemMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/pv\//i) ) { processPvMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/verbraucher\//i) ) { processVerbraucherMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/set\//i) ) { processSetMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/lp\//i) ) { processLpMessages(mqttmsg, mqttpayload); }
}  // end handlevar

function processGraphMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/graph
	// called by handlevar
	if ( mqttmsg == "openWB/graph/boolDisplayHouseConsumption" ) {
		if ( mqttpayload == 1) {
			boolDisplayHouseConsumption = false;
			hidehaus = "foo";
		} else {
			boolDisplayHouseConsumption = true;
			hidehaus = "Hausverbrauch";
		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayLegend" ) {
		if ( mqttpayload == 0) {
			boolDisplayLegend = false;
		} else {
			boolDisplayLegend = true;
		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayLiveGraph" ) {
		if ( mqttpayload == 0) {
			$("#thegraph").hide();
			boolDisplayLiveGraph = false;
		} else {
			$("#thegraph").show();
			boolDisplayLiveGraph = true;
		}
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayEvu" ) {
		if ( mqttpayload == 1) {
			boolDisplayEvu = false;
			hideevu = "foo";
		} else {
			boolDisplayEvu = true;
			hideevu = "Bezug";
		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayPv" ) {
		if ( mqttpayload == 1) {
			boolDisplayPv = false;
			hidepv = "foo";
		} else {
			boolDisplayPv = true;
			hidepv = "PV";
		}
		checkgraphload();
	}
	else if ( mqttmsg.match( /^openwb\/graph\/booldisplaylp[1-9][0-9]*$/i ) ) {
		// matches to all messages containing "openwb/graph/booldisplaylp#"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		// now call functions or set variables corresponding to the index
		if ( mqttpayload == 1) {
			window["boolDisplayLp"+index] = false;
			window["hidelp"+index] = "foo";
		} else {
			window["boolDisplayLp"+index] = true;
			window["hidelp"+index] = "Lp" + index;
		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayLpAll" ) {
		if ( mqttpayload == 1) {
			boolDisplayLpAll = false;
			hidelpa = "foo";
		} else {
			boolDisplayLpAll = true;
			hidelpa = "LP Gesamt";
		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplaySpeicher" ) {
		if ( mqttpayload == 1) {
			boolDisplaySpeicher = false;
			hidespeicher = "foo";
		} else {
			hidespeicher = "Speicherleistung";
			boolDisplaySpeicher = true;
		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplaySpeicherSoc" ) {
		if ( mqttpayload == 1) {
			hidespeichersoc = "foo";
			boolDisplaySpeicherSoc = false;
		} else {
			hidespeichersoc = "Speicher SoC";
			boolDisplaySpeicherSoc = true;
		}
		checkgraphload();
	}
	else if ( mqttmsg.match( /^openwb\/graph\/booldisplaylp[1-9][0-9]*soc$/i ) ) {
		// matches to all messages containing "openwb/graph/booldisplaylp#soc"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		if ( mqttpayload == 1) {
			$("#socenabledlp"+index).show();
			window["boolDisplayLp"+index+"Soc"] = false;
			window["hidelp"+index+"soc"] = "foo";
		} else {
			$("#socenabledlp"+index).hide();
			window["boolDisplayLp"+index+"Soc"] = true;
			window["hidelp"+index+"soc"] = "LP"+index+" SoC";
		}
		checkgraphload();
	}
	else if ( mqttmsg.match( /^openwb\/graph\/booldisplayload[1-9][0-9]*$/i ) ) {
		// matches to all messages containing "openwb/graph/booldisplayload#"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		// now call functions or set variables corresponding to the index
		if ( mqttpayload == 1) {
			window["hideload"+index] = "foo";
			window["boolDisplayLoad"+index] = false;
		} else {
			window["hideload"+index] = "Verbraucher " + index;
			window["boolDisplayLoad"+index] = true;
		}
		checkgraphload();
	}
	else if ( mqttmsg.match( /^openwb\/graph\/[1-9][0-9]*alllivevalues$/i ) ) {
		// matches to all messages containing "openwb/graph/#alllivevalues"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		// now call functions or set variables corresponding to the index
		if (initialread == 0) {
			window["all"+index+"p"] = mqttpayload;
			window["all"+index] = 1;
			putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/graph/lastlivevalues" ) {
		if ( initialread > 0) {
			updateGraph(mqttpayload);
		}
	}
}  // end processGraphMessages

function processEvuMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/evu
	// called by handlevar
	if ( mqttmsg == "openWB/evu/W" ) {
	    var powerEvu = mqttpayload;
	    var powerEvu = parseInt(powerEvu, 10);
		if ( isNaN(powerEvu) || powerEvu == 0 ) {
			powerEvu = "0 W";
		} else if (powerEvu > 0) {
	    	if (powerEvu > 999) {
		    	powerEvu = (powerEvu / 1000).toFixed(2);
	    	    powerEvu += " kW Bezug";
	    	} else {
				powerEvu += " W Bezug";
			}
    	} else {
    	    powerEvu *= -1;
			if (powerEvu > 999) {
		    	powerEvu = (powerEvu / 1000).toFixed(2);
	    	    powerEvu += " kW Einspeisung";
	    	} else {
				powerEvu += " W Einspeisung";
			}
    	}
	    $("#bezug").text(powerEvu);
	 }
}

function processGlobalMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/global
	// called by handlevar
	if ( mqttmsg == "openWB/global/WHouseConsumption" ) {
		var powerHouse = parseInt(mqttpayload, 10);
		if ( isNaN(powerHouse) ) {
			powerHouse = 0;
		}
		if ( powerHouse > 999 ) {
			powerHouse = (powerHouse / 1000).toFixed(2) + " kW";
		} else {
			powerHouse += " W";
		}
		$("#hausverbrauch").text(powerHouse);
	}
	else if ( mqttmsg == "openWB/global/WAllChargePoints") {
		var isAnyEvPlugged = false;
		// show charging power only if ev is/are plugged
		for ( index = 1; index <= 8; index++) {
			if ( $("#plugstatlp" + index).is(':visible') ) {
				isAnyEvPlugged = true;
				break;
			}
		}
		if ( isAnyEvPlugged ) {
			var powerAllLp = parseInt(mqttpayload, 10);
			if ( isNaN(powerAllLp) ) {
				powerAllLp = 0;
			}
			if (powerAllLp > 999) {
				powerAllLp = (powerAllLp / 1000).toFixed(2) + " kW";
			} else {
				powerAllLp += " W";
			}
		} else {
			var powerAllLp = "0 W";
		}
		$("#powerAllLp").text(powerAllLp);
	}
	else if ( mqttmsg == "openWB/global/strLastmanagementActive" ) {
		if ( mqttpayload.length >= 5 ) {
			// if there is info-text in payload for topic, show the text
			$("#lastregelungaktiv").text(mqttpayload);
		} else {
			// if there is no text, show nothing (hides row)
			$("#lastregelungaktiv").text("");
		}
	}
	else if ( mqttmsg == "openWB/global/awattar/pricelist" ) {
		// read awattar values and trigger graph creation
		// loadawattargraph will show awattardiv is awataraktiv=1 in openwb.conf
		// graph will be redrawn after 5 minutes (new data pushed from cron5min.sh)
		var csvaData = [];
		var rawacsv = mqttpayload.split(/\r?\n|\r/);
		for (var i = 0; i < rawacsv.length; i++) {
			  csvaData.push(rawacsv[i].split(","));
		}
		awattartime = getCol(csvaData, 0);
		graphawattarprice = getCol(csvaData, 1);
		loadawattargraph();
	}
	else if ( mqttmsg == "openWB/global/awattar/MaxPriceForCharging" ) {
		$("#awattar1s").val(mqttpayload);
		$("#awattar1l").text(mqttpayload);
	}
	else if ( mqttmsg == "openWB/global/ChargeMode" ) {
		// set button colors depending on charge mode
		switch (mqttpayload) {
			case "0":
				// mode sofort
				$("#chargeModeSelect").text(">> Sofortladen <<");
				$(".chargeModeBtn").removeClass("btn-green");
				$("#chargeModeSofortBtn").addClass("btn-green");
				$("#targetChargingProgress").show();
				$("#sofortladenEinstellungen").show();
				break;
			case "1":
				// mode min+pv
				$("#chargeModeSelect").text(">> Min+PV-Laden <<");
				$(".chargeModeBtn").removeClass("btn-green");
				$("#chargeModeMinPVBtn").addClass("btn-green");
				$("#targetChargingProgress").hide();
				$("#sofortladenEinstellungen").hide();
				break;
			case "2":
				// mode pv
				$("#chargeModeSelect").text(">> PV-Laden <<");
				$(".chargeModeBtn").removeClass("btn-green");
				$("#chargeModePVBtn").addClass("btn-green");
				$("#targetChargingProgress").hide();
				$("#sofortladenEinstellungen").hide();
				break;
			case "3":
				// mode stop
				$("#chargeModeSelect").text(">> Stop <<");
				$(".chargeModeBtn").removeClass("btn-green");
				$("#chargeModeStopBtn").addClass("btn-green");
				$("#targetChargingProgress").hide();
				$("#sofortladenEinstellungen").hide();
				break;
			case "4":
				// mode standby
				$("#chargeModeSelect").text(">> Standby <<");
				$(".chargeModeBtn").removeClass("btn-green");
				$("#chargeModeStdbyBtn").addClass("btn-green");
				$("#targetChargingProgress").hide();
				$("#sofortladenEinstellungen").hide();
		}
	}
}

function processHousebatteryMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/housebattery
	// called by handlevar
	if ( mqttmsg == "openWB/housebattery/W" ) {
		var speicherwatt = mqttpayload;
		var speicherwatt = parseInt(speicherwatt, 10);
		if ( isNaN(speicherwatt) ) {
			speicherwatt = 0;
		}
		if ( speicherwatt == 0 ) {
			speicherwatt = "0 W";
		} else if (speicherwatt > 0) {
			if ( speicherwatt > 999 ) {
				speicherwatt = (speicherwatt / 1000).toFixed(2);
				speicherwatt = speicherwatt + " kW Ladung";
			} else {
				speicherwatt = speicherwatt + " W Ladung";
			}
		} else {
	    	speicherwatt *= -1;
			if (speicherwatt > 999) {
				speicherwatt = (speicherwatt / 1000).toFixed(2);
				speicherwatt = speicherwatt + " kW Entladung";
			} else {
				speicherwatt = speicherwatt + " W Entladung";
			}
		}
		$("#speicherleistung").text(speicherwatt);
	}
	else if ( mqttmsg == "openWB/housebattery/%Soc" ) {
		var speicherSoc = parseInt(mqttpayload, 10);
		if ( isNaN(speicherSoc) ) {
			speicherSoc = 0;
		}
		speichersoc = ", " + speicherSoc + " % SoC";
		$("#speichersoc").text(speichersoc);
	}
	else if ( mqttmsg == "openWB/housebattery/boolHouseBatteryConfigured" ) {
		if ( mqttpayload == 1 ) {
			// if housebattery is configured, show div
			$("#speicher").show();
		}
	}
}

function processSystemMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/system
	// called by handlevar
	if ( mqttmsg == "openWB/system/Timestamp") {
		var dateObject = new Date(mqttpayload * 1000);  // Unix timestamp to date-object
		var time = "&nbsp;";
		var date = "&nbsp;";
		if ( dateObject instanceof Date && !isNaN(dateObject.valueOf()) ) {
			// timestamp is valid date so process
			var HH = String(dateObject.getHours()).padStart(2, '0');
			var MM = String(dateObject.getMinutes()).padStart(2, '0');
			time = HH + ":"  + MM;
			var dd = String(dateObject.getDate()).padStart(2, '0');  // format with leading zeros
			var mm = String(dateObject.getMonth() + 1).padStart(2, '0'); //January is 0 so add +1!
			var dayOfWeek = dateObject.toLocaleDateString('de-DE', { weekday: 'short'});
			date = dayOfWeek + ", " + dd + "." + mm + "." + dateObject.getFullYear();
		}
		$("#time").text(time);
		$("#date").text(date);
	}
}

function processPvMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/pv
	// called by handlevar
	if ( mqttmsg == "openWB/pv/W") {
		var pvwatt = parseInt(mqttpayload, 10);
		if ( isNaN(pvwatt) || pvwatt > 0 ) {
			// if pv-power is not a number or positive, adjust to 0 because pv cannot consume power
			pvwatt = 0;
		}
		if ( pvwatt <= 0){
			// production is negative for calculations so adjust for display
			pvwatt *= -1;
			// adjust and add unit
			if (pvwatt > 999) {
				pvwatt = (pvwatt / 1000).toFixed(2) + " kW";
			} else {
				pvwatt += " W";
			}
		}
		$("#pvleistung").text(pvwatt);
	}
	else if ( mqttmsg == "openWB/pv/DailyYieldKwh") {
		var pvDailyYield = parseFloat(mqttpayload);
		if ( isNaN(pvDailyYield) ) {
			pvDailyYield = 0;
		}
		var pvDailyYieldStr = " (" + pvDailyYield.toFixed(2) + " kWh)";
		$("#pvdailyyield").text(pvDailyYieldStr);
	}
}

function processVerbraucherMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/Verbraucher
	// called by handlevar
}

function processSetMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/set
	// called by handlevar
}

function processLpMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/lp
	// called by handlevar
	if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/chargepointenabled$/i ) ) {
		// matches to all messages containing "openwb/lp/#/boolchargepointenabled"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		if ( mqttpayload == 0 ) {
			$("#nameLp" + index).removeClass("lpEnabledStyle").addClass("lpDisabledStyle");
		} else {
			$("#nameLp" + index).removeClass("lpDisabledStyle").addClass("lpEnabledStyle");
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/autolockconfigured$/i ) ) {
		// matches to all messages containing "openwb/lp/#/autolockconfigured"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		if ( mqttpayload == 0 ) {
			// hide icon
			$("#lp" + index + "AutolockConfigured").hide();
		} else {
			// show icon
			$("#lp" + index + "AutolockConfigured").show();
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/autolockstatus$/i ) ) {
		// matches to all messages containing "openwb/lp/#/waitingforautolock"
		// where # is an integer > 0
		// search is case insensitive
		// values used for AutolockStatus flag:
		// 0 = standby
		// 1 = waiting for autolock
		// 2 = autolock performed
		// 3 = auto-unlock performed

		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		var element = "#lp" + index + "AutolockConfigured";  // element to manipulate
		switch ( mqttpayload ) {
			case "0":
				// remove animation from span and set standard colored key icon
				$(element).removeClass("fa-lock fa-lock-open animate-alertPulsation text-red text-green");
				$(element).addClass("fa-key");
				break;
			case "1":
				// add animation to standard icon
				$(element).removeClass("fa-lock fa-lock-open text-red text-green");
				$(element).addClass("fa-key animate-alertPulsation");
				break;
			case "2":
				// add red locked icon
				$(element).removeClass("fa-lock-open fa-key animate-alertPulsation text-green");
				$(element).addClass("fa-lock text-red");
				break;
			case "3":
				// add green unlock icon
				$(element).removeClass("fa-lock fa-key animate-alertPulsation text-red");
				$(element).addClass("fa-lock-open text-green");
				break;
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolchargeatnight$/i ) ) {
		// matches to all messages containing "openwb/lp/#/boolchargeatnight"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		if ( mqttpayload == 1 ) {
			$("#nachtladenaktivlp" + index).show();
		} else {
			$("#nachtladenaktivlp" + index).hide();
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/kWhactualcharged$/i ) ) {
		// matches to all messages containing "openwb/lp/#/kWhactualcharged"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		var energyCharged = parseInt(mqttpayload, 10);
		if ( isNaN(energyCharged) ) {
			energyCharged = 0;
		}
		$("#aktgeladen" + index).text(energyCharged+" kWh");
		$("prog" + index).val(energyCharged);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/w$/i ) ) {
		// actual charing power at respective charge point
		// matches to all messages containing "openwb/lp/#/w"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		if ( $("#plugstatlp" + index).is(':visible') ) {
			// only show value if ev is plugged in
			var actualPower = parseInt(mqttpayload, 10);
			if ( isNaN(actualPower) ) {
				actualPower = 0;
			}
			if (actualPower > 999) {
				actualPower = (actualPower / 1000).toFixed(2);
				actualPower += " kW";
			} else {
				actualPower += " W";
			}
		} else {
			var actualPower = "0 W"
		}
		$("#actualPowerLp" + index).text(actualPower);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/kWhchargedsinceplugged$/i ) ) {
		// energy charged since ev was plugged in
		// also calculates and displays km charged
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		var energyCharged = parseFloat(mqttpayload, 10);
		if ( isNaN(energyCharged) ) {
			energyCharged = 0;
		}
		$("#energyChargedLp" + index).text(energyCharged.toFixed(1) + " kWh");
		var consumption = $("#kmChargedLp" + index).attr("consumption");
		var kmCharged = "";
		if ( !isNaN(consumption) && consumption > 0 ) {
			kmCharged = (energyCharged / consumption) * 100;
			kmCharged = " / " + kmCharged.toFixed(1) + " km";
		}
		$("#kmChargedLp" + index).text(kmCharged);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/energyconsumptionper100km$/i ) ) {
		// store configured value in element attribute
		// to calculate charged km upon receipt of charged energy
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		var consumption = parseFloat(mqttpayload);
		if ( isNaN(consumption) ) {
			consumption = 0;
		}
		$("#kmChargedLp" + index).attr("consumption", consumption);

		// if already energyCharged-displayed, update kmCharged
		var energyCharged = parseFloat($("#energyChargedLp" + index).text());
		var kmCharged = "";
		if ( !isNaN(energyCharged) && consumption > 0 ) {
			kmCharged = (energyCharged / consumption) * 100;
			kmCharged = " / " + kmCharged.toFixed(1) + " km";
		}
		$("#kmChargedLp" + index).text(kmCharged);

	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/timeremaining$/i ) ) {
		// time remaining for charging to target value
		// matches to all messages containing "openwb/lp/#/timeremaining"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		$("#restzeitlp" + index).text(mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolplugstat$/i ) ) {
		// matches to all messages containing "openwb/lp/#/boolplugstat"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		if ( mqttpayload == 1 ) {
			$("#plugstatlp" + index).show();
		} else {
			$("#plugstatlp" + index).addClass("text-white").hide();
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolchargestat$/i ) ) {
		// matches to all messages containing "openwb/lp/#/boolchargestat"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		if ( mqttpayload == 1 ) {
			$("#plugstatlp" + index + ":visible").removeClass("text-white").addClass("text-green");
			$("#socstatlp" + index).removeClass("text-black").addClass("text-green");
		} else {
			$("#plugstatlp" + index + ":visible").removeClass("text-green").addClass("text-white");
			$("#socstatlp" + index).removeClass("text-green").addClass("text-black");
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/\%soc$/i ) ) {
		// soc of ev at respective charge point
		// matches to all messages containing "openwb/lp/#/%soc"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		var soc = parseInt(mqttpayload, 10);
		if ( isNaN(soc) ) {
			soc = 0;
		}
		window["lp" + index + "soc"] = soc;
		$("#socLp" + index).text(soc + " %");
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/chargestatus$/i ) ) {
		// matches to all messages containing "openwb/lp/#/chargestatus"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		if ($("#stationlp" + index).length > 0) {
			if (mqttpayload == 1) {
				$("#stationlp" + index).removeClass("text-blue").addClass("text-green");
			} else {
				$("#stationlp" + index).removeClass("text-green").addClass("text-blue");
			}
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/adirectmodeamps$/i ) ) {
		// matches to all messages containing "openwb/lp/#/adirectmodeamps"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		var current = parseInt(mqttpayload, 10);
		if ( isNaN(current) ) {
			current = 0;
		}
		$("#sofortlllp" + index + "s").val(current);
		$("sofortlllp" + index + "l").text(current);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/strchargepointname$/i ) ) {
		// matches to all messages containing "openwb/lp/#/strchargepointname"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		// fill span-tags from class=strChargePointName with respective payload-string
		// and set the div visibility from hidden to visible
		var ele = $(".nameLp"+index);
	    for( var i=0; i<ele.length; i++ ) {
	      	ele[i].textContent = mqttpayload;
	    }
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolsocconfigured$/i ) ) {
		// is a soc-module configured for respective charge point
		// matches to all messages containing "openwb/lp/#/boolsocconfigured"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		// change visibility of div
		if (mqttpayload == 1) {
			$("#socNotConfiguredLp" + index).hide();
			$("#socConfiguredLp" + index).show();
		}
	}
}
