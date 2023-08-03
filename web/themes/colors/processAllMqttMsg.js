/**
 * Functions to update graph and gui values via MQTT-messages
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

var graphrefreshcounter = 0;


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

	if (mqttmsg.match(/^openwb\/graph\//i)) { processGraphMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/evu\//i)) { processEvuMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/global\/awattar\//i)) { processETProviderMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/global\/ETProvider\//i)) { processETProviderMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/global\//i)) { processGlobalMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/housebattery\//i)) { processHousebatteryMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/system\//i)) { processSystemMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/pv\//i)) { processPvMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/verbraucher\//i)) { processVerbraucherMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/lp\//i)) { processLpMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/hook\//i)) { processHookMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/SmartHome\/Devices\//i)) { processSmartHomeDevicesMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/config\/get\/SmartHome\/Devices\//i)) { processSmartHomeDevicesConfigMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/SmartHome\/Status\//i)) { processSmartHomeDevicesStatusMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/config\/get\/sofort\/lp\//i)) { processSofortConfigMessages(mqttmsg, mqttpayload); }
	else if (mqttmsg.match(/^openwb\/config\/get\/pv\//i)) { processPvConfigMessages(mqttmsg, mqttpayload); }
}  // end handlevar

function processETProviderMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/global
	// called by handlevar
	processPreloader(mqttmsg);

	// colors theme
	if (mqttmsg == 'openWB/global/ETProvider/providerName') {
		wbdata.updateET('etProviderName', mqttpayload);
	} else if (mqttmsg == 'openWB/global/ETProvider/modulePath') {
		wbdata.updateET('etModulePath', mqttpayload);
	} else if (mqttmsg == 'openWB/global/awattar/boolAwattarEnabled') {
		wbdata.updateET('isEtEnabled', (mqttpayload == '1'))
	} else if (mqttmsg == 'openWB/global/awattar/pricelist') {
		wbdata.updateET('etPriceList', mqttpayload);
	} else if (mqttmsg == 'openWB/global/awattar/MaxPriceForCharging') {
		wbdata.updateET('etMaxPrice', parseFloat(mqttpayload));
	} else if (mqttmsg == 'openWB/global/awattar/ActualPriceForCharging') {
		wbdata.updateET('etPrice', parseFloat(mqttpayload));
	}


	// end color theme

	if (mqttmsg == 'openWB/global/ETProvider/providerName') {
		$('.etproviderName').text(mqttpayload);
	}
	else if (mqttmsg == 'openWB/global/ETProvider/modulePath') {
		$('.etproviderLink').attr("href", "/openWB/modules/" + mqttpayload + "/stromtarifinfo/infopage.php");
	}
	else if (mqttmsg == 'openWB/global/awattar/boolAwattarEnabled') {
		// sets icon, graph and price-info-field visible/invisible
		if (mqttpayload == '1') {
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

}

function processPvConfigMessages(mqttmsg, mqttpayload) {
	processPreloader(mqttmsg);
	if (mqttmsg == 'openWB/config/get/pv/priorityModeEVBattery') {
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
	else if (mqttmsg == 'openWB/config/get/pv/nurpv70dynact') {
		//  and sets icon in mode select button
		switch (mqttpayload) {
			case '0':
				// deaktiviert
				$('#70ModeBtn').hide();
				break;
			case '1':
				// aktiviert
				$('#70ModeBtn').show();
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
	processPreloader(mqttmsg);
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
	processPreloader(mqttmsg);
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
	processPreloader(mqttmsg);

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
		var prefix = ': ';
		var unit = ' W';
		var powerEvu = parseInt(mqttpayload, 10);
		if (isNaN(powerEvu)) {
			powerEvu = 0;
		}

		if (powerEvu > 0) {
			prefix = ' Imp: ';
		} else if (powerEvu < 0) {
			powerEvu *= -1;
			prefix = ' Exp: ';
		}



		if (powerEvu > 999) {
			powerEvu = (powerEvu / 1000).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
			unit = ' kW';
		}
		$('#bezug').text(prefix + powerEvu + unit);


	}
	else if (mqttmsg == 'openWB/evu/DailyYieldImportKwh') {
		var evuiDailyYield = parseFloat(mqttpayload);
		if (isNaN(evuiDailyYield)) {
			evuiDailyYield = 0;
		}
		if (evuiDailyYield >= 0) {
			var evuiDailyYieldStr = ' (' + evuiDailyYield.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' kWh I)';
			$('#evuidailyyield').text(evuiDailyYieldStr);
		} else {
			$('#evuidailyyield').text("");
		}

	}
	else if (mqttmsg == 'openWB/evu/DailyYieldExportKwh') {
		var evueDailyYield = parseFloat(mqttpayload);
		if (isNaN(evueDailyYield)) {
			evueDailyYield = 0;
		}
		if (evueDailyYield >= 0) {
			var evueDailyYieldStr = ' (' + evueDailyYield.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' kWh E)';
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
	else if (mqttmsg == 'openWB/global/rfidConfigured') {
		wbdata.updateGlobal("rfidConfigured", (mqttpayload == 1))
	}
	else if (mqttmsg == 'openWB/global/DailyYieldAllChargePointsKwh') {
		wbdata.updateGlobal("chargeEnergy", makeFloat(mqttpayload));
	}
	else if (mqttmsg == 'openWB/global/DailyYieldHausverbrauchKwh') {
		wbdata.updateGlobal("houseEnergy", makeFloat(mqttpayload));
	}
	// end color theme

	if (mqttmsg == 'openWB/global/strLastmanagementActive') {
		if (mqttpayload.length >= 5) {
			// if there is info-text in payload for topic, show the text
			$('#lastregelungaktiv').text(mqttpayload);
		} else {
			// if there is no text, show nothing (hides row)
			$('#lastregelungaktiv').text('');
		}
	}
	else if (mqttmsg == 'openWB/global/awattar/boolAwattarEnabled') {
		// sets icon, graph and price-info-field visible/invisible
		if (mqttpayload == '1') {
			$('#etproviderEnabledIcon').show();
			$('#priceBasedCharging').show();
			$('#strompreis').show();
			$('#navStromtarifInfo').removeClass('hide');
		} else {
			$('#etproviderEnabledIcon').hide();
			$('#priceBasedCharging').hide();
			$('#strompreis').hide();
			$('#navStromtarifInfo').addClass('hide');
		}
	}
	else if (mqttmsg == 'openWB/global/awattar/pricelist') {
		// read etprovider values and trigger graph creation
		// loadElectricityPriceChart will show electricityPriceChartCanvas if etprovideraktiv=1 in openwb.conf
		// graph will be redrawn after 5 minutes (new data pushed from cron5min.sh)
		var csvaData = [];
		var rawacsv = mqttpayload.split(/\r?\n|\r/);
		// skip first entry: it is module-name responsible for list
		for (var i = 1; i < rawcsv.length; i++) {
			csvaData.push(rawacsv[i].split(','));
		}
		electricityPriceTimeline = getCol(csvaData, 0);
		electricityPriceChartline = getCol(csvaData, 1);
		loadElectricityPriceChart();
	}
	else if (mqttmsg == 'openWB/global/awattar/MaxPriceForCharging') {
		setInputValue('MaxPriceForCharging', mqttpayload);
	}
	else if (mqttmsg == 'openWB/global/awattar/ActualPriceForCharging') {
		$('#aktuellerStrompreis').text(parseFloat(mqttpayload).toLocaleString(undefined, { maximumFractionDigits: 2 }) + ' ct/kWh');
	}
	else if (mqttmsg == 'openWB/global/ChargeMode') {
		// set modal button colors depending on charge mode
		// set visibility of divs
		// set visibility of priority icon depending on charge mode
		// (priority icon is encapsulated in another element hidden/shown by housebattery configured or not)
		switch (mqttpayload) {
			case '0':
				// mode sofort
				$('#chargeModeSelectBtnText').text('Sofortladen');  // text btn mainpage
				$('.chargeModeBtn').removeClass('btn-success');  // changes to select btns in modal
				$('#chargeModeSofortBtn').addClass('btn-success');
				$('#targetChargingProgress').show();  // visibility of divs for special settings
				$('#sofortladenEinstellungen').show();
				$('#priorityEvBatteryIcon').hide();  // visibility of priority icon
				$('#minundpvladenEinstellungen').hide();

				break;
			case '1':
				// mode min+pv
				$('#chargeModeSelectBtnText').text('Min+PV-Laden');
				$('.chargeModeBtn').removeClass('btn-success');
				$('#chargeModeMinPVBtn').addClass('btn-success');
				$('#targetChargingProgress').hide();
				$('#sofortladenEinstellungen').hide();
				$('#priorityEvBatteryIcon').hide();
				$('#minundpvladenEinstellungen').show();

				break;
			case '2':
				// mode pv
				$('#chargeModeSelectBtnText').text('PV-Laden');
				$('.chargeModeBtn').removeClass('btn-success');
				$('#chargeModePVBtn').addClass('btn-success');
				$('#targetChargingProgress').hide();
				$('#sofortladenEinstellungen').hide();
				$('#priorityEvBatteryIcon').show();
				$('#minundpvladenEinstellungen').hide();

				break;
			case '3':
				// mode stop
				$('#chargeModeSelectBtnText').text('Stop');
				$('.chargeModeBtn').removeClass('btn-success');
				$('#chargeModeStopBtn').addClass('btn-success');
				$('#targetChargingProgress').hide();
				$('#sofortladenEinstellungen').hide();
				$('#priorityEvBatteryIcon').hide();
				$('#minundpvladenEinstellungen').hide();

				break;
			case '4':
				// mode standby
				$('#chargeModeSelectBtnText').text('Standby');
				$('.chargeModeBtn').removeClass('btn-success');
				$('#chargeModeStdbyBtn').addClass('btn-success');
				$('#targetChargingProgress').hide();
				$('#sofortladenEinstellungen').hide();
				$('#priorityEvBatteryIcon').hide();
				$('#minundpvladenEinstellungen').hide();

		}
	}
	else if (mqttmsg == 'openWB/global/DailyYieldAllChargePointsKwh') {
		var llaDailyYield = parseFloat(mqttpayload);
		if (isNaN(llaDailyYield)) {
			llaDailyYield = 0;
		}
		if (llaDailyYield >= 0) {
			var llaDailyYieldStr = ' (' + llaDailyYield.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' kWh)';
			$('#lladailyyield').text(llaDailyYieldStr);
		} else {
			$('#lladailyyield').text("");
		}

	}
	else if (mqttmsg == 'openWB/global/DailyYieldHausverbrauchKwh') {
		var hausverbrauchDailyYield = parseFloat(mqttpayload);
		if (isNaN(hausverbrauchDailyYield)) {
			hausverbrauchDailyYield = 0;
		}
		if (hausverbrauchDailyYield >= 0) {
			var hausverbrauchDailyYieldStr = ' (' + hausverbrauchDailyYield.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' kWh)';
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

	if (mqttmsg == 'openWB/housebattery/boolHouseBatteryConfigured') {
		if (mqttpayload == 1) {
			// if housebattery is configured, show info-div
			$('#speicher').show();
			// and outer element for priority icon in pv mode
			$('#priorityEvBattery').show();
			// priority buttons in modal
			$('#priorityModeBtns').show();
		} else {
			$('#speicher').hide();
			$('#priorityEvBattery').hide();
			$('#priorityModeBtns').hide();
		}
	}
}

function processSystemMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/system
	// called by handlevar
	processPreloader(mqttmsg);
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
			date = dayOfWeek + ', ' + dd + '.' + mm + '.' + dateObject.getFullYear();
		}
		$('#time').text(time);
		$('#date').text(date);
	}
	else if (mqttmsg.match(/^openwb\/system\/daygraphdata[1-9][0-9]*$/i)) {
		powerGraph.updateDay(mqttmsg, mqttpayload);
	}
	else if (mqttmsg.match(/^openwb\/system\/monthgraphdatan[1-9][0-9]*$/i)) {
		powerGraph.updateMonth(mqttmsg, mqttpayload);
	}
	else if (mqttmsg.match(/^openwb\/system\/yeargraphdatan[1-9][0-9]*$/i)) {
		powerGraph.updateYear(mqttmsg, mqttpayload);
	}
	
}

function processPvMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/pv
	// called by handlevar
	processPreloader(mqttmsg);

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
		var pvwatt = parseInt(mqttpayload, 10);
		if (isNaN(pvwatt)) {
			pvwatt = 0;
		}
		if (pvwatt <= 0) {
			// production is negative for calculations so adjust for display
			pvwatt *= -1;
			// adjust and add unit
			if (pvwatt > 999) {
				pvwatt = (pvwatt / 1000).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' kW';
			} else {
				pvwatt += ' W';
			}
		}
		$('#pvleistung').text(pvwatt);
	}
	else if (mqttmsg == 'openWB/pv/DailyYieldKwh') {
		var pvDailyYield = parseFloat(mqttpayload);
		if (isNaN(pvDailyYield)) {
			pvDailyYield = 0;
		}
		if (pvDailyYield >= 0) {
			var pvDailyYieldStr = ' (' + pvDailyYield.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' kWh)';
			$('#pvdailyyield').text(pvDailyYieldStr);
		} else {
			$('#pvdailyyield').text("");
		}

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
}

function processVerbraucherMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/Verbraucher
	// called by handlevar
	processPreloader(mqttmsg);

	// color theme
	var index = getIndex(mqttmsg); // extract number between two / /
	if (mqttmsg.match(/^openwb\/Verbraucher\/[1-2]\/Configured$/i)) {
		wbdata.updateConsumer(index, "configured", (mqttpayload == 1));
	} else if (mqttmsg.match(/^openwb\/Verbraucher\/[1-2]\/Name$/i)) {
		if (mqttpayload != "Name") {
			wbdata.updateConsumer(index, "name", mqttpayload);
		}
	} else if (mqttmsg.match(/^openwb\/Verbraucher\/[1-2]\/Watt$/i)) {
		var consumerPower = parseInt(mqttpayload, 10);
		if (isNaN(consumerPower)) {
			consumerPower = 0;
		}
		wbdata.updateConsumer(index, "power", consumerPower);
	} else if (mqttmsg.match(/^openwb\/Verbraucher\/[1-2]\/DailyYieldImportkWh$/i)) {
		var consumerDailyYield = parseFloat(mqttpayload);
		if (isNaN(consumerDailyYield)) {
			consumerDailyYield = 0;
		}
		wbdata.updateConsumer(index, "energy", consumerDailyYield);

	}

	// end color theme
	var index = getIndex(mqttmsg);  // extract number between two / /
	if (mqttmsg.match(/^openwb\/Verbraucher\/[1-2]\/Configured$/i)) {
		if (mqttpayload == 1) {
			// if at least one device is configured, show info-div
			$('#verbraucher').removeClass("hide");
			// now show info-div for this device
			$('#verbraucher' + index).removeClass("hide");
		} else {
			$('#verbraucher' + index).addClass("hide");
		}
	} else if (mqttmsg.match(/^openwb\/Verbraucher\/[1-2]\/Name$/i)) {
		if (mqttpayload != "Name") {
			$('#verbraucher' + index + 'name').text(mqttpayload);
		}
	} else if (mqttmsg.match(/^openwb\/Verbraucher\/[1-2]\/Watt$/i)) {
		var unit = ' W';
		var verbraucherwatt = parseInt(mqttpayload, 10);
		if (isNaN(verbraucherwatt)) {
			verbraucherwatt = 0;
		}
		if (verbraucherwatt > 999) {
			verbraucherwatt = (verbraucherwatt / 1000).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
			unit = ' kW';
		}
		$('#verbraucher' + index + 'leistung').text(verbraucherwatt + unit);
	} else if (mqttmsg.match(/^openwb\/Verbraucher\/[1-2]\/DailyYieldImportkWh$/i)) {
		var verbraucherDailyYield = parseFloat(mqttpayload);
		if (isNaN(verbraucherDailyYield)) {
			verbraucherDailyYield = 0;
		}
		if (verbraucherDailyYield >= 0) {
			var verbraucherDailyYieldStr = ' (' + verbraucherDailyYield.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' kWh)';
			$('#verbraucher' + index + 'dailyyield').text(verbraucherDailyYieldStr);
		} else {
			$('#verbraucher' + index + 'dailyyield').text("");
		}

	}
}

function processLpMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/lp
	// called by handlevar
	processPreloader(mqttmsg);

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
		wbdata.updateCP(index, "energySincePlugged", energyCharged);
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
	if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/kWhactualcharged$/i)) {
		// energy charged since reset of limitation
		var index = getIndex(mqttmsg);  // extract number between two / /
		if (isNaN(mqttpayload)) {
			mqttpayload = 0;
		}
		var parent = $('[data-lp="' + index + '"]');  // get parent div element for charge limitation
		var element = parent.find('.progress-bar');  // now get parents progressbar
		element.data('actualCharged', mqttpayload);  // store value received
		var limitElementId = 'lp/' + index + '/energyToCharge';
		var limit = $('#' + $.escapeSelector(limitElementId)).val();  // slider value
		if (isNaN(limit) || limit < 2) {
			limit = 2;  // minimum value
		}
		var progress = (mqttpayload / limit * 100).toFixed(0);
		element.width(progress + "%");
	}

	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/timeremaining$/i)) {
		// time remaining for charging to target value
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('.chargeLimitation[data-lp="' + index + '"]');  // get parent div element for charge limitation
		var element = parent.find('.restzeitLp');  // get element
		element.text('Restzeit ' + mqttpayload);
	}



	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/strchargepointname$/i)) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		$('.nameLp').each(function () {  // fill in name for all element of class '.nameLp'
			var lp = $(this).closest('[data-lp]').data('lp');  // get attribute lp from parent
			if (lp == index) {
				$(this).text(mqttpayload);
			}
		});
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/chargepointenabled$/i)) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		$('.nameLp').each(function () {  // check all elements of class '.nameLp'
			var lp = $(this).closest('[data-lp]').data('lp');  // get attribute lp from parent
			if (lp == index) {
				if ($(this).hasClass('enableLp')) {
					// but only apply styles to element in chargepoint info data block
					if (mqttpayload == 0) {
						$(this).removeClass('lpEnabledStyle').addClass('lpDisabledStyle');
					} else {
						$(this).removeClass('lpDisabledStyle').addClass('lpEnabledStyle');
					}
				}
			}
		});
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
			$(elementIsNotConfigured).hide();
			$(elementIsConfigured).show();
		} else {
			$(elementIsNotConfigured).show();
			$(elementIsConfigured).hide();
		}
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/boolchargepointconfigured$/i)) {
		// respective charge point configured
		var index = getIndex(mqttmsg);  // extract number between two / /
		// now show/hide element containing data-lp attribute with value=index
		switch (mqttpayload) {
			case '0':
				$('[data-lp="' + index + '"]').hide();
				break;
			case '1':
				$('[data-lp="' + index + '"]').show();
				break;

		}
	}
	else if (mqttmsg.match(/^openwb\/lp\/[1-9][0-9]*\/autolockconfigured$/i)) {
		var index = getIndex(mqttmsg);  // extract first match = number from
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.autolockConfiguredLp');  // now get parents respective child element
		if (mqttpayload == 0) {
			element.hide();
		} else {
			element.show();
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


}

function processHookMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/hook
	// called by handlevar
	processPreloader(mqttmsg);
	if (mqttmsg.match(/^openwb\/hook\/[1-9][0-9]*\/boolhookstatus$/i)) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		if (mqttpayload == 1) {
			$('#hook' + index).removeClass("bg-danger").addClass("bg-success");
		} else {
			$('#hook' + index).removeClass("bg-success").addClass("bg-danger");
		}
	}
	else if (mqttmsg.match(/^openwb\/hook\/[1-9][0-9]*\/boolhookconfigured$/i)) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		if (mqttpayload == 1) {
			$('#hook' + index).show();
		} else {
			$('#hook' + index).hide();
		}
	}
}

function processSmartHomeDevicesMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/SmartHomeDevices - actual values only!
	// called by handlevar
	processPreloader(mqttmsg);
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
			actualTemp = 0.0;
		}
		wbdata.updateSH(index, "temp1", actualTemp);
	}
	else if (mqttmsg.match(/^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/TemperatureSensor1$/i)) {
		var actualTemp = parseFloat(mqttpayload);
		if (isNaN(actualTemp)) {
			actualTemp = 0.0;
		}
		wbdata.updateSH(index, "temp2", actualTemp);
	}
	else if (mqttmsg.match(/^openwb\/SmartHome\/Devices\/[1-9][0-9]*\/TemperatureSensor2$/i)) {
		var actualTemp = parseFloat(mqttpayload);
		if (isNaN(actualTemp)) {
			actualTemp = 0.0;
		}
		wbdata.updateSH(index, "temp3", actualTemp);
	}



	// end of color theme




}

function processSmartHomeDevicesConfigMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/config/get/SmartHome/Devices - config variables (Name / configured only!), actual Variables in proccessSMartHomeDevices
	// called by handlevar
	processPreloader(mqttmsg);

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
	if (mqttmsg.match(/^openwb\/config\/get\/SmartHome\/Devices\/[1-9][0-9]*\/device_configured$/i)) {
		// respective SH Device configured
		var index = getIndex(mqttmsg);  // extract number between two / /
		var infoElement = $('[data-dev="' + index + '"]');  // get row of SH Device
		if (mqttpayload == 1) {
			infoElement.show();
		} else {
			infoElement.hide();
		}
		var visibleRows = $('[data-dev]:visible');  // show/hide complete block depending on visible rows within
		if (visibleRows.length > 0) {
			$('.smartHome').show();
		} else {
			$('.smartHome').hide();
		}
	}
	else if (mqttmsg.match(/^openwb\/config\/get\/SmartHome\/Devices\/[1-9][0-9]*\/mode$/i)) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-dev="' + index + '"]');  // get parent row element for SH Device
		var element = parent.find('.actualModeDevice');  // now get parents respective child element
		if (mqttpayload == 0) {
			actualMode = "Automatik"
		} else {
			actualMode = "Manuell"
		}
		element.text(actualMode);
		$('.nameDevice').each(function () {  // check all elements of class '.nameDevice'
			var dev = $(this).closest('[data-dev]').data('dev');  // get attribute Device from parent
			if (dev == index) {
				if ($(this).hasClass('enableDevice')) {
					// but only apply styles to element in chargepoint info data block
					if (mqttpayload == 1) {
						$(this).addClass('cursor-pointer').addClass('locked');
					} else {
						$(this).removeClass('cursor-pointer').removeClass('locked');
					}
				}
			}
		});
	}
	else if (mqttmsg.match(/^openWB\/config\/get\/SmartHome\/Devices\/[1-9][0-9]*\/device_name$/i)) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-dev="' + index + '"]');  // get parent row element for SH Device
		var element = parent.find('.nameDevice');  // now get parents respective child element
		element.text(mqttpayload);
		window['d' + index + 'name'] = mqttpayload;
	}
}
function processSmartHomeDevicesStatusMessages(mqttmsg, mqttpayload) {
	processPreloader(mqttmsg);
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

function subscribeDayGraph(date) {
	// var today = new Date();
	var dd = String(date.getDate()).padStart(2, '0');
	var mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
	var yyyy = date.getFullYear();
	graphdate = yyyy + mm + dd;
	for (var segment = 1; segment < 13; segment++) {
		var topic = "openWB/system/DayGraphData" + segment;
		client.subscribe(topic, { qos: 0 });
	}
	publish(graphdate, "openWB/set/graph/RequestDayGraph");
}

function unsubscribeDayGraph() {
	publish("0", "openWB/set/graph/RequestDayGraph");
}

function subscribeMonthGraph(date) {
	var mm = String(date.month + 1).padStart(2, '0'); //January is 0!
	var yyyy = date.year;
	graphdate = yyyy + mm;
	for (var segment = 1; segment < 13; segment++) {
		var topic = "openWB/system/MonthGraphDatan" + segment;
		client.subscribe(topic, { qos: 0 });
	}
	publish(graphdate, "openWB/set/graph/RequestMonthGraphv1");
}

function unsubscribeMonthGraph() {
	for (var segment = 1; segment < 13; segment++) {
		var topic = "openWB/system/MonthGraphDatan" + segment;
		client.unsubscribe(topic);
	}
	publish("0", "openWB/set/graph/RequestMonthGraphv1");
}
function subscribeYearGraph(year) {
	for (var segment = 1; segment < 13; segment++) {
		var topic = "openWB/system/YearGraphDatan" + segment;
		client.subscribe(topic, { qos: 0 });
	}
	publish(String(year), "openWB/set/graph/RequestYearGraphv1");
}

function unsubscribeYearGraph() {
	for (var segment = 1; segment < 13; segment++) {
		var topic = "openWB/system/YearGraphDatan" + segment;
		client.unsubscribe(topic);
	}
	publish("0", "openWB/set/graph/RequestYearGraphv1");
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

