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
	setTimeout(function () {
		publish("0", "openWB/set/system/reloadDisplay");
		// wait again to give the broker some time and avoid a reload loop
		setTimeout(function () {
			location.reload();
		}, 2000);
	}, 2000);
}

function getCol(matrix, col) {
	var column = [];
	for (var i = 0; i < matrix.length; i++) {
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
	// get occurence of numbers between / / in topic
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
	if (mqttmsg.match(/^openwb\/graph\//i)) { processGraphMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/evu\//i)) { processEvuMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/global\//i)) { processGlobalMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/housebattery\//i)) { processHousebatteryMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/system\//i)) { processSystemMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/pv\//i)) { processPvMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/lp\//i)) { processLpMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/config\/get\/sofort\/lp\//i)) { processSofortConfigMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/config\/get\/pv\//i)) { processPvConfigMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/config\/get\/display\//i)) { processDisplayConfigMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/SmartHome\/Status\//i)) { processSmartHomeDevicesStatusMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/SmartHome\/Devices\//i)) { processSmartHomeDevicesMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/config\/get\/SmartHome\/Devices\//i)) { processSmartHomeDevicesConfigMessages(mqttmsg, mqttpayload); }



}  // end handlevar

function processDisplayConfigMessages(mqttmsg, mqttpayload) {

	if (mqttmsg == 'openWB/config/get/display/showHouseConsumption') {
		/* 	switch (mqttpayload) {
				case '0':
					// hide house consumption
					$('.hausverbrauch').addClass('hide');
					break;
				case '1':
					// show house consumption
					$('.hausverbrauch').removeClass('hide');
					break;
			} */
	}
	else if (mqttmsg == 'openWB/config/get/display/chartHouseConsumptionMax') {
		/* 	var chartElement = $('.sparkline[data-chartname=hausverbrauchlchart]');
			chartElement.attr('data-sparkChartRangeMax', mqttpayload); */
	}
	else if (mqttmsg == 'openWB/config/get/display/chartEvuMinMax') {
		/* 	var chartElement = $('.sparkline[data-chartname=evulchart]');
			chartElement.attr('data-sparkChartRangeMax', mqttpayload);
			chartElement.attr('data-sparkChartRangeMin', mqttpayload*-1); */
	}
	else if (mqttmsg == 'openWB/config/get/display/chartBatteryMinMax') {
		/* var chartElement = $('.sparkline[data-chartname=hausbatteriellchart]');
		chartElement.attr('data-sparkChartRangeMax', mqttpayload);
		chartElement.attr('data-sparkChartRangeMin', mqttpayload*-1); */
	}
	else if (mqttmsg == 'openWB/config/get/display/chartPvMax') {
		/* 	var chartElement = $('.sparkline[data-chartname=pvlchart]');
			chartElement.attr('data-sparkChartRangeMax', mqttpayload); */
	}
	else if (mqttmsg.match(/^openwb\/config\/get\/display\/chartLp\/[1-9][0-9]*\/max$/i)) {
		/* 	var index = getIndex(mqttmsg);  // extract number between two / /
			var chartElement = $('.sparkline[data-chartname=ladepunkt'+index+'llchart]');
			chartElement.attr('data-sparkChartRangeMax', mqttpayload); */
	}
}

function processPvConfigMessages(mqttmsg, mqttpayload) {
	// color theme
	if (mqttmsg == 'openWB/config/get/pv/priorityModeEVBattery') {
		wbdata.updatePv("hasEVPriority", (mqttpayload == "1"))
	}
	//end color theme

	if (mqttmsg == 'openWB/config/get/pv/priorityModeEVBattery') {
		// sets button color in charge mode modal and sets icon in mode select button
		switch (mqttpayload) {
			case '0':
				// battery priority
				$('#evPriorityBtn').removeClass('btn-success');
				$('#batteryPriorityBtn').addClass('btn-success');
				$('.priorityEvBatteryIcon').removeClass('fa-car').addClass('fa-car-battery')
				break;
			case '1':
				// ev priority
				$('#evPriorityBtn').addClass('btn-success');
				$('#batteryPriorityBtn').removeClass('btn-success');
				$('.priorityEvBatteryIcon').removeClass('fa-car-battery').addClass('fa-car')
				break;
		}
	}
	else if (mqttmsg == 'openWB/config/get/pv/nurpv70dynact') {
		//  and sets icon in mode select button
		switch (mqttpayload) {
			case '0':
				// deaktiviert
				$('#70ModeBtn').addClass('hide');
				break;
			case '1':
				// activiert
				$('#70ModeBtn').removeClass('hide');
				break;
		}
	}
	else if (mqttmsg == 'openWB/config/get/pv/minCurrentMinPv') {
		setInputValue('minCurrentMinPv', mqttpayload);
	}
}

function processSofortConfigMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/config/get/sofort/
	// called by handlevar
	var elementId = mqttmsg.replace('openWB/config/get/sofort/', '');
	var element = $('#' + $.escapeSelector(elementId));
	if (element.attr('type') == 'range') {
		setInputValue(elementId, mqttpayload);
	} else if (element.hasClass('btn-group-toggle')) {
		setToggleBtnGroup(elementId, mqttpayload);
	}
}

function processGraphMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/graph
	// called by handlevar
	if (mqttmsg == 'openWB/graph/boolDisplayHouseConsumption') {
		if (mqttpayload == 1) {
			boolDisplayHouseConsumption = false;
			hidehaus = 'foo';
		} else {
			boolDisplayHouseConsumption = true;
			hidehaus = 'Hausverbrauch';
		}
		//checkgraphload();
	}
	else if (mqttmsg == 'openWB/graph/boolDisplayLegend') {
		if (mqttpayload == 0) {
			boolDisplayLegend = false;
		} else {
			boolDisplayLegend = true;
		}
		//checkgraphload();
	}
	else if (mqttmsg == 'openWB/graph/boolDisplayLiveGraph') {
		if (mqttpayload == 0) {
			$('#thegraph').hide();
			boolDisplayLiveGraph = false;
		} else {
			$('#thegraph').show();
			boolDisplayLiveGraph = true;
		}
	}
	else if (mqttmsg == 'openWB/graph/boolDisplayEvu') {
		if (mqttpayload == 1) {
			boolDisplayEvu = false;
			hideevu = 'foo';
		} else {
			boolDisplayEvu = true;
			hideevu = 'Bezug';
		}
		//checkgraphload();
	}
	else if (mqttmsg == 'openWB/graph/boolDisplayPv') {
		if (mqttpayload == 1) {
			boolDisplayPv = false;
			hidepv = 'foo';
		} else {
			boolDisplayPv = true;
			hidepv = 'PV';
		}
		//checkgraphload();
	}
	else if (mqttmsg.match(/^openwb\/graph\/booldisplaylp[1-9][0-9]*$/i)) {
		var index = mqttmsg.match(/(\d+)(?!.*\d)/g)[0];  // extract last match = number from mqttmsg
		// now call functions or set variables corresponding to the index
		if (mqttpayload == 1) {
			window['boolDisplayLp' + index] = false;
			window['hidelp' + index] = 'foo';
		} else {
			window['boolDisplayLp' + index] = true;
			window['hidelp' + index] = 'Lp' + index;
		}
		//checkgraphload();
	}
	else if (mqttmsg == 'openWB/graph/boolDisplayLpAll') {
		if (mqttpayload == 1) {
			boolDisplayLpAll = false;
			hidelpa = 'foo';
		} else {
			boolDisplayLpAll = true;
			hidelpa = 'LP Gesamt';
		}
		//checkgraphload();
	}
	else if (mqttmsg == 'openWB/graph/boolDisplaySpeicher') {
		if (mqttpayload == 1) {
			boolDisplaySpeicher = false;
			hidespeicher = 'foo';
		} else {
			hidespeicher = 'Speicher';
			boolDisplaySpeicher = true;
		}
		//checkgraphload();
	}
	else if (mqttmsg == 'openWB/graph/boolDisplaySpeicherSoc') {
		if (mqttpayload == 1) {
			hidespeichersoc = 'foo';
			boolDisplaySpeicherSoc = false;
		} else {
			hidespeichersoc = 'Speicher SoC';
			boolDisplaySpeicherSoc = true;
		}
		//checkgraphload();
	}
	else if (mqttmsg.match(/^openwb\/graph\/booldisplaylp[1-9][0-9]*soc$/i)) {
		var index = mqttmsg.match(/(\d+)(?!.*\d)/g)[0];  // extract last match = number from mqttmsg
		if (mqttpayload == 1) {
			$('#socenabledlp' + index).show();
			window['boolDisplayLp' + index + 'Soc'] = false;
			window['hidelp' + index + 'soc'] = 'foo';
		} else {
			$('#socenabledlp' + index).hide();
			window['boolDisplayLp' + index + 'Soc'] = true;
			window['hidelp' + index + 'soc'] = 'LP' + index + ' SoC';
		}
		//checkgraphload();
	}
	else if (mqttmsg.match(/^openwb\/graph\/booldisplayload[1-9][0-9]*$/i)) {
		var index = mqttmsg.match(/(\d+)(?!.*\d)/g)[0];  // extract last match = number from mqttmsg
		// now call functions or set variables corresponding to the index
		if (mqttpayload == 1) {
			window['hideload' + index] = 'foo';
			window['boolDisplayLoad' + index] = false;
		} else {
			window['hideload' + index] = 'Verbraucher ' + index;
			window['boolDisplayLoad' + index] = true;
		}
		//checkgraphload();
	}
	else if (mqttmsg.match(/^openwb\/graph\/[1-9][0-9]*alllivevalues$/i)) {
		powerGraph.updateLive(mqttmsg, mqttpayload);
		/* var index = mqttmsg.match(/(\d+)(?!.*\d)/g)[0];  // extract last match = number from mqttmsg
		// now call functions or set variables corresponding to the index
		if (initialread == 0) {
			window['all'+index+'p'] = mqttpayload;
			window['all'+index] = 1;
			//putgraphtogether();
		}*/
	}
	else if (mqttmsg == 'openWB/graph/lastlivevalues') {
		powerGraph.updateLive(mqttmsg, mqttpayload);
		/* 	if ( initialread > 0) {
				//updateGraph(mqttpayload);
			}
			if (graphrefreshcounter > 60) {
				// reload graph completety
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
			} */
		// graphrefreshcounter += 1;
	}
}  // end processGraphMessages
function processEvuMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/evu
	// called by handlevar
	// color theme
	if (mqttmsg == 'openWB/evu/W') {
		var powerEvu = parseInt(mqttpayload, 10);
		if (isNaN(powerEvu)) {
			powerEvu = 0;
		}
		if (powerEvu >= 0) {
			wbdata.updateEvu("powerEvuIn", powerEvu);
			wbdata.updateEvu("powerEvuOut", 0);
		} else {
			wbdata.updateEvu("powerEvuIn", 0);
			wbdata.updateEvu("powerEvuOut", -powerEvu);
		}

	} else if (mqttmsg == 'openWB/evu/DailyYieldImportKwh') {
		var evuiDailyYield = parseFloat(mqttpayload);
		if (isNaN(evuiDailyYield)) {
			evuiDailyYield = 0;
		}
		if (evuiDailyYield >= 0) {
			wbdata.updateEvu("evuiDailyYield", evuiDailyYield);
		} else {
			wbdata.updateEvu("evuiDailyYield", 0);
		}

	} else if (mqttmsg == 'openWB/evu/DailyYieldExportKwh') {
		var evueDailyYield = parseFloat(mqttpayload);
		if (isNaN(evueDailyYield)) {
			evueDailyYield = 0;
		}
		if (evueDailyYield >= 0) {
			wbdata.updateEvu("evueDailyYield", evueDailyYield);
		} else {
			wbdata.updateEvu("evueDailyYield", 0);
		}
	};
	// end color theme
	if (mqttmsg == 'openWB/evu/W') {
		/* var prefix = '';
		var unit = ' W';
		var powerEvu = parseInt(mqttpayload, 10);
		if ( isNaN(powerEvu) ) {
			powerEvu = 0;
		}
		// now use a temp value to keep original value with sign for sparkline
		var powerEvuValue = powerEvu;
		if ( powerEvuValue > 0 ) {
			prefix = ' Imp: ';
		} else if( powerEvuValue < 0 ) {
			powerEvuValue *= -1;
			prefix = ' Exp: ';
		}
		var powerEvuText = powerEvuValue.toString();
		if ( powerEvuValue >= 1000 ) {
			powerEvuText = (powerEvuValue / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
			unit = ' kW';
		}
		var element = $('#evul');
		var elementChart = $('#evulchart');
		updateDashboardElement(element, elementChart, prefix + powerEvuText + unit, powerEvu); */
	}
}

function processGlobalMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/global
	// called by handlevar

	// color theme
	if (mqttmsg == 'openWB/global/WHouseConsumption') {
		wbdata.updateGlobal("housePower", makeInt(mqttpayload));
	}
	else if (mqttmsg == 'openWB/global/WAllChargePoints') {
		wbdata.updateGlobal("chargePower", makeInt(mqttpayload));
	}
	else if (mqttmsg == 'openWB/global/strLastmanagementActive') {
		wbdata.updateGlobal("loadMgtText", (mqttpayload.length >= 5 ? mqttpayload : ''));
	}
	else if (mqttmsg == 'openWB/global/ChargeMode') {
		wbdata.updateGlobal("chargeMode", mqttpayload);
		// '0': mode sofort
		// '1': mode min+pv
		// '2': mode pv
		// '3': mode stop
		// '4': mode standby
	}
	else if (mqttmsg == 'openWB/global/DailyYieldAllChargePointsKwh') {
		wbdata.updateGlobal("chargeEnergy", makeFloat(mqttpayload));
	}
	else if (mqttmsg == 'openWB/global/DailyYieldHausverbrauchKwh') {
		wbdata.updateGlobal("houseEnergy", makeFloat(mqttpayload));
	}
	// end color theme

	if (mqttmsg == 'openWB/global/WHouseConsumption') {

	}
	else if (mqttmsg == 'openWB/global/WAllChargePoints') {

	}
	else if (mqttmsg == 'openWB/global/strLastmanagementActive') {
		if (mqttpayload.length >= 5) {
			// if there is info-text in payload for topic, show the text
			$('#lastregelungaktiv').text(mqttpayload);
			$('#lastmanagementShowBtn').removeClass('hide');
		} else {
			// if there is no text, show nothing (hides row)
			$('#lastregelungaktiv').text('');
			$('#lastmanagementShowBtn').addClass('hide');
		}
	}
	else if (mqttmsg == 'openWB/global/ChargeMode') {
		// set modal button colors depending on charge mode
		// set visibility of divs
		// set visibility of priority icon depending on charge mode
		// (priority icon is encapsulated in another element hidden/shown by housebattery configured or not)
		switch (mqttpayload) {
			case '0':
				// mode sofort
				$('.chargeModeSelectBtnText').text('Sofort');  // text btn mainpage
				$('.chargeModeBtn').removeClass('btn-success');  // changes to select btns in modal
				$('.chargeModeBtnSofort').addClass('btn-success');
				$('.priorityEvBatteryIcon').addClass('hide');  // visibility of priority icon
				$('.chargeMode').addClass('hide'); // modal chargepoint config
				$('.chargeModeSofort').removeClass('hide'); // modal chargepoint config
				break;
			case '1':
				// mode min+pv
				$('.chargeModeSelectBtnText').text('Min+PV');
				$('.chargeModeBtn').removeClass('btn-success');
				$('.chargeModeBtnMinPV').addClass('btn-success');
				$('.priorityEvBatteryIcon').addClass('hide');
				$('.chargeMode').addClass('hide'); // modal chargepoint config
				$('.chargeModeMinPv').removeClass('hide'); // modal chargepoint config
				break;
			case '2':
				// mode pv
				$('.chargeModeSelectBtnText').text('PV');
				$('.chargeModeBtn').removeClass('btn-success');
				$('.chargeModeBtnPV').addClass('btn-success');
				$('.priorityEvBatteryIcon').removeClass('hide');
				$('.chargeMode').addClass('hide'); // modal chargepoint config
				$('.chargeModePv').removeClass('hide'); // modal chargepoint config
				break;
			case '3':
				// mode stop
				$('.chargeModeSelectBtnText').text('Stop');
				$('.chargeModeBtn').removeClass('btn-success');
				$('.chargeModeBtnStop').addClass('btn-success');
				$('.priorityEvBatteryIcon').addClass('hide');
				$('.chargeMode').addClass('hide'); // modal chargepoint config
				$('.chargeModeStop').removeClass('hide'); // modal chargepoint config
				break;
			case '4':
				// mode standby
				$('.chargeModeSelectBtnText').text('Standby');
				$('.chargeModeBtn').removeClass('btn-success');
				$('.chargeModeBtnStandby').addClass('btn-success');
				$('.priorityEvBatteryIcon').addClass('hide');
				$('.chargeMode').addClass('hide'); // modal chargepoint config
				$('.chargeModeStandby').removeClass('hide'); // modal chargepoint config
				break;
		}
	}
	else if (mqttmsg == 'openWB/global/rfidConfigured') {
		if (mqttpayload == '0') {
			// disable manuel Rfid Code
			$('#rfidCodeBtn').addClass('hide');
		} else {
			// enable manuel Rfid Code
			$('#rfidCodeBtn').removeClass('hide');
		}
	}
}

function processHousebatteryMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/housebattery
	// called by handlevar

	// color theme

	if (mqttmsg == 'openWB/housebattery/W') {
		var speicherwatt = makeInt(mqttpayload);
		if (speicherwatt >= 0) {
			wbdata.updateBat("batteryPowerImport", speicherwatt);
			wbdata.updateBat("batteryPowerExport", 0);
		} else if (speicherwatt < 0) {
			wbdata.updateBat("batteryPowerExport", -speicherwatt);
			wbdata.updateBat("batteryPowerImport", 0);
		}
	}
	else if (mqttmsg == 'openWB/housebattery/%Soc') {
		var speicherSoc = parseInt(mqttpayload, 10);
		if (isNaN(speicherSoc) || speicherSoc < 0 || speicherSoc > 100) {
			speicherSoc = 0;
		}
		wbdata.updateBat("batterySoc", speicherSoc);
	}
	else if (mqttmsg == 'openWB/housebattery/boolHouseBatteryConfigured') {
		wbdata.updateBat("isBatteryConfigured", (mqttpayload == 1));
	}
	else if (mqttmsg == 'openWB/housebattery/DailyYieldExportKwh') {
		wbdata.updateBat("batteryEnergyExport", makeFloat(mqttpayload));
	}
	else if (mqttmsg == 'openWB/housebattery/DailyYieldImportKwh') {
		wbdata.updateBat("batteryEnergyImport", makeFloat(mqttpayload))
	}
	// end color theme

	if (mqttmsg == 'openWB/housebattery/W') {
	}
	else if (mqttmsg == 'openWB/housebattery/%Soc') {
	}
	else if (mqttmsg == 'openWB/housebattery/boolHouseBatteryConfigured') {
		if (mqttpayload == 1) {
			// if housebattery is configured, show info-cards
			$('.hausbatterie').removeClass('hide');
			// and outer element for priority icon in pv mode
			$('.priorityEvBattery').removeClass('hide');
			// priority buttons in modal
			$('#priorityModeBtns').removeClass('hide');
			// update sparklines
			//	$.sparkline_display_visible();
		} else {
			$('.hausbatterie').addClass('hide');
			$('.priorityEvBattery').addClass('hide');
			$('#priorityModeBtns').addClass('hide');
		}
	}
}

function processSystemMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/system
	// called by handlevar
	if (mqttmsg == 'openWB/system/Timestamp') {
		var dateObject = new Date(mqttpayload * 1000);  // Unix timestamp to date-object
		var time = '&nbsp;';
		var date = '&nbsp;';
		if (dateObject instanceof Date && !isNaN(dateObject.valueOf())) {
			// timestamp is valid date so process
			var HH = String(dateObject.getHours()).padStart(2, '0');
			var MM = String(dateObject.getMinutes()).padStart(2, '0');
			time = HH + ':' + MM;
			var dd = String(dateObject.getDate()).padStart(2, '0');  // format with leading zeros
			var mm = String(dateObject.getMonth() + 1).padStart(2, '0'); //January is 0 so add +1!
			var dayOfWeek = dateObject.toLocaleDateString('de-DE', { weekday: 'short' });
			date = dd + '.' + mm + '.' + dateObject.getFullYear();
		}
		$('#time').text(time);
		$('#date').text(date);
	} else if (mqttmsg == 'openWB/system/IpAddress') {
		$('.systemIpAddress').text(mqttpayload);
	} else if (mqttmsg == 'openWB/system/wizzardDone') {
		if (mqttpayload > 99) {
			$("#wizzardModal").modal("hide");
		} else {
			$("#wizzardModal").modal("show");
		}
	} else if (mqttmsg == 'openWB/system/reloadDisplay') {
		if (mqttpayload == '1') {
			reloadDisplay();
		}
	} else if (mqttmsg == 'openWB/system/Uptime') {
		$('.systemUptime').text(mqttpayload);
	} else if (mqttmsg == 'openWB/system/Version') {
		$('.systemVersion').text(mqttpayload);
	}

}

