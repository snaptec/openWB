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
	 else {
		switch(mqttmsg){
			case "openWB/evu/ASchieflast": directShow(mqttpayload, '#schieflastdiv'); visibilityValue('#schieflastEvuStatusId', '#schieflastdiv'); break;
			case "openWB/evu/APhase1": directShow(mqttpayload, '#bezuga1div'); visibilityRow('#stromstaerkeEvuStatusId', '#bezuga1div', '#bezuga2div', '#bezuga3div'); break;
			case "openWB/evu/APhase2": directShow(mqttpayload, '#bezuga2div'); visibilityRow('#stromstaerkeEvuStatusId', '#bezuga1div', '#bezuga2div', '#bezuga3div'); break;
			case "openWB/evu/APhase3": directShow(mqttpayload, '#bezuga3div'); visibilityRow('#stromstaerkeEvuStatusId', '#bezuga1div', '#bezuga2div', '#bezuga3div'); break;
			case "openWB/evu/WPhase1": impExpShow(mqttpayload, '#bezugw1div'); visibilityRow('#leistungEvuStatusId', '#bezugw1div', '#bezugw2div', '#bezugw3div'); break;
			case "openWB/evu/WPhase2": impExpShow(mqttpayload, '#bezugw2div'); visibilityRow('#leistungEvuStatusId', '#bezugw1div', '#bezugw2div', '#bezugw3div'); break;
			case "openWB/evu/WPhase3": impExpShow(mqttpayload, '#bezugw3div'); visibilityRow('#leistungEvuStatusId', '#bezugw1div', '#bezugw2div', '#bezugw3div'); break;
			case "openWB/evu/W": impExpShow(mqttpayload, '#wattbezugdiv'); visibilityValue('#gesamtleistungEvuStatusId', '#wattbezugdiv'); break;
			case "openWB/Verbraucher/1/Watt": directShow(mqttpayload, '#loads1 .verbraucherWatt'); visibilityValue('#loads1 .leistungVerbraucherRow', '#loads1 .verbraucherWatt'); break;
			case "openWB/Verbraucher/1/WhImported": kShow(mqttpayload, "#loads1 .importVerbraucher"); visibilityValue('#loads1 .importVerbraucherRow', '#loads1 .importVerbraucher'); break;
			case "openWB/Verbraucher/1/WhExported": kShow(mqttpayload, "#loads1 .exportVerbraucher"); visibilityValue('#loads1 .exportVerbraucherRow', '#loads1 .exportVerbraucher'); break;
			case "openWB/Verbraucher/2/Watt": directShow(mqttpayload, '#loads2 .verbraucherWatt'); visibilityValue('#loads2 .leistungVerbraucherRow', '#loads2 .verbraucherWatt'); break;
			case "openWB/Verbraucher/2/WhImported": kShow(mqttpayload, "#loads2 .importVerbraucher"); visibilityValue('#loads2 .importVerbraucherRow', '#loads2 .importVerbraucher'); break;
			case "openWB/Verbraucher/2/WhExported": kShow(mqttpayload, "#loads2 .exportVerbraucher"); visibilityValue('#loads2 .exportVerbraucherRow', '#loads2 .exportVerbraucher'); break;
			case "openWB/evu/WhExported": kShow(mqttpayload, "#einspeisungkwhdiv"); visibilityValue('#einspeisungEvuStatusId', "#einspeisungkwhdiv"); break;
			case "openWB/evu/WhImported": kShow(mqttpayload, "#bezugkwhdiv"); visibilityValue('#bezugEvuStatusId', "#bezugkwhdiv"); break;
			case "openWB/housebattery/WhImported": kShow(mqttpayload, '#speicherikwhdiv'); visibilityValue('#geladenRow', '#speicherikwhdiv'); break;
			case "openWB/housebattery/WhExported": kShow(mqttpayload, '#speicherekwhdiv'); visibilityValue('#entladenRow', '#speicherekwhdiv');break;
			case "openWB/pv/boolPVConfigured": visibilityCard('#pvGes', mqttpayload); visibilityCard('#inverter1', mqttpayload); visibilityCard('#inverter2', mqttpayload); break;
			case "openWB/pv/CounterTillStartPvCharging": directShow(mqttpayload, '#pvcounterdiv'); visibilityValue('#pvCounterRow', "#pvcounterdiv"); break;
			case "openWB/pv/W": invertShow(mqttpayload, '#pvkwhdiv'); visibilityMin('#gesamtertragRow', "#pvkwhdiv"); break;
			case "openWB/pv/DailyYieldKwh": directShow(mqttpayload, '#daily_pvkwhdiv'); visibilityValue('#tagesertragRow', "#daily_pvkwhdiv"); break;
			case "openWB/pv/MonthlyYieldKwh": directShow(mqttpayload, '#monthly_pvkwhdiv'); visibilityValue('#monatsertragRow', "#monthly_pvkwhdiv"); break;
			case "openWB/pv/YearlyYieldKwh": directShow(mqttpayload, '#yearly_pvkwhdiv'); visibilityValue('#jahresertragRow', "#yearly_pvkwhdiv"); break;
			case "openWB/pv/Modul1W": invertShow(mqttpayload, '#inverter1 .pvwattdiv'); visibilityValue('#inverter1 .gesamtertragPvRow', '#inverter1 .pvwattdiv'); break;
			case "openWB/pv/Modul2W": invertShow(mqttpayload, '#inverter2 .pvwattdiv'); visibilityValue('#inverter2 .gesamtertragPvRow', '#inverter2 .pvwattdiv'); break;
			case "openWB/evu/VPhase1": directShow(mqttpayload, '#evuv1div'); visibilityRow('#spannungEvuStatusId', '#evuv1div', '#evuv2div', '#evuv3div'); break;
			case "openWB/evu/VPhase2": directShow(mqttpayload, '#evuv2div'); visibilityRow('#spannungEvuStatusId', '#evuv1div', '#evuv2div', '#evuv3div'); break;
			case "openWB/evu/VPhase3": directShow(mqttpayload, '#evuv3div'); visibilityRow('#spannungEvuStatusId', '#evuv1div', '#evuv2div', '#evuv3div'); break;
			case "openWB/evu/Hz": directShow(mqttpayload, '#evuhzdiv'); visibilityValue('#frequenzEvuStatusId', '#evuhzdiv'); break;
			case "openWB/evu/PfPhase1": directShow(mqttpayload, '#evupf1div'); visibilityRow('#powerfaktorEvuStatusId', '#evupf1div', '#evupf2div', '#evupf3div'); break;
			case "openWB/evu/PfPhase2": directShow(mqttpayload, '#evupf2div'); visibilityRow('#powerfaktorEvuStatusId', '#evupf1div', '#evupf2div', '#evupf3div'); break;
			case "openWB/evu/PfPhase3": directShow(mqttpayload, '#evupf3div'); visibilityRow('#powerfaktorEvuStatusId', '#evupf1div', '#evupf2div', '#evupf3div'); break;
			case "openWB/housebattery/boolHouseBatteryConfigured": visibilityCard('#speicher', mqttpayload); break;
			case "openWB/Verbraucher/1/Configured": visibilityCard('#loads1', mqttpayload); break;
			case "openWB/Verbraucher/2/Configured": visibilityCard('#loads2', mqttpayload); break;
			case "openWB/global/WAllChargePoints": directShow(mqttpayload, '#ladeleistungAll'); visibilityValue('#ladeleistungAllRow', '#ladeleistungAll'); break;
			case "openWB/global/kWhCounterAllChargePoints": directShow(mqttpayload, '#kWhCounterAll'); visibilityValue('#kWhCounterAllRow', '#ladeleistkWhCounterAllungAll'); break;
			default: break;
		}
	}
}  // end handlevar

