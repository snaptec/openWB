/**
 * Functions to update graph and gui values via MQTT-messages
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 * @author Lutz Bender
 * @author Lena Kümmel
 */

function formatJsonString(str) {
	try {
		parsed = JSON.parse(str)
		if (typeof parsed === 'string') {
			return parsed
		}
		// if it is not a string, we just use the json as supplied
	} catch (e) {
		// ignore error - just use the original text
	}
	return str
}

function getIndex(topic) {
	// get occurrence of numbers between / / in topic
	// since this is supposed to be the index like in openwb/lp/4/w
	// no lookbehind supported by safari, so workaround with replace needed
	var index = topic.match(/(?:\/)([0-9]+)(?=\/)/g)[0].replace(/[^0-9]+/g, '');
	if (typeof index === 'undefined') {
		index = '';
	}
	return index;
}

function handlevar(mqttmsg, mqttpayload) {
	// receives all messages and calls respective function to process them
	processPreloader(mqttmsg);
	if (mqttmsg.match(/^openwb\/lp\//i)) {
		processLpMsg(mqttmsg, mqttpayload);
	}
	else if (mqttmsg.match(/^openwb\/evu\//i)) {
		processEvuMsg(mqttmsg, mqttpayload);
	}
	else if (mqttmsg.match(/^openwb\/pv\//i)) {
		processPvMsg(mqttmsg, mqttpayload);
	}
	else if (mqttmsg.match(/^openwb\/Verbraucher\//i)) {
		processVerbraucherMsg(mqttmsg, mqttpayload);
	}
	else if (mqttmsg.match(/^openwb\/housebattery\//i)) {
		processBatMsg(mqttmsg, mqttpayload);
	}
	else if (mqttmsg.match(/^openwb\/SmartHome\//i)) {
		processSmartHomeMsg(mqttmsg, mqttpayload);
	}

	else if (mqttmsg.match(/^openwb\/global\//i)) {
		processGlobalMsg(mqttmsg, mqttpayload);
	}
	else {
		console.log("Unknown topic: " + mqttmsg + ": " + mqttpayload);
	}
}  // end handlevar

function processGlobalMsg(mqttmsg, mqttpayload) {
	switch (mqttmsg) {
		case "openWB/global/WAllChargePoints":
			directShow(mqttpayload, '#ladeleistungAll');
			break;
		case "openWB/global/kWhCounterAllChargePoints":
			fractionDigitsShow(mqttpayload, '#kWhCounterAll');
			break;
		default:
			break;
	}
}

function processEvuMsg(mqttmsg, mqttpayload) {
	switch (mqttmsg) {
		case "openWB/evu/ASchieflast":
			directShow(mqttpayload, '#schieflastdiv');
			break;
		case "openWB/evu/APhase1":
			directShow(mqttpayload, '#bezuga1div');
			break;
		case "openWB/evu/APhase2":
			directShow(mqttpayload, '#bezuga2div');
			break;
		case "openWB/evu/APhase3":
			directShow(mqttpayload, '#bezuga3div');
			break;
		case "openWB/evu/WPhase1":
			impExpShow(mqttpayload, '#bezugw1div');
			break;
		case "openWB/evu/WPhase2":
			impExpShow(mqttpayload, '#bezugw2div');
			break;
		case "openWB/evu/WPhase3":
			impExpShow(mqttpayload, '#bezugw3div');
			break;
		case "openWB/evu/W":
			impExpShow(mqttpayload, '#wattbezugdiv');
			break;
		case "openWB/evu/WhExported":
			kShow(mqttpayload, "#einspeisungkwhdiv");
			break;
		case "openWB/evu/WhImported":
			kShow(mqttpayload, "#bezugkwhdiv");
			break;
		case "openWB/evu/VPhase1":
			directShow(mqttpayload, '#evuv1div');
			break;
		case "openWB/evu/VPhase2":
			directShow(mqttpayload, '#evuv2div');
			break;
		case "openWB/evu/VPhase3":
			directShow(mqttpayload, '#evuv3div');
			break;
		case "openWB/evu/Hz":
			directShow(mqttpayload, '#evuhzdiv');
			break;
		case "openWB/evu/PfPhase1":
			directShow(mqttpayload, '#evupf1div');
			break;
		case "openWB/evu/PfPhase2":
			directShow(mqttpayload, '#evupf2div');
			break;
		case "openWB/evu/PfPhase3":
			directShow(mqttpayload, '#evupf3div');
			break;
		case "openWB/evu/faultState":
			setWarningLevel(mqttpayload, '#faultStrEvuRow');
			break;
		case "openWB/evu/faultStr":
			textShow(formatJsonString(mqttpayload), '#faultStrEvu');
			break;
	}
}

function processPvMsg(mqttmsg, mqttpayload) {
	if (mqttmsg.match(/^openWB\/pv\/[0-9]+\/.*$/i)) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		if (mqttmsg.match(/^openWB\/pv\/[0-9]+\/W$/i)) {
			absShow(mqttpayload, '#inverter' + index + ' .powerInverter');
		}
		else if (mqttmsg.match(/^openWB\/pv\/[0-9]+\/WhCounter$/i)) {
			kShow(mqttpayload, '#inverter' + index + ' .yieldInverter');
		}
		// no data in openWB 1.x
		// else if ( mqttmsg.match(/^openWB\/pv\/[0-9]+\/DailyYieldKwh$/i) )
		// {
		// 	fractionDigitsShow(mqttpayload, '#inverter' + index + ' .dYieldInverter');
		// }
		// else if ( mqttmsg.match(/^openWB\/pv\/[0-9]+\/MonthlyYieldKwh$/i) )
		// {
		// 	fractionDigitsShow(mqttpayload, '#inverter' + index + ' .mYieldInverter');
		// }
		// else if ( mqttmsg.match(/^openWB\/pv\/[0-9]+\/YearlyYieldKwh$/i) )
		// {
		// 	fractionDigitsShow(mqttpayload, '#inverter' + index + ' .yYieldInverter');
		// }
		else if (mqttmsg.match(/^openWB\/pv\/[0-9]+\/faultState$/i)) {
			setWarningLevel(mqttpayload, '#inverter' + index + ' .faultStrPvRow');
		}
		else if (mqttmsg.match(/^openWB\/pv\/[0-9]+\/faultStr$/i)) {
			textShow(formatJsonString(mqttpayload), '#inverter' + index + ' .faultStrPv');
		}
		else if (mqttmsg.match(/^openWB\/pv\/[0-9]+\/boolPVConfigured$/i)) {
			visibilityCard('#inverter' + index, mqttpayload);
		}
	}
	else {
		switch (mqttmsg) {
			case "openWB/pv/CounterTillStartPvCharging":
				directShow(mqttpayload, '#pvcounterdiv');
				break;
			case "openWB/pv/W":
				absShow(mqttpayload, '#pvwattdiv');
				break;
			case "openWB/pv/WhCounter":
				kShow(mqttpayload, '#pvkwhdiv');
				break;
			case "openWB/pv/DailyYieldKwh":
				fractionDigitsShow(mqttpayload, '#daily_pvkwhdiv');
				break;
			case "openWB/pv/MonthlyYieldKwh":
				fractionDigitsShow(mqttpayload, '#monthly_pvkwhdiv');
				if (mqttpayload != "0") {
					showSection("#monatsertragRow");
				} else {
					hideSection("#monatsertragRow");
				}
				break;
			case "openWB/pv/YearlyYieldKwh":
				fractionDigitsShow(mqttpayload, '#yearly_pvkwhdiv');
				if (mqttpayload != "0") {
					showSection("#jahresertragRow");
				} else {
					hideSection("#jahresertragRow");
				}
				break;
		}
	}
}

function processBatMsg(mqttmsg, mqttpayload) {
	switch (mqttmsg) {
		case "openWB/housebattery/boolHouseBatteryConfigured":
			visibilityCard('#speicher', mqttpayload);
			break;
		case "openWB/housebattery/WhImported":
			kShow(mqttpayload, '#speicherikwhdiv');
			break;
		case "openWB/housebattery/WhExported":
			kShow(mqttpayload, '#speicherekwhdiv');
			break;
		case "openWB/housebattery/W":
			directShow(mqttpayload, '#wBatDiv');
			break;
		case "openWB/housebattery/%Soc":
			directShow(mqttpayload, '#socBatDiv');
			break;
		case "openWB/housebattery/boolHouseBatteryConfigured":
			visibilityCard('#speicher', mqttpayload);
			break;
		case "openWB/housebattery/faultState":
			setWarningLevel(mqttpayload, '#faultStrBatRow');
			break;
		case "openWB/housebattery/faultStr":
			textShow(formatJsonString(mqttpayload), '#faultStrBat');
			break;
	}
}

function processSmartHomeMsg(mqttmsg, mqttpayload) {
	switch (mqttmsg) {
		case "openWB/SmartHome/Status/maxspeicherladung":
			directShow(mqttpayload, '#wmaxspeicherladung');
			break;
		case "openWB/SmartHome/Status/wattschalt":
			directShow(mqttpayload, '#wwattschalt');
			break;
		case "openWB/SmartHome/Status/wattnichtschalt":
			directShow(mqttpayload, '#wwattnichtschalt');
			break;
		case "openWB/SmartHome/Status/uberschuss":
			directShow(mqttpayload, '#wuberschuss');
			break;
		case "openWB/SmartHome/Status/uberschussoffset":
			directShow(mqttpayload, '#wuberschussoffset');
			break;
	}
}

function processVerbraucherMsg(mqttmsg, mqttpayload) {
	var index = getIndex(mqttmsg);  // extract number between two / /
	if (mqttmsg.match(/^openwb\/Verbraucher\/[1-2]\/Configured$/i)) {
		visibilityCard('#loads' + index, mqttpayload);
	}
	else if (mqttmsg.match(/^openwb\/Verbraucher\/[1-2]\/Watt$/i)) {
		directShow(mqttpayload, '#loads' + index + ' .verbraucherWatt');
	}
	else if (mqttmsg.match(/^openwb\/Verbraucher\/[1-2]\/WhImported$/i)) {
		kShow(mqttpayload, '#loads' + index + ' .importVerbraucher');
	}
	else if (mqttmsg.match(/^openwb\/Verbraucher\/[1-2]\/WhExported$/i)) {
		kShow(mqttpayload, '#loads' + index + ' .exportVerbraucher');
	}
}

function processLpMsg(mqttmsg, mqttpayload) {
	var index = getIndex(mqttmsg);  // extract number between two / /
	if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolChargePointConfigured$/i)) {
		visibilityCard('#lp' + index, mqttpayload);
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/APhase1$/i)) {
		directShow(mqttpayload, '#lp' + index + ' .stromstaerkeP1');
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/APhase2$/i)) {
		directShow(mqttpayload, '#lp' + index + ' .stromstaerkeP2');
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/APhase3$/i)) {
		directShow(mqttpayload, '#lp' + index + ' .stromstaerkeP3');
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/AConfigured$/i)) {
		directShow(mqttpayload, '#lp' + index + ' .stromvorgabe');
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/kWhCounter$/i)) {
		fractionDigitsShow(mqttpayload, '#lp' + index + ' .kWhCounter');
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/VPhase1$/i)) {
		directShow(mqttpayload, '#lp' + index + ' .spannungP1');
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/VPhase2$/i)) {
		directShow(mqttpayload, '#lp' + index + ' .spannungP2');
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/VPhase3$/i)) {
		directShow(mqttpayload, '#lp' + index + ' .spannungP3');
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/W$/i)) {
		directShow(mqttpayload, '#lp' + index + ' .ladeleistung');
	}
	else if (mqttmsg.match(/^openWB\/lp\/[1-9][0-9]*\/boolSocConfigured$/i)) {
		if (mqttpayload == "1") {
			showSection('#lp' + index + ' .socRow');
		} else {
			hideSection('#lp' + index + ' .socRow');
		}
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/%Soc$/i)) {
		directShow(mqttpayload, '#lp' + index + ' .soc');
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/faultState$/i)) {
		setWarningLevel(mqttpayload, '#lp' + index + ' .faultStrLpRow');
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/faultStr$/i)) {
		textShow(formatJsonString(mqttpayload), '#lp' + index + ' .faultStrLp');
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/socFaultState$/i)) {
		setWarningLevel(mqttpayload, '#lp' + index + ' .faultStrSocLpRow');
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/socFaultStr$/i)) {
		textShow(formatJsonString(mqttpayload), '#lp' + index + ' .faultStrSocLp');
	}
	else {
		switch (mqttmsg) {
			case "openWB/lp/1/PfPhase1":
				showSection('#lp1 .powerFaktorRow');
				directShow(mqttpayload, '#lp1 .powerFaktorP1');
				break;
			case "openWB/lp/1/PfPhase2":
				showSection('#lp1 .powerFaktorRow');
				directShow(mqttpayload, '#lp1 .powerFaktorP2');
				break;
			case "openWB/lp/1/PfPhase3":
				showSection('#lp1 .powerFaktorRow');
				directShow(mqttpayload, '#lp1 .powerFaktorP3');
				break;
			default:
				break;
		}
	}
}

