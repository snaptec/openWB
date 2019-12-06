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
var lp1enabled
var lp2enabled
var lp3enabled
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

	else if ( mqttmsg == "openWB/lp/1/kWhActualharged") {
		$("#aktgeladenprog1div").html(mqttpayload);
		document.getElementById("prog1").value= mqttpayload;
	}
	else if ( mqttmsg == "openWB/lp/2/kWhActualharged") {
		$("#aktgeladens1div").html(mqttpayload);
		document.getElementById("progs1").value= mqttpayload;
	}
	else if ( mqttmsg == "openWB/lp/3/kWhActualharged") {
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
	else if ( mqttmsg  == mqtttopic ) {
		$(htmldiv).html(mqttpayload);
	}
	else {
		//do nothing
	} 
}
//Gets  called if the websocket/mqtt connection gets disconnected for any reason
client.onConnectionLost = function (responseObject) {
	client.connect(options);
};
//Gets called whenever you receive a message
client.onMessageArrived = function (message) {
	thevalues.forEach(function(thevar) {
		handlevar(message.destinationName, message.payloadString, thevar[0], thevar[1]);
	});
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
function getfile() {



if (document.getElementById("hook1div")) {

$(function() {
    if(hook1_aktiv == '1') {
 $.ajax({
    url: "/openWB/ramdisk/hook1akt",
    complete: function(request){
		if (request.responseText == 1) {
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
