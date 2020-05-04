/**
 * Functions to update graph and values via MQTT
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */
var awattartime = new Array();
var graphawattarprice;
var doInterval;
var do2Interval;
var speichersoc;
var lp1soc;
var lp2soc;
var lp1enabled;
var lp2enabled;
var lp3enabled;
var initialread = 0;
var graphloaded = 0;
var boolDisplayHouseConsumption;
var boolDisplayLoad1;
var boolDisplayLp1Soc;
var boolDisplayLoad2;
var boolDisplayLp2Soc;
var boolDisplayLp1;
var boolDisplayLp2;
var boolDisplayLp3;
var boolDisplayLp4;
var boolDisplayLp5;
var boolDisplayLp6;
var boolDisplayLp7;
var boolDisplayLp8;
var boolDisplayLpAll;
var boolDisplaySpeicherSoc;
var boolDisplaySpeicher;
var boolDisplayEvu;
var boolDisplayPv;
var boolDisplayLegend;
var boolDisplayLiveGraph;
var datasend = 0;
var all1 = 0;
var all2 = 0;
var all3 = 0;
var all4 = 0;
var all5 = 0;
var all6 = 0;
var all7 = 0;
var all8 = 0;
var all1p;
var all2p;
var all3p;
var all4p;
var all5p;
var all6p;
var all7p;
var all8p;
var hidehaus;
// thevalues declare all mqtttopics to be subsribed
var thevalues = [
	["openWB/global/awattar/MaxPriceForCharging", "#"],
	["openWB/global/awattar/pricelist", "#"],
	["openWB/graph/lastlivevalues", "#"],
	["openWB/graph/1alllivevalues", "#"],
	["openWB/graph/2alllivevalues", "#"],
	["openWB/graph/3alllivevalues", "#"],
	["openWB/graph/4alllivevalues", "#"],
	["openWB/graph/5alllivevalues", "#"],
	["openWB/graph/6alllivevalues", "#"],
	["openWB/graph/7alllivevalues", "#"],
	["openWB/graph/8alllivevalues", "#"],
	["openWB/graph/boolDisplayHouseConsumption", "#"],
	["openWB/graph/boolDisplayLoad1", "#"],
	["openWB/graph/boolDisplayLoad2", "#"],
	["openWB/graph/boolDisplayLp1Soc", "#"],
	["openWB/graph/boolDisplayLp2Soc", "#"],
	["openWB/graph/boolDisplayLp1", "#"],
	["openWB/graph/boolDisplayLp2", "#"],
	["openWB/graph/boolDisplayLp3", "#"],
	["openWB/graph/boolDisplayLp4", "#"],
	["openWB/graph/boolDisplayLp5", "#"],
	["openWB/graph/boolDisplayLp6", "#"],
	["openWB/graph/boolDisplayLp7", "#"],
	["openWB/graph/boolDisplayLp8", "#"],
	["openWB/graph/boolDisplayLpAll", "#"],
	["openWB/graph/boolDisplaySpeicherSoc", "#"],
	["openWB/graph/boolDisplaySpeicher", "#"],
	["openWB/graph/boolDisplayEvu", "#"],
	["openWB/graph/boolDisplayLegend", "#"],
	["openWB/graph/boolDisplayLiveGraph", "#"],
	["openWB/graph/boolDisplayPv", "#"],
	["openWB/evu/W", "#"],
	["openWB/global/WHouseConsumption", "#"],
	["openWB/pv/W", "#"],
	["openWB/lp/1/%Soc", "#"],
	["openWB/lp/2/%Soc", "#"],
	// heute geladene kWh ... nicht benutzt im Theme
	["openWB/lp/1/kWhDailyCharged", "#"],
	["openWB/lp/2/kWhDailyCharged", "#"],
	["openWB/lp/3/kWhDailyCharged", "#"],
	// geladene kWh des aktuellen Ladesegments
	["openWB/lp/1/kWhActualCharged", "#"],
	["openWB/lp/2/kWhActualCharged", "#"],
	["openWB/lp/3/kWhActualCharged", "#"],
	// geladene kWh seit anstecken des EV
	["openWB/lp/1/kWhChargedSincePlugged", "#"],
	["openWB/lp/2/kWhChargedSincePlugged", "#"],
	["openWB/lp/3/kWhChargedSincePlugged", "#"],
	["openWB/lp/4/kWhChargedSincePlugged", "#"],
	["openWB/lp/5/kWhChargedSincePlugged", "#"],
	["openWB/lp/6/kWhChargedSincePlugged", "#"],
	["openWB/lp/7/kWhChargedSincePlugged", "#"],
	["openWB/lp/8/kWhChargedSincePlugged", "#"],
	// Ladeleistung am LP
	["openWB/lp/1/W", "#"],
	["openWB/lp/2/W", "#"],
	["openWB/lp/3/W", "#"],
	["openWB/lp/4/W", "#"],
	["openWB/lp/5/W", "#"],
	["openWB/lp/6/W", "#"],
	["openWB/lp/7/W", "#"],
	["openWB/lp/8/W", "#"],
	["openWB/lp/1/boolPlugStat", "#"],
	["openWB/lp/2/boolPlugStat", "#"],
	["openWB/lp/3/boolPlugStat", "#"],
	["openWB/lp/4/boolPlugStat", "#"],
	["openWB/lp/5/boolPlugStat", "#"],
	["openWB/lp/6/boolPlugStat", "#"],
	["openWB/lp/7/boolPlugStat", "#"],
	["openWB/lp/8/boolPlugStat", "#"],
	["openWB/lp/1/boolChargeStat", "#"],
	["openWB/lp/2/boolChargeStat", "#"],
	["openWB/lp/3/boolChargeStat", "#"],
	["openWB/lp/4/boolChargeStat", "#"],
	["openWB/lp/5/boolChargeStat", "#"],
	["openWB/lp/6/boolChargeStat", "#"],
	["openWB/lp/7/boolChargeStat", "#"],
	["openWB/lp/8/boolChargeStat", "#"],
	["openWB/lp/1/boolSocConfigured", "#"],
	["openWB/lp/2/boolSocConfigured", "#"],
	["openWB/lp/1/AConfigured", "#"],
	["openWB/lp/2/AConfigured", "#"],
	["openWB/lp/3/AConfigured", "#"],
	["openWB/lp/8/AConfigured", "#"],
	["openWB/lp/4/AConfigured", "#"],
	["openWB/lp/5/AConfigured", "#"],
	["openWB/lp/6/AConfigured", "#"],
	["openWB/lp/7/AConfigured", "#"],
	["openWB/lp/1/TimeRemaining", "#"],
	["openWB/lp/2/TimeRemaining", "#"],
	["openWB/lp/3/TimeRemaining", "#"],
	["openWB/lp/1/kmCharged", "#"],
	["openWB/lp/2/kmCharged", "#"],
	["openWB/lp/3/kmCharged", "#"],
	// geglätteter Wert erst einmal nicht angezeigt
	["openWB/evu/WAverage", "#"],
	["openWB/lp/1/ChargeStatus", "#"],
	["openWB/lp/2/ChargeStatus", "#"],
	["openWB/lp/3/ChargeStatus", "#"],
	["openWB/lp/4/ChargeStatus", "#"],
	["openWB/lp/5/ChargeStatus", "#"],
	["openWB/lp/6/ChargeStatus", "#"],
	["openWB/lp/7/ChargeStatus", "#"],
	["openWB/lp/8/ChargeStatus", "#"],
	["openWB/global/ChargeMode", "#"],
	["openWB/global/WAllChargePoints", "#"],
	["openWB/housebattery/boolHouseBatteryConfigured", "#"],
	["openWB/housebattery/W", "#"],
	["openWB/housebattery/%Soc", "#"],
	["openWB/global/strLastmanagementActive", "#"],
	["openWB/lp/1/boolChargePointConfigured", "#"],
	["openWB/lp/2/boolChargePointConfigured", "#"],
	["openWB/lp/3/boolChargePointConfigured", "#"],
	["openWB/lp/4/boolChargePointConfigured", "#"],
	["openWB/lp/5/boolChargePointConfigured", "#"],
	["openWB/lp/6/boolChargePointConfigured", "#"],
	["openWB/lp/7/boolChargePointConfigured", "#"],
	["openWB/lp/8/boolChargePointConfigured", "#"],
	["openWB/lp/1/boolDirectChargeMode_none_kwh_soc", "#"],
	["openWB/lp/2/boolDirectChargeMode_none_kwh_soc", "#"],
	["openWB/lp/3/boolDirectChargeMode_none_kwh_soc", "#"],
	["openWB/lp/4/boolDirectChargeMode_none_kwh_soc", "#"],
	["openWB/lp/5/boolDirectChargeMode_none_kwh_soc", "#"],
	["openWB/lp/6/boolDirectChargeMode_none_kwh_soc", "#"],
	["openWB/lp/7/boolDirectChargeMode_none_kwh_soc", "#"],
	["openWB/lp/8/boolDirectChargeMode_none_kwh_soc", "#"],
	["openWB/lp/1/ChargePointEnabled", "#"],
	["openWB/lp/2/ChargePointEnabled", "#"],
	["openWB/lp/3/ChargePointEnabled", "#"],
	["openWB/lp/4/ChargePointEnabled", "#"],
	["openWB/lp/5/ChargePointEnabled", "#"],
	["openWB/lp/6/ChargePointEnabled", "#"],
	["openWB/lp/7/ChargePointEnabled", "#"],
	["openWB/lp/8/ChargePointEnabled", "#"],
	["openWB/lp/1/strChargePointName", "#"],
	["openWB/lp/2/strChargePointName", "#"],
	["openWB/lp/3/strChargePointName", "#"],
	["openWB/lp/4/strChargePointName", "#"],
	["openWB/lp/5/strChargePointName", "#"],
	["openWB/lp/6/strChargePointName", "#"],
	["openWB/lp/7/strChargePointName", "#"],
	["openWB/lp/8/strChargePointName", "#"],
	["openWB/lp/1/AutolockConfigured", "#"],
	["openWB/lp/2/AutolockConfigured", "#"],
	["openWB/lp/3/AutolockConfigured", "#"],
	["openWB/lp/4/AutolockConfigured", "#"],
	["openWB/lp/5/AutolockConfigured", "#"],
	["openWB/lp/6/AutolockConfigured", "#"],
	["openWB/lp/7/AutolockConfigured", "#"],
	["openWB/lp/8/AutolockConfigured", "#"],
	["openWB/lp/1/AutolockStatus", "#"],
	["openWB/lp/2/AutolockStatus", "#"],
	["openWB/lp/3/AutolockStatus", "#"],
	["openWB/lp/4/AutolockStatus", "#"],
	["openWB/lp/5/AutolockStatus", "#"],
	["openWB/lp/6/AutolockStatus", "#"],
	["openWB/lp/7/AutolockStatus", "#"],
	["openWB/lp/8/AutolockStatus", "#"],
	["openWB/lp/1/ADirectModeAmps", "#"],
	["openWB/lp/2/ADirectModeAmps", "#"],
	["openWB/lp/3/ADirectModeAmps", "#"],
	["openWB/lp/4/ADirectModeAmps", "#"],
	["openWB/lp/5/ADirectModeAmps", "#"],
	["openWB/lp/6/ADirectModeAmps", "#"],
	["openWB/lp/7/ADirectModeAmps", "#"],
	["openWB/lp/8/ADirectModeAmps", "#"]
];
var clientuid = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
var client = new Messaging.Client(location.host, 9001, clientuid);