// don't parse value
function directShow(mqttpayload, variable) {
	var value = parseFloat(mqttpayload);
	if (isNaN(value)) {
		value = 0;
	}
	var valueStr = value.toLocaleString(undefined);
	$(variable).text(valueStr);
}

// show missing value or zero value as --
function noZeroShow(mqttpayload, variable) {
	var value = parseFloat(mqttpayload);
	if (isNaN(value) || (value == 0)) {
		valueStr = "--";
	}
	else {
		var valueStr = value.toLocaleString(undefined);
	}
	$(variable).text(valueStr);
}

//show with imp/exp
function impExpShow(mqttpayload, variable) {
	// zur Anzeige Wert um "Bezug"/"Einspeisung" ergänzen
	var value = parseInt(mqttpayload);
	var valueStr = Math.abs(value).toLocaleString(undefined);
	if (value < 0) {
		valueStr += " (Exp.)";
	} else if (value > 0) {
		valueStr += " (Imp.)";
	}
	$(variable).text(valueStr);
}

// show value as kilo
function kShow(mqttpayload, variable) {
	var value = parseFloat(mqttpayload);
	value = (value / 1000);
	var valueStr = value.toLocaleString(undefined, { minimumFractionDigits: 3, maximumFractionDigits: 3 });
	$(variable).text(valueStr);
}

