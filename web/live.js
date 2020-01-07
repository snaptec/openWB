var doInterval;
var do2Interval;
var pvwattarrow;
var llaktuellarrow;
var llaktuelllp2arrow;
var llaktuelllp3arrow;
var llaktuelllp4arrow;
var llaktuelllp5arrow;
var llaktuelllp6arrow;
var llaktuelllp7arrow;
var llaktuelllp8arrow;
var llaktuellgarrow;
var intbezugarrow;
var intspeicherarrow;
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
["openWB/lp/1/kWhActualCharged", "#aktgeladendiv"],
["openWB/lp/2/kWhActualCharged", "#aktgeladens1div"],
["openWB/lp/3/kWhActualCharged", "#aktgeladens2div"],
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

["openWB/lp/1/AConfigured", "#llsolldiv"],
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
["openWB/lp/1/kWhChargedSincePlugged", "#pluggedladungbishergeladendiv"],
["openWB/lp/2/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp2div"],
["openWB/lp/3/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp3div"],
["openWB/lp/4/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp4div"],
["openWB/lp/5/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp5div"],
["openWB/lp/6/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp6div"],
["openWB/lp/7/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp7div"],
["openWB/lp/8/kWhChargedSincePlugged", "#pluggedladungbishergeladenlp8div"],
["openWB/global/ChargeMode", "#"],
["openWB/global/WAllChargePoints", "#"],
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
["openWB/lp/1/ADirectModeAmps", "#"],
["openWB/lp/2/ADirectModeAmps", "#"],
["openWB/lp/3/ADirectModeAmps", "#"],
["openWB/lp/4/ADirectModeAmps", "#"],
["openWB/lp/5/ADirectModeAmps", "#"],
["openWB/lp/6/ADirectModeAmps", "#"],
["openWB/lp/7/ADirectModeAmps", "#"],
["openWB/lp/8/ADirectModeAmps", "#"]
];
function getCol(matrix, col){
	var column = [];
	for(var i=0; i<matrix.length; i++){
		column.push(matrix[i][col]);
	}
	return column;
}

