/**
 * Functions to update graph and values via MQTT
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

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
$('#lp2div').hide();
$('#lp3div').hide();
$('#lp4div').hide();
$('#lp5div').hide();
$('#lp6div').hide();
$('#lp7div').hide();
$('#lp8div').hide();
$('#slider2div').hide();
$('#slider3div').hide();
$('#slider4div').hide();
$('#slider5div').hide();
$('#slider6div').hide();
$('#slider7div').hide();
$('#slider8div').hide();
var thevalues = [
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
	["openWB/evu/W", "#bezugdiv"],
	["openWB/global/WHouseConsumption", "#hausverbrauchdiv"],
	["openWB/lp/1/%Soc", "#"],
	["openWB/lp/2/%Soc", "#"],
	["openWB/lp/1/kWhDailyCharged", "#dailychargelp1div"],
	["openWB/lp/2/kWhDailyCharged", "#dailychargelp2div"],
	["openWB/lp/3/kWhDailyCharged", "#dailychargelp3div"],
	["openWB/lp/1/kWhActualCharged", "#aktgeladen1div"],
	["openWB/lp/2/kWhActualCharged", "#aktgeladen2div"],
	["openWB/lp/3/kWhActualCharged", "#aktgeladen3div"],
	["openWB/pv/W", "#"],
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
	["openWB/lp/1/AConfigured", "#llsolllp1div"],
	["openWB/lp/2/AConfigured", "#llsolllp2div"],
	["openWB/lp/3/AConfigured", "#llsolllp3div"],
	["openWB/lp/8/AConfigured", "#llsolllp8div"],
	["openWB/lp/4/AConfigured", "#llsolllp4div"],
	["openWB/lp/5/AConfigured", "#llsolllp5div"],
	["openWB/lp/6/AConfigured", "#llsolllp6div"],
	["openWB/lp/7/AConfigured", "#llsolllp7div"],
	["openWB/lp/1/TimeRemaining", "#restzeitlp1div"],
	["openWB/lp/2/TimeRemaining", "#restzeitlp2div"],
	["openWB/lp/3/TimeRemaining", "#restzeitlp3div"],
	["openWB/lp/1/kmCharged", "#gelrlp1div"],
	["openWB/lp/2/kmCharged", "#gelrlp2div"],
	["openWB/lp/3/kmCharged", "#gelrlp3div"],
	["openWB/evu/WAverage", "#bezugglattdiv"],
	["openWB/lp/1/ChargeStatus", "#"],
	["openWB/lp/2/ChargeStatus", "#"],
	["openWB/lp/3/ChargeStatus", "#"],
	["openWB/lp/4/ChargeStatus", "#"],
	["openWB/lp/5/ChargeStatus", "#"],
	["openWB/lp/6/ChargeStatus", "#"],
	["openWB/lp/7/ChargeStatus", "#"],
	["openWB/lp/8/ChargeStatus", "#"],
	["openWB/lp/1/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp1div"],
	["openWB/lp/2/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp2div"],
	["openWB/lp/3/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp3div"],
	["openWB/lp/4/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp4div"],
	["openWB/lp/5/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp5div"],
	["openWB/lp/6/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp6div"],
	["openWB/lp/7/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp7div"],
	["openWB/lp/8/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp8div"],
	["openWB/global/ChargeMode", "#"],
	["openWB/global/WAllChargePoints", "#"],
	["openWB/global/rfidConfigured", "#"],
	["openWB/housebattery/W", "#speicherleistungdiv"],
	["openWB/housebattery/%Soc", "#"],
	["openWB/global/strLastmanagementActive", "#lastregelungaktivdiv"],
	["openWB/lp/1/boolChargePointConfigured", "#"],
	["openWB/lp/2/boolChargePointConfigured", "#"],
	["openWB/lp/3/boolChargePointConfigured", "#"],
	["openWB/lp/4/boolChargePointConfigured", "#"],
	["openWB/lp/5/boolChargePointConfigured", "#"],
	["openWB/lp/6/boolChargePointConfigured", "#"],
	["openWB/lp/7/boolChargePointConfigured", "#"],
	["openWB/lp/8/boolChargePointConfigured", "#"],
	["openWB/lp/1/ChargePointEnabled", "#lp1enabled"],
	["openWB/lp/2/ChargePointEnabled", "#lp2enabled"],
	["openWB/lp/3/ChargePointEnabled", "#lp3enabled"],
	["openWB/lp/4/ChargePointEnabled", "#lp4enabled"],
	["openWB/lp/5/ChargePointEnabled", "#lp5enabled"],
	["openWB/lp/6/ChargePointEnabled", "#lp6enabled"],
	["openWB/lp/7/ChargePointEnabled", "#lp7enabled"],
	["openWB/lp/8/ChargePointEnabled", "#lp8enabled"],
	["openWB/lp/1/strChargePointName", "#lp1name"],
	["openWB/lp/2/strChargePointName", "#lp2name"],
	["openWB/lp/3/strChargePointName", "#lp3name"],
	["openWB/lp/4/strChargePointName", "#lp4name"],
	["openWB/lp/5/strChargePointName", "#lp5name"],
	["openWB/lp/6/strChargePointName", "#lp6name"],
	["openWB/lp/7/strChargePointName", "#lp7name"],
	["openWB/lp/8/strChargePointName", "#lp8name"],
	["openWB/config/get/sofort/lp/1/current", "#"],
	["openWB/config/get/sofort/lp/2/current", "#"],
	["openWB/config/get/sofort/lp/3/current", "#"],
	["openWB/config/get/sofort/lp/4/current", "#"],
	["openWB/config/get/sofort/lp/5/current", "#"],
	["openWB/config/get/sofort/lp/6/current", "#"],
	["openWB/config/get/sofort/lp/7/current", "#"],
	["openWB/config/get/sofort/lp/8/current", "#"],
	["openWB/system/reloadDisplay", "#"]
];

function getCol(matrix, col){
	var column = [];
	for(var i=0; i<matrix.length; i++){
		column.push(matrix[i][col]);
	}
	return column;
}

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

var clientuid = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
var client = new Messaging.Client(location.hostname, 9001, clientuid);

function handlevar(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
//console.log('new mqttmsg...');
//console.log('mqttmsg: '+mqttmsg+'--endmessage');
//console.log('load='+mqttpayload+'--endload');
//console.log('topic='+mqtttopic+'--endtopic');
//console.log('topic='+htmldiv+'--endhtmldiv');
//console.log('');

	if ( mqttmsg == "openWB/evu/W" ) {
		var wattbezug = mqttpayload;
		intbezug = parseInt(wattbezug, 10);
		intbezugarrow = intbezug;
			if (intbezug > 0) {
			if (intbezug > 999) {
				intbezug = (intbezug / 1000).toFixed(2);
					wattbezug = intbezug + " kW Bezug";
			} else {
			wattbezug = intbezug + " W Bezug";
			}
		} else {
				intbezug = intbezug * -1;
			if (intbezug > 999) {
				intbezug = (intbezug / 1000).toFixed(2);
					wattbezug = intbezug + " kW Einspeisung";
			} else {
			wattbezug = intbezug + " W Einspeisung";
			}
		}
		$("#bezugdiv").html(wattbezug);
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayHouseConsumption" ) {
		if ( mqttpayload == 1) {
			boolDisplayHouseConsumption = false;
			hidehaus = 'foo';
			$("#graphhausdiv").css("color", "green");
			$("#graphhausdiv").removeClass("fa-toggle-off");
			$("#graphhausdiv").addClass("fa-toggle-on");

		} else {
			boolDisplayHouseConsumption = true;
			$("#graphhausdiv").css("color", "red");
			$("#graphhausdiv").removeClass("fa-toggle-on");
			$("#graphhausdiv").addClass("fa-toggle-off");
			hidehaus = 'Hausverbrauch';
		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayLegend" ) {
		if ( mqttpayload == 0) {
			boolDisplayLegend = false;
			$("#graphlegenddiv").css("color", "red");
			$("#graphlegenddiv").removeClass("fa-toggle-on");
			$("#graphlegenddiv").addClass("fa-toggle-off");
		} else {
			boolDisplayLegend = true;
			$("#graphlegenddiv").css("color", "green");
			$("#graphlegenddiv").removeClass("fa-toggle-off");
			$("#graphlegenddiv").addClass("fa-toggle-on");

		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayLiveGraph" ) {
		if ( mqttpayload == 0) {
			$('#thegraph').hide();
			boolDisplayLiveGraph = false;
			$("#graphgraphdiv").css("color", "red");
			$("#graphgraphdiv").removeClass("fa-toggle-on");
			$("#graphgraphdiv").addClass("fa-toggle-off");
		} else {
			$('#thegraph').show();
			boolDisplayLiveGraph = true;
			$("#graphgraphdiv").css("color", "green");
			$("#graphgraphdiv").removeClass("fa-toggle-off");
			$("#graphgraphdiv").addClass("fa-toggle-on");
		}
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayEvu" ) {
		if ( mqttpayload == 1) {
			boolDisplayEvu = false;
			hideevu = 'foo';
			$("#graphevudiv").css("color", "green");
			$("#graphevudiv").removeClass("fa-toggle-off");
			$("#graphevudiv").addClass("fa-toggle-on");

		} else {
			boolDisplayEvu = true;
			hideevu = 'Bezug';
			$("#graphevudiv").css("color", "red");
			$("#graphevudiv").removeClass("fa-toggle-on");
			$("#graphevudiv").addClass("fa-toggle-off");

		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayPv" ) {
		if ( mqttpayload == 1) {
			boolDisplayPv = false;
			hidepv = 'foo';
			$("#graphpvdiv").css("color", "green");
			$("#graphpvdiv").removeClass("fa-toggle-off");
			$("#graphpvdiv").addClass("fa-toggle-on");
		} else {
			boolDisplayPv = true;
			hidepv = 'PV';
			$("#graphpvdiv").css("color", "red");
			$("#graphpvdiv").removeClass("fa-toggle-on");
			$("#graphpvdiv").addClass("fa-toggle-off");
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
			$("#graphlp"+index+"div").css("color", "green");
			$("#graphlp"+index+"div").removeClass('fa-toggle-off');
			$("#graphlp"+index+"div").addClass('fa-toggle-on');
		} else {
			window['boolDisplayLp'+index] = true;
			window['hidelp'+index] = 'Lp' + index;
			$("#graphlp"+index+"div").css("color", "red");
			$("#graphlp"+index+"div").removeClass('fa-toggle-on');
			$("#graphlp"+index+"div").addClass('fa-toggle-off');
		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplayLpAll" ) {
		if ( mqttpayload == 1) {
			boolDisplayLpAll = false;
			hidelpa = 'foo';
			$("#graphlpalldiv").removeClass("fa-toggle-off");
			$("#graphlpalldiv").addClass("fa-toggle-on");
			$("#graphlpalldiv").css("color", "green");
		} else {
			boolDisplayLpAll = true;
			hidelpa = 'LP Gesamt';
			$("#graphlpalldiv").removeClass("fa-toggle-on");
			$("#graphlpalldiv").addClass("fa-toggle-off");
			$("#graphlpalldiv").css("color", "red");

		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplaySpeicher" ) {
		if ( mqttpayload == 1) {
			boolDisplaySpeicher = false;
			hidespeicher = 'foo';
			$("#graphspeicherdiv").css("color", "green");
			$("#graphspeicherdiv").removeClass("fa-toggle-off");
			$("#graphspeicherdiv").addClass("fa-toggle-on");
		} else {
			hidespeicher = 'Speicherleistung';
			boolDisplaySpeicher = true;
			$("#graphspeicherdiv").css("color", "red");
			$("#graphspeicherdiv").removeClass("fa-toggle-on");
			$("#graphspeicherdiv").addClass("fa-toggle-off");

		}
		checkgraphload();
	}
	else if ( mqttmsg == "openWB/graph/boolDisplaySpeicherSoc" ) {
		if ( mqttpayload == 1) {
			hidespeichersoc = 'foo';
			boolDisplaySpeicherSoc = false;
			$("#graphspeichersocdiv").css("color", "green");
			$("#graphspeichersocdiv").removeClass("fa-toggle-off");
			$("#graphspeichersocdiv").addClass("fa-toggle-on");
		} else {
			hidespeichersoc = 'Speicher SoC';
			boolDisplaySpeicherSoc = true;
			$("#graphspeichersocdiv").css("color", "red");
			$("#graphspeichersocdiv").removeClass("fa-toggle-on");
			$("#graphspeichersocdiv").addClass("fa-toggle-off");

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
			$("#graphlp"+index+"socdiv").css("color", "green");
			$("#graphlp"+index+"socdiv").removeClass('fa-toggle-off');
			$("#graphlp"+index+"socdiv").addClass('fa-toggle-on');
		} else {
			$('#socenabledlp'+index).hide();
			window['boolDisplayLp'+index+'Soc'] = true;
			window['hidelp'+index+'soc'] = 'LP'+index+' SoC';
			$("#graphlp"+index+"socdiv").css("color", "red");
			$("#graphlp"+index+"socdiv").removeClass('fa-toggle-on');
			$("#graphlp"+index+"socdiv").addClass('fa-toggle-off');
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
			$("#graphload"+index+"div").css("color", "green");
			$("#graphload"+index+"div").removeClass('fa-toggle-off');
			$("#graphload"+index+"div").addClass('fa-toggle-on');
		} else {
			window['hideload'+index] = 'Verbraucher ' + index;
			window['boolDisplayLoad'+index] = true;
			$("#graphload"+index+"div").css("color", "red");
			$("#graphload"+index+"div").removeClass('fa-toggle-on');
			$("#graphload"+index+"div").addClass('fa-toggle-off');
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
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolchargepointconfigured$/i ) ) {
		// matches to all messages containing "openwb/lp/#/boolchargepointconfigured"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		// console.log('mqttmsg-boolChargePointConfigured: '+index+'   load='+mqttpayload);
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
	else if ( mqttmsg == "openWB/housebattery/W" ) {
		var speicherwatt = mqttpayload;
		intspeicherw = parseInt(speicherwatt, 10);
		intspeicherarrow = intspeicherw;
		if (intspeicherw > 0) {
			if (intspeicherw > 999) {
				intspeicherw = (intspeicherw / 1000).toFixed(2);
				speicherwatt = intspeicherw + " kW Ladung";
			} else {
				speicherwatt = intspeicherw + " W Ladung";
			}
		} else {
				intspeicherw = intspeicherw * -1;
			if (intspeicherw > 999) {
				intspeicherw = (intspeicherw / 1000).toFixed(2);
				speicherwatt = intspeicherw + " kW Entladung";
			} else {
				speicherwatt = intspeicherw + " W Entladung";
			}
		}
		$("#speicherleistungdiv").html(speicherwatt);
	}
	else if ( mqttmsg == "openWB/global/WHouseConsumption" ) {
		if (mqttpayload > 999) {
			mqttpayload = (mqttpayload / 1000).toFixed(2);
				mqttpayload = mqttpayload + " kW";
		} else {
			mqttpayload = mqttpayload + " W";
		}
		$("#hausverbrauchdiv").html(mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/chargepointenabled$/i ) ) {
		// matches to all messages containing "openwb/lp/#/boolchargepointenabled"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-ChargePointEnabled: '+index+'   load='+mqttpayload);
		if ( mqttpayload == 0 ) {
			window['lp'+index+'enabled'] = 0;
			$("#lp"+index+"enableddiv").removeClass("fa-check");
			$("#lp"+index+"enableddiv").addClass("fa-times");
			$("#lp"+index+"enableddiv").css("color", "red");
		} else {
			window['lp'+index+'enabled'] = 1;
			$("#lp"+index+"enableddiv").removeClass("fa-times");
			$("#lp"+index+"enableddiv").addClass("fa-check");
			$("#lp"+index+"enableddiv").css("color", "lightgreen");
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/kWhactualcharged$/i ) ) {
		// matches to all messages containing "openwb/lp/#/kWhactualcharged"
		// where # is an integer > 0
		// search is case insensitive
		if ( $("#prog"+index) ) {
			// only if target element exists
			var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
			//console.log('mqttmsg-kWhActualCharged: '+index+'   load='+mqttpayload);
			$("#aktgeladen"+index+"div").html(mqttpayload);
			$("#prog"+index).value= mqttpayload;
		}
	}
	else if ( mqttmsg == "openWB/pv/W") {
		pvwatt = parseInt(mqttpayload, 10);
		if ( pvwatt > 0 ) {
			// if pv-power is positive, adjust to 0
			// since pv cannot consume power
			pvwatt = 0;
		}
		// convert raw number for display
		if ( pvwatt <= 0){
			// production is negative for calculations so adjust for display
			pvwatt = pvwatt * -1;
			pvwattarrow = pvwatt;
			// adjust and add unit
			if (pvwatt > 999) {
				pvwattStr = (pvwatt / 1000).toFixed(2) + " kW";
			} else {
				pvwattStr = pvwatt + " W";
			}
			// only if production
			if (pvwatt > 0) {
				pvwattStr += " Erzeugung";
			}
		}
		$("#pvdiv").html(pvwattStr);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/w$/i ) ) {
		// matches to all messages containing "openwb/lp/#/w"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-W: '+index+'   load='+mqttpayload);
		llaktuell = parseInt(mqttpayload, 10);
		llaktuellarrow = llaktuell;
		if (mqttpayload > 999) {
			mqttpayload = (mqttpayload / 1000).toFixed(2);
			mqttpayload = mqttpayload + " kW";
		} else {
		mqttpayload = mqttpayload + " W";
		}
		$("#lllp"+index+"div").html(mqttpayload);
	}
	else if ( mqttmsg == "openWB/global/WAllChargePoints") {
		llaktuell = parseInt(mqttpayload, 10);
		llaktuellgarrow = llaktuell;
		if (mqttpayload > 999) {
			mqttpayload = (mqttpayload / 1000).toFixed(2);
			mqttpayload = mqttpayload + " kW";
		} else {
		mqttpayload = mqttpayload + " W";
		}
		$("#gesamtllwdiv").html(mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolplugstat$/i ) ) {
		// matches to all messages containing "openwb/lp/#/boolplugstat"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-boolPlugStat: '+index+'   load='+mqttpayload);
		if ( $('#plugstatlp'+index+'div') ) {
			if ( mqttpayload == 1 ) {
				$("#plugstatlp"+index+"div").addClass("fa-plug");
			} else {
				$("#plugstatlp"+index+"div").removeClass("fa-plug");
			}
		}
		if ($('#carlp'+index)) {
			if (mqttpayload == 1) {
				$("#carlp"+index).css("color", "green");
			} else {
				$("#carlp"+index).css("color", "blue");
			}
		}
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/boolchargestat$/i ) ) {
		// matches to all messages containing "openwb/lp/#/boolchargestat"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-boolChargeStat: '+index+'   load='+mqttpayload);
		if ($('#plugstatlp'+index+'div')) {
			if (mqttpayload == 1) {
				$("#plugstatlp"+index+"div").css("color", "#00FF00");
			} else {
				$("#plugstatlp"+index+"div").css("color", "white");
			}
		}
		if ($('#socstatlp'+index)) {
			if (mqttpayload == 1) {
				$("#socstatlp"+index).css("color", "#00FF00");
			} else {
				$("#socstatlp"+index).css("color", "black");
			}
		}
	}
	else if ( mqttmsg == "openWB/housebattery/%Soc" ) {
		speichersoc = mqttpayload;
		$("#speichersocdiv").html(mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/\%soc$/i ) ) {
		// matches to all messages containing "openwb/lp/#/%soc"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-SoC: '+index+'   load='+mqttpayload);
		window['lp'+index+'soc'] = mqttpayload;
		$("#soclp"+index).html(mqttpayload);
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/chargestatus$/i ) ) {
		// matches to all messages containing "openwb/lp/#/chargestatus"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-ChargeStatus: '+index+'   load='+mqttpayload);
		if ($('#stationlp'+index)) {
			if (mqttpayload == 1) {
				$("#stationlp"+index).css("color", "#00FF00");
			} else {
				$("#stationlp"+index).css("color", "blue");
			}
		}
	}
	else if ( mqttmsg == "openWB/global/strLastmanagementActive" ) {
		if ( $("#lastregelungaktivdiv") ) {
			// if the div for info text "Lastregelung" is present in theme
			$('#lastregelungaktivdiv').html(mqttpayload);
			if ( mqttpayload.length >= 5 ) {
				// if there is info-text in payload for topic, show the div
				$('#lastregelungaktivdiv').show();
			} else {
				// if there is no text, hide the div
				$('#lastregelungaktivdiv').hide();
			}
		}
	}
	else if ( mqttmsg == "openWB/global/ChargeMode" ) {
		// console.log('mqttmsg-ChargeMode:   load='+mqttpayload);
 		if(mqttpayload == 0){
			// mode sofort
			// set buttons
			$('.actstat .btn').addClass("btn-green");
			$('.actstat1 .btn').addClass("btn-red");
			$('.actstat2 .btn').addClass("btn-red");
			$('.actstat3 .btn').addClass("btn-red");
			$('.actstat3 .btn').removeClass("btn-green");
			$('.actstat4 .btn').addClass("btn-red");
			$('.actstat4 .btn').removeClass("btn-green");
			$('.actstat1 .btn').removeClass("btn-green");
			$('.actstat2 .btn').removeClass("btn-green");
			// show Sofortladen Ladeziel Progress
			$('#sofortladenLadezielProgressDiv').show();
		}
		if(mqttpayload == 1){
			// mode min+pv
			// set buttons
			$('.actstat1 .btn').addClass("btn-green");
			$('.actstat .btn').addClass("btn-red");
			$('.actstat2 .btn').addClass("btn-red");
			$('.actstat3 .btn').addClass("btn-red");
			$('.actstat .btn').removeClass("btn-green");
			$('.actstat3 .btn').removeClass("btn-green");
			$('.actstat2 .btn').removeClass("btn-green");
			$('.actstat4 .btn').addClass("btn-red");
			$('.actstat4 .btn').removeClass("btn-green");
			// hide Sofortladen Ladeziel Progress
			$('#sofortladenLadezielProgressDiv').hide();

		}
		if(mqttpayload == 2){
			// mode nurpv
			// set buttons
			$('.actstat2 .btn').addClass("btn-green");
			$('.actstat .btn').addClass("btn-red");
			$('.actstat1 .btn').addClass("btn-red");
			$('.actstat3 .btn').addClass("btn-red");
			$('.actstat .btn').removeClass("btn-green");
			$('.actstat3 .btn').removeClass("btn-green");
			$('.actstat1 .btn').removeClass("btn-green");
			$('.actstat4 .btn').addClass("btn-red");
			$('.actstat4 .btn').removeClass("btn-green");
			// hide Sofortladen Ladeziel Progress
			$('#sofortladenLadezielProgressDiv').hide();
		}
		if(mqttpayload == 3){
			// mode stop
			// set buttons
			$('.actstat2 .btn').addClass("btn-red");
			$('.actstat3 .btn').addClass("btn-green");
			$('.actstat2 .btn').removeClass("btn-green");
			$('.actstat .btn').addClass("btn-red");
			$('.actstat1 .btn').addClass("btn-red");
			$('.actstat .btn').removeClass("btn-green");
			$('.actstat1 .btn').removeClass("btn-green");
			$('.actstat4 .btn').addClass("btn-red");
			$('.actstat4 .btn').removeClass("btn-green");
			// hide Sofortladen Ladeziel Progress
			$('#sofortladenLadezielProgressDiv').hide();
		}
		if(mqttpayload == 4){
			// mode standby
			// set buttons
			$('.actstat2 .btn').addClass("btn-red");
			$('.actstat3 .btn').addClass("btn-red");
			$('.actstat .btn').addClass("btn-red");
			$('.actstat1 .btn').addClass("btn-red");
			$('.actstat .btn').removeClass("btn-green");
			$('.actstat2 .btn').removeClass("btn-green");
			$('.actstat3 .btn').removeClass("btn-green");
			$('.actstat1 .btn').removeClass("btn-green");
			$('.actstat4 .btn').addClass("btn-green");
			$('.actstat4 .btn').removeClass("btn-red");
			// hide Sofortladen Ladeziel Progress
			$('#sofortladenLadezielProgressDiv').hide();
		}
		loaddivs();
	}
	else if ( mqttmsg.match( /^openwb\/config\/get\/sofort\/lp\/[1-9][0-9]*\/current$/i ) ) {
		// matches to all messages containing "openwb/lp/#/adirectmodeamps"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		//console.log('mqttmsg-ADirectModeAmps: '+index+'   load='+mqttpayload);
		$("#sofortlllp"+index+"s").value = mqttpayload;
		$("#sofortlllp"+index+"l").html( mqttpayload );
	}
	else if ( mqttmsg.match( /^openwb\/lp\/[1-9][0-9]*\/strChargePointName$/i ) ) {
		// matches to all messages containing "openwb/lp/#/strchargepointname"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		// fill span-tags from class=strChargePointName with respective payload-string
		var myElem = document.getElementsByClassName("nameLp"+index);
		for(var i=0; i<myElem.length; i++) {
			myElem[i].textContent = mqttpayload;
		}
	}
	else if ( mqttmsg == "openWB/system/reloadDisplay" ) {
		if ( mqttpayload == "1" ) {
			reloadDisplay();
		}
	}
	else if ( mqttmsg == "openWB/global/rfidConfigured" ) {
		if ( mqttpayload == "0" ) {
			$('#pinpad').addClass('hide');
		} else {
			$('#pinpad').removeClass('hide');
		}
	}
	else {
		thevalues.forEach(function(thevar){
			if ( mqttmsg == thevar[0] ) {
				$(thevar[1]).html(mqttpayload);
			}
		});
	}
}  // end handlevar

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
		$('#backend .connectionState').text("verbunden");
		// $('#backend .reloadBtn').addClass('hide');
		$('#backend .counter').text(retries+1);
		console.log("connected, resetting counter");
		retries = 0;
		thevalues.forEach(function(thevar) {
			client.subscribe(thevar[0], {qos: 0});
		});
	},
	//Gets Called if the connection could not be established
	onFailure: function (message) {
		retries = retries + 1;
		console.log("connection failed, incrementing counter: " + retries);
		$('#backend .connectionState').text("getrennt");
		// $('#backend .reloadBtn').removeClass('hide');
		$('#backend .counter').text(retries+1);
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
function sendrfidtag(thetag) {
		publish(thetag,"openWB/set/system/SimulateRFID");
}
function graphoptionclick() {
	if ( $("#graphoptiondiv").css( "display" ) === "none") {
		$("#graphoptiondiv").css( "display", "block" );
	} else {
		$("#graphoptiondiv").css( "display", "none" );
	}
}

function lp1enabledclick() {
	if ( lp1enabled == 0 ) {
		publish("1","openWB/set/lp/1/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/1/ChargePointEnabled");
	}
}

function lp2enabledclick() {
	if ( lp2enabled == 0 ) {
		publish("1","openWB/set/lp/2/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/2/ChargePointEnabled");
	}
}

function lp3enabledclick() {
	if ( lp3enabled == 0 ) {
		publish("1","openWB/set/lp/3/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/3/ChargePointEnabled");
	}
}

function lp4enabledclick() {
	if ( lp4enabled == 0 ) {
		publish("1","openWB/set/lp/4/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/4/ChargePointEnabled");
	}
}

function lp5enabledclick() {
	if ( lp5enabled == 0 ) {
		publish("1","openWB/set/lp/5/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/5/ChargePointEnabled");
	}
}

function lp6enabledclick() {
	if ( lp6enabled == 0 ) {
		publish("1","openWB/set/lp/6/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/6/ChargePointEnabled");
	}
}

function lp7enabledclick() {
	if ( lp7enabled == 0 ) {
		publish("1","openWB/set/lp/7/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/7/ChargePointEnabled");
	}
}

function lp8enabledclick() {
	if ( lp8enabled == 0 ) {
		publish("1","openWB/set/lp/8/ChargePointEnabled");
	} else {
		publish("0","openWB/set/lp/8/ChargePointEnabled");
	}
}

function lp1DirectChargeAmpsClick() {
	publish($("#sofortlllp1l").html(),"openWB/config/set/sofort/lp/1/current");
}

function lp2DirectChargeAmpsClick() {
	publish($("#sofortlllp2l").html(),"openWB/config/set/sofort/lp/2/current");
}

function lp3DirectChargeAmpsClick() {
	publish($("#sofortlllp3l").html(),"openWB/config/set/sofort/lp/3/current");
}

function lp4DirectChargeAmpsClick() {
	publish($("#sofortlllp4l").html(),"openWB/config/set/sofort/lp/4/current");
}

function lp5DirectChargeAmpsClick() {
	publish($("#sofortlllp5l").html(),"openWB/config/set/sofort/lp/5/current");
}

function lp6DirectChargeAmpsClick() {
	publish($("#sofortlllp6l").html(),"openWB/config/set/sofort/lp/6/current");
}

function lp7DirectChargeAmpsClick() {
	publish($("#sofortlllp7l").html(),"openWB/config/set/sofort/lp/7/current");
}

function lp8DirectChargeAmpsClick() {
	publish($("#sofortlllp8l").html(),"openWB/config/set/sofort/lp/8/current");
}

function sofortclick() {
	publish("0","openWB/set/ChargeMode");
	publish("0","openWB/global/ChargeMode");
}

function minundpvclick() {
	publish("1","openWB/set/ChargeMode");
	publish("1","openWB/global/ChargeMode");
}

function nurpvclick() {
	publish("2","openWB/set/ChargeMode");
	publish("2","openWB/global/ChargeMode");
}

function standbyclick() {
	publish("4","openWB/set/ChargeMode");
	publish("4","openWB/global/ChargeMode");
}

function stopclick() {
	publish("3","openWB/set/ChargeMode");
	publish("3","openWB/global/ChargeMode");
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

function getfile() {
	if ( $("#webhooksdiv") ) {
		if ( hook1_aktiv == '1' || hook2_aktiv == '1' || hook3_aktiv == '1' ) {
			$('#webhooksdiv').show();
		}
	}
	if ($("#hook1div")) {
		$(function() {
			if(hook1_aktiv == '1') {
				$.ajax({
					url: "/openWB/ramdisk/hook1akt",
					contentType: "text/plain",
					dataType: "text",
					beforeSend: function(xhr){  xhr.overrideMimeType( "text/plain; charset=x-user-defined" );},
					complete: function(request){
						var hook1akt = request.responseText;
						if (hook1akt == 1) {
							if ( activetheme == "symbol") {
								$("#hook1div").addClass("fa");
								$("#hook1div").addClass("fa-plug");
								$("#hook1div").css("color", "green");
							} else {
								$("#hook1div").css("background-color", "green");
							}
						} else {
						if ( activetheme == "symbol") {
							$("#hook1div").addClass("fa");
							$("#hook1div").addClass("fa-plug");
							$("#hook1div").css("color", "red");
							} else {
							$("#hook1div").css("background-color", "red");
							}
						}
					}
				});
			} else {
				$('#hook1div').hide();
			}
		});
	}
	if ($("#hook2div")) {
		$(function() {
			if(hook2_aktiv == '1') {
				$.ajax({
					url: "/openWB/ramdisk/hook2akt",
					beforeSend: function(xhr){  xhr.overrideMimeType( "text/plain; charset=x-user-defined" );},
					complete: function(request){
						if (request.responseText == 1) {
							if ( activetheme == "symbol") {
								$("#hook2div").addClass("fa");
								$("#hook2div").addClass("fa-plug");
								$("#hook2div").css("color", "green");
							} else {
								$("#hook2div").css("background-color", "green");
							}
						} else {
							if ( activetheme == "symbol") {
								$("#hook2div").addClass("fa");
								$("#hook2div").addClass("fa-plug");
								$("#hook2div").css("color", "red");
							} else {
								$("#hook2div").css("background-color", "red");
							}
						}
					}
				});
			} else {
				$('#hook2div').hide();
			}
		});
	}
	if ($("#hook3div")) {
		$(function() {
			if(hook3_aktiv == '1') {
				$.ajax({
					url: "/openWB/ramdisk/hook3akt",
					complete: function(request){
						if (request.responseText == 1) {
							if ( activetheme == "symbol") {
								$("#hook3div").addClass("fa");
								$("#hook3div").addClass("fa-plug");
								$("#hook3div").css("color", "green");
							} else {
								$("#hook3div").css("background-color", "green");
							}
						} else {
							if ( activetheme == "symbol") {
								$("#hook3div").addClass("fa");
								$("#hook3div").addClass("fa-plug");
								$("#hook3div").css("color", "red");
							} else {
								$("#hook3div").css("background-color", "red");
							}
						}
					}
				});
			} else {
				$('#hook3div').hide();
			}
		});
	}
}  // end getfile

doInterval = setInterval(getfile, 5000);
getfile();