// show absolute value (always >0)
function absShow(mqttpayload, variable) {
	var value = Math.abs(parseInt(mqttpayload));
	var valueStr = value.toLocaleString(undefined);
	$(variable).text(valueStr);
}

//show kilo-payloads with 3 fraction digits
function fractionDigitsShow(mqttpayload, variable) {
	var value = parseFloat(mqttpayload);
	if (isNaN(value)) {
		value = 0;
	}
	var valueStr = value.toLocaleString(undefined, { minimumFractionDigits: 3, maximumFractionDigits: 3 });
	$(variable).text(valueStr);
}

function textShow(mqttpayload, variable) {
	$(variable).text(mqttpayload);
}

// shows table row colored regarding to the fault state
function setWarningLevel(mqttpayload, variable) {
	switch (mqttpayload) {
		case "0":
			$(variable).removeClass("text-warning").removeClass("text-danger");
			hideSection(variable);
			break;
		case "1":
			$(variable).addClass("text-warning").removeClass("text-danger");
			showSection(variable);
			break;
		case "2":
			$(variable).addClass("text-danger").removeClass("text-warning");
			showSection(variable);
			break;
	}
}

//show only values over 100
//Der String ist mit einem Tausender-Punkt versehen. Daher den Payload für die if-Abfrage verwenden.
function visibilityMin(row, mqttpayload) {
	var value = parseFloat(mqttpayload) * -1;
	if (value > 100) {
		showSection(row);
	}
	else {
		hideSection(row);
	}
}

