/**
 * Functions to update graph and gui values via MQTT-messages
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 * @author Lutz Bender
 */

 // global object to store values from mqtt
var lastSparklineValues = [];
// stores data as array of js objects: { chartElement: null, value: 0 }

function storeSparklineValue( element, value ) {
	//console.log("storing Sparkline value: element: "+element.attr('data-chartName')+" value: "+value);
	var done = false;
	for ( index = 0; (index < lastSparklineValues.length) && !done; index++ ) {
		if( lastSparklineValues[index].chartElement.attr('data-chartName') == element.attr('data-chartName') ){
			lastSparklineValues[index].value = value;
			done = true;
		}
	}
	if ( !done ) {
		lastSparklineValues.push( { "chartElement": element, "value": value } );
	}
}

setInterval( updateSparklines, 15000);

function updateSparklines(){
	//console.log("updating Sparklines...");
	for ( index = 0; index < lastSparklineValues.length; index++ ) {
		var chartElement = lastSparklineValues[index].chartElement;
		//console.log("chartElement: "+chartElement.attr('data-chartName'));
		var chartdata = lastSparklineValues[index].chartElement.attr('data-values');
		var chartdataarray = chartdata.split(',');
		// add new value
		chartdataarray.push( lastSparklineValues[index].value );
		// limit data length to 57 values
		chartdataarray = chartdataarray.slice(-57);
		// store values
		chartElement.attr('data-values', chartdataarray.join(','));
		// update chart
		chartElement.sparkline( chartdataarray, {
			// global settings
			//	width: '100%', // problem with hidden sparklines!
			width: '280px',
			height: '60px',
			disableInteraction: true,
			type: 'bar',
			enableTagOptions: true,
			tagOptionsPrefix: 'data-spark',
			tagValuesAttribute: 'data-values'
		});
	}
	//console.log("done updating Sparklines");
}

function updateDashboardElement(elementText, elementChart, text, value){
	// update text
	if(elementText != null){
		elementText.text(text);
	}
	// store value for sparklines
	storeSparklineValue( elementChart, value );
}