function getCol(matrix, col){
	var column = [];
	for(var i=0; i<matrix.length; i++){
		column.push(matrix[i][col]);
	}
	return column;
}

function handlevar(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	// receives all messages and calls respective function to process them
	if ( mqttmsg.match( /^openwb\/graph\//i ) ) { processGraphMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv); }
	else if ( mqttmsg.match( /^openwb\/evu\//i) ) { processEvuMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv); }
	else if ( mqttmsg.match( /^openwb\/global\//i) ) { processGlobalMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv); }
	else if ( mqttmsg.match( /^openwb\/housebattery\//i) ) { processHousebatteryMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv); }
	else if ( mqttmsg.match( /^openwb\/system\//i) ) { processSystemMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv); }
	else if ( mqttmsg.match( /^openwb\/pv\//i) ) { processPvMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv); }
	else if ( mqttmsg.match( /^openwb\/verbraucher\//i) ) { processVerbraucherMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv); }
	else if ( mqttmsg.match( /^openwb\/set\//i) ) { processSetMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv); }
	else if ( mqttmsg.match( /^openwb\/lp\//i) ) { processLpMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv); }
}  // end handlevar

function processGraphMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	// processes mqttmsg for topic openWB/graph
	// called by handlevar
	if ( mqttmsg == "openWB/graph/boolDisplayHouseConsumption" ) {
		if ( mqttpayload == 1) {
			boolDisplayHouseConsumption = false;
			hidehaus = 'foo';
			$("graphhausdiv").removeClass("fa-toggle-off");
			$("graphhausdiv").addClass("fa-toggle-on");
			$("graphhausdiv").attr("style", "color: green;");
		} else {
			boolDisplayHouseConsumption = true;
			$("graphhausdiv").removeClass("fa-toggle-on");
			$("graphhausdiv").addClass("fa-toggle-off");
			$("graphhausdiv").attr("style", "color: red;");
			hidehaus = 'Hausverbrauch';
		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayLegend" ) {
		if ( mqttpayload == 0) {
			boolDisplayLegend = false;
			document.getElementById("graphlegenddiv").setAttribute("style", "color: red;");
			graphlegenddiv.classList.remove("fa-toggle-on");
			graphlegenddiv.classList.add("fa-toggle-off");
		} else {
			boolDisplayLegend = true;
			document.getElementById("graphlegenddiv").setAttribute("style", "color: green;");
			graphlegenddiv.classList.remove("fa-toggle-off");
			graphlegenddiv.classList.add("fa-toggle-on");

		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayLiveGraph" ) {
		if ( mqttpayload == 0) {
			$('#thegraph').hide();
			boolDisplayLiveGraph = false;
			document.getElementById("graphgraphdiv").setAttribute("style", "color: red;");
			graphgraphdiv.classList.remove("fa-toggle-on");
			graphgraphdiv.classList.add("fa-toggle-off");
		} else {
			$('#thegraph').show();
			boolDisplayLiveGraph = true;
			document.getElementById("graphgraphdiv").setAttribute("style", "color: green;");
			graphgraphdiv.classList.remove("fa-toggle-off");
			graphgraphdiv.classList.add("fa-toggle-on");
		}
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayEvu" ) {
		if ( mqttpayload == 1) {
			boolDisplayEvu = false;
			hideevu = 'foo';
			document.getElementById("graphevudiv").setAttribute("style", "color: green;");
			graphevudiv.classList.remove("fa-toggle-off");
			graphevudiv.classList.add("fa-toggle-on");

		} else {
			boolDisplayEvu = true;
			hideevu = 'Bezug';
			document.getElementById("graphevudiv").setAttribute("style", "color: red;");
			graphevudiv.classList.remove("fa-toggle-on");
			graphevudiv.classList.add("fa-toggle-off");

		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayPv" ) {
		if ( mqttpayload == 1) {
			boolDisplayPv = false;
			hidepv = 'foo';
			document.getElementById("graphpvdiv").setAttribute("style", "color: green;");
			graphpvdiv.classList.remove("fa-toggle-off");
			graphpvdiv.classList.add("fa-toggle-on");
		} else {
			boolDisplayPv = true;
			hidepv = 'PV';
			document.getElementById("graphpvdiv").setAttribute("style", "color: red;");
			graphpvdiv.classList.remove("fa-toggle-on");
			graphpvdiv.classList.add("fa-toggle-off");
		}
		checkgraphload();
	}
	else if ( mqttmsg.match( /^openwb\/graph\/booldisplaylp[1-9][0-9]*$/i ) ) {
		// matches to all messages containing "openwb/graph/booldisplaylp#"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-boolDisplayLP: '+index+'   load='+mqttpayload);
		// now call functions or set variables corresponding to the index
		if ( mqttpayload == 1) {
			window['boolDisplayLp'+index] = false;
			window['hidelp'+index] = 'foo';
			document.getElementById("graphlp"+index+"div").setAttribute("style", "color: green;");
			window['graphlp'+index+'div'].classList.remove('fa-toggle-off');
			window['graphlp'+index+'div'].classList.add('fa-toggle-on');
		} else {
			window['boolDisplayLp'+index] = true;
			window['hidelp'+index] = 'Lp' + index;
			document.getElementById("graphlp"+index+"div").setAttribute("style", "color: red;");
			window['graphlp'+index+'div'].classList.remove('fa-toggle-on');
			window['graphlp'+index+'div'].classList.add('fa-toggle-off');
		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayLpAll" ) {
		if ( mqttpayload == 1) {
			boolDisplayLpAll = false;
			hidelpa = 'foo';
			var element = document.getElementById("graphlpalldiv");
			graphlpalldiv.classList.remove("fa-toggle-off");
			graphlpalldiv.classList.add("fa-toggle-on");
			element.setAttribute("style", "color: green;");
		} else {
			boolDisplayLpAll = true;
			hidelpa = 'LP Gesamt';
			var element = document.getElementById("graphlpalldiv");
			graphlpalldiv.classList.remove("fa-toggle-on");
			graphlpalldiv.classList.add("fa-toggle-off");
			element.setAttribute("style", "color: red;");

		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplaySpeicher" ) {
		if ( mqttpayload == 1) {
			boolDisplaySpeicher = false;
			hidespeicher = 'foo';
			document.getElementById("graphspeicherdiv").setAttribute("style", "color: green;");
			graphspeicherdiv.classList.remove("fa-toggle-off");
			graphspeicherdiv.classList.add("fa-toggle-on");
		} else {
			hidespeicher = 'Speicherleistung';
			boolDisplaySpeicher = true;
			document.getElementById("graphspeicherdiv").setAttribute("style", "color: red;");
			graphspeicherdiv.classList.remove("fa-toggle-on");
			graphspeicherdiv.classList.add("fa-toggle-off");

		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplaySpeicherSoc" ) {
		if ( mqttpayload == 1) {
			hidespeichersoc = 'foo';
			boolDisplaySpeicherSoc = false;
			document.getElementById("graphspeichersocdiv").setAttribute("style", "color: green;");
			graphspeichersocdiv.classList.remove("fa-toggle-off");
			graphspeichersocdiv.classList.add("fa-toggle-on");
		} else {
			hidespeichersoc = 'Speicher SoC';
			boolDisplaySpeicherSoc = true;
			document.getElementById("graphspeichersocdiv").setAttribute("style", "color: red;");
			graphspeichersocdiv.classList.remove("fa-toggle-on");
			graphspeichersocdiv.classList.add("fa-toggle-off");

		}
		checkgraphload();
	}
	else if ( mqttmsg.match( /^openwb\/graph\/booldisplaylp[1-9][0-9]*soc$/i ) ) {
		// matches to all messages containing "openwb/graph/booldisplaylp#soc"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-boolDisplayLpSoc: '+index+'   load='+mqttpayload);
		if ( mqttpayload == 1) {
			$('#socenabledlp'+index).show();
			window['boolDisplayLp'+index+'Soc'] = false;
			window['hidelp'+index+'soc'] = 'foo';
			document.getElementById("graphlp"+index+"socdiv").setAttribute("style", "color: green;");
			window['graphlp'+index+'socdiv'].classList.remove('fa-toggle-off');
			window['graphlp'+index+'socdiv'].classList.add('fa-toggle-on');
		} else {
			$('#socenabledlp'+index).hide();
			window['boolDisplayLp'+index+'Soc'] = true;
			window['hidelp'+index+'soc'] = 'LP'+index+' SoC';
			document.getElementById("graphlp"+index+"socdiv").setAttribute("style", "color: red;");
			window['graphlp'+index+'socdiv'].classList.remove('fa-toggle-on');
			window['graphlp'+index+'socdiv'].classList.add('fa-toggle-off');
		}
		checkgraphload();
	}
	else if ( mqttmsg.match( /^openwb\/graph\/booldisplayload[1-9][0-9]*$/i ) ) {
		// matches to all messages containing "openwb/graph/booldisplayload#"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-boolDisplayLoad: '+index+'   load='+mqttpayload);
		// now call functions or set variables corresponding to the index
		if ( mqttpayload == 1) {
			window['hideload'+index] = 'foo';
			window['boolDisplayLoad'+index] = false;
			document.getElementById("graphload"+index+"div").setAttribute("style", "color: green;");
			window['graphload'+index+'div'].classList.remove('fa-toggle-off');
			window['graphload'+index+'div'].classList.add('fa-toggle-on');
		} else {
			window['hideload'+index] = 'Verbraucher ' + index;
			window['boolDisplayLoad'+index] = true;
			document.getElementById("graphload"+index+"div").setAttribute("style", "color: red;");
			window['graphload'+index+'div'].classList.remove('fa-toggle-on');
			window['graphload'+index+'div'].classList.add('fa-toggle-off');
		}
		checkgraphload();
	}
	else if ( mqttmsg.match( /^openwb\/graph\/[1-9][0-9]*alllivevalues$/i ) ) {
		// matches to all messages containing "openwb/graph/#alllivevalues"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-alllivevalues: '+index);
		// now call functions or set variables corresponding to the index
		if (initialread == 0) {
			window['all'+index+'p'] = mqttpayload;
			window['all'+index] = 1;
		putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/graph/alllivevalues" ) {
		if ( initialread == -10) {
			var csvData = new Array();
			var rawcsv = mqttpayload.split(/\r?\n|\r/);
			for (var i = 0; i < rawcsv.length; i++) {
				  csvData.push(rawcsv[i].split(','));
			}
			// Retrived data from csv file content
			var splittime = new Array();
			getCol(csvData, 0).forEach(function(zeit){
				splittime.push(zeit.substring(0, zeit.length -3));
			});
			atime = splittime;
			//atime = getCol(csvData, 0);
			abezug = getCol(csvData, 1);
			alpa = getCol(csvData, 2);
			apv = getCol(csvData, 3);
			alp1 = getCol(csvData, 4);
			alp2 = getCol(csvData, 5);
			aspeicherl = getCol(csvData, 7);
			aspeichersoc = getCol(csvData, 8);
			asoc = getCol(csvData, 9);
			asoc1 = getCol(csvData, 10);
			ahausverbrauch = getCol(csvData, 11);
			averbraucher1 = getCol(csvData, 12);
			averbraucher2 = getCol(csvData, 13);
			alp3 = getCol(csvData, 14);
			alp4 = getCol(csvData, 15);
			alp5 = getCol(csvData, 16);
			alp6 = getCol(csvData, 17);
			alp7 = getCol(csvData, 18);
			alp8 = getCol(csvData, 19);
			initialread +=1 ;
			checkgraphload();
		}
	}
	else if ( mqttmsg == "openWB/graph/lastlivevalues" ) {
		if ( initialread > 0) {
			var lines = mqttpayload.split("\n");
			for (var i = 0; i < lines.length; i++) {
				var ldate = lines[i].split(",")[0];
				var lbezug = lines[i].split(",")[1];
				var lpv = lines[i].split(",")[3];
				var llp2 = lines[i].split(",")[5];
				var lspeicherl = lines[i].split(",")[7];
				var lsoc = lines[i].split(",")[9];
				var lspeichersoc = lines[i].split(",")[8];
				var lpa = lines[i].split(",")[2];
				var llp1 = lines[i].split(",")[4];
				var lsoc1 = lines[i].split(",")[10];
				var lhausverbrauch = lines[i].split(",")[11];
				var lverbraucher1 = lines[i].split(",")[12];
				var lverbraucher2 = lines[i].split(",")[13];
				var lp3 = lines[i].split(",")[14];
				var lp4 = lines[i].split(",")[15];
				var lp5 = lines[i].split(",")[16];
				var lp6 = lines[i].split(",")[17];
				var lp7 = lines[i].split(",")[18];
				var lp8 = lines[i].split(",")[19];
			}
			myLine.data.labels.push(ldate.substring(0, ldate.length -3));
			myLine.data.datasets[2].data.push(lbezug);
			myLine.data.datasets[3].data.push(lpv);
			myLine.data.datasets[4].data.push(lspeicherl);
			myLine.data.datasets[5].data.push(lspeichersoc);
			myLine.data.datasets[6].data.push(lsoc);
			myLine.data.datasets[0].data.push(llp1);
			myLine.data.datasets[1].data.push(llp2);
			myLine.data.datasets[7].data.push(lsoc1);
			myLine.data.datasets[8].data.push(lhausverbrauch);
			myLine.data.datasets[9].data.push(lverbraucher1);
			myLine.data.datasets[10].data.push(lverbraucher2);
			myLine.data.datasets[11].data.push(lpa);
			myLine.data.datasets[12].data.push(lp3);
			myLine.data.datasets[13].data.push(lp4);
			myLine.data.datasets[14].data.push(lp5);
			myLine.data.datasets[15].data.push(lp6);
			myLine.data.datasets[16].data.push(lp7);
			myLine.data.datasets[17].data.push(lp8);
			myLine.data.labels.splice(0, 1);
			myLine.data.datasets.forEach(function(dataset) {
				dataset.data.splice(0, 1);
			});
			myLine.update();
		}
	}
}  // end processGraphMessages

function processEvuMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	// processes mqttmsg for topic openWB/evu
	// called by handlevar
	if ( mqttmsg == "openWB/evu/W" ) {
		// zur Regelung: Einspeisung = negativ, Bezug = positiv
		// Vorzeichen zur Darstellung umdrehen
		var anzeigeWert = parseInt(mqttpayload,10) * -1;
		var anzeigeText = 'Einspeisung';
		if (anzeigeWert < 0) anzeigeText = 'Bezug';
		// Text und Farbe des Labels anpassen je nach Einspeisung/Bezug
		// Neuzeichnung erfolgt bei Update der Werte
		// updateGaugeBottomText(gaugeEVU, anzeigeText, true, true);
		// Gauge mit Rückgabewert und Text erneuern, symmetrische Gauge Min-Max, kein AutoRescale
		updateGaugeValue(gaugeEVU, anzeigeWert, anzeigeText, true, true, false);
	 }
}

function processGlobalMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	// processes mqttmsg for topic openWB/global
	// called by handlevar
	if ( mqttmsg == "openWB/global/WHouseConsumption" ) {
		var anzeigeWert = parseInt(mqttpayload,10);
		if (anzeigeWert < 0) {
			// beim Hausverbrauch bleibt Gauge im positiven Bereich
			// negative Werte werden = 0 gesetzt
			anzeigeWert = 0;
		}
		// Gauge mit Rückgabewert erneuern, kein Text, asymmetrische Gauge 0-Max, AutoRescale
		updateGaugeValue(gaugeHome, anzeigeWert, '', false, false, true);
	}
	else if ( mqttmsg == "openWB/global/awattar/pricelist" ) {
		// read awattar values and trigger graph creation
		// loadawattargraph will show awattardiv is awataraktiv=1 in openwb.conf
		// graph will be redrawn after 5 minutes (new data pushed from cron5min.sh)
		var csvaData = new Array();
		var rawacsv = mqttpayload.split(/\r?\n|\r/);
		for (var i = 0; i < rawacsv.length; i++) {
			  csvaData.push(rawacsv[i].split(','));
		}
		awattartime = getCol(csvaData, 0);
		graphawattarprice = getCol(csvaData, 1);
		loadawattargraph();
	}
	else if ( mqttmsg == "openWB/global/awattar/MaxPriceForCharging" ) {
		document.getElementById("awattar1s").value = mqttpayload;
		document.getElementById("awattar1l").innerHTML = mqttpayload;
	}
	else if ( mqttmsg == "openWB/global/ChargeMode" ) {
		// set button colors depending on charge mode
		switch (mqttpayload) {
			case "0":
				// mode sofort
				$('#targetChargingProgressDiv').show();
				$('#sofortBtn').addClass("btn-green").removeClass("btn-red");
				$('#minUndPvBtn').addClass("btn-red").removeClass("btn-green");
				$('#pvBtn').addClass("btn-red").removeClass("btn-green");
				$('#stopBtn').addClass("btn-red").removeClass("btn-green");
				$('#standbyBtn').addClass("btn-red").removeClass("btn-green");
				break;
			case "1":
				// mode min+pv
				$('#targetChargingProgressDiv').hide();
				$('#sofortBtn').addClass("btn-red").removeClass("btn-green");
				$('#minUndPvBtn').addClass("btn-green").removeClass("btn-red");
				$('#pvBtn').addClass("btn-red").removeClass("btn-green");
				$('#stopBtn').addClass("btn-red").removeClass("btn-green");
				$('#standbyBtn').addClass("btn-red").removeClass("btn-green");
				break;
			case "2":
				// mode pv
				$('#targetChargingProgressDiv').hide();
				$('#sofortBtn').addClass("btn-red").removeClass("btn-green");
				$('#minUndPvBtn').addClass("btn-red").removeClass("btn-green");
				$('#pvBtn').addClass("btn-green").removeClass("btn-red");
				$('#stopBtn').addClass("btn-red").removeClass("btn-green");
				$('#standbyBtn').addClass("btn-red").removeClass("btn-green");
				break;
			case "3":
				// mode stop
				$('#targetChargingProgressDiv').hide();
				$('#sofortBtn').addClass("btn-red").removeClass("btn-green");
				$('#minUndPvBtn').addClass("btn-red").removeClass("btn-green");
				$('#pvBtn').addClass("btn-red").removeClass("btn-green");
				$('#stopBtn').addClass("btn-green").removeClass("btn-red");
				$('#standbyBtn').addClass("btn-red").removeClass("btn-green");
				break;
			case "4":
				// mode standby
				$('#targetChargingProgressDiv').hide();
				$('#sofortBtn').addClass("btn-red").removeClass("btn-green");
				$('#minUndPvBtn').addClass("btn-red").removeClass("btn-green");
				$('#pvBtn').addClass("btn-red").removeClass("btn-green");
				$('#stopBtn').addClass("btn-red").removeClass("btn-green");
				$('#standbyBtn').addClass("btn-green").removeClass("btn-red");
		}
		loaddivs();
	}
}

function processHousebatteryMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	// processes mqttmsg for topic openWB/housebattery
	// called by handlevar
	if ( mqttmsg == "openWB/housebattery/W" ) {
		// Entladung = negativ, Ladung = positiv
		var anzeigeWert = parseInt(mqttpayload, 10);
		var anzeigeText = 'Ladung';
		if (anzeigeWert < 0) anzeigeText = 'Entadung';
		// Text und Farbe des Labels anpassen je nach Ladung/Entadung
		// Neuzeichnung erfolgt bei Update der Werte
		// updateGaugeBottomText(gaugeBatt, anzeigeText, true, true);
		// Gauge mit Rückgabewert und Text erneuern, symmetrische Gauge Min-Max, kein AutoRescale
		updateGaugeValue(gaugeBatt, anzeigeWert, anzeigeText, true, true, false);
	}

	else if ( mqttmsg == "openWB/housebattery/%Soc" ) {
		// ProgressBar mit Rückgabewert erneuern
		progressBarSoC.value = parseInt(mqttpayload, 10);
		progressBarSoC.set('title', 'SoC: '+mqttpayload+'%');
		progressBarSoC.grow();
	}
	else if ( mqttmsg == "openWB/housebattery/boolHouseBatteryConfigured" ) {
		if ( mqttpayload == 1 ) {
			// if housebattery is configured, show div
			$('#speicherdiv').show();
		}
	}
}

function processSystemMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	// processes mqttmsg for topic openWB/system
	// called by handlevar
}

function processPvMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	// processes mqttmsg for topic openWB/pv
	// called by handlevar
	if ( mqttmsg == "openWB/pv/W") {
		var pvPower = parseInt(mqttpayload, 10);
		if ( pvPower > 0 ) {
			// if pv-power is positive, adjust to 0
			// since pv cannot consume power
			pvPower = 0;
		}
		// convert raw number for display
		if ( pvPower <= 0){
			// production is negative for calculations so adjust for display
			pvPower = pvPower * -1;
			updateGaugeValue(gaugePV, pvPower, "", true, true, false);
			// adjust and add unit
			if (pvPower > 999) {
				var pvPowerStr = (pvPower / 1000).toFixed(2) + " kW";
			} else {
				var pvPowerStr = pvPower + " W";
			}
			// only if production
			if (pvPower > 0) {
				pvPowerStr += " Erzeugung";
			}
		}
	}
}

function processVerbraucherMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	// processes mqttmsg for topic openWB/Verbraucher
	// called by handlevar
}

function processSetMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	// processes mqttmsg for topic openWB/set
	// called by handlevar
}

function processLpMessages(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	// processes mqttmsg for topic openWB/lp
	// called by handlevar
	if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolchargepointconfigured$/i ) ) {
		// matches to all messages containing "openwb/lp/#/boolchargepointconfigured"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
 		if ( mqttpayload == 0 ) {
			$('#lp'+index+'div').hide();
			$('#slider'+index+'div').hide();
		} else {
			$('#lp'+index+'div').show();
			$('#slider'+index+'div').show();
			// until functionality is still in livefunctions.js
			// only process LP1 here
			if ( index == 1 ) {
				$('#lp'+index+'lldiv').show();
			}
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/chargepointenabled$/i ) ) {
		// matches to all messages containing "openwb/lp/#/boolchargepointenabled"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		var element = "#lp"+index+"enableddiv";
		if ( mqttpayload == 0 ) {
			window['lp'+index+'enabled'] = 0;
			$(element).removeClass("fa-check text-success");
			$(element).addClass("fa-times text-danger");
		} else {
			window['lp'+index+'enabled'] = 1;
			$(element).removeClass("fa-times text-danger");
			$(element).addClass("fa-check text-success");
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/autolockconfigured$/i ) ) {
		// matches to all messages containing "openwb/lp/#/autolockconfigured"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		if ( mqttpayload == 0 ) {
			// hide icon
			$("#lp"+index+"AutolockConfiguredSpan").hide();
		} else {
			// show icon
			$("#lp"+index+"AutolockConfiguredSpan").show();
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
		var element = "#lp"+index+"AutolockConfiguredSpan";  // element to manipulate
		switch ( mqttpayload ) {
			case "0":
				// remove animation from span and set standard colored key icon
				$(element).removeClass("fa-lock fa-lock-open animate-alertPulsation text-danger text-success");
				$(element).addClass("fa-key");
				break;
			case "1":
				// add animation to standard icon
				$(element).removeClass("fa-lock fa-lock-open text-danger text-success");
				$(element).addClass("fa-key animate-alertPulsation");
				break;
			case "2":
				// add red locked icon
				$(element).removeClass("fa-lock-open fa-key animate-alertPulsation text-success");
				$(element).addClass("fa-lock text-danger");
				break;
			case "3":
				// add green unlock icon
				$(element).removeClass("fa-lock fa-key animate-alertPulsation text-danger");
				$(element).addClass("fa-lock-open text-success");
				break;
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolchargeatnight$/i ) ) {
		// matches to all messages containing "openwb/lp/#/boolchargeatnight"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		if ( document.getElementById("nachtladenaktivlp"+index+"div") ) {
			if ( mqttpayload == 1 ) {
				document.getElementById("nachtladenaktivlp"+index+"div").classList.add("fa-moon");
			} else {
				document.getElementById("nachtladenaktivlp"+index+"div").classList.remove("fa-moon");
			}
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/kWhactualcharged$/i ) ) {
		// matches to all messages containing "openwb/lp/#/kWhactualcharged"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		$("#aktgeladen"+index+"div").html(mqttpayload+" kWh");
		if ( document.getElementById("prog"+index) ) {
			// only if target element exists
			document.getElementById("prog"+index).value= mqttpayload;
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/w$/i ) ) {
		// actual charing power at respective charge point
		// matches to all messages containing "openwb/lp/#/w"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		var actualPower = parseInt(mqttpayload, 10);
		if (actualPower > 999) {
			actualPower = (actualPower / 1000).toFixed(2);
			actualPower += " kW";
		} else {
		actualPower += " W";
		}
		$("#actualPowerLp"+index+"div").html(actualPower);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/kWhchargedsinceplugged$/i ) ) {
		// energy charged since ev was plugged in
		// matches to all messages containing "openwb/lp/#/kWhchargedsinceplugged"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-W: '+index+'   load='+mqttpayload);
		var energyCharged = parseFloat(mqttpayload, 10).toFixed(2) + " kWh";
		$("#energyChargedLp"+index+"div").html(energyCharged);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/kmcharged$/i ) ) {
		// km charged at current charging segment
		// matches to all messages containing "openwb/lp/#/timeremaining"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		$("#gelrlp"+index+"div").html(mqttpayload+" km");
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/timeremaining$/i ) ) {
		// time remaining for charging to target value
		// matches to all messages containing "openwb/lp/#/timeremaining"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-W: '+index+'   load='+mqttpayload);
		$("#restzeitlp"+index+"div").html(mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/aconfigured$/i ) ) {
		// target current value at charge point
		// matches to all messages containing "openwb/lp/#/aconfigured"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		var targetCurrent = " / " + parseInt(mqttpayload, 10) + " A";
		$("#targetCurrentLp"+index+"div").html(targetCurrent);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolplugstat$/i ) ) {
		// matches to all messages containing "openwb/lp/#/boolplugstat"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-boolPlugStat: '+index+'   load='+mqttpayload);
		if ( $('#plugstatlp'+index+'div').length > 0 ) {
			if ( mqttpayload == 1 ) {
				document.getElementById("plugstatlp"+index+"div").classList.add("fa-plug");
			} else {
				document.getElementById("plugstatlp"+index+"div").classList.remove("fa-plug");
			}
		}
		if ($('#carlp'+index).length > 0) {
			var elementcarlp1 = document.getElementById("carlp1");
			if (mqttpayload == 1) {
				document.getElementById("carlp"+index).setAttribute("style", "color: green;");
			} else {
				document.getElementById("carlp"+index).setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolchargestat$/i ) ) {
		// matches to all messages containing "openwb/lp/#/boolchargestat"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-boolChargeStat: '+index+'   load='+mqttpayload);
		if ($('#plugstatlp'+index+'div').length > 0) {
			if (mqttpayload == 1) {
				document.getElementById("plugstatlp"+index+"div").setAttribute("style", "color: #00FF00;");
			} else {
				document.getElementById("plugstatlp"+index+"div").setAttribute("style", "color: white;");
			}
		}
		if ($('#socstatlp'+index).length > 0) {
			if (mqttpayload == 1) {
				document.getElementById("socstatlp"+index).setAttribute("style", "color: #00FF00;");
			} else {
				document.getElementById("socstatlp"+index).setAttribute("style", "color: black;");
			}
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/\%soc$/i ) ) {
		// soc of ev at respective charge point
		// matches to all messages containing "openwb/lp/#/%soc"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		window['lp'+index+'soc'] = mqttpayload;
		$("#socLp"+index).html(mqttpayload+' %');
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/chargestatus$/i ) ) {
		// matches to all messages containing "openwb/lp/#/chargestatus"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-ChargeStatus: '+index+'   load='+mqttpayload);
		if ($('#stationlp'+index).length > 0) {
			if (mqttpayload == 1) {
				document.getElementById("stationlp"+index).setAttribute("style", "color: #00FF00;");
			} else {
				document.getElementById("stationlp"+index).setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/adirectmodeamps$/i ) ) {
		// matches to all messages containing "openwb/lp/#/adirectmodeamps"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-ADirectModeAmps: '+index+'   load='+mqttpayload);
		document.getElementById("sofortlllp"+index+"s").value = mqttpayload;
		document.getElementById("sofortlllp"+index+"l").innerHTML = mqttpayload;
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/booldirectchargemode_none_kwh_soc$/i ) ) {
		// matches to all messages containing "openwb/lp/#/booldirectchargemode_none_kwh_soc"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		// selects the direct charge sub mode in the selector if in the mode-range 0..2
		// and shows the correspnding parameter selector and achievment fields
		var mode = parseInt(mqttpayload);
		if ( !isNaN(mode) ) {
			// make sure that mqttmsg is a number
			if ( mqttpayload >= 0 && mqttpayload <= 2 ) {
			 	// if ( document.getElementById("directChargeSubModeLp"+index) ) {
				// 	document.getElementById("directChargeSubModeLp"+index).val = mode;
			  	//};
				//var myElem1 = document.getElementById("directChargeSubModeProgressLp"+index+"div");
				//var myElem2 = document.getElementById("directChargeSubModeTimeRemainingLp"+index+"div");
				//if ( myElem1 && myElem2 ) {
					// if both divs exist make them visible/invisible as needed
					//switch ( mode ) {
						//case 0:
								//$(myElem1).show();
								//$(myElem2).show();
								//console.log("alles ist an");
							//break;
						//case 1:
							//break;
						//case 2:
							//break;
					//}
		  		//}
			}
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/strchargepointname$/i ) ) {
		// matches to all messages containing "openwb/lp/#/strchargepointname"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		// fill span-tags from class=strChargePointName with respective payload-string
		// and set the div visibility from hidden to visible
		var ele = document.getElementsByClassName("nameLp"+index);
	    for(var i=0; i<ele.length; i++) {
	      	ele[i].textContent = mqttpayload;
	    }
		if ( document.getElementById("directChargeSubModeLp"+index+"div") ) {
				document.getElementById("directChargeSubModeLp"+index+"div").style.visibility = "visible";
		}
	}
	if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolsocconfigured$/i ) ) {
		// is a soc-module configured for respective charge point
		// matches to all messages containing "openwb/lp/#/boolsocconfigured"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		// change visibility of div
		if (mqttpayload == 1) {
			$('#socNotConfiguredLp'+index+'div').hide();
			$('#socConfiguredLp'+index+'div').show();
		}
	}
}

//Gets  called if the websocket/mqtt connection gets disconnected for any reason
client.onConnectionLost = function (responseObject) {
	client.connect(options);
};
//Gets called whenever you receive a message
client.onMessageArrived = function (message) {
		handlevar(message.destinationName, message.payloadString, thevalues[0], thevalues[1]);
};
var retries = 0;

//Connect Options
var isSSL = location.protocol == 'https:';
var options = {
	timeout: 5,
	useSSL: isSSL,
	//Gets Called if the connection has sucessfully been established
	onSuccess: function () {
		retries = 0;
		thevalues.forEach(function(thevar) {
			client.subscribe(thevar[0], {qos: 0});
		});
	},
	//Gets Called if the connection could not be established
	onFailure: function (message) {
		client.connect(options);
	}
	};

//Creates a new Messaging.Message Object and sends it
var publish = function (payload, topic) {
	var message = new Messaging.Message(payload);
	message.destinationName = topic;
	message.qos = 2;
	message.retained = true;
	client.send(message);
}

client.connect(options);

function graphoptionclick() {
	if ( document.getElementById("graphoptiondiv").style.display === "none") {
		document.getElementById("graphoptiondiv").style.display = "block";
	} else {
		document.getElementById("graphoptiondiv").style.display = "none";
	}
}

function lp1enabledclick() {
	publish("0","openWB/set/lp/1/AutolockStatus");
	if ( lp1enabled == 0 ) {
		publish("1","openWB/set/lp/1/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/1/ChargePointEnabled");
	}
}

function lp2enabledclick() {
	publish("0","openWB/set/lp/1/AutolockStatus");
	if ( lp2enabled == 0 ) {
		publish("1","openWB/set/lp/2/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/2/ChargePointEnabled");
	}
}

function lp3enabledclick() {
	publish("0","openWB/set/lp/1/AutolockStatus");
	if ( lp3enabled == 0 ) {
		publish("1","openWB/set/lp/3/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/3/ChargePointEnabled");
	}
}

function lp4enabledclick() {
	publish("0","openWB/set/lp/1/AutolockStatus");
	if ( lp4enabled == 0 ) {
		publish("1","openWB/set/lp/4/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/4/ChargePointEnabled");
	}
}

function lp5enabledclick() {
	publish("0","openWB/set/lp/1/AutolockStatus");
	if ( lp5enabled == 0 ) {
		publish("1","openWB/set/lp/5/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/5/ChargePointEnabled");
	}
}

function lp6enabledclick() {
	publish("0","openWB/set/lp/1/AutolockStatus");
	if ( lp6enabled == 0 ) {
		publish("1","openWB/set/lp/6/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/6/ChargePointEnabled");
	}
}

function lp7enabledclick() {
	publish("0","openWB/set/lp/1/AutolockStatus");
	if ( lp7enabled == 0 ) {
		publish("1","openWB/set/lp/7/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/7/ChargePointEnabled");
	}
}

function lp8enabledclick() {
	publish("0","openWB/set/lp/1/AutolockStatus");
	if ( lp8enabled == 0 ) {
		publish("1","openWB/set/lp/8/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/8/ChargePointEnabled");
	}
}
function AwattarMaxPriceClick() {
	publish(document.getElementById("awattar1l").innerHTML,"openWB/set/awattar/MaxPriceForCharging");
}
function lp1DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp1l").innerHTML,"openWB/set/lp/1/DirectChargeAmps");
}

function lp2DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp2l").innerHTML,"openWB/set/lp/2/DirectChargeAmps");
}

function lp3DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp3l").innerHTML,"openWB/set/lp/3/DirectChargeAmps");
}

function lp4DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp4l").innerHTML,"openWB/set/lp/4/DirectChargeAmps");
}

function lp5DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp5l").innerHTML,"openWB/set/lp/5/DirectChargeAmps");
}

function lp6DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp6l").innerHTML,"openWB/set/lp/6/DirectChargeAmps");
}

function lp7DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp7l").innerHTML,"openWB/set/lp/7/DirectChargeAmps");
}

function lp8DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp8l").innerHTML,"openWB/set/lp/8/DirectChargeAmps");
}