//show/hide row with only one value
function visibilityValue(row, variable) {
	var value = parseFloat($(variable).text()); // zu Berücksichtigung von 0,00
	if ((value != 0) && ($(variable).text() != "")) {
		showSection(row);
	}
	else {
		hideSection(row);
	}
	var valueStr = value.toLocaleString(undefined, { minimumFractionDigits: 3, maximumFractionDigits: 3 });
	$(variable).text(valueStr);
}

//show/hide complete row, if all three values are zero or empty
function visibilityRow(row, var1, var2, var3) {
	var val1 = parseFloat($(var1).text()); // zu Berücksichtigung von 0,00
	var val2 = parseFloat($(var2).text());
	var val3 = parseFloat($(var3).text());
	if (((val1 == 0) || ($(var1).text() == "")) &&
		((val2 == 0) || ($(var2).text() == "")) &&
		((val3 == 0) || ($(var3).text() == ""))) {
		hideSection(row);
	}
	else {
		showSection(row);
	}
}

var lpGesCardShown = false; // flag, show lpGes-Card if any other cp than cp1 is configured
var pv1 = 0;
var pv2 = 0;

//show/hide card, if module is configured
function visibilityCard(card, mqttpayload) {
	var value = parseInt(mqttpayload);
	if (value == 0) {
		hideSection(card);
	} else {
		showSection(card);
		if ((card.match(/^[#]lp[2-8]$/i)) && lpGesCardShown == false) {
			showSection('#lpges');
			lpGesCardShown = true;
		} else if (card.match(/^[#]inverter[1-2]+$/i)) {
			if (card == "#inverter1") {
				pv1 = mqttpayload;
			} else {
				pv2 = mqttpayload;
			}

			if ((pv1 + pv2) > 0) {
				showSection('#pvGes');
			} else {
				hideSection('#pvGes');
			}
		}
	}
}