var pv1 = 0;
var pv2 = 0;
function processPvMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/pv
	// called by handlevar

	// color theme
	switch (mqttmsg) {
		case 'openWB/pv/W':
			var pvwatt = parseInt(mqttpayload, 10);
			if (isNaN(pvwatt)) {
				pvwatt = 0;
			}
			if (pvwatt <= 0) {
				pvwatt *= -1;
			}
			wbdata.updatePv("pvwatt", pvwatt);
			break;
		case 'openWB/pv/DailyYieldKwh':
			var pvDailyYield = parseFloat(mqttpayload);
			if (isNaN(pvDailyYield)) {
				pvDailyYield = 0;
			}
			if (pvDailyYield >= 0) {
				wbdata.updatePv("pvDailyYield", pvDailyYield);
			}

			break;
		case 'openWB/pv/bool70PVDynStatus':
			switch (mqttpayload) {
				case '0':
					// deaktiviert
					wbdata.updatePv("pvDyn70Status", false);
					break;
				case '1':
					// ev priority
					wbdata.updatePv("pvDyn70Status", true);
					break;
			}
	}
	// end color theme

	if (mqttmsg == 'openWB/pv/W') {

	}
	else if (mqttmsg == 'openWB/pv/bool70PVDynStatus') {
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
	else if (mqttmsg.match(/^openWB\/pv\/[1-2]+\/boolPVConfigured$/i)) {
		if (mqttmsg == 'openWB/pv/1/boolPVConfigured') {
			pv1 = mqttpayload;
		} else {
			pv2 = mqttpayload;
		}

		if ((pv1 + pv2) > 0) {
			// if pv is configured, show info-cards
			$('.pv').removeClass('hide');
			// update sparklines
			//	$.sparkline_display_visible();
		} else {
			$('.pv').addClass('hide');
		}
	}
}

function processLpMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/lp
	// called by handlevar

	// color theme

	var index = getIndex(mqttmsg); // extraxt number between two / /
	if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/w$/i)) {
		var actualPower = parseInt(mqttpayload, 10);
		if (isNaN(actualPower)) {
			actualPower = 0;
		}
		wbdata.updateCP(index, "power", actualPower);

	} else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/kWhchargedsinceplugged$/i)) {
		// energy charged since ev was plugged in
		// also calculates and displays km charged
		var energyCharged = parseFloat(mqttpayload, 10);
		if (isNaN(energyCharged)) {
			energyCharged = 0;
		}
		wbdata.updateCP(index, "energy", energyCharged);
	} else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/kWhactualcharged$/i)) {
		// energy charged since reset of limitation
		var actualCharged = parseFloat(mqttpayload, 10)
		if (isNaN(actualCharged)) {
			actualCharged = 0;
		}
		wbdata.updateCP(index, "actualCharged", actualCharged);

	} else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/\%soc$/i)) {
		// soc of ev at respective charge point
		var soc = parseInt(mqttpayload, 10);
		if (isNaN(soc) || soc < 0 || soc > 100) {
			soc = 0;
		}
		wbdata.updateCP(index, "soc", soc);
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/timeremaining$/i)) {
		// time remaining for charging to target value
		wbdata.updateCP(index, "timeRemaining", mqttpayload);
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolchargeatnight$/i)) {
		if (mqttpayload == 1) {
			wbdata.updateCP(index, "chargeAtNight", true);
		} else {
			wbdata.updateCP(index, "chargeAtNight", false); 
		}
	} else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolplugstat$/i)) {
		// status ev plugged in or not
		wbdata.updateCP(index, "isPluggedIn", (mqttpayload == 1));
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolchargestat$/i)) {
		wbdata.updateCP(index, "isCharging", (mqttpayload == 1));
	}

	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/strchargepointname$/i)) {
		wbdata.updateCP(index, "name", mqttpayload);
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/chargepointenabled$/i)) {
		wbdata.updateCP(index, "isEnabled", (mqttpayload == 1));
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/countphasesinuse/i)) {
		var phasesInUse = parseInt(mqttpayload, 10);
		if (isNaN(phasesInUse) || phasesInUse < 1 || phasesInUse > 3) {
			phasesInUse = 0;
		}
		wbdata.updateCP(index, "phasesInUse", phasesInUse);
	} else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/aconfigured$/i)) {
		// target current value at charge point
		var targetCurrent = parseInt(mqttpayload, 10);
		if (isNaN(targetCurrent)) {
			targetCurrent = 0;
		}
		wbdata.updateCP(index, "targetCurrent", targetCurrent);
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolsocconfigured$/i)) {
		// soc-module configured for respective charge point
		wbdata.updateCP(index, "isSocConfigured", (mqttpayload == 1));
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolsocmanual$/i)) {
		// manual soc-module configured for respective charge point
		wbdata.updateCP(index, "isSocManual", (mqttpayload == 1));
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolchargepointconfigured$/i)) {
		// respective charge point configured
		wbdata.updateCP(index, "configured", (mqttpayload == 1));
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/autolockconfigured$/i)) {
		wbdata.updateCP(index, "isAutolockConfigured", (mqttpayload == 1));
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/autolockstatus$/i)) {
		// values used for AutolockStatus flag:
		// 0 = standby
		// 1 = waiting for autolock
		// 2 = autolock performed
		// 3 = auto-unlock performed
		wbdata.updateCP(index, "autoLockStatus", mqttpayload);
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/energyconsumptionper100km$/i)) {
		// store configured value in element attribute
		// to calculate charged km upon receipt of charged energy
		var consumption = parseFloat(mqttpayload);
		if (isNaN(consumption)) {
			consumption = 0;
		}
		wbdata.updateCP(index, "energyPer100km", consumption);
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolfinishattimechargeactive$/i)) {
		// respective charge point configured
		wbdata.updateCP(index, "willFinishAtTime", (mqttpayload == 1)); 
	}
	// end color theme

	if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/w$/i)) {

	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/kWhchargedsinceplugged$/i)) {

	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/kWhactualcharged$/i)) { // TODO!

	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/\%soc$/i)) {

	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/timeremaining$/i)) {

	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolchargeatnight$/i)) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.nightChargingLp');  // now get parents respective child element
		if (mqttpayload == 1) {
			element.removeClass('hide');
		} else {
			element.addClass('hide');
		}
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolplugstat$/i)) {
		// status ev plugged in or not
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.plugstatLp');  // now get parents respective child element
		if (mqttpayload == 1) {
			element.removeClass('hide');
		} else {
			element.addClass('hide');
		}
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolchargestat$/i)) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.plugstatLp');  // now get parents respective child element
		if (mqttpayload == 1) {
			element.removeClass('text-warning').addClass('text-success');
		} else {
			element.removeClass('text-success').addClass('text-warning');
		}
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/strchargepointname$/i)) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		if (mqttpayload != 'LP' + index) {
			parent.find('.nameLp').text(mqttpayload + ' (LP' + index + ')');
		}
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/chargepointenabled$/i)) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.enableLp');  // now get parents respective child element
		if (mqttpayload == 0) {
			element.addClass('lpDisabledStyle');
		} else {
			element.removeClass('lpDisabledStyle');
		}
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/countphasesinuse/i)) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.phasesInUseLp');  // now get parents respective child element
		var phasesInUse = parseInt(mqttpayload, 10);
		if (isNaN(phasesInUse) || phasesInUse < 1 || phasesInUse > 3) {
			element.text(' /');
		} else {
			var phaseSymbols = ['', '\u2460', '\u2461', '\u2462'];
			element.text(' ' + phaseSymbols[phasesInUse]);
		}
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/aconfigured$/i)) {
		// target current value at charge point
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.targetCurrentLp');  // now get parents respective child element
		var targetCurrent = parseInt(mqttpayload, 10);
		if (isNaN(targetCurrent)) {
			element.text(' 0 A');
		} else {
			element.text(' ' + targetCurrent + ' A');
		}
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolsocconfigured$/i)) {
		// soc-module configured for respective charge point
		var index = getIndex(mqttmsg);  // extract number between two / /
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
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolsocmanual$/i)) {
		// manual soc-module configured for respective charge point
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var elementIsConfigured = $(parent).find('.socConfiguredLp');  // now get parents respective child element
		if (mqttpayload == 1) {
			$(elementIsConfigured).addClass('manualSoC');
			$(elementIsConfigured).find('.manualSocSymbol').removeClass('hide');
			$(elementIsConfigured).find('.socSymbol').addClass('hide');
		} else {
			$(elementIsConfigured).removeClass('manualSoC');
			$(elementIsConfigured).find('.manualSocSymbol').addClass('hide');
			$(elementIsConfigured).find('.socSymbol').removeClass('hide');
		}
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolchargepointconfigured$/i)) {
		// respective charge point configured
		var index = getIndex(mqttmsg);  // extract number between two / /
		var element = $('[data-lp="' + index + '"]');
		// now show/hide element containing data-lp attribute with value=index
		switch (mqttpayload) {
			case '0':
				element.addClass('hide');
				break;
			case '1':
				element.removeClass('hide');
				// update sparklines
				//	$.sparkline_display_visible();
				break;
		}
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/autolockconfigured$/i)) {
		var index = getIndex(mqttmsg);  // extract first match = number from
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.autolockConfiguredLp');  // now get parents respective child element
		if (mqttpayload == 0) {
			element.addClass('hide');
		} else {
			element.removeClass('hide');
		}
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/autolockstatus$/i)) {
		// values used for AutolockStatus flag:
		// 0 = standby
		// 1 = waiting for autolock
		// 2 = autolock performed
		// 3 = auto-unlock performed
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.autolockConfiguredLp');  // now get parents respective child element
		switch (mqttpayload) {
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
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/energyconsumptionper100km$/i)) {
		// store configured value in element attribute
		// to calculate charged km upon receipt of charged energy
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.kmChargedLp');  // now get parents respective child element
		var consumption = parseFloat(mqttpayload);
		if (isNaN(consumption)) {
			consumption = 0;
		}
		element.data('consumption', consumption);  // store value in data-attribute
		// if already energyCharged-displayed, update kmCharged
		var energyChargedLp = parent.find('.energyChargedLp');  // now get parents respective energyCharged child element
		var energyCharged = parseFloat($(energyChargedLp).text());
		var kmCharged = '';
		if (!isNaN(energyCharged) && consumption > 0) {
			kmCharged = (energyCharged / consumption) * 100;
			kmCharged = kmCharged.toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + ' km';
		} else {
			kmCharged = '-- km';
		}
		element.text(kmCharged);
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolfinishattimechargeactive$/i)) {
		// respective charge point configured
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.targetChargingLp');  // now get parents respective child element
		if (mqttpayload == 1) {
			element.removeClass('hide');
		} else {
			element.addClass('hide');
		}
	}
}
function processSmartHomeDevicesConfigMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/config/get/SmartHome/Devices - config variables (Name / configured only!), actual Variables in proccessSMartHomeDevices
	// called by handlevar
	// color theme
	var index = getIndex(mqttmsg);  // extract number between two / /
	if (mqttmsg.match(/^openwb\/config\/get\/SmartHome\/Devices\/[1-9][0-9]*\/device_configured$/i)) {
		// respective SH Device configured
		wbdata.updateSH(index, "configured", (mqttpayload == 1));
	}
	else if (mqttmsg.match(/^openwb\/config\/get\/SmartHome\/Devices\/[1-9][0-9]*\/mode$/i)) {
		wbdata.updateSH(index, "isAutomatic", (mqttpayload == 0));
	}
	else if (mqttmsg.match(/^openWB\/config\/get\/SmartHome\/Devices\/[1-9][0-9]*\/device_name$/i)) {
		wbdata.updateSH(index, "name", mqttpayload);
	}
	else if (mqttmsg.match(/^openWB\/config\/get\/SmartHome\/Devices\/[1-9][0-9]*\/device_homeConsumtion$/i)) {
		wbdata.updateSH(index, "countAsHouse", (mqttpayload == "1"));
	}

	// end color theme
}
function processSmartHomeDevicesMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/SmartHomeDevices - actual values only!
	// called by handlevar
	var index = getIndex(mqttmsg);  // extract number between two / /
	// color theme
	if (mqttmsg.match(/^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/Watt$/i)) {
		var actualPower = parseInt(mqttpayload, 10);
		if (isNaN(actualPower)) {
			actualPower = 0;
		}
		wbdata.updateSH(index, "power", actualPower);
		// smartHomeList.update();
	} else if (mqttmsg.match(/^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/DailyYieldKwh$/i)) {
		var actualDailyYield = parseFloat(mqttpayload);
		if (isNaN(actualDailyYield)) {
			actualDailyYield = 0;
		}
		wbdata.updateSH(index, "energy", actualDailyYield);
	}
	else if (mqttmsg.match(/^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/RunningTimeToday$/i)) {
		var rTime = parseInt(mqttpayload, 10);
		if (isNaN(rTime)) {
			rTime = 0;
		}
		wbdata.updateSH(index, "runningTime", rTime);
	}
	else if (mqttmsg.match(/^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/RelayStatus$/i)) {
		wbdata.updateSH(index, "isOn", (mqttpayload == 1));
	}
	else if (mqttmsg.match(/^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/Status$/i)) {
		switch (mqttpayload) {
			case '10':
				wbdata.updateSH(index, "status", 'off');
				break;
			case '11':
				wbdata.updateSH(index, "status", 'on');
				break;
			case '20':
				wbdata.updateSH(index, "status", 'on-by-detection');
				break;
			case '30':
				wbdata.updateSH(index, "status", 'on-by-timeout');
				break;
			default:
				wbdata.updateSH(index, "status", 'off');
		}
	}
	else if (mqttmsg.match(/^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/TemperatureSensor0$/i)) {
		var actualTemp = parseFloat(mqttpayload);
		if (isNaN(actualTemp)) {
			actualTemp = 0;
		}
		wbdata.updateSH(index, "temp1", actualTemp);
	}
	else if (mqttmsg.match(/^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/TemperatureSensor1$/i)) {
		var actualTemp = parseFloat(mqttpayload);
		if (isNaN(actualTemp)) {
			actualTemp = 0;
		}
		wbdata.updateSH(index, "temp2", actualTemp);
	}
	else if (mqttmsg.match(/^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/TemperatureSensor2$/i)) {
		var actualTemp = parseFloat(mqttpayload);
		if (isNaN(actualTemp)) {
			actualTemp = 0;
		}
		wbdata.updateSH(index, "temp3", actualTemp);
	}



	// end of color theme




}
function processSmartHomeDevicesStatusMessages(mqttmsg, mqttpayload) {

	// color theme
	if (mqttmsg.match(/^openwb\/SmartHome\/Status\/wattnichtHaus$/i)) {
		var SHPower = parseInt(mqttpayload, 10);
		if (isNaN(SHPower)) {
			SHPower = 0;
		}
		wbdata.updateGlobal("smarthomePower", SHPower);
	}
}
function subscribeMqttGraphSegments() {
	for (var segments = 1; segments < 17; segments++) {
		topic = "openWB/graph/" + segments + "alllivevalues";
		client.subscribe(topic, { qos: 0 });
	}
}

function unsubscribeMqttGraphSegments() {
	for (var segments = 1; segments < 17; segments++) {
		topic = "openWB/graph/" + segments + "alllivevalues";
		client.unsubscribe(topic);
	}
}

function subscribeGraphUpdates() {
	topic = "openWB/graph/lastlivevalues";
	client.subscribe(topic, { qos: 0 });
}

function unsubscribeGraphUpdates() {
	topic = "openWB/graph/lastlivevalues";
	client.unsubscribe(topic);
}

function makeInt(message) {
	var number = parseInt(message, 10);
	if (isNaN(number)) {
		number = 0;
	}
	return number;
}

function makeFloat(message) {
	var number = parseFloat(message, 10);
	if (isNaN(number)) {
		number = 0.0;
	}
	return number;
}