function renewMQTTclick() {
	publish("1","openWB/set/RenewMQTT");
	alert("Erneuern der Werte initiert, dies dauert ca 15-20 Sekunden.");
}

function putgraphtogether() {
	if ( (all1 == 1) && (all2 == 1) && (all3 == 1) && (all4 == 1) && (all5 == 1) && (all6 == 1) && (all7 == 1) && (all8 == 1) ){
		var alldata = all1p + "\n" + all2p + "\n" + all3p + "\n" + all4p + "\n" + all5p + "\n" + all6p + "\n" + all7p + "\n" + all8p;
		alldata = alldata.replace(/^\s*[\n]/gm, '');
		alldata = alldata.replace(/^\s*-[\n]/gm, '');
		var csvData = new Array();
		var rawcsv = alldata.split(/\r?\n|\r/);
		for (var i = 0; i < rawcsv.length; i++) {
			  csvData.push(rawcsv[i].split(','));
		}
		csvData.pop();
		// Retrived data from csv file content
		var splittime = new Array();
		getCol(csvData, 0).forEach(function(zeit){
			splittime.push(zeit.substring(0, zeit.length -3));
		});
		atime = splittime;
		//atime = getCol(csvData, 0);
		abezug = getCol(csvData, 1);
		alpa = getCol(csvData, 2);
		apv = getCol(csvData, 3);
		alp1 = getCol(csvData, 4);
		alp2 = getCol(csvData, 5);
		aspeicherl = getCol(csvData, 7);
		aspeichersoc = getCol(csvData, 8);
		asoc = getCol(csvData, 9);
		asoc1 = getCol(csvData, 10);
		ahausverbrauch = getCol(csvData, 11);
		averbraucher1 = getCol(csvData, 12);
		averbraucher2 = getCol(csvData, 13);
		alp3 = getCol(csvData, 14);
		alp4 = getCol(csvData, 15);
		alp5 = getCol(csvData, 16);
		alp6 = getCol(csvData, 17);
		alp7 = getCol(csvData, 18);
		alp8 = getCol(csvData, 19);
		initialread = 1 ;
		checkgraphload();
	}
}  // end putgraphtogether