function processLpMsg (mqttmsg, mqttpayload) {
	var index = getIndex(mqttmsg);  // extract number between two / /
	if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolChargePointConfigured$/i ) ) {
		visibilityCard('#lp' + index, mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/APhase1$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .stromstaerkeP1'); 
		visibilityRow('#lp' + index + ' .stromstaerkeRow', '#lp' + index + ' .stromstaerkeP1', '#lp' + index + ' .stromstaerkeP2', '#lp' + index + ' .stromstaerkeP3'); 
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/APhase2$/i ) ) {		
		directShow(mqttpayload, '#lp' + index + ' .stromstaerkeP2'); 
		visibilityRow('#lp' + index + ' .stromstaerkeRow', '#lp' + index + ' .stromstaerkeP1', '#lp' + index + ' .stromstaerkeP2', '#lp' + index + ' .stromstaerkeP3'); 
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/APhase3$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .stromstaerkeP3'); 
		visibilityRow('#lp' + index + ' .stromstaerkeRow', '#lp' + index + ' .stromstaerkeP1', '#lp' + index + ' .stromstaerkeP2', '#lp' + index + ' .stromstaerkeP3'); 
	} 
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/AConfigured$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .stromvorgabe'); 
		visibilityValue('#lp' + index + ' .stromvorgabeRow', '#lp' + index + ' .stromvorgabe');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/kWhCounter$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .kWhCounter'); 
		visibilityValue('#lp' + index + ' .kWhCounterRow', '#lp' + index + ' .kWhCounter');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/VPhase1$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .spannungP1'); 
		visibilityRow('#lp' + index + ' .spannungRow', '#lp' + index + ' .spannungP1', '#lp' + index + ' .spannungP2', '#lp' + index + ' .spannungP3');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/VPhase2$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .spannungP2'); 
		visibilityRow('#lp' + index + ' .spannungRow', '#lp' + index + ' .spannungP1', '#lp' + index + ' .spannungP2', '#lp' + index + ' .spannungP3');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/VPhase3$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .spannungP3'); 
		visibilityRow('#lp' + index + ' .spannungRow', '#lp' + index + ' .spannungP1', '#lp' + index + ' .spannungP2', '#lp' + index + ' .spannungP3');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/W$/i ) ) {
		directShow(mqttpayload, '#lp' + index + ' .ladeleistung'); 
		visibilityValue('#lp' + index + ' .ladeleistungRow', '#lp' + index + ' .ladeleistung');
	}
	else 
	{
		switch (mqttmsg) {
		case "openWB/lp/1/PfPhase1": directShow(mqttpayload, '#lp1 .powerFaktorP1'); visibilityRow('#lp1 .powerFaktorRow', '#lp1 .powerFaktorP1', '#lp1 .powerFaktorP2', '#lp1 .powerFaktorP3'); 
			// bei allen anderen LPs diese Zeilen ausblenden
			hideSection('#lp2 .powerFaktorRow');
			hideSection('#lp3 .powerFaktorRow');
			hideSection('#lp4 .powerFaktorRow');
			hideSection('#lp5 .powerFaktorRow');
			hideSection('#lp6 .powerFaktorRow');
			hideSection('#lp7 .powerFaktorRow');
			hideSection('#lp8 .powerFaktorRow'); 
		break;
		case "openWB/lp/1/PfPhase2": directShow(mqttpayload, '#lp1 .powerFaktorP2'); visibilityRow('#lp1 .powerFaktorRow', '#lp1 .powerFaktorP1', '#lp1 .powerFaktorP2', '#lp1 .powerFaktorP3'); 
			// bei allen anderen LPs diese Zeilen ausblenden
			hideSection('#lp2 .powerFaktorRow');
			hideSection('#lp3 .powerFaktorRow');
			hideSection('#lp4 .powerFaktorRow');
			hideSection('#lp5 .powerFaktorRow');
			hideSection('#lp6 .powerFaktorRow');
			hideSection('#lp7 .powerFaktorRow');
			hideSection('#lp8 .powerFaktorRow'); 
			break;
		case "openWB/lp/1/PfPhase3": directShow(mqttpayload, '#lp1 .powerFaktorP3'); visibilityRow('#lp1 .powerFaktorRow', '#lp1 .powerFaktorP1', '#lp1 .powerFaktorP2', '#lp1 .powerFaktorP3'); 
			// bei allen anderen LPs diese Zeilen ausblenden
			hideSection('#lp2 .powerFaktorRow');
			hideSection('#lp3 .powerFaktorRow');
			hideSection('#lp4 .powerFaktorRow');
			hideSection('#lp5 .powerFaktorRow');
			hideSection('#lp6 .powerFaktorRow');
			hideSection('#lp7 .powerFaktorRow');
			hideSection('#lp8 .powerFaktorRow'); 
			break;
		case "openWB/lp/1/%Soc": directShow(mqttpayload, '#lp1 .soc'); visibilityValue('#socRow', '#lp1 .soc'); 
			// bei allen anderen LPs diese Zeilen ausblenden
			hideSection('#lp2 .socRow');
			hideSection('#lp3 .socRow');
			hideSection('#lp4 .socRow');
			hideSection('#lp5 .socRow');
			hideSection('#lp6 .socRow');
			hideSection('#lp7 .socRow');
			hideSection('#lp8 .socRow'); 
			break;
		default: break;
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

//show with imp/exp
function impExpShow(mqttpayload, variable) {
	// zur Anzeige Wert um "Bezug"/"Einspeisung" ergänzen
	var value = parseInt(mqttpayload);
	var valueStr = "";
	if(value<0) {
		value = value * -1;
		valueStr = valueStr+value+" (E)"
	} else if (value>0) {
		valueStr = valueStr+value+" (B)"
	} else  {
		// Bezug = 0
		valueStr = valueStr+value
	}
	$(variable).text(valueStr);
}

// show value as kilo
function kShow(mqttpayload, variable) {
	var value = parseFloat(mqttpayload);
	value = (value / 1000).toFixed(3);
	var valueStr = value.toLocaleString(undefined) ;
	$(variable).text(valueStr);
}

// multiply value with -1
function invertShow(mqttpayload, variable) {
	var value = parseInt(mqttpayload) * -1;
	var valueStr = value.toLocaleString(undefined) ;
	$(variable).text(valueStr);
}

//show only values over 100
function visibilityMin(row, variable) {
	var value = parseInt($(variable).text());
	if (value>100){
		showSection($(row));
	}
	else {
		hideSection($(row));
	}
}

//show/hide row with only one value
function visibilityValue(row, variable){
	var value = parseFloat($(variable).text()); // zu Berücksichtigung von 0,00
	if (( value != 0) && ( $(variable).text() != "")) {
		showSection($(row));
	}
	else {
		hideSection($(row));
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
		hideSection($(row));
	}
	else {
		showSection($(row));
	}
}

//show/hide card, if lp is configured
function visibilityCard(card, mqttpayload) {
	var value = parseInt(mqttpayload);
	if (value == 0)
	{
		hideSection($(card));
	}
	else {
		showSection($(card));
	}
}