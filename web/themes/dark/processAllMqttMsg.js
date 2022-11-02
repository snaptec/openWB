/**
 * Functions to update graph and gui values via MQTT-messages
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */
var graphrefreshcounter = 0;
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

function getIndex(topic) {
	// get occurrence of numbers between / / in topic
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
	if ( mqttmsg.match( /^openwb\/graph\//i ) ) { processGraphMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/evu\//i) ) { processEvuMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/global\/awattar\//i) ) { processETProviderMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/global\/ETProvider\//i) ) { processETProviderMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/global\//i) ) { processGlobalMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/housebattery\//i) ) { processHousebatteryMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/system\//i) ) { processSystemMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/pv\//i) ) { processPvMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/verbraucher\//i) ) { processVerbraucherMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/lp\//i) ) { processLpMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/hook\//i) ) { processHookMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/SmartHome\/Devices\//i) ) { processSmartHomeDevicesMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/config\/get\/SmartHome\/Devices\//i) ) { processSmartHomeDevicesConfigMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/config\/get\/sofort\/lp\//i) ) { processSofortConfigMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/config\/get\/pv\//i) ) { processPvConfigMessages(mqttmsg, mqttpayload); }
}  // end handlevar

function processETProviderMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/global
	// called by handlevar
	processPreloader(mqttmsg);
	if ( mqttmsg == 'openWB/global/ETProvider/providerName' ) {
		$('.etproviderName').text(mqttpayload);
	}
	else if ( mqttmsg == 'openWB/global/ETProvider/modulePath' ) {
		$('.etproviderLink').attr("href", "/openWB/modules/"+mqttpayload+"/stromtarifinfo/infopage.php");
	}
	else if ( mqttmsg == 'openWB/global/awattar/boolAwattarEnabled' ) {
		// sets icon, graph and price-info-field visible/invisible
		if ( mqttpayload == '1' ) {
			$('#etproviderEnabledIcon').removeClass('hide');
			$('#priceBasedCharging').removeClass('hide');
			$('#strompreis').removeClass('hide');
			$('#navStromtarifInfo').removeClass('hide');
		} else {
			$('#etproviderEnabledIcon').addClass('hide');
			$('#priceBasedCharging').addClass('hide');
			$('#strompreis').addClass('hide');
			$('#navStromtarifInfo').addClass('hide');
		}
	}
	else if ( mqttmsg == 'openWB/global/awattar/pricelist' ) {
		// read etprovider values and trigger graph creation
		// loadElectricityPriceChart will show electricityPriceChartCanvas if etprovideraktiv=1 in openwb.conf
		// graph will be redrawn after 5 minutes (new data pushed from cron5min.sh)
		var csvData = [];
		var rawcsv = mqttpayload.split(/\r?\n|\r/);
		// skip first entry: it is module-name responsible for list
		for (var i = 1; i < rawcsv.length; i++) {
			csvData.push(rawcsv[i].split(','));
		}
		// Timeline (x-Achse) ist UNIX Timestamp in UTC, deshalb Umrechnung (*1000) in Javascript-Timestamp (mit Millisekunden)
		electricityPriceTimeline = getCol(csvData, 0).map(function(x) { return x * 1000; });
		// Chartline (y-Achse) ist Preis in ct/kWh
		electricityPriceChartline = getCol(csvData, 1);

		loadElectricityPriceChart();
	}
	else if ( mqttmsg == 'openWB/global/awattar/MaxPriceForCharging' ) {
		setInputValue('MaxPriceForCharging', mqttpayload);
		loadElectricityPriceChart();
	}
	else if ( mqttmsg == 'openWB/global/awattar/ActualPriceForCharging' ) {
		$('#aktuellerStrompreis').text(parseFloat(mqttpayload).toLocaleString(undefined, {maximumFractionDigits: 2}) + ' ct/kWh');
	}

}

function processPvConfigMessages(mqttmsg, mqttpayload) {
	processPreloader(mqttmsg);
	if ( mqttmsg == 'openWB/config/get/pv/priorityModeEVBattery' ) {
		// sets button color in charge mode modal and sets icon in mode select button
		switch (mqttpayload) {
			case '0':
				// battery priority
				$('#evPriorityBtn').removeClass('btn-success');
				$('#batteryPriorityBtn').addClass('btn-success');
				$('#priorityEvBatteryIcon').removeClass('fa-car').addClass('fa-car-battery')
				break;
			case '1':
				// ev priority
				$('#evPriorityBtn').addClass('btn-success');
				$('#batteryPriorityBtn').removeClass('btn-success');
				$('#priorityEvBatteryIcon').removeClass('fa-car-battery').addClass('fa-car')
			break;
		}
	}
	else if ( mqttmsg == 'openWB/config/get/pv/nurpv70dynact' ) {
		//  and sets icon in mode select button
		switch (mqttpayload) {
			case '0':
				// deaktiviert
				$('#70ModeBtn').addClass('hide');
				break;
			case '1':
				// aktiviert
				$('#70ModeBtn').removeClass('hide');
			break;
		}
	}
	else if ( mqttmsg == 'openWB/config/get/pv/minCurrentMinPv' ) {
		setInputValue('minCurrentMinPv', mqttpayload);
	}
}

function processSofortConfigMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/config/get/sofort/
	// called by handlevar
	processPreloader(mqttmsg);
	var elementId = mqttmsg.replace('openWB/config/get/sofort/', '');
	var element = $('#' + $.escapeSelector(elementId));
	if ( element.attr('type') == 'range' ) {
		setInputValue(elementId, mqttpayload);
	} else if ( element.hasClass('btn-group-toggle') ) {
		setToggleBtnGroup(elementId, mqttpayload);
	}
}

function processGraphMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/graph
	// called by handlevar
	// console.log("received graph msg: " + mqttmsg + ": " + mqttpayload);
	processPreloader(mqttmsg);
	if ( mqttmsg == 'openWB/graph/boolDisplayHouseConsumption' ) {
		if ( mqttpayload == 1) {
			boolDisplayHouseConsumption = false;
			hidehaus = 'foo';
		} else {
			boolDisplayHouseConsumption = true;
			hidehaus = 'Hausverbrauch';
		}
		checkgraphload();
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayLegend' ) {
		if ( mqttpayload == 0) {
			boolDisplayLegend = false;
		} else {
			boolDisplayLegend = true;
		}
		checkgraphload();
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayLiveGraph' ) {
		if ( mqttpayload == 0) {
			$('#thegraph').addClass('hide');
			boolDisplayLiveGraph = false;
		} else {
			$('#thegraph').removeClass('hide');
			boolDisplayLiveGraph = true;
		}
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayEvu' ) {
		if ( mqttpayload == 1) {
			boolDisplayEvu = false;
			hideevu = 'foo';
		} else {
			boolDisplayEvu = true;
			hideevu = 'Bezug';
		}
		checkgraphload();
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayPv' ) {
		if ( mqttpayload == 1) {
			boolDisplayPv = false;
			hidepv = 'foo';
		} else {
			boolDisplayPv = true;
			hidepv = 'PV';
		}
		checkgraphload();
	}
	else if ( mqttmsg.match( /^openwb\/graph\/booldisplaylp[1-9][0-9]*$/i ) ) {
		var index = mqttmsg.match(/(\d+)(?!.*\d)/g)[0];  // extract last match = number from mqttmsg
		// now call functions or set variables corresponding to the index
		if ( mqttpayload == 1) {
			window['boolDisplayLp'+index] = false;
			window['hidelp'+index] = 'foo';
		} else {
			window['boolDisplayLp'+index] = true;
			window['hidelp'+index] = 'Lp' + index;
		}
		checkgraphload();
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayLpAll' ) {
		if ( mqttpayload == 1) {
			boolDisplayLpAll = false;
			hidelpa = 'foo';
		} else {
			boolDisplayLpAll = true;
			hidelpa = 'LP Gesamt';
		}
		checkgraphload();
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplaySpeicher' ) {
		if ( mqttpayload == 1) {
			boolDisplaySpeicher = false;
			hidespeicher = 'foo';
		} else {
			hidespeicher = 'Speicher';
			boolDisplaySpeicher = true;
		}
		checkgraphload();
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplaySpeicherSoc' ) {
		if ( mqttpayload == 1) {
			hidespeichersoc = 'foo';
			boolDisplaySpeicherSoc = false;
		} else {
			hidespeichersoc = 'Speicher SoC';
			boolDisplaySpeicherSoc = true;
		}
		checkgraphload();
	}
	else if ( mqttmsg.match( /^openwb\/graph\/booldisplaylp[1-9][0-9]*soc$/i ) ) {
		var index = mqttmsg.match(/(\d+)(?!.*\d)/g)[0];  // extract last match = number from mqttmsg
		if ( mqttpayload == 1) {
			$('#socenabledlp' + index).removeClass('hide');
			window['boolDisplayLp' + index + 'Soc'] = false;
			window['hidelp' + index + 'soc'] = 'foo';
		} else {
			$('#socenabledlp' + index).addClass('hide');
			window['boolDisplayLp' + index + 'Soc'] = true;
			window['hidelp' + index + 'soc'] = 'LP' + index + ' SoC';
		}
		checkgraphload();
	}
	else if ( mqttmsg.match( /^openwb\/graph\/booldisplayload[1-9][0-9]*$/i ) ) {
		var index = mqttmsg.match(/(\d+)(?!.*\d)/g)[0];  // extract last match = number from mqttmsg
		// now call functions or set variables corresponding to the index
		if ( mqttpayload == 1) {
			window['hideload'+index] = 'foo';
			window['boolDisplayLoad'+index] = false;
		} else {
			window['hideload'+index] = 'Verbraucher ' + index;
			window['boolDisplayLoad'+index] = true;
		}
		checkgraphload();
	}
	else if ( mqttmsg.match( /^openwb\/graph\/[1-9][0-9]*alllivevalues$/i ) ) {
		// graph messages if local connection
		var index = mqttmsg.match(/(\d+)(?!.*\d)/g)[0];  // extract last match = number from mqttmsg
		// now call functions or set variables corresponding to the index
		if (initialread == 0) {
			window['all'+index+'p'] = mqttpayload;
			window['all'+index] = 1;
			putgraphtogether();
		}
	}
	else if ( mqttmsg == 'openWB/graph/lastlivevalues' ) {
		// graph messages if local connection
		if ( initialread > 0) {
			updateGraph(mqttpayload);
		}
		if (graphrefreshcounter > 60) {
			// reload graph completely
			initialread = 0;
			all1 = 0;
			all2 = 0;
			all3 = 0;
			all4 = 0;
			all5 = 0;
			all6 = 0;
			all7 = 0;
			all8 = 0;
			all9 = 0;
			all10 = 0;
			all11 = 0;
			all12 = 0;
			all13 = 0;
			all14 = 0;
			all15 = 0;
			all16 = 0;
			graphrefreshcounter = 0;
			subscribeMqttGraphSegments();
		}
		graphrefreshcounter += 1;
	}
}  // end processGraphMessages

function processEvuMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/evu
	// called by handlevar
	processPreloader(mqttmsg);
	if ( mqttmsg == 'openWB/evu/W' ) {
		var prefix = ': ';
		var unit = ' W';
		var powerEvu = parseInt(mqttpayload, 10);
		if ( isNaN(powerEvu) ) {
			powerEvu = 0;
		}
		if ( powerEvu > 0 ) {
			prefix = ' Imp: ';
		} else if ( powerEvu < 0 ) {
			powerEvu *= -1;
			prefix = ' Exp: ';
		}
		if ( powerEvu > 999 ) {
			powerEvu = (powerEvu / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
			unit = ' kW';
		}
		$('#bezug').text(prefix + powerEvu + unit);
	}
	else if ( mqttmsg == 'openWB/evu/DailyYieldImportKwh') {
		var evuiDailyYield = parseFloat(mqttpayload);
		if ( isNaN(evuiDailyYield) ) {
			evuiDailyYield = 0;
		}
		if ( evuiDailyYield >= 0 ) {
			var evuiDailyYieldStr = ' (' + evuiDailyYield.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kWh I)';
			$('#evuidailyyield').text(evuiDailyYieldStr);
		} else {
			$('#evuidailyyield').text("");
		}

	}
	else if ( mqttmsg == 'openWB/evu/DailyYieldExportKwh') {
		var evueDailyYield = parseFloat(mqttpayload);
		if ( isNaN(evueDailyYield) ) {
			evueDailyYield = 0;
		}
		if ( evueDailyYield >= 0 ) {
			var evueDailyYieldStr = ' (' + evueDailyYield.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kWh E)';
			$('#evuedailyyield').text(evueDailyYieldStr);
		} else {
			$('#evuedailyyield').text("");
		}

	}
}

function processGlobalMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/global
	// called by handlevar
	processPreloader(mqttmsg);
	if ( mqttmsg == 'openWB/global/WHouseConsumption' ) {
		var powerHouse = parseInt(mqttpayload, 10);
		if ( isNaN(powerHouse) ) {
			powerHouse = 0;
		}
		if ( powerHouse > 999 ) {
			powerHouse = (powerHouse / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kW';
		} else {
			powerHouse += ' W';
		}
		$('#hausverbrauch').text(powerHouse);
	}
	else if ( mqttmsg == 'openWB/global/WAllChargePoints') {
		var powerAllLp = parseInt(mqttpayload, 10);
		if ( isNaN(powerAllLp) ) {
			powerAllLp = 0;
		}
		if (powerAllLp > 999) {
			powerAllLp = (powerAllLp / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kW';
		} else {
			powerAllLp += ' W';
		}
		$('#powerAllLp').text(powerAllLp);
	}
	else if ( mqttmsg == 'openWB/global/strLastmanagementActive' ) {
		if ( mqttpayload.length >= 5 ) {
			// if there is info-text in payload for topic, show the text
			$('#lastregelungaktiv').text(mqttpayload);
		} else {
			// if there is no text, show nothing (hides row)
			$('#lastregelungaktiv').text('');
		}
	}
	else if ( mqttmsg == 'openWB/global/ChargeMode' ) {
		// set modal button colors depending on charge mode
		// set visibility of divs
		// set visibility of priority icon depending on charge mode
		// (priority icon is encapsulated in another element hidden/shown by housebattery configured or not)
		switch (mqttpayload) {
			case '0':
				// mode sofort
				$('#chargeModeSelectBtnText').text('Sofortladen');  // text btn main page
				$('.chargeModeBtn').removeClass('btn-success');  // changes to select buttons in modal
				$('#chargeModeSofortBtn').addClass('btn-success');
				$('#targetChargingProgress').removeClass('hide');  // visibility of divs for special settings
				$('#sofortladenEinstellungen').removeClass('hide');
				$('#priorityEvBatteryIcon').addClass('hide');  // visibility of priority icon
				$('#minundpvladenEinstellungen').addClass('hide');

				break;
			case '1':
				// mode min+pv
				$('#chargeModeSelectBtnText').text('Min+PV-Laden');
				$('.chargeModeBtn').removeClass('btn-success');
				$('#chargeModeMinPVBtn').addClass('btn-success');
				$('#targetChargingProgress').addClass('hide');
				$('#sofortladenEinstellungen').addClass('hide');
				$('#priorityEvBatteryIcon').addClass('hide');
				$('#minundpvladenEinstellungen').removeClass('hide');

				break;
			case '2':
				// mode pv
				$('#chargeModeSelectBtnText').text('PV-Laden');
				$('.chargeModeBtn').removeClass('btn-success');
				$('#chargeModePVBtn').addClass('btn-success');
				$('#targetChargingProgress').addClass('hide');
				$('#sofortladenEinstellungen').addClass('hide');
				$('#priorityEvBatteryIcon').removeClass('hide');
				$('#minundpvladenEinstellungen').addClass('hide');

				break;
			case '3':
				// mode stop
				$('#chargeModeSelectBtnText').text('Stop');
				$('.chargeModeBtn').removeClass('btn-success');
				$('#chargeModeStopBtn').addClass('btn-success');
				$('#targetChargingProgress').addClass('hide');
				$('#sofortladenEinstellungen').addClass('hide');
				$('#priorityEvBatteryIcon').addClass('hide');
				$('#minundpvladenEinstellungen').addClass('hide');

				break;
			case '4':
				// mode standby
				$('#chargeModeSelectBtnText').text('Standby');
				$('.chargeModeBtn').removeClass('btn-success');
				$('#chargeModeStdbyBtn').addClass('btn-success');
				$('#targetChargingProgress').addClass('hide');
				$('#sofortladenEinstellungen').addClass('hide');
				$('#priorityEvBatteryIcon').addClass('hide');
				$('#minundpvladenEinstellungen').addClass('hide');
		}
	}
	else if ( mqttmsg == 'openWB/global/DailyYieldAllChargePointsKwh') {
		var llaDailyYield = parseFloat(mqttpayload);
		if ( isNaN(llaDailyYield) ) {
			llaDailyYield = 0;
		}
		if ( llaDailyYield >= 0 ) {
			var llaDailyYieldStr = ' (' + llaDailyYield.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kWh)';
			$('#lladailyyield').text(llaDailyYieldStr);
		} else {
			$('#lladailyyield').text("");
		}

	}
	else if ( mqttmsg == 'openWB/global/DailyYieldHausverbrauchKwh') {
		var hausverbrauchDailyYield = parseFloat(mqttpayload);
		if ( isNaN(hausverbrauchDailyYield) ) {
			hausverbrauchDailyYield = 0;
		}
		if ( hausverbrauchDailyYield >= 0 ) {
			var hausverbrauchDailyYieldStr = ' (' + hausverbrauchDailyYield.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kWh)';
			$('#hausverbrauchdailyyield').text(hausverbrauchDailyYieldStr);
		} else {
			$('#hausverbrauchdailyyield').text("");
		}

	}
}

function processHousebatteryMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/housebattery
	// called by handlevar
	processPreloader(mqttmsg);
	if ( mqttmsg == 'openWB/housebattery/W' ) {
		var prefix = ': ';
		var unit = ' W';
		var speicherwatt = parseInt(mqttpayload, 10);
		if ( isNaN(speicherwatt) ) {
			speicherwatt = 0;
		}
		if ( speicherwatt > 0 ) {
			prefix = '-Ladung: ';
		} else if ( speicherwatt < 0 ) {
			speicherwatt *= -1;
			prefix = '-Entladung: ';
		}
		if ( speicherwatt > 999 ) {
			speicherwatt = (speicherwatt / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
			unit = ' kW';
		}
		$('#speicherleistung').text(prefix + speicherwatt + unit);
	}
	else if ( mqttmsg == 'openWB/housebattery/%Soc' ) {
		var speicherSoc = parseInt(mqttpayload, 10);
		if ( isNaN(speicherSoc) || speicherSoc < 0 || speicherSoc > 100 ) {
			speicherSoc = '--';
		}
		speichersoc = speicherSoc + ' %';
		$('#speichersoc').text(speichersoc);
	}
	else if ( mqttmsg == 'openWB/housebattery/boolHouseBatteryConfigured' ) {
		if ( mqttpayload == 1 ) {
			// if housebattery is configured, show info-div
			$('#speicher').removeClass('hide');
			// and outer element for priority icon in pv mode
			$('#priorityEvBattery').removeClass('hide');
			// priority buttons in modal
			$('#priorityModeBtns').removeClass('hide');
		} else {
			$('#speicher').addClass('hide');
			$('#priorityEvBattery').addClass('hide');
			$('#priorityModeBtns').addClass('hide');
		}
	}

	else if ( mqttmsg == 'openWB/housebattery/DailyYieldExportKwh') {
		var sieDailyYield = parseFloat(mqttpayload);
		if ( isNaN(sieDailyYield) ) {
			sieDailyYield = 0;
		}
		if ( sieDailyYield >= 0 ) {
			var sieDailyYieldStr = ' (' + sieDailyYield.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kWh E)';
			$('#siedailyyield').text(sieDailyYieldStr);
		} else {
			$('#siedailyyield').text("");
		}

	}
	else if ( mqttmsg == 'openWB/housebattery/DailyYieldImportKwh') {
		var siiDailyYield = parseFloat(mqttpayload);
		if ( isNaN(siiDailyYield) ) {
			siiDailyYield = 0;
		}
		if ( siiDailyYield >= 0 ) {
			var siiDailyYieldStr = ' (' + siiDailyYield.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kWh I)';
			$('#siidailyyield').text(siiDailyYieldStr);
		} else {
			$('#siidailyyield').text("");
		}

	}
}

function processSystemMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/system
	// called by handlevar
	// console.log("received system msg: " + mqttmsg + ": " + mqttpayload);
	processPreloader(mqttmsg);
	if ( mqttmsg == 'openWB/system/Timestamp') {
		var dateObject = new Date(mqttpayload * 1000);  // Unix timestamp to date-object
		var time = '&nbsp;';
		var date = '&nbsp;';
		if ( dateObject instanceof Date && !isNaN(dateObject.valueOf()) ) {
			// timestamp is valid date so process
			var HH = String(dateObject.getHours()).padStart(2, '0');
			var MM = String(dateObject.getMinutes()).padStart(2, '0');
			time = HH + ':'  + MM;
			var dd = String(dateObject.getDate()).padStart(2, '0');  // format with leading zeros
			var mm = String(dateObject.getMonth() + 1).padStart(2, '0'); //January is 0 so add +1!
			var dayOfWeek = dateObject.toLocaleDateString('de-DE', { weekday: 'short'});
			date = dayOfWeek + ', ' + dd + '.' + mm + '.' + dateObject.getFullYear();
		}
		$('#time').text(time);
		$('#date').text(date);
	}
}

function processPvMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/pv
	// called by handlevar
	processPreloader(mqttmsg);
	if ( mqttmsg == 'openWB/pv/W') {
		var pvwatt = parseInt(mqttpayload, 10);
		if ( isNaN(pvwatt) ) {
			pvwatt = 0;
		}
		if ( pvwatt <= 0){
			// production is negative for calculations so adjust for display
			pvwatt *= -1;
			// adjust and add unit
			if (pvwatt > 999) {
				pvwatt = (pvwatt / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kW';
			} else {
				pvwatt += ' W';
			}
		}
		$('#pvleistung').text(pvwatt);
	}
	else if ( mqttmsg == 'openWB/pv/DailyYieldKwh') {
		var pvDailyYield = parseFloat(mqttpayload);
		if ( isNaN(pvDailyYield) ) {
			pvDailyYield = 0;
		}
		if ( pvDailyYield >= 0 ) {
			var pvDailyYieldStr = ' (' + pvDailyYield.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kWh)';
			$('#pvdailyyield').text(pvDailyYieldStr);
		} else {
			$('#pvdailyyield').text("");
		}

	}
	else if ( mqttmsg == 'openWB/pv/bool70PVDynStatus') {
		switch (mqttpayload) {
			case '0':
				// deaktiviert
				$('#70PvBtn').removeClass('btn-success');
				break;
			case '1':
				// ev priority
				$('#70PvBtn').addClass('btn-success');
			break;
		}
	}
}

function processVerbraucherMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/Verbraucher
	// called by handlevar
	processPreloader(mqttmsg);
	var index = getIndex(mqttmsg);  // extract number between two / /
	if ( mqttmsg.match( /^openwb\/Verbraucher\/[1-2]\/Configured$/i ) ) {
		if ( mqttpayload == 1 ) {
			// if at least one device is configured, show info-div
			$('#verbraucher').removeClass("hide");
			// now show info-div for this device
			$('#verbraucher'+index).removeClass("hide");
		} else {
			$('#verbraucher'+index).addClass("hide");
		}
	} else if ( mqttmsg.match( /^openwb\/Verbraucher\/[1-2]\/Name$/i ) ) {
		if ( mqttpayload != "Name" ){
			$('#verbraucher'+index+'name').text(mqttpayload);
		}
	} else if ( mqttmsg.match( /^openwb\/Verbraucher\/[1-2]\/Watt$/i ) ) {
		var unit = ' W';
		var verbraucherwatt = parseInt(mqttpayload, 10);
		if ( isNaN(verbraucherwatt) ) {
			verbraucherwatt = 0;
		}
		if ( verbraucherwatt > 999 ) {
			verbraucherwatt = (verbraucherwatt / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
			unit = ' kW';
		}
		$('#verbraucher'+index+'leistung').text(verbraucherwatt + unit);
	} else if ( mqttmsg.match( /^openwb\/Verbraucher\/[1-2]\/DailyYieldImportkWh$/i ) ) {
		var verbraucherDailyYield = parseFloat(mqttpayload);
		if ( isNaN(verbraucherDailyYield) ) {
			verbraucherDailyYield = 0;
		}
		if ( verbraucherDailyYield >= 0 ) {
			var verbraucherDailyYieldStr = ' (' + verbraucherDailyYield.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kWh)';
			$('#verbraucher'+index+'dailyyield').text(verbraucherDailyYieldStr);
		} else {
			$('#verbraucher'+index+'dailyyield').text("");
		}

	}
}

function processLpMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/lp
	// called by handlevar
	processPreloader(mqttmsg);
	let match = /^openWB\/lp\/(\d+)\/(.*)$/.exec(mqttmsg);
	let index = match[1];
	let lpSubTopic = match[2];
	if (lpSubTopic === "W") {
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.actualPowerLp');  // now get parents respective child element
		var actualPower = parseInt(mqttpayload, 10);
		if ( isNaN(actualPower) ) {
			actualPower = 0;
		}
		if (actualPower > 999) {
			actualPower = (actualPower / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
			actualPower += ' kW';
		} else {
			actualPower += ' W';
		}
		element.text(actualPower);
	}
	else if (lpSubTopic === "kWhChargedSincePlugged") {
		// energy charged since ev was plugged in
		// also calculates and displays km charged
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.energyChargedLp');  // now get parents respective child element
		var energyCharged = parseFloat(mqttpayload, 10);
		if ( isNaN(energyCharged) ) {
			energyCharged = 0;
		}
		element.text(energyCharged.toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) + ' kWh');
		var kmChargedLp = parent.find('.kmChargedLp');  // now get parents kmChargedLp child element
		var consumption = parseFloat($(kmChargedLp).data('consumption'));
		var kmCharged = '';
		if ( !isNaN(consumption) && consumption > 0 ) {
			kmCharged = (energyCharged / consumption) * 100;
			kmCharged = ' / ' + kmCharged.toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) + ' km';
		} else {
			kmCharged = ' / -- km';
		}
		$(kmChargedLp).text(kmCharged);
	}
	else if (lpSubTopic === "kWhActualCharged") {
		// energy charged since reset of limitation
		if ( isNaN(mqttpayload) ) {
			mqttpayload = 0;
		}
		var parent = $('[data-lp="' + index + '"]');  // get parent div element for charge limitation
		var element = parent.find('.progress-bar');  // now get parents progressbar
		element.data('actualCharged', mqttpayload);  // store value received
		var limitElementId = 'lp/' + index + '/energyToCharge';
		var limit = $('#' + $.escapeSelector(limitElementId)).val();  // slider value
		if ( isNaN(limit) || limit < 2 ) {
			limit = 2;  // minimum value
		}
		var progress = (mqttpayload / limit * 100).toFixed(0);
		element.width(progress+"%");
	}
	else if (lpSubTopic === "%Soc") {
		// soc of ev at respective charge point
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.socLp');  // now get parents respective child element
		var soc = parseInt(mqttpayload, 10);
		if ( isNaN(soc) || soc < 0 || soc > 100 ) {
			soc = '--';
		}
		element.text(soc);
		var spinner = parent.find('.reloadLpSoc');
		if ( spinner.hasClass('fa-spin') ) {
			spinner.removeClass('fa-spin');
		}
	}
	else if (lpSubTopic === "TimeRemaining") {
		// time remaining for charging to target value
		var parent = $('.chargeLimitation[data-lp="' + index + '"]');  // get parent div element for charge limitation
		var element = parent.find('.restzeitLp');  // get element
		element.text('Restzeit ' + mqttpayload);
	}
	else if (lpSubTopic === "boolChargeAtNight") {
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.nightChargingLp');  // now get parents respective child element
		if ( mqttpayload == 1 ) {
			element.removeClass('hide');
		} else {
			element.addClass('hide');
		}
	}
	else if (lpSubTopic === "boolPlugStat") {
		// status ev plugged in or not
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.plugstatLp');  // now get parents respective child element
		if ( mqttpayload == 1 ) {
			element.removeClass('hide');
		} else {
			element.addClass('hide');
		}
	}
	else if (lpSubTopic === "boolChargeStat") {
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.plugstatLp');  // now get parents respective child element
		if ( mqttpayload == 1 ) {
			element.removeClass('text-orange').addClass('text-green');
		} else {
			element.removeClass('text-green').addClass('text-orange');
		}
	}
	else if (lpSubTopic === "strChargePointName") {
		$('.nameLp').each(function() {  // fill in name for all element of class '.nameLp'
			var lp = $(this).closest('[data-lp]').data('lp');  // get attribute lp from parent
			if ( lp == index ) {
				$(this).text(mqttpayload);
			}
		});
	}
	else if (lpSubTopic === "ChargePointEnabled") {
		$('.nameLp').each(function() {  // check all elements of class '.nameLp'
			var lp = $(this).closest('[data-lp]').data('lp');  // get attribute lp from parent
			if ( lp == index ) {
				if ( $(this).hasClass('enableLp') ) {
					// but only apply styles to element in chargepoint info data block
					if ( mqttpayload == 0 ) {
						$(this).removeClass('lpEnabledStyle').addClass('lpDisabledStyle');
					} else {
						$(this).removeClass('lpDisabledStyle').addClass('lpEnabledStyle');
					}
				}
			}
		});
	}
	else if (lpSubTopic === "countPhasesInUse") {
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.phasesInUseLp');  // now get parents respective child element
		var phasesInUse = parseInt(mqttpayload, 10);
		if ( isNaN(phasesInUse) || phasesInUse < 1 || phasesInUse > 3 ) {
			element.text(' /');
		} else {
			var phaseSymbols = ['', '\u2460', '\u2461', '\u2462'];
			element.text(' ' + phaseSymbols[phasesInUse]);
		}
	}
	else if (lpSubTopic === "AConfigured") {
		// target current value at charge point
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.targetCurrentLp');  // now get parents respective child element
		var targetCurrent = parseInt(mqttpayload, 10);
		if ( isNaN(targetCurrent) ) {
			element.text(' 0 A');
		} else {
			element.text(' ' + targetCurrent + ' A');
		}
	}
	else if (lpSubTopic === "boolSocConfigured") {
		// soc-module configured for respective charge point
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var elementIsConfigured = $(parent).find('.socConfiguredLp');  // now get parents respective child element
		var elementIsNotConfigured = $(parent).find('.socNotConfiguredLp');  // now get parents respective child element
		if (mqttpayload == 1) {
			$(elementIsNotConfigured).addClass('hide');
			$(elementIsConfigured).removeClass('hide');
		} else {
			$(elementIsNotConfigured).removeClass('hide');
			$(elementIsConfigured).addClass('hide');
		}
	}
	else if (lpSubTopic === "boolSocManual") {
		// manual soc-module configured for respective charge point
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var elementIsConfigured = $(parent).find('.socConfiguredLp');  // now get parents respective child element
		if (mqttpayload == 1) {
			$(elementIsConfigured).addClass('manualSoC');
			$(elementIsConfigured).find('.manualSocSymbol').removeClass('hide');
			$(elementIsConfigured).find('.reloadLpSoc').addClass('hide');
		} else {
			$(elementIsConfigured).removeClass('manualSoC');
			$(elementIsConfigured).find('.manualSocSymbol').addClass('hide');
			$(elementIsConfigured).find('.reloadLpSoc').removeClass('hide');
		}
	}
	else if (lpSubTopic === "boolChargePointConfigured") {
		// respective charge point configured
		// now show/hide element containing data-lp attribute with value=index
		switch (mqttpayload) {
			case '0':
				$('[data-lp="' + index + '"]').addClass('hide');
				break;
			case '1':
				$('[data-lp="' + index + '"]').removeClass('hide');
				break;
		}
	}
	else if (lpSubTopic === "AutolockConfigured") {
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.autolockConfiguredLp');  // now get parents respective child element
		if ( mqttpayload == 0 ) {
			element.addClass('hide');
		} else {
			element.removeClass('hide');
		}
	}
	else if (lpSubTopic === "AutolockStatus") {
		// values used for AutolockStatus flag:
		// 0 = standby
		// 1 = waiting for autolock
		// 2 = autolock performed
		// 3 = auto-unlock performed
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.autolockConfiguredLp');  // now get parents respective child element
		switch ( mqttpayload ) {
			case '0':
				// remove animation from span and set standard colored key icon
				element.removeClass('fa-lock fa-lock-open animate-alertPulsation text-red text-green');
				element.addClass('fa-key');
				break;
			case '1':
				// add animation to standard icon
				element.removeClass('fa-lock fa-lock-open text-red text-green');
				element.addClass('fa-key animate-alertPulsation');
				break;
			case '2':
				// add red locked icon
				element.removeClass('fa-lock-open fa-key animate-alertPulsation text-green');
				element.addClass('fa-lock text-red');
				break;
			case '3':
				// add green unlock icon
				element.removeClass('fa-lock fa-key animate-alertPulsation text-red');
				element.addClass('fa-lock-open text-green');
				break;
		}
	}
	else if (lpSubTopic === "energyConsumptionPer100km") {
		// store configured value in element attribute
		// to calculate charged km upon receipt of charged energy
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.kmChargedLp');  // now get parents respective child element
		var consumption = parseFloat(mqttpayload);
		if ( isNaN(consumption) ) {
			consumption = 0;
		}
		element.data('consumption', consumption);  // store value in data-attribute
		// if already energyCharged-displayed, update kmCharged
		var energyChargedLp = parent.find('.energyChargedLp');  // now get parents respective energyCharged child element
		var energyCharged = parseFloat($(energyChargedLp).text());
		var kmCharged = '';
		if ( !isNaN(energyCharged) && consumption > 0 ) {
			kmCharged = (energyCharged / consumption) * 100;
			kmCharged = ' / ' + kmCharged.toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) + ' km';
		} else {
			kmCharged = ' / -- km';
		}
		element.text(kmCharged);
	}
	else if (lpSubTopic === "boolFinishAtTimeChargeActive") {
		// respective charge point configured
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.targetChargingLp');  // now get parents respective child element
		if (mqttpayload == 1) {
			element.removeClass('hide');
		} else {
			element.addClass('hide');
		}
	}
	else if (lpSubTopic === "faultState") {
		$('[data-lp="' + index + '"] .socHasError')[mqttpayload === "0" ? "addClass" : "removeClass"]("hide");
	}
}

function processHookMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/hook
	// called by handlevar
	processPreloader(mqttmsg);
	if ( mqttmsg.match( /^openwb\/hook\/[1-9][0-9]*\/boolhookstatus$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		if ( mqttpayload == 1 ) {
			$('#hook' + index).removeClass("bg-danger").addClass("bg-success");
		} else {
			$('#hook' + index).removeClass("bg-success").addClass("bg-danger");
		}
	}
	else if ( mqttmsg.match( /^openwb\/hook\/[1-9][0-9]*\/boolhookconfigured$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		if ( mqttpayload == 1 ) {
			$('#hook' + index).removeClass('hide');
		} else {
			$('#hook' + index).addClass('hide');
		}
	}
}

function processSmartHomeDevicesMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/SmartHomeDevices - actual values only!
	// called by handlevar
	processPreloader(mqttmsg);
	if ( mqttmsg.match( /^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/Watt$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-dev="' + index + '"]');  // get parent row element for SH Device
		var element = parent.find('.actualPowerDevice');  // now get parents respective child element
		var actualPower = parseInt(mqttpayload, 10);
		if ( isNaN(actualPower) ) {
			actualPower = 0;
		}
		if (actualPower > 999) {
			actualPower = (actualPower / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
			actualPower += ' kW';
		} else {
			actualPower += ' W';
		}
		element.text(actualPower);
	}
	else if ( mqttmsg.match( /^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/DailyYieldKwh$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-dev="' + index + '"]');  // get parent row element for SH Device
		var element = parent.find('.actualDailyYieldDevice');  // now get parents respective child element
		var actualDailyYield = parseFloat(mqttpayload);
		if ( isNaN(actualDailyYield) ) {
			siiDailyYield = 0;
		}
		if ( actualDailyYield >= 0 ) {
			var actualDailyYieldStr = ' (' + actualDailyYield.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' kWh)';
			element.text(actualDailyYieldStr);
		} else {
			element.text("");
		}
	}
	else if ( mqttmsg.match( /^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/RunningTimeToday$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-dev="' + index + '"]');  // get parent row element for SH Device
		var element = parent.find('.actualRunningTimeDevice');  // now get parents respective child element
		var actualPower = parseInt(mqttpayload, 10);
		if ( isNaN(actualPower) ) {
			actualPower = 0;
		}
		if (actualPower < 3600) {
			actualPower = (actualPower / 60).toFixed(0);
			actualPower += ' Min';
		} else {
			rest = (actualPower % 3600 / 60).toFixed(0);
			ganz = Math.floor(actualPower / 3600);
			actualPower = ganz + ' H ' + rest +' Min';
		}
		element.text(actualPower);
	}
	else if ( mqttmsg.match( /^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/Status$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		$('.nameDevice').each(function() {  // check all elements of class '.nameLp'
			var dev = $(this).closest('[data-dev]').data('dev');  // get attribute lp from parent
			if ( dev == index ) {
				if ( $(this).hasClass('enableDevice') ) {
					// but only apply styles to element in chargepoint info data block
					// 10 Device on (manuell oder automatisch)
					if ( mqttpayload == 10 ) {
						$(this).removeClass('lpEnabledStyle').removeClass('text-blue').removeClass('text-white').removeClass('lpWaitingStyle').addClass('lpDisabledStyle');
					// 11 Device off(manuell oder automatisch)
					} else if ( mqttpayload == 11 ) {
						$(this).removeClass('lpDisabledStyle').removeClass('text-blue').removeClass('text-white').removeClass('lpWaitingStyle').addClass('lpEnabledStyle');
					// 20 Anlauferkennung aktiv
					} else if ( mqttpayload == 20) {
						$(this).removeClass('lpDisabledStyle').removeClass('lpEnabledStyle').removeClass('text-white').removeClass('lpWaitingStyle').addClass('text-blue');
					// 30 Finistime laueft
					} else {
						$(this).removeClass('lpDisabledStyle').removeClass('lpEnabledStyle').removeClass('text-blue').removeClass('lpWaitingStyle').addClass('text-white');
					}
				}
			}
		});
	}
	else if ( mqttmsg.match( /^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/TemperatureSensor0$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('.SmartHomeTemp[data-dev="' + index + '"]');  // get parent row element for SH Device
		var element = parent.find('.actualTemp0Device');  // now get parents respective child element
		var actualTemp = parseFloat(mqttpayload);
		if ( isNaN(actualTemp) ) {
			StringTemp = '';
			parent.addClass('hide');
		} else {
			if (actualTemp > 200) {
				StringTemp = ''; // display only something if we got a value
				parent.addClass('hide');
			} else {
				StringTemp = 'Temp1 ' + actualTemp.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}); // make complete string to display
				parent.removeClass('hide');
			}
		}
		element.text(StringTemp);
	}
	else if ( mqttmsg.match( /^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/TemperatureSensor1$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('.SmartHomeTemp[data-dev="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.actualTemp1Device');  // now get parents respective child element
		var actualTemp = parseFloat(mqttpayload);
		if ( isNaN(actualTemp) ) {
			StringTemp = '';
		} else {
			if (actualTemp > 200) {
				StringTemp = ''; // display only something if we got a value
			} else {
				StringTemp = 'Temp2 ' + actualTemp.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}); // make complete string to display
			}
		}
		element.text(StringTemp);
	}
	else if ( mqttmsg.match( /^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/TemperatureSensor2$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('.SmartHomeTemp[data-dev="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.actualTemp2Device');  // now get parents respective child element
		var actualTemp = parseFloat(mqttpayload);
		if ( isNaN(actualTemp) ) {
			StringTemp = '';
		} else {
			if (actualTemp > 200) {
				StringTemp = ''; // display only something if we got a value
			} else {
				StringTemp = 'Temp3 ' + actualTemp.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}); // make complete string to display
			}
		}
		element.text(StringTemp);
	}
}

function processSmartHomeDevicesConfigMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/config/get/SmartHome/Devices - config variables (Name / configured only!), actual Variables in proccessSMartHomeDevices
	// called by handlevar
	processPreloader(mqttmsg);
	if ( mqttmsg.match( /^openwb\/config\/get\/SmartHome\/Devices\/[1-9][0-9]*\/device_configured$/i ) ) {
		// respective SH Device configured
		var index = getIndex(mqttmsg);  // extract number between two / /
		var infoElement = $('[data-dev="' + index + '"]');  // get row of SH Device
		if (mqttpayload == 1) {
			infoElement.removeClass('hide');
		} else {
			infoElement.addClass('hide');
		}
		var visibleRows = $('.smartHome [data-dev]').not('.hide');  // show/hide complete block depending on visible rows within
		if ( visibleRows.length > 0 ) {
			$('.smartHome').removeClass('hide');
		} else {
			$('.smartHome').addClass('hide');
		}
	}
	else if ( mqttmsg.match( /^openwb\/config\/get\/SmartHome\/Devices\/[1-9][0-9]*\/mode$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-dev="' + index + '"]');  // get parent row element for SH Device
		var element = parent.find('.actualModeDevice');  // now get parents respective child element
		if ( mqttpayload == 0 ) {
			actualMode = "Automatik"
		} else {
			actualMode = "Manuell"
		}
		element.text(actualMode);
		$('.nameDevice').each(function() {  // check all elements of class '.nameDevice'
			var dev = $(this).closest('[data-dev]').data('dev');  // get attribute Device from parent
			if ( dev == index ) {
				if ( $(this).hasClass('enableDevice') ) {
					// but only apply styles to element in chargepoint info data block
					if ( mqttpayload == 1 ) {
						$(this).addClass('cursor-pointer').addClass('locked');
					} else {
						$(this).removeClass('cursor-pointer').removeClass('locked');
					}
				}
			}
		});
	}
	else if ( mqttmsg.match( /^openWB\/config\/get\/SmartHome\/Devices\/[1-9][0-9]*\/device_name$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-dev="' + index + '"]');  // get parent row element for SH Device
		var element = parent.find('.nameDevice');  // now get parents respective child element
		element.text(mqttpayload);
		window['d'+index+'name']=mqttpayload;
	}
}