function getHookStatus(dataURL) {
	// read dataURL filecontent and return it
	return $.get(dataURL);
}

function displayHookStatus(hookNumber) {
	var element = "#hook"+hookNumber+"div";
	getHookStatus("/openWB/ramdisk/hook"+hookNumber+"akt").done(function(result) {
		if ( result == 1 ) {
			$(element).removeClass("bg-danger");
			$(element).addClass("bg-success");
		} else {
			$(element).removeClass("bg-success");
			$(element).addClass("bg-danger");
		}
	});
}

function processAllHooks() {
	for (numberOfHook=1; numberOfHook<=3; numberOfHook++) {
		displayHookStatus(numberOfHook);
	}
}

function updateGaugeValue(gauge, value, text, setText, isSymmetric, autoRescale) {
    // gauge: zu erneuernde Gauge
    // value: neuer Wert
    // text: ggf. neuer Text
    // setText: Text und Farbe des Labels anpassen
    // isSymmetric: symmetrische Gauge oder nicht (min-max or 0-max)
    // autoRescale: Skala passt sich nach defaultScaleCounter-Aufrufen selbst nach unten an
    if(isNaN(value)){
        // es wurde keine Zahl als Wert übergeben
	     return;  // gleich wieder zurück
    }
    var needsScaling = false;
    var newGaugeMax = Math.ceil((Math.abs(value) / 1000)) * 1000;
    if (gauge.max < newGaugeMax) {
        // benötigtes Maximum ist größer als Skala
        gauge.max = newGaugeMax;  // Skala positiv anpassen
        gauge.scaleCounter = defaultScaleCounter;  // Counter reset
        needsScaling = true;
        if (!autoRescale) {
            // neues Maximum der Gauge als Cookie speichern
            gauge_identifier = 'dark_gauges_1_' + gauge.id;
            $.ajax({
                type: "GET",
                url: "./setGaugeScaleCookie.php",
                data: {
                    name: gauge_identifier,
                    value: newGaugeMax
                }
            });
        }
    } else if (gauge.max > newGaugeMax) {
        // Skala ist aktuell eigentlich zu groß
        if (autoRescale) {
            // und Anpassung soll automatisch erfolgen
            gauge.scaleCounter -= 1; // dann Counter reduzieren
            if (gauge.scaleCounter == 0) {
                // wenn Zeit rum
                gauge.scaleCounter = defaultScaleCounter;  // Counter reset
                gauge.max = gauge.max-(Math.ceil((gauge.max-newGaugeMax) / 2000) * 1000);  // Skala anpassen
                needsScaling = true;
            }
        }
    } else {
        // Skala soll bleiben, keine automatische Anpassung
        if (gauge.scaleCounter < defaultScaleCounter) {
            // aber Zähler zum Wechsel ist schon angelaufen
            gauge.scaleCounter = defaultScaleCounter;  // Counter reset
        }
    }
    if (needsScaling) {
        // wenn Skala angepasst werden muss
        if (isSymmetric) {
            // bei symmetrischer Gauge die negative Skala angleichen
            gauge.min = gauge.max *-1;
        }
        // farbigen Rand anpassen
        gauge.set('colorsRanges', [[gauge.min, 0, 'red', 3], [0, gauge.max, 'green', 3]]);
        // Labels in kW
        gauge.set('labelsSpecific', [(gauge.min/1000), ((gauge.max-Math.abs(gauge.min))/2000), (gauge.max/1000)]);
    }
    // neuen Wert für Gauge setzen, ggf. Text im Label ändern
    gauge.value = value;
    if (setText) {
        gauge.set('titleBottom', text);
        // Farben der Schrift ggf. anpassen
        if (value < 0) {
            gauge.set('titleBottomColor', 'red');
        } else {
            gauge.set('titleBottomColor', 'green');
        }
    }
    // und Anzeige erneuern
    gauge.grow();
}

function getValueDailyYieldLabel() {
    // regelmäßig Werte für Tagesertrag-Label vom Server holen
    $.ajax({
        // Tagesertrag PV für Gauge für PV-Leistung lesen
        url:
            "/openWB/ramdisk/daily_pvkwhk",
        complete:
            function(request){
				var anzeigeText = "";
				if ( request.responseText > 0 ) {
					anzeigeText = request.responseText + ' kWh';
				}
                // Text setzen
                gaugePV.set('titleBottom', anzeigeText).grow();
                // Neuzeichnen erfolgt bei regelmäßiger Werte-Aktualisierung
            }
    });
}

doInterval = setInterval(processAllHooks, 5000);
processAllHooks();
dailyYieldLabelIntervall = setInterval(getValueDailyYieldLabel, 20000);  // alle 20 Sekunden Label mit Tagesertrag erneuern
getValueDailyYieldLabel();