function reloadDisplay() {
    /** @function reloadDisplay
     * triggers a reload of the current page
     */
    // wait some seconds to allow other instances receive this message
    setTimeout(function(){
        publish( "0", "openWB/set/system/reloadDisplay" );
        // wait again to give the broker some time and avoid a reload loop
        setTimeout(function(){
            location.reload();
        }, 2000);
    }, 2000);
}

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
	//console.log("Topic: "+mqttmsg+" Message: "+mqttpayload);
	// receives all messages and calls respective function to process them
	if ( mqttmsg.match( /^openwb\/evu\//i) ) { processEvuMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/global\//i) ) { processGlobalMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/housebattery\//i) ) { processHousebatteryMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/system\//i) ) { processSystemMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/pv\//i) ) { processPvMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/lp\//i) ) { processLpMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/config\/get\/sofort\/lp\//i) ) { processSofortConfigMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/config\/get\/pv\//i) ) { processPvConfigMessages(mqttmsg, mqttpayload); }
	else if ( mqttmsg.match( /^openwb\/config\/get\/display\//i) ) { processDisplayConfigMessages(mqttmsg, mqttpayload); }
}  // end handlevar

function processDisplayConfigMessages(mqttmsg, mqttpayload) {
	//console.log("Msg: "+mqttmsg+": "+mqttpayload);
	if ( mqttmsg == 'openWB/config/get/display/showHouseConsumption' ) {
		switch (mqttpayload) {
			case '0':
				// hide house consumption
				$('.hausverbrauch').addClass('hide');
				break;
			case '1':
				// show house consumption
				$('.hausverbrauch').removeClass('hide');
				break;
		}
	}
	else if ( mqttmsg == 'openWB/config/get/display/chartHouseConsumptionMax' ) {
		var chartElement = $('.sparkline[data-chartname=hausverbrauchlchart]');
		chartElement.attr('data-sparkChartRangeMax', mqttpayload);
	}
	else if ( mqttmsg == 'openWB/config/get/display/chartEvuMinMax' ) {
		var chartElement = $('.sparkline[data-chartname=evulchart]');
		chartElement.attr('data-sparkChartRangeMax', mqttpayload);
		chartElement.attr('data-sparkChartRangeMin', mqttpayload*-1);
	}
	else if ( mqttmsg == 'openWB/config/get/display/chartBatteryMinMax' ) {
		var chartElement = $('.sparkline[data-chartname=hausbatteriellchart]');
		chartElement.attr('data-sparkChartRangeMax', mqttpayload);
		chartElement.attr('data-sparkChartRangeMin', mqttpayload*-1);
	}
	else if ( mqttmsg == 'openWB/config/get/display/chartPvMax' ) {
		var chartElement = $('.sparkline[data-chartname=pvlchart]');
		chartElement.attr('data-sparkChartRangeMax', mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/config\/get\/display\/chartLp\/[1-9][0-9]*\/max$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var chartElement = $('.sparkline[data-chartname=ladepunkt'+index+'llchart]');
		chartElement.attr('data-sparkChartRangeMax', mqttpayload);
	}
}

function processPvConfigMessages(mqttmsg, mqttpayload) {
	if ( mqttmsg == 'openWB/config/get/pv/priorityModeEVBattery' ) {
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
	else if ( mqttmsg == 'openWB/config/get/pv/nurpv70dynact' ) {
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
	else if ( mqttmsg == 'openWB/config/get/pv/minCurrentMinPv' ) {
		setInputValue('minCurrentMinPv', mqttpayload);
	}
}

function processSofortConfigMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/config/get/sofort/
	// called by handlevar
	var elementId = mqttmsg.replace('openWB/config/get/sofort/', '');
	var element = $('#' + $.escapeSelector(elementId));
	if ( element.attr('type') == 'range' ) {
		setInputValue(elementId, mqttpayload);
	} else if ( element.hasClass('btn-group-toggle') ) {
		setToggleBtnGroup(elementId, mqttpayload);
	}

}

function processEvuMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/evu
	// called by handlevar
	if ( mqttmsg == 'openWB/evu/W' ) {
		var prefix = '';
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
		updateDashboardElement(element, elementChart, prefix + powerEvuText + unit, powerEvu);
	 }
}

function processGlobalMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/global
	// called by handlevar
	if ( mqttmsg == 'openWB/global/WHouseConsumption' ) {
		var unit = ' W';
		var powerHouse = parseInt(mqttpayload, 10);
		if ( isNaN(powerHouse) || (powerHouse < 0) ) {
			powerHouse = 0;
		}
		powerHouseText = powerHouse.toString();
		if ( powerHouse > 999 ) {
			powerHouseText = (powerHouse / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
			unit = ' kW';
		}
		var element = $('#hausverbrauchl');
		var elementChart = $('#hausverbrauchlchart');
		updateDashboardElement(element, elementChart, powerHouseText + unit, powerHouse);
	}
	else if ( mqttmsg == 'openWB/global/WAllChargePoints') {
		var unit = ' W';
		var powerAllLp = parseInt(mqttpayload, 10);
		if ( isNaN(powerAllLp) ) {
			powerAllLp = 0;
		}
		powerAllLpText = powerAllLp.toString();
		if (powerAllLp > 999) {
			powerAllLpText = (powerAllLp / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
			unit = ' kW';
		}
		var element = $('#gesamtll');
		var elementChart = $('#gesamtllchart');
		updateDashboardElement(element, elementChart, powerAllLpText + unit, powerAllLp);
	}
	else if ( mqttmsg == 'openWB/global/strLastmanagementActive' ) {
		if ( mqttpayload.length >= 5 ) {
			// if there is info-text in payload for topic, show the text
			$('#lastregelungaktiv').text(mqttpayload);
			$('#lastmanagementShowBtn').removeClass('hide');
		} else {
			// if there is no text, show nothing (hides row)
			$('#lastregelungaktiv').text('');
			$('#lastmanagementShowBtn').addClass('hide');
		}
	}
	else if ( mqttmsg == 'openWB/global/ChargeMode' ) {
		// set modal button colors depending on charge mode
		// set visibility of divs
		// set visibility of priority icon depending on charge mode
		// (priority icon is encapsulated in another element hidden/shown by house battery configured or not)
		switch (mqttpayload) {
			case '0':
				// mode sofort
				$('.chargeModeSelectBtnText').text('Sofort');  // text btn main page
				$('.chargeModeBtn').removeClass('btn-success');  // changes to select buttons in modal
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
	else if ( mqttmsg == 'openWB/global/rfidConfigured' ) {
		if ( mqttpayload == '0' ) {
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
	if ( mqttmsg == 'openWB/housebattery/W' ) {
		var prefix = '';
		var unit = ' W';
		var speicherwatt = parseInt(mqttpayload, 10);
		if ( isNaN(speicherwatt) ) {
			speicherwatt = 0;
		}
		// now use a temp value to keep original value with sign for sparkline
		var speicherwattValue = speicherwatt;
		if ( speicherwattValue > 0 ) {
			prefix = 'Ladung: ';
		} else if ( speicherwattValue < 0 ) {
			speicherwattValue *= -1;
			prefix = 'Entladung: ';
		}
		var speicherwattText = speicherwattValue.toString();
		if ( speicherwattValue > 999 ) {
			speicherwattText = (speicherwatt / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
			unit = ' kW';
		}
		var element = $('#hausbatteriell');
		var elementChart = $('#hausbatteriellchart');
		updateDashboardElement(element, elementChart, prefix + speicherwattText + unit, speicherwatt);
	}
	else if ( mqttmsg == 'openWB/housebattery/%Soc' ) {
		var speicherSoc = parseInt(mqttpayload, 10);
		var unit = ' %';
		var speicherSocText = speicherSoc.toString();
		if ( isNaN(speicherSoc) || speicherSoc < 0 || speicherSoc > 100 ) {
			speicherSocText = '--';
		}
		// adjust value for sparkline
		if ( isNaN(speicherSoc) || speicherSoc < 0 ) {
			speicherSoc = 0;
		}
		if ( speicherSoc > 100 ) {
			speicherSoc = 100;
		}
		var element = $('#hausbatteriesoc');
		var elementChart = $('#hausbatteriesocchart');
		updateDashboardElement(element, elementChart, speicherSocText + unit, speicherSoc);
	}
	else if ( mqttmsg == 'openWB/housebattery/boolHouseBatteryConfigured' ) {
		if ( mqttpayload == 1 ) {
			// if housebattery is configured, show info-cards
			$('.hausbatterie').removeClass('hide');
			// and outer element for priority icon in pv mode
			$('.priorityEvBattery').removeClass('hide');
			// priority buttons in modal
			$('#priorityModeBtns').removeClass('hide');
			// update sparklines
			$.sparkline_display_visible();
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
	// console.log(mqttmsg+': '+mqttpayload);
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
	} else if ( mqttmsg == 'openWB/system/IpAddress') {
		$('.systemIpAddress').text(mqttpayload);
	} else if ( mqttmsg == 'openWB/system/wizzardDone' ) {
		if( mqttpayload > 99 ){
			$("#wizzardModal").modal("hide");
		} else {
			$("#wizzardModal").modal("show");
		}
	} else if ( mqttmsg == 'openWB/system/reloadDisplay' ) {
		if( mqttpayload == '1' ){
			reloadDisplay();
		}
	} else if ( mqttmsg == 'openWB/system/Uptime' ) {
		$('.systemUptime').text(mqttpayload);
	} else if ( mqttmsg =='openWB/system/Version' ) {
		$('.systemVersion').text(mqttpayload);
	}

}

var pv1 = 0;
var pv2 = 0;
function processPvMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/pv
	// called by handlevar
	if ( mqttmsg == 'openWB/pv/W') {
		var pvwatt = parseInt(mqttpayload, 10);
		var unit = ' W';
		if ( isNaN(pvwatt) ) {
			pvwatt = 0;
		}
		if ( pvwatt > 0){
			pvwatt = 0;
		}
		if ( pvwatt < 0 ) {
			// production is negative for calculations so adjust for display
			pvwatt *= -1;
		}
		var pvwattText = pvwatt.toString();
		if (pvwatt > 999) {
			pvwattText = (pvwatt / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
			unit = ' kW';
		}
		var element = $('#pvl');
		var elementChart = $('#pvlchart');
		updateDashboardElement(element, elementChart, pvwattText + unit, pvwatt);
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
	else if ( mqttmsg.match(/^openWB\/pv\/[1-2]+\/boolPVConfigured$/i) ) {
		if (mqttmsg == 'openWB/pv/1/boolPVConfigured') {
			pv1 = mqttpayload;
		} else {
			pv2 = mqttpayload;
		}

		if ( (pv1 + pv2) > 0 ) {
			// if pv is configured, show info-cards
			$('.pv').removeClass('hide');
			// update sparklines
			$.sparkline_display_visible();
		} else {
			$('.pv').addClass('hide');
		}
	}
}

function processLpMessages(mqttmsg, mqttpayload) {
	// processes mqttmsg for topic openWB/lp
	// called by handlevar
	if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/w$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.ladepunktll');  // now get parents respective child element
		var actualPower = parseInt(mqttpayload, 10);
		var unit = ' W';
		if ( isNaN(actualPower) ) {
			actualPower = 0;
		}
		var actualPowerText = actualPower.toString();
		if (actualPower > 999) {
			actualPowerText = (actualPower / 1000).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
			unit = ' kW';
		}
		var elementChart = parent.find('.ladepunktllchart');
		updateDashboardElement(element, elementChart, actualPowerText + unit, actualPower);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/kWhchargedsinceplugged$/i ) ) {
		// energy charged since ev was plugged in
		// also calculates and displays km charged
		var index = getIndex(mqttmsg);  // extract number between two / /
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
			kmCharged = kmCharged.toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) + ' km';
		} else {
			kmCharged = '-- km';
		}
		$(kmChargedLp).text(kmCharged);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/kWhactualcharged$/i ) ) { // TODO!
		// energy charged since reset of limitation
		var index = getIndex(mqttmsg);  // extract number between two / /
		if ( isNaN(mqttpayload) ) {
			mqttpayload = 0;
		}
		var parent = $('[data-lp="' + index + '"]');  // get parent div element for charge limitation
		var element = parent.find('.limit-progress-bar');  // now get parents progress bar
		element.data('actualCharged', mqttpayload);  // store value received
		var limitElementId = 'lp/' + index + '/energyToCharge';
		var limit = $('#' + $.escapeSelector(limitElementId)).val();  // slider value
		if ( isNaN(limit) || limit < 2 ) {
			limit = 2;  // minimum value
		}
		var progress = (mqttpayload / limit * 100).toFixed(0);
		element.width(progress+"%");
		parent.find('.limit-progress-label').text(progress+"%");
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/\%soc$/i ) ) {
		// soc of ev at respective charge point
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.socLp');  // now get parents respective child element
		var soc = parseInt(mqttpayload, 10);
		if ( isNaN(soc) || soc < 0 || soc > 100 ) {
			soc = '--';
		}
		element.text(soc + ' %');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/timeremaining$/i ) ) {
		// time remaining for charging to target value
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent div element for charge limitation
		var element = parent.find('.restzeitLp');  // get element
		element.text(mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolchargeatnight$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.nightChargingLp');  // now get parents respective child element
		if ( mqttpayload == 1 ) {
			element.removeClass('hide');
		} else {
			element.addClass('hide');
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolplugstat$/i ) ) {
		// status ev plugged in or not
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.plugstatLp');  // now get parents respective child element
		if ( mqttpayload == 1 ) {
			element.removeClass('hide');
		} else {
			element.addClass('hide');
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolchargestat$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.plugstatLp');  // now get parents respective child element
		if ( mqttpayload == 1 ) {
			element.removeClass('text-warning').addClass('text-success');
		} else {
			element.removeClass('text-success').addClass('text-warning');
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/strchargepointname$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		if( mqttpayload != 'LP'+index ){
			parent.find('.nameLp').text(mqttpayload+' (LP'+index+')');
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/chargepointenabled$/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.enableLp');  // now get parents respective child element
		if ( mqttpayload == 0 ) {
			element.addClass('lpDisabledStyle');
		} else {
			element.removeClass('lpDisabledStyle');
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/countphasesinuse/i ) ) {
		var index = getIndex(mqttmsg);  // extract number between two / /
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
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/aconfigured$/i ) ) {
		// target current value at charge point
		var index = getIndex(mqttmsg);  // extract number between two / /
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.targetCurrentLp');  // now get parents respective child element
		var targetCurrent = parseInt(mqttpayload, 10);
		if ( isNaN(targetCurrent) ) {
			element.text(' 0 A');
		} else {
			element.text(' ' + targetCurrent + ' A');
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolsocconfigured$/i ) ) {
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
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolsocmanual$/i ) ) {
		// console.log(mqttmsg+': '+mqttpayload);
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
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolchargepointconfigured$/i ) ) {
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
				$.sparkline_display_visible();
				break;
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/autolockconfigured$/i ) ) {
		var index = getIndex(mqttmsg);  // extract first match = number from
		var parent = $('[data-lp="' + index + '"]');  // get parent row element for charge point
		var element = parent.find('.autolockConfiguredLp');  // now get parents respective child element
		if ( mqttpayload == 0 ) {
			element.addClass('hide');
		} else {
			element.removeClass('hide');
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/autolockstatus$/i ) ) {
		// values used for AutolockStatus flag:
		// 0 = standby
		// 1 = waiting for autolock
		// 2 = autolock performed
		// 3 = auto-unlock performed
		var index = getIndex(mqttmsg);  // extract number between two / /
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
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/energyconsumptionper100km$/i ) ) {
		// store configured value in element attribute
		// to calculate charged km upon receipt of charged energy
		var index = getIndex(mqttmsg);  // extract number between two / /
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
			kmCharged = kmCharged.toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1}) + ' km';
		} else {
			kmCharged = '-- km';
		}
		element.text(kmCharged);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolfinishattimechargeactive$/i ) ) {
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
