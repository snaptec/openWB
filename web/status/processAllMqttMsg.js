/**
 * Functions to update graph and gui values via MQTT-messages
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

function getIndex(topic) {
	// get occurence of numbers between / / in topic
	// since this is supposed to be the index like in openwb/lp/4/w
	// no lookbehind supported by safari, so workaround with replace needed
	var index = topic.match(/(?:\/)([0-9]+)(?=\/)/g)[0].replace(/[^0-9]+/g, '');
	if ( typeof index === 'undefined' ) {
		index = '';
	}
	return index;
}

function handlevar(mqttmsg, mqttpayload) {
	// receives all messages and calls respective function to process them
	processPreloader(mqttmsg);
	if ( mqttmsg.match( /^openwb\/lp\//i) ) {
		processLpMsg(mqttmsg, mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/evu\//i) ) {
		processEvuMsg(mqttmsg, mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/pv\//i) ) {
		processPvMsg(mqttmsg, mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/Verbraucher\//i) ) {
		processVerbraucherMsg(mqttmsg, mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/housebattery\//i) ) {
		processBatMsg(mqttmsg, mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/global\//i) ) {
		processGlobalMsg(mqttmsg, mqttpayload);
	}
	else {
		console.log("Unknown topic: "+mqttmsg+": "+mqttpayload);
	}
}  // end handlevar

function processGlobalMsg (mqttmsg, mqttpayload) {
	switch(mqttmsg){
		case "openWB/global/WAllChargePoints":
			directShow(mqttpayload, '#ladeleistungAll');
			noZeroShow(mqttpayload, '#ladeleistungAll');
			break;
		case "openWB/global/kWhCounterAllChargePoints":
			directShow(mqttpayload, '#kWhCounterAll');
			noZeroShow(mqttpayload, '#kWhCounterAll');
			break;
		default:
			break;
	}
}

function processEvuMsg (mqttmsg, mqttpayload) {
	switch(mqttmsg){
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
			noZeroShow($('#einspeisungkwhdiv').text(), '#einspeisungkwhdiv');
			break;
		case "openWB/evu/WhImported":
			kShow(mqttpayload, "#bezugkwhdiv");
			noZeroShow($('#bezugkwhdiv').text(), '#bezugkwhdiv');
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
			noZeroShow(mqttpayload, '#evuhzdiv');
			break;
		case "openWB/evu/PfPhase1":
			directShow(mqttpayload, '#evupf1div');
			visibilityRow('#powerfaktorEvuStatusId', '#evupf1div', '#evupf2div', '#evupf3div');
			break;
		case "openWB/evu/PfPhase2":
			directShow(mqttpayload, '#evupf2div');
			visibilityRow('#powerfaktorEvuStatusId', '#evupf1div', '#evupf2div', '#evupf3div');
			break;
		case "openWB/evu/PfPhase3":
			directShow(mqttpayload, '#evupf3div');
			visibilityRow('#powerfaktorEvuStatusId', '#evupf1div', '#evupf2div', '#evupf3div');
			break;
	}
}

function processPvMsg (mqttmsg, mqttpayload) {
	switch(mqttmsg){
		case "openWB/pv/boolPVConfigured":
			visibilityCard('#pvGes', mqttpayload);
			visibilityCard('#inverter1', 0);
			visibilityCard('#inverter2', 0);
			break;
		case "openWB/pv/CounterTillStartPvCharging":
			noZeroShow(mqttpayload, '#pvcounterdiv');
			break;
		case "openWB/pv/W":
			invertShow(mqttpayload, '#pvwattdiv');
			break;
		case "openWB/pv/WhCounter":
			kShow(mqttpayload, '#pvkwhdiv');
			noZeroShow($('#pvkwhdiv').text(), '#pvkwhdiv');
			break;
		case "openWB/pv/DailyYieldKwh":
			directShow(mqttpayload, '#daily_pvkwhdiv');
			noZeroShow($('#daily_pvkwhdiv').text(), '#daily_pvkwhdiv');
			break;
		case "openWB/pv/MonthlyYieldKwh":
			directShow(mqttpayload, '#monthly_pvkwhdiv');
			noZeroShow($('#monthly_pvkwhdiv').text(), '#monthly_pvkwhdiv');
			break;
		case "openWB/pv/YearlyYieldKwh":
			directShow(mqttpayload, '#yearly_pvkwhdiv');
			noZeroShow($('#yearly_pvkwhdiv').text(), '#yearly_pvkwhdiv');
			break;
		case "openWB/pv/Modul1W":
			invertShow(mqttpayload, '#inverter1 .pvwattdiv');
			break;
		case "openWB/pv/Modul2W":
			invertShow(mqttpayload, '#inverter2 .pvwattdiv');
			break;
	}
}

function processBatMsg (mqttmsg, mqttpayload) {
	switch(mqttmsg){
		case "openWB/housebattery/WhImported":
			kShow(mqttpayload, '#speicherikwhdiv');
			noZeroShow($('#speicherikwhdiv').text(), '#speicherikwhdiv');
			break;
		case "openWB/housebattery/WhExported":
			kShow(mqttpayload, '#speicherekwhdiv');
			noZeroShow($('#speicherekwhdiv').text(), '#speicherekwhdiv');
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
	}
}

function processVerbraucherMsg (mqttmsg, mqttpayload) {
	var index = getIndex(mqttmsg);  // extract number between two / /
	if ( mqttmsg.match( /^openwb\/Verbraucher\/[1-2]\/Configured$/i ) ) {
		visibilityCard('#loads'+index, mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/Verbraucher\/[1-2]\/Watt$/i ) ) {
		directShow(mqttpayload, '#loads'+index+' .verbraucherWatt');
	}
	else if ( mqttmsg.match( /^openwb\/Verbraucher\/[1-2]\/WhImported$/i ) ) {
		kShow(mqttpayload, '#loads'+index+' .importVerbraucher');
		noZeroShow($('#loads'+index+' .importVerbraucher').text(), '#loads'+index+' .importVerbraucher');
	}
	else if ( mqttmsg.match( /^openwb\/Verbraucher\/[1-2]\/WhExported$/i ) ) {
		kShow(mqttpayload, '#loads'+index+' .exportVerbraucher');
		noZeroShow($('#loads'+index+' .exportVerbraucher').text(), '#loads'+index+' .exportVerbraucher');
	}
}

function processLpMsg (mqttmsg, mqttpayload) {
	var index = getIndex(mqttmsg);  // extract number between two / /
	if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolChargePointConfigured$/i ) ) {
		visibilityCard('#lp' + index, mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/APhase1$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .stromstaerkeP1');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/APhase2$/i ) ) {		
		directShow(mqttpayload, '#lp' + index + ' .stromstaerkeP2');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/APhase3$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .stromstaerkeP3');
	} 
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/AConfigured$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .stromvorgabe');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/kWhCounter$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .kWhCounter');
		noZeroShow($('#lp' + index + ' .kWhCounter').text(), '#lp' + index + ' .kWhCounter');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/VPhase1$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .spannungP1');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/VPhase2$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .spannungP2');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/VPhase3$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .spannungP3');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/W$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .ladeleistung');
	}
	else {
		switch (mqttmsg) {
			case "openWB/lp/1/PfPhase1":
				directShow(mqttpayload, '#lp1 .powerFaktorP1');
				visibilityRow('#lp1 .powerFaktorRow', '#lp1 .powerFaktorP1', '#lp1 .powerFaktorP2', '#lp1 .powerFaktorP3');
				// bei allen anderen LPs diese Zeilen ausblenden
				hideSection('#lp2 .powerFaktorRow');
				hideSection('#lp3 .powerFaktorRow');
				hideSection('#lp4 .powerFaktorRow');
				hideSection('#lp5 .powerFaktorRow');
				hideSection('#lp6 .powerFaktorRow');
				hideSection('#lp7 .powerFaktorRow');
				hideSection('#lp8 .powerFaktorRow');
				break;
			case "openWB/lp/1/PfPhase2":
				directShow(mqttpayload, '#lp1 .powerFaktorP2');
				visibilityRow('#lp1 .powerFaktorRow', '#lp1 .powerFaktorP1', '#lp1 .powerFaktorP2', '#lp1 .powerFaktorP3');
				// bei allen anderen LPs diese Zeilen ausblenden
				hideSection('#lp2 .powerFaktorRow');
				hideSection('#lp3 .powerFaktorRow');
				hideSection('#lp4 .powerFaktorRow');
				hideSection('#lp5 .powerFaktorRow');
				hideSection('#lp6 .powerFaktorRow');
				hideSection('#lp7 .powerFaktorRow');
				hideSection('#lp8 .powerFaktorRow');
				break;
			case "openWB/lp/1/PfPhase3":
				directShow(mqttpayload, '#lp1 .powerFaktorP3');
				visibilityRow('#lp1 .powerFaktorRow', '#lp1 .powerFaktorP1', '#lp1 .powerFaktorP2', '#lp1 .powerFaktorP3');
				// bei allen anderen LPs diese Zeilen ausblenden
				hideSection('#lp2 .powerFaktorRow');
				hideSection('#lp3 .powerFaktorRow');
				hideSection('#lp4 .powerFaktorRow');
				hideSection('#lp5 .powerFaktorRow');
				hideSection('#lp6 .powerFaktorRow');
				hideSection('#lp7 .powerFaktorRow');
				hideSection('#lp8 .powerFaktorRow');
				break;
			case "openWB/lp/1/%Soc":
				directShow(mqttpayload, '#lp1 .soc');
				visibilityValue('#socRow', '#lp1 .soc');
				// bei allen anderen LPs diese Zeilen ausblenden
				hideSection('#lp2 .socRow');
				hideSection('#lp3 .socRow');
				hideSection('#lp4 .socRow');
				hideSection('#lp5 .socRow');
				hideSection('#lp6 .socRow');
				hideSection('#lp7 .socRow');
				hideSection('#lp8 .socRow');
				break;
			default:
				break;
		}
	}
}

// don't parse value
function directShow(mqttpayload, variable) {
		var value = parseFloat(mqttpayload);
		if ( isNaN(value) ) {
			value = 0;
		}
		var valueStr = value.toLocaleString(undefined) ;
		$(variable).text(valueStr);
}

// show missing value oder zero value as --
function noZeroShow(mqttpayload, variable) {
	var value = parseFloat(mqttpayload);
	if ( isNaN(value) || (value == 0) ) {
		valueStr = "--";
		$(variable).text(valueStr);
	}
}

//show with imp/exp
function impExpShow(mqttpayload, variable) {
	// zur Anzeige Wert um "Bezug"/"Einspeisung" ergänzen
	var value = parseInt(mqttpayload);
	var valueStr = "";
	if(value<0) {
		value = value * -1;
		valueStr = value.toLocaleString(undefined)+" (E)";
	} else if (value>0) {
		valueStr = value.toLocaleString(undefined)+" (B)";
	} else  {
		// Bezug = 0
		valueStr = value.toLocaleString(undefined);
	}
	$(variable).text(valueStr);
}

// show value as kilo
function kShow(mqttpayload, variable) {
	var value = parseFloat(mqttpayload);
	value = (value / 1000);
	var valueStr = value.toLocaleString({maximumFractionDigits: 3}) ;
	$(variable).text(valueStr);
}

// multiply value with -1
function invertShow(mqttpayload, variable) {
	var value = parseInt(mqttpayload) * -1;
	var valueStr = value.toLocaleString(undefined) ;
	$(variable).text(valueStr);
}

//show only values over 100
//Der String ist mit einem Tausender-Punkt versehen. Daher den Payload für die if-Abfrage verwenden.
function visibilityMin(row, mqttpayload) {
	var value = parseFloat(mqttpayload) * -1;
	if (value>100) { 
		showSection(row);
	}
	else {
		hideSection(row);
	}
}

//show/hide row with only one value
function visibilityValue(row, variable){
	var value = parseFloat($(variable).text()); // zu Berücksichtigung von 0,00
	if (( value != 0) && ( $(variable).text() != "")) {
		showSection(row);
	}
	else {
		hideSection(row);
	}
}

//show/hide complete row, if all three values are zero or empty
function visibilityRow(row, var1, var2, var3) {
	var val1 = parseFloat($(var1).text()); // zu Berücksichtigung von 0,00
	var val2 = parseFloat($(var2).text());
	var val3 = parseFloat($(var3).text());
	if ( ( (val1 == 0) || ($(var1).text() == "") ) &&
		 ( (val2 == 0) || ($(var2).text() == "") ) &&
		 ( (val3 == 0) || ($(var3).text() == "") ) ) {
		hideSection(row);
	}
	else {
		showSection(row);
	}
}

//show/hide card, if lp is configured
function visibilityCard(card, mqttpayload) {
	var value = parseInt(mqttpayload);
	if (value == 0)
	{
		hideSection(card);
	}
	else {
		showSection(card);
	}
}