var clientuid = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
var client = new Messaging.Client(location.host, 9001, clientuid);
function handlevar(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
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
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayHouseConsumption" ) {
		if ( mqttpayload == 1) {
			boolDisplayHouseConsumption = false;
			hidehaus = 'foo';
			document.getElementById("graphhausdiv").setAttribute("style", "color: green;");
			graphhausdiv.classList.remove("fa-toggle-off");
			graphhausdiv.classList.add("fa-toggle-on");

		} else {
			boolDisplayHouseConsumption = true;
			document.getElementById("graphhausdiv").setAttribute("style", "color: red;");
			graphhausdiv.classList.remove("fa-toggle-on");
			graphhausdiv.classList.add("fa-toggle-off");
			hidehaus = 'Hausverbrauch';
		}
		checkgraphload();
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLegend" ) {
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
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLiveGraph" ) {
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
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayEvu" ) {
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
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayPv" ) {
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
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLp1" ) {
		if ( mqttpayload == 1) {
			boolDisplayLp1 = false;
			hidelp1 = 'foo';
			document.getElementById("graphlp1div").setAttribute("style", "color: green;");
			graphlp1div.classList.remove("fa-toggle-off");
			graphlp1div.classList.add("fa-toggle-on");
		} else {
			boolDisplayLp1 = true;
			hidelp1 = 'Lp1';
			document.getElementById("graphlp1div").setAttribute("style", "color: red;");
			graphlp1div.classList.remove("fa-toggle-on");
			graphlp1div.classList.add("fa-toggle-off");

		}

		checkgraphload();
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLp2" ) {
		if ( mqttpayload == 1) {
			boolDisplayLp2 = false;
			hidelp2 = 'foo';
			var element = document.getElementById("graphlp2div");
			graphlp2div.classList.remove("fa-toggle-off");
			graphlp2div.classList.add("fa-toggle-on");
			element.setAttribute("style", "color: green;");
		} else {
			var element = document.getElementById("graphlp2div");
			boolDisplayLp2 = true;
			hidelp2 = 'Lp2';
			graphlp2div.classList.remove("fa-toggle-on");
			graphlp2div.classList.add("fa-toggle-off");
			element.setAttribute("style", "color: red;");
		}

		checkgraphload();
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLp3" ) {
		if ( mqttpayload == 1) {
			hidelp3 = 'foo';
			boolDisplayLp3 = false;
			var element = document.getElementById("graphlp3div");
			graphlp3div.classList.remove("fa-toggle-off");
			graphlp3div.classList.add("fa-toggle-on");
			element.setAttribute("style", "color: green;");
		} else {
			var element = document.getElementById("graphlp3div");
			boolDisplayLp3 = true;
			hidelp3 = 'Lp3';
			graphlp3div.classList.remove("fa-toggle-on");
			graphlp3div.classList.add("fa-toggle-off");
			element.setAttribute("style", "color: red;");
		}
		checkgraphload();
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLp4" ) {
		if ( mqttpayload == 1) {
			boolDisplayLp4 = false;
			hidelp4 = 'foo';
			var element = document.getElementById("graphlp4div");
			graphlp4div.classList.remove("fa-toggle-off");
			graphlp4div.classList.add("fa-toggle-on");
			element.setAttribute("style", "color: green;");
		} else {
			var element = document.getElementById("graphlp4div");
			boolDisplayLp4 = true;
			hidelp4 = 'Lp4';
			graphlp4div.classList.remove("fa-toggle-on");
			graphlp4div.classList.add("fa-toggle-off");
			element.setAttribute("style", "color: red;");
		}
		checkgraphload();
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLp5" ) {
		if ( mqttpayload == 1) {
			boolDisplayLp5 = false;
			hidelp5 = 'foo';
			var element = document.getElementById("graphlp5div");
			graphlp5div.classList.remove("fa-toggle-off");
			graphlp5div.classList.add("fa-toggle-on");
			element.setAttribute("style", "color: green;");
		} else {
			var element = document.getElementById("graphlp5div");
			boolDisplayLp5 = true;
			hidelp5 = 'Lp5';
			graphlp5div.classList.remove("fa-toggle-on");
			graphlp5div.classList.add("fa-toggle-off");
			element.setAttribute("style", "color: red;");
		}
		checkgraphload();
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLp6" ) {
		if ( mqttpayload == 1) {
			boolDisplayLp6 = false;
			hidelp6 = 'foo';
			var element = document.getElementById("graphlp6div");
			graphlp6div.classList.remove("fa-toggle-off");
			graphlp6div.classList.add("fa-toggle-on");
			element.setAttribute("style", "color: green;");
		} else {
			var element = document.getElementById("graphlp6div");
			boolDisplayLp6 = true;
			hidelp6 = 'Lp6';
			graphlp6div.classList.remove("fa-toggle-on");
			graphlp6div.classList.add("fa-toggle-off");
			element.setAttribute("style", "color: red;");
		}
		checkgraphload();
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLp7" ) {
		if ( mqttpayload == 1) {
			boolDisplayLp7 = false;
			hidelp7 = 'foo';
			var element = document.getElementById("graphlp7div");
			graphlp7div.classList.remove("fa-toggle-off");
			graphlp7div.classList.add("fa-toggle-on");
			element.setAttribute("style", "color: green;");
		} else {
			var element = document.getElementById("graphlp7div");
			boolDisplayLp7 = true;
			hidelp7 = 'Lp7';
			graphlp7div.classList.remove("fa-toggle-on");
			graphlp7div.classList.add("fa-toggle-off");
			element.setAttribute("style", "color: red;");
		}
		checkgraphload();
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLp8" ) {
		if ( mqttpayload == 1) {
			boolDisplayLp8 = false;
			hidelp8 = 'foo';
			var element = document.getElementById("graphlp8div");
			graphlp8div.classList.remove("fa-toggle-off");
			graphlp8div.classList.add("fa-toggle-on");
			element.setAttribute("style", "color: green;");
		} else {
			var element = document.getElementById("graphlp8div");
			boolDisplayLp8 = true;
			hidelp8 = 'Lp8';
			graphlp8div.classList.remove("fa-toggle-on");
			graphlp8div.classList.add("fa-toggle-off");
			element.setAttribute("style", "color: red;");
		}
		checkgraphload();
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLpAll" ) {
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
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplaySpeicher" ) {
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
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplaySpeicherSoc" ) {
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
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLp1Soc" ) {
		if ( mqttpayload == 1) {
			$('#socenabledlp1').show();
			hidelp1soc = 'foo';
			boolDisplayLp1Soc = false;
			document.getElementById("graphlp1socdiv").setAttribute("style", "color: green;");
			graphlp1socdiv.classList.remove("fa-toggle-off");
			graphlp1socdiv.classList.add("fa-toggle-on");

		} else {
			hidelp1soc = 'LP1 SoC';
			$('#socenabledlp1').hide();
			boolDisplayLp1Soc = true;
			document.getElementById("graphlp1socdiv").setAttribute("style", "color: red;");
			graphlp1socdiv.classList.remove("fa-toggle-on");
			graphlp1socdiv.classList.add("fa-toggle-off");


		}
		checkgraphload();
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLp2Soc" ) {
		if ( mqttpayload == 1) {
			hidelp2soc = 'foo';
			$('#socenabledlp2').show();
			boolDisplayLp2Soc = false;
			document.getElementById("graphlp2socdiv").setAttribute("style", "color: green;");
			graphlp2socdiv.classList.remove("fa-toggle-off");
			graphlp2socdiv.classList.add("fa-toggle-on");
		} else {
			hidelp2soc = 'LP2 SoC';
			$('#socenabledlp2').hide();
			boolDisplayLp2Soc = true;
			document.getElementById("graphlp2socdiv").setAttribute("style", "color: red;");
			graphlp2socdiv.classList.remove("fa-toggle-on");
			graphlp2socdiv.classList.add("fa-toggle-off");
		}
		checkgraphload();
	}

	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLoad1" ) {
		if ( mqttpayload == 1) {
			hideload1 = 'foo';
			boolDisplayLoad1 = false;
			document.getElementById("graphload1div").setAttribute("style", "color: green;");
			graphload1div.classList.remove("fa-toggle-off");
			graphload1div.classList.add("fa-toggle-on");

		} else {
			hideload1 = 'Verbraucher 1';
			boolDisplayLoad1 = true;
			document.getElementById("graphload1div").setAttribute("style", "color: red;");
			graphload1div.classList.remove("fa-toggle-on");
			graphload1div.classList.add("fa-toggle-off");

		}
		checkgraphload();
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/boolDisplayLoad2" ) {
		if ( mqttpayload == 1) {
			hideload2 = 'foo';
			boolDisplayLoad2 = false;
			document.getElementById("graphload2div").setAttribute("style", "color: green;");
			graphload2div.classList.remove("fa-toggle-off");
			graphload2div.classList.add("fa-toggle-on");

		} else {
			hideload2 = 'Verbraucher 2';
			boolDisplayLoad2 = true;
			document.getElementById("graphload2div").setAttribute("style", "color: red;");
			graphload2div.classList.remove("fa-toggle-on");
			graphload2div.classList.add("fa-toggle-off");
		}
		checkgraphload();
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/1alllivevalues" ) {
		if (initialread == 0) {
			all1p = mqttpayload;
			all1 = 1;
		putgraphtogether();
		}
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/2alllivevalues" ) {
		if (initialread == 0) {
			all2p = mqttpayload;
			all2 = 1;
		putgraphtogether();
		}
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/3alllivevalues" ) {
		if (initialread == 0) {
			all3p = mqttpayload;
			all3 = 1;
		putgraphtogether();
		}
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/4alllivevalues" ) {
		if (initialread == 0) {
			all4p = mqttpayload;
			all4 = 1;
		putgraphtogether();
		}
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/5alllivevalues" ) {
		if (initialread == 0) {
			all5p = mqttpayload;
			all5 = 1;
		putgraphtogether();
		}
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/6alllivevalues" ) {
		if (initialread == 0) {
			all6p = mqttpayload;
			all6 = 1;
		putgraphtogether();
		}
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/7alllivevalues" ) {
		if (initialread == 0) {
			all7p = mqttpayload;
			all7 = 1;
		putgraphtogether();
		}
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/8alllivevalues" ) {
		if (initialread == 0) {
			all8p = mqttpayload;
			all8 = 1;
		putgraphtogether();
		}
	}
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/alllivevalues" ) {
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
	else if ( chartjsSelected == 1 && mqttmsg == "openWB/graph/lastlivevalues" ) {
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
			window.myLine.update();
		}

	}

	else if ( mqttmsg == "openWB/lp/1/boolChargePointConfigured" ) {
 		if ( mqttpayload == 0 ) {
			$('#lp1div').hide();
			$('#slider1div').hide();
		} else {
 			$('#lp1div').show();
			$('#slider1div').show();

		}
	}
	else if ( mqttmsg == "openWB/lp/2/boolChargePointConfigured" ) {
 		if ( mqttpayload == 0 ) {
			$('#lp2div').hide();
			$('#slider2div').hide();
		} else {
 			$('#lp2div').show();
			$('#slider2div').show();

		}
	}
	else if ( mqttmsg == "openWB/lp/3/boolChargePointConfigured" ) {
 		if ( mqttpayload == 0 ) {
			$('#lp3div').hide();
			$('#slider3div').hide();
		} else {
 			$('#lp3div').show();
			$('#slider3div').show();

		}
	}
	else if ( mqttmsg == "openWB/lp/4/boolChargePointConfigured" ) {
 		if ( mqttpayload == 0 ) {
			$('#lp4div').hide();
			$('#slider4div').hide();
		} else {
 			$('#lp4div').show();
			$('#slider4div').show();

		}
	}
	else if ( mqttmsg == "openWB/lp/5/boolChargePointConfigured" ) {
 		if ( mqttpayload == 0 ) {
			$('#lp5div').hide();
			$('#slider5div').hide();
		} else {
 			$('#lp5div').show();
			$('#slider5div').show();
		}
	}

	else if ( mqttmsg == "openWB/lp/6/boolChargePointConfigured" ) {
 		if ( mqttpayload == 0 ) {
			$('#lp6div').hide();
			$('#slider6div').hide();
		} else {
 			$('#lp6div').show();
			$('#slider6div').show();
		}
	}

	else if ( mqttmsg == "openWB/lp/7/boolChargePointConfigured" ) {
 		if ( mqttpayload == 0 ) {
			$('#lp7div').hide();
			$('#slider7div').hide();
		} else {
 			$('#lp7div').show();
			$('#slider7div').show();
		}
	}

	else if ( mqttmsg == "openWB/lp/8/boolChargePointConfigured" ) {
 		if ( mqttpayload == 0 ) {
			$('#lp8div').hide();
			$('#slider8div').hide();
		} else {
 			$('#lp8div').show();
			$('#slider8div').show();
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
	else if ( mqttmsg == "openWB/lp/1/ChargePointEnabled" ) {
		var lp1enabledelement = document.getElementById("lp1enableddiv");

		if ( mqttpayload == 0 ) {
			lp1enabledelement.classList.remove("fa-check");
			lp1enabledelement.classList.add("fa-times");
			lp1enabled = 0
		} else {
			lp1enabledelement.classList.remove("fa-times");
			lp1enabledelement.classList.add("fa-check");
			lp1enabled = 1
		}
	}
	else if ( mqttmsg == "openWB/lp/2/ChargePointEnabled" ) {
		var lp2enabledelement = document.getElementById("lp2enableddiv");

		if ( mqttpayload == 0 ) {
			lp2enabledelement.classList.remove("fa-check");
			lp2enabledelement.classList.add("fa-times");
			lp2enabled = 0
		} else {
			lp2enabledelement.classList.remove("fa-times");
			lp2enabledelement.classList.add("fa-check");
			lp2enabled = 1
		}
	}
	else if ( mqttmsg == "openWB/lp/3/ChargePointEnabled" ) {
		var lp3enabledelement = document.getElementById("lp3enableddiv");

		if ( mqttpayload == 0 ) {
			lp3enabledelement.classList.remove("fa-check");
			lp3enabledelement.classList.add("fa-times");
			lp3enabled = 0
		} else {
			lp3enabledelement.classList.remove("fa-times");
			lp3enabledelement.classList.add("fa-check");
			lp3enabled = 1
		}
	}
	else if ( mqttmsg == "openWB/lp/4/ChargePointEnabled" ) {
		var lp4enabledelement = document.getElementById("lp4enableddiv");

		if ( mqttpayload == 0 ) {
			lp4enabledelement.classList.remove("fa-check");
			lp4enabledelement.classList.add("fa-times");
			lp4enabled = 0
		} else {
			lp4enabledelement.classList.remove("fa-times");
			lp4enabledelement.classList.add("fa-check");
			lp4enabled = 1
		}
	}
	else if ( mqttmsg == "openWB/lp/5/ChargePointEnabled" ) {
		var lp5enabledelement = document.getElementById("lp5enableddiv");

		if ( mqttpayload == 0 ) {
			lp5enabledelement.classList.remove("fa-check");
			lp5enabledelement.classList.add("fa-times");
			lp5enabled = 0
		} else {
			lp5enabledelement.classList.remove("fa-times");
			lp5enabledelement.classList.add("fa-check");
			lp5enabled = 1
		}
	}
	else if ( mqttmsg == "openWB/lp/6/ChargePointEnabled" ) {
		var lp6enabledelement = document.getElementById("lp6enableddiv");

		if ( mqttpayload == 0 ) {
			lp6enabledelement.classList.remove("fa-check");
			lp6enabledelement.classList.add("fa-times");
			lp6enabled = 0
		} else {
			lp6enabledelement.classList.remove("fa-times");
			lp6enabledelement.classList.add("fa-check");
			lp6enabled = 1
		}
	}
	else if ( mqttmsg == "openWB/lp/7/ChargePointEnabled" ) {
		var lp7enabledelement = document.getElementById("lp7enableddiv");

		if ( mqttpayload == 0 ) {
			lp7enabledelement.classList.remove("fa-check");
			lp7enabledelement.classList.add("fa-times");
			lp7enabled = 0
		} else {
			lp7enabledelement.classList.remove("fa-times");
			lp7enabledelement.classList.add("fa-check");
			lp7enabled = 1
		}
	}
	else if ( mqttmsg == "openWB/lp/8/ChargePointEnabled" ) {
		var lp8enabledelement = document.getElementById("lp8enableddiv");

		if ( mqttpayload == 0 ) {
			lp8enabledelement.classList.remove("fa-check");
			lp8enabledelement.classList.add("fa-times");
			lp8enabled = 0
		} else {
			lp8enabledelement.classList.remove("fa-times");
			lp8enabledelement.classList.add("fa-check");
			lp8enabled = 1
		}
	}

	else if ( mqttmsg == "openWB/lp/1/kWhActualCharged") {
		$("#aktgeladendiv").html(mqttpayload);
		document.getElementById("prog1").value= mqttpayload;
	}
	else if ( mqttmsg == "openWB/lp/2/kWhActualCharged") {
		$("#aktgeladens1div").html(mqttpayload);
		document.getElementById("progs1").value= mqttpayload;
	}
	else if ( mqttmsg == "openWB/lp/3/kWhActualCharged") {
		$("#aktgeladens2div").html(mqttpayload);
		document.getElementById("progs2").value= mqttpayload;
	}
	else if ( mqttmsg == "openWB/pv/W") {
		pvwatt = parseInt(mqttpayload, 10);
		if ( pvwatt <= 0){
			pvwatt = pvwatt * -1;
			pvwattarrow = pvwatt;
			if (pvwatt > 999) {
				pvwatt = (pvwatt / 1000).toFixed(2);
				pvwatt = pvwatt + " kW Erzeugung";
			} else {
				pvwatt = pvwatt + " W Erzeugung";
			}
		}
		$("#pvdiv").html(pvwatt);
	}
	else if ( mqttmsg == "openWB/lp/1/W") {
		llaktuell = parseInt(mqttpayload, 10);
		llaktuellarrow = llaktuell;
		if (mqttpayload > 999) {
			mqttpayload = (mqttpayload / 1000).toFixed(2);
			mqttpayload = mqttpayload + " kW";
		} else {
		mqttpayload = mqttpayload + " W";
		}
		$("#lldiv").html(mqttpayload);
	}
	else if ( mqttmsg == "openWB/lp/2/W") {
		llaktuell = parseInt(mqttpayload, 10);
		llaktuelllp2arrow = llaktuell;
		if (mqttpayload > 999) {
			mqttpayload = (mqttpayload / 1000).toFixed(2);
			mqttpayload = mqttpayload + " kW";
		} else {
		mqttpayload = mqttpayload + " W";
		}
		$("#lllp2div").html(mqttpayload);
	}
	else if ( mqttmsg == "openWB/lp/3/W") {
		llaktuell = parseInt(mqttpayload, 10);
		llaktuelllp3arrow = llaktuell;
		if (mqttpayload > 999) {
			mqttpayload = (mqttpayload / 1000).toFixed(2);
			mqttpayload = mqttpayload + " kW";
		} else {
		mqttpayload = mqttpayload + " W";
		}
		$("#lllp3div").html(mqttpayload);
	}
	else if ( mqttmsg == "openWB/lp/4/W") {
		llaktuell = parseInt(mqttpayload, 10);
		llaktuelllp4arrow = llaktuell;
		if (mqttpayload > 999) {
			mqttpayload = (mqttpayload / 1000).toFixed(2);
			mqttpayload = mqttpayload + " kW";
		} else {
		mqttpayload = mqttpayload + " W";
		}
		$("#lllp4div").html(mqttpayload);
	}
	else if ( mqttmsg == "openWB/lp/5/W") {
		llaktuell = parseInt(mqttpayload, 10);
		llaktuelllp5arrow = llaktuell;
		if (mqttpayload > 999) {
			mqttpayload = (mqttpayload / 1000).toFixed(2);
			mqttpayload = mqttpayload + " kW";
		} else {
		mqttpayload = mqttpayload + " W";
		}
		$("#lllp5div").html(mqttpayload);
	}
	else if ( mqttmsg == "openWB/lp/6/W") {
		llaktuell = parseInt(mqttpayload, 10);
		llaktuelllp6arrow = llaktuell;
		if (mqttpayload > 999) {
			mqttpayload = (mqttpayload / 1000).toFixed(2);
			mqttpayload = mqttpayload + " kW";
		} else {
		mqttpayload = mqttpayload + " W";
		}
		$("#lllp6div").html(mqttpayload);
	}
	else if ( mqttmsg == "openWB/lp/7/W") {
		llaktuell = parseInt(mqttpayload, 10);
		llaktuelllp7arrow = llaktuell;
		if (mqttpayload > 999) {
			mqttpayload = (mqttpayload / 1000).toFixed(2);
			mqttpayload = mqttpayload + " kW";
		} else {
		mqttpayload = mqttpayload + " W";
		}
		$("#lllp7div").html(mqttpayload);
	}
	else if ( mqttmsg == "openWB/lp/8/W") {
		llaktuell = parseInt(mqttpayload, 10);
		llaktuelllp8arrow = llaktuell;
		if (mqttpayload > 999) {
			mqttpayload = (mqttpayload / 1000).toFixed(2);
			mqttpayload = mqttpayload + " kW";
		} else {
		mqttpayload = mqttpayload + " W";
		}
		$("#lllp8div").html(mqttpayload);
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
	else if ( mqttmsg == "openWB/lp/1/boolPlugStat") {
		if ($('#plugstatlp1div').length > 0) {
		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp1div");
			element.classList.add("fa");
			element.classList.add("fa-plug");
		} else {
			var element = document.getElementById("plugstatlp1div");
			element.classList.remove("fa");
			element.classList.remove("fa-plug");
		}
		}
		if ($('#carlp1').length > 0) {
			var elementcarlp1 = document.getElementById("carlp1");
			if (mqttpayload == 1) {
				elementcarlp1.setAttribute("style", "color: green;");
			} else {
				elementcarlp1.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/2/boolPlugStat") {
		if ($('#plugstatlp2div').length > 0) {
		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp2div");
			element.classList.add("fa");
			element.classList.add("fa-plug");
		} else {
			var element = document.getElementById("plugstatlp2div");
			element.classList.remove("fa");
			element.classList.remove("fa-plug");
		}
		}
		if ($('#carlp2').length > 0) {
			var elementcarlp2 = document.getElementById("carlp2");
			if (mqttpayload == 1) {
				elementcarlp2.setAttribute("style", "color: green;");
			} else {
				elementcarlp2.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/3/boolPlugStat") {
		if ($('#plugstatlp3div').length > 0) {
		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp3div");
			element.classList.add("fa");
			element.classList.add("fa-plug");
		} else {
			var element = document.getElementById("plugstatlp3div");
			element.classList.remove("fa");
			element.classList.remove("fa-plug");
		}
		}
		if ($('#carlp3').length > 0) {
			var elementcarlp3 = document.getElementById("carlp3");
			if (mqttpayload == 1) {
				elementcarlp3.setAttribute("style", "color: green;");
			} else {
				elementcarlp3.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/3/boolChargeStat") {
		if ($('#plugstatlp3div').length > 0) {
		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp3div");
			element.setAttribute("style", "color: #00FF00;");
		} else {
			var element = document.getElementById("plugstatlp3div");
			element.setAttribute("style", "color: white;");
		}
		}
		if ($('#socstatlp3').length > 0) {
			var element = document.getElementById("socstatlp3");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: black;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/4/boolPlugStat") {
		if ($('#plugstatlp4div').length > 0) {

		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp4div");
			element.classList.add("fa");
			element.classList.add("fa-plug");
		} else {
			var element = document.getElementById("plugstatlp4div");
			element.classList.remove("fa");
			element.classList.remove("fa-plug");
		}
		}
		if ($('#carlp4').length > 0) {
			var elementcarlp4 = document.getElementById("carlp4");
			if (mqttpayload == 1) {
				elementcarlp4.setAttribute("style", "color: green;");
			} else {
				elementcarlp4.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/4/boolChargeStat") {
		if ($('#plugstatlp4div').length > 0) {
		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp4div");
			element.setAttribute("style", "color: #00FF00;");
		} else {
			var element = document.getElementById("plugstatlp4div");
			element.setAttribute("style", "color: white;");
		}
		}
		if ($('#socstatlp4').length > 0) {
			var element = document.getElementById("socstatlp4");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: black;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/5/boolPlugStat") {
		if ($('#plugstatlp5div').length > 0) {

		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp5div");
			element.classList.add("fa");
			element.classList.add("fa-plug");
		} else {
			var element = document.getElementById("plugstatlp5div");
			element.classList.remove("fa");
			element.classList.remove("fa-plug");
		}
		}
		if ($('#carlp5').length > 0) {
			var elementcarlp5 = document.getElementById("carlp5");
			if (mqttpayload == 1) {
				elementcarlp5.setAttribute("style", "color: green;");
			} else {
				elementcarlp5.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/5/boolChargeStat") {
		if ($('#plugstatlp5div').length > 0) {
		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp5div");
			element.setAttribute("style", "color: #00FF00;");
		} else {
			var element = document.getElementById("plugstatlp5div");
			element.setAttribute("style", "color: white;");
		}
		}
		if ($('#socstatlp5').length > 0) {
			var element = document.getElementById("socstatlp5");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: black;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/6/boolPlugStat") {
		if ($('#plugstatlp6div').length > 0) {

		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp6div");
			element.classList.add("fa");
			element.classList.add("fa-plug");
		} else {
			var element = document.getElementById("plugstatlp6div");
			element.classList.remove("fa");
			element.classList.remove("fa-plug");
		}
		}
		if ($('#carlp6').length > 0) {
			var elementcarlp6 = document.getElementById("carlp6");
			if (mqttpayload == 1) {
				elementcarlp6.setAttribute("style", "color: green;");
			} else {
				elementcarlp6.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/6/boolChargeStat") {
		if ($('#plugstatlp6div').length > 0) {
		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp6div");
			element.setAttribute("style", "color: #00FF00;");
		} else {
			var element = document.getElementById("plugstatlp6div");
			element.setAttribute("style", "color: white;");
		}
		}
		if ($('#socstatlp6').length > 0) {
			var element = document.getElementById("socstatlp6");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: black;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/7/boolPlugStat") {
		if ($('#plugstatlp7div').length > 0) {

		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp7div");
			element.classList.add("fa");
			element.classList.add("fa-plug");
		} else {
			var element = document.getElementById("plugstatlp7div");
			element.classList.remove("fa");
			element.classList.remove("fa-plug");
		}
		}
		if ($('#carlp7').length > 0) {
			var elementcarlp7 = document.getElementById("carlp7");
			if (mqttpayload == 1) {
				elementcarlp7.setAttribute("style", "color: green;");
			} else {
				elementcarlp7.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/7/boolChargeStat") {
		if ($('#plugstatlp7div').length > 0) {

		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp7div");
			element.setAttribute("style", "color: #00FF00;");
		} else {
			var element = document.getElementById("plugstatlp7div");
			element.setAttribute("style", "color: white;");
		}
		}
		if ($('#socstatlp7').length > 0) {
			var element = document.getElementById("socstatlp7");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: black;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/8/boolPlugStat") {
		if ($('#plugstatlp8div').length > 0) {

		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp8div");
			element.classList.add("fa");
			element.classList.add("fa-plug");
		} else {
			var element = document.getElementById("plugstatlp8div");
			element.classList.remove("fa");
			element.classList.remove("fa-plug");
		}
		}
		if ($('#carlp8').length > 0) {
			var elementcarlp8 = document.getElementById("carlp8");
			if (mqttpayload == 1) {
				elementcarlp8.setAttribute("style", "color: green;");
			} else {
				elementcarlp8.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/8/boolChargeStat") {
		if ($('#plugstatlp8div').length > 0) {
		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp8div");
			element.setAttribute("style", "color: #00FF00;");
		} else {
			var element = document.getElementById("plugstatlp8div");
			element.setAttribute("style", "color: white;");
		}
		}
		if ($('#socstatlp8').length > 0) {
			var element = document.getElementById("socstatlp8");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: black;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/1/boolChargeStat") {
		if ($('#plugstatlp1div').length > 0) {
		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp1div");
			element.setAttribute("style", "color: #00FF00;");
		} else {
			var element = document.getElementById("plugstatlp1div");
			element.setAttribute("style", "color: white;");
		}
		}
		if ($('#socstatlp1').length > 0) {
			var element = document.getElementById("socstatlp1");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: black;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/2/boolChargeStat") {
		if ($('#plugstatlp2div').length > 0) {

		if (mqttpayload == 1) {
			var element = document.getElementById("plugstatlp2div");
			element.setAttribute("style", "color: #00FF00;");
		} else {
			var element = document.getElementById("plugstatlp2div");
			element.setAttribute("style", "color: white;");
		}
		}
		if ($('#socstatlp2').length > 0) {
			var element = document.getElementById("socstatlp2");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: black;");
			}
		}
	}
	else if ( mqttmsg == "openWB/housebattery/%Soc" ) {
		speichersoc = mqttpayload;
		$("#speichersocdiv").html(mqttpayload);
	}
	else if ( mqttmsg == "openWB/lp/1/%Soc" ) {
		lp1soc = mqttpayload;
		$("#soclevel").html(mqttpayload);
	}
	else if ( mqttmsg == "openWB/lp/2/%Soc" ) {
		lp2soc = mqttpayload;
		$("#soc1level").html(mqttpayload);
	}
	else if ( mqttmsg == "openWB/lp/1/ChargeStatus" ) {
		if ($('#stationlp1').length > 0) {
			var element = document.getElementById("stationlp1");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/2/ChargeStatus" ) {
		if ($('#stationlp2').length > 0) {
			var element = document.getElementById("stationlp2");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/3/ChargeStatus" ) {
		if ($('#stationlp3').length > 0) {
			var element = document.getElementById("stationlp3");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/4/ChargeStatus" ) {
		if ($('#stationlp4').length > 0) {
			var element = document.getElementById("stationlp4");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/5/ChargeStatus" ) {
		if ($('#stationlp5').length > 0) {
			var element = document.getElementById("stationlp5");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/6/ChargeStatus" ) {
		if ($('#stationlp6').length > 0) {
			var element = document.getElementById("stationlp6");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/7/ChargeStatus" ) {
		if ($('#stationlp7').length > 0) {
			var element = document.getElementById("stationlp7");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: blue;");
			}
		}
	}
	else if ( mqttmsg == "openWB/lp/8/ChargeStatus" ) {
		if ($('#stationlp8').length > 0) {
			var element = document.getElementById("stationlp8");
			if (mqttpayload == 1) {
				element.setAttribute("style", "color: #00FF00;");
			} else {
				element.setAttribute("style", "color: blue;");
			}
		}
	}

	else if ( mqttmsg == "openWB/global/ChargeMode" ) {
		     if(mqttpayload == 0){
			$('.actstat .btn').addClass("btn-green");
			$('.actstat1 .btn').addClass("btn-red");
			$('.actstat2 .btn').addClass("btn-red");
			$('.actstat3 .btn').addClass("btn-red");
			$('.actstat3 .btn').removeClass("btn-green");
			$('.actstat4 .btn').addClass("btn-red");
			$('.actstat4 .btn').removeClass("btn-green");
			$('.actstat1 .btn').removeClass("btn-green");
			$('.actstat2 .btn').removeClass("btn-green");
		   	loaddivs();
		     }
		    if(mqttpayload == 1){
			$('.actstat1 .btn').addClass("btn-green");
			$('.actstat .btn').addClass("btn-red");
			$('.actstat2 .btn').addClass("btn-red");
			$('.actstat3 .btn').addClass("btn-red");
			$('.actstat .btn').removeClass("btn-green");
			$('.actstat3 .btn').removeClass("btn-green");
			$('.actstat2 .btn').removeClass("btn-green");
			$('.actstat4 .btn').addClass("btn-red");
			$('.actstat4 .btn').removeClass("btn-green");
		   	loaddivs();
		    }
		    if(mqttpayload == 2){
			$('.actstat2 .btn').addClass("btn-green");
			$('.actstat .btn').addClass("btn-red");
			$('.actstat1 .btn').addClass("btn-red");
			$('.actstat3 .btn').addClass("btn-red");
			$('.actstat .btn').removeClass("btn-green");
			$('.actstat3 .btn').removeClass("btn-green");
			$('.actstat1 .btn').removeClass("btn-green");
			$('.actstat4 .btn').addClass("btn-red");
			$('.actstat4 .btn').removeClass("btn-green");
		   	loaddivs();
		    }
		    if(mqttpayload == 3){
			$('.actstat2 .btn').addClass("btn-red");
			$('.actstat3 .btn').addClass("btn-green");
			$('.actstat2 .btn').removeClass("btn-green");

			$('.actstat .btn').addClass("btn-red");
			$('.actstat1 .btn').addClass("btn-red");
			$('.actstat .btn').removeClass("btn-green");
			$('.actstat1 .btn').removeClass("btn-green");
			$('.actstat4 .btn').addClass("btn-red");
			$('.actstat4 .btn').removeClass("btn-green");
		   	loaddivs();
		    }
		    if(mqttpayload == 4){
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
		   	loaddivs();
		    }
	}
	else if ( mqttmsg == "openWB/lp/1/ADirectModeAmps" ) {
		document.getElementById("sofortlllp1s").value = mqttpayload;
		document.getElementById("sofortlllp1l").innerHTML = mqttpayload;
	}

	else if ( mqttmsg == "openWB/lp/2/ADirectModeAmps" ) {
		document.getElementById("sofortlllp2s").value = mqttpayload;
		document.getElementById("sofortlllp2l").innerHTML = mqttpayload;
	}

	else if ( mqttmsg == "openWB/lp/3/ADirectModeAmps" ) {
		document.getElementById("sofortlllp3s").value = mqttpayload;
		document.getElementById("sofortlllp3l").innerHTML = mqttpayload;
	}
	else if ( mqttmsg == "openWB/lp/4/ADirectModeAmps" ) {
		document.getElementById("sofortlllp4s").value = mqttpayload;
		document.getElementById("sofortlllp4l").innerHTML = mqttpayload;
	}
	else if ( mqttmsg == "openWB/lp/5/ADirectModeAmps" ) {
		document.getElementById("sofortlllp5s").value = mqttpayload;
		document.getElementById("sofortlllp5l").innerHTML = mqttpayload;
	}
	else if ( mqttmsg == "openWB/lp/6/ADirectModeAmps" ) {
		document.getElementById("sofortlllp6s").value = mqttpayload;
		document.getElementById("sofortlllp6l").innerHTML = mqttpayload;
	}
	else if ( mqttmsg == "openWB/lp/7/ADirectModeAmps" ) {
		document.getElementById("sofortlllp7s").value = mqttpayload;
		document.getElementById("sofortlllp7l").innerHTML = mqttpayload;
	}
	else if ( mqttmsg == "openWB/lp/8/ADirectModeAmps" ) {
		document.getElementById("sofortlllp8s").value = mqttpayload;
		document.getElementById("sofortlllp8l").innerHTML = mqttpayload;
	}
	else {
		thevalues.forEach(function(thevar){
			if ( mqttmsg == thevar[0] ) {
				$(thevar[1]).html(mqttpayload);
			}
		});
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
var options = {
	timeout: 5,
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
	if ( lp1enabled == 0 ) {
	publish("1","openWB/set/lp1/ChargePointEnabled");
	} else {
	publish("0","openWB/set/lp1/ChargePointEnabled");
	}
};

function lp2enabledclick() {
	if ( lp2enabled == 0 ) {
	publish("1","openWB/set/lp2/ChargePointEnabled");
	} else {
	publish("0","openWB/set/lp2/ChargePointEnabled");
	}
};
function lp3enabledclick() {
	if ( lp3enabled == 0 ) {
	publish("1","openWB/set/lp3/ChargePointEnabled");
	} else {
	publish("0","openWB/set/lp3/ChargePointEnabled");
	}
};
function lp4enabledclick() {
	if ( lp4enabled == 0 ) {
	publish("1","openWB/set/lp4/ChargePointEnabled");
	} else {
	publish("0","openWB/set/lp4/ChargePointEnabled");
	}
};
function lp5enabledclick() {
	if ( lp5enabled == 0 ) {
	publish("1","openWB/set/lp5/ChargePointEnabled");
	} else {
	publish("0","openWB/set/lp5/ChargePointEnabled");
	}
};
function lp6enabledclick() {
	if ( lp6enabled == 0 ) {
	publish("1","openWB/set/lp6/ChargePointEnabled");
	} else {
	publish("0","openWB/set/lp6/ChargePointEnabled");
	}
};
function lp7enabledclick() {
	if ( lp7enabled == 0 ) {
	publish("1","openWB/set/lp7/ChargePointEnabled");
	} else {
	publish("0","openWB/set/lp7/ChargePointEnabled");
	}
};
function lp8enabledclick() {
	if ( lp8enabled == 0 ) {
	publish("1","openWB/set/lp8/ChargePointEnabled");
	} else {
	publish("0","openWB/set/lp8/ChargePointEnabled");
	}
};
function lp1DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp1l").innerHTML,"openWB/set/lp1/DirectChargeAmps");
};
function lp2DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp2l").innerHTML,"openWB/set/lp2/DirectChargeAmps");
};
function lp3DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp3l").innerHTML,"openWB/set/lp3/DirectChargeAmps");
};
function lp4DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp4l").innerHTML,"openWB/set/lp4/DirectChargeAmps");
};
function lp5DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp5l").innerHTML,"openWB/set/lp5/DirectChargeAmps");
};
function lp6DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp6l").innerHTML,"openWB/set/lp6/DirectChargeAmps");
};
function lp7DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp7l").innerHTML,"openWB/set/lp7/DirectChargeAmps");
};
function lp8DirectChargeAmpsClick() {
	publish(document.getElementById("sofortlllp8l").innerHTML,"openWB/set/lp8/DirectChargeAmps");
};
function sofortclick() {
	        publish("0","openWB/set/ChargeMode");
	        publish("0","openWB/global/ChargeMode");
};
function minundpvclick() {
	        publish("1","openWB/set/ChargeMode");
	        publish("1","openWB/global/ChargeMode");

};
function nurpvclick() {
	        publish("2","openWB/set/ChargeMode");
	        publish("2","openWB/global/ChargeMode");
};
function standbyclick() {
	        publish("4","openWB/set/ChargeMode");
	        publish("4","openWB/global/ChargeMode");
};
function stopclick() {
	        publish("3","openWB/set/ChargeMode");
	        publish("3","openWB/global/ChargeMode");
};
function renewMQTTclick() {
	        publish("1","openWB/set/RenewMQTT");
		alert("Erneuern der Werte initiert, dies dauert ca 15-20 Sekunden.");
}
function putgraphtogether() {
	if ( (all1 == 1) && (all2 == 1) && (all3 == 1) && (all4 == 1) && (all5 == 1) && (all6 == 1) && (all7 == 1) && (all8 == 1) ){
		var alldata = all1p + "\n" + all2p + "\n" + all3p + "\n" + all4p + "\n" + all5p + "\n" + all6p + "\n" + all7p + "\n" + all8p;
		alldata = alldata.replace(/^\s*[\n]/gm, '');
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
}

function getfile() {



if (document.getElementById("hook1div")) {

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
				var element = document.getElementById("hook1div");
				element.classList.add("fa");
				element.classList.add("fa-plug");
				element.setAttribute("style", "color: green;");
			    } else {
				var element = document.getElementById("hook1div");
				element.setAttribute("style", "background-color: green;");
			    }
		    } else {
			if ( activetheme == "symbol") {
				var element = document.getElementById("hook1div");
				element.classList.add("fa");
				element.classList.add("fa-plug");
				element.setAttribute("style", "color: red;");
			    } else {
				var element = document.getElementById("hook1div");
				element.setAttribute("style", "background-color: red;");
			}
		    }
    }
  });
} else {
        $('#hook1div').hide();
    }
});
}
if (document.getElementById("hook2div")) {
$(function() {
    if(hook2_aktiv == '1') {

 $.ajax({
    url: "/openWB/ramdisk/hook2akt",
    beforeSend: function(xhr){  xhr.overrideMimeType( "text/plain; charset=x-user-defined" );},
    complete: function(request){
		if (request.responseText == 1) {
			if ( activetheme == "symbol") {
				var element = document.getElementById("hook2div");
				element.classList.add("fa");
				element.classList.add("fa-plug");
				element.setAttribute("style", "color: green;");
			    } else {
				var element = document.getElementById("hook2div");
				element.setAttribute("style", "background-color: green;");
			    }
		    } else {
			if ( activetheme == "symbol") {
				var element = document.getElementById("hook1div");
				element.classList.add("fa");
				element.classList.add("fa-plug");
				element.setAttribute("style", "color: red;");
			    } else {

				var element = document.getElementById("hook2div");
				element.setAttribute("style", "background-color: red;");
			}
		    }
    }
  });
   } else {
        $('#hook2div').hide();
    }
});
}
if (document.getElementById("hook3div")) {

    $(function() {
    if(hook3_aktiv == '1') {

 $.ajax({
    url: "/openWB/ramdisk/hook3akt",
    complete: function(request){
		if (request.responseText == 1) {
			if ( activetheme == "symbol") {
				var element = document.getElementById("hook3div");
				element.classList.add("fa");
				element.classList.add("fa-plug");
				element.setAttribute("style", "color: green;");
			    } else {

				var element = document.getElementById("hook3div");
				element.setAttribute("style", "background-color: green;");
			    }
		    } else {
			if ( activetheme == "symbol") {
				var element = document.getElementById("hook3div");
				element.classList.add("fa");
				element.classList.add("fa-plug");
				element.setAttribute("style", "color: red;");
			    } else {

				var element = document.getElementById("hook3div");
				element.setAttribute("style", "background-color: red;");
			}
		    }
    }
  });
  } else {
        $('#hook3div').hide();
    }
});
}
}

doInterval = setInterval(getfile, 5000);
getfile();
