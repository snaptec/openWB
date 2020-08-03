/**
 * functions to setup graph via MQTT-messages
 *
 * @author Michael Ortenstein
 */

function switchToggleOn(elementName) {
	document.getElementById(elementName).setAttribute('style', 'color: green;');
	$("#"+elementName).removeClass('fa-toggle-off fa-question-circle');
	$("#"+elementName).addClass('fa-toggle-on');
}

function switchToggleOff(elementName) {
	document.getElementById(elementName).setAttribute('style', 'color: red;');
	$("#"+elementName).removeClass('fa-toggle-on fa-question-circle');
	$("#"+elementName).addClass('fa-toggle-off');
}

function processMessages(mqttmsg, mqttpayload) {
	if ( mqttmsg == 'openWB/graph/boolDisplayHouseConsumption' ) {
		if ( mqttpayload == 1) {
			boolDisplayHouseConsumption = false;
			hidehaus = 'foo';
			switchToggleOn('graphhausdiv');
		} else {
			boolDisplayHouseConsumption = true;
			hidehaus = 'Hausverbrauch';
			switchToggleOff('graphhausdiv')
		}
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayLegend' ) {
		if ( mqttpayload == 1) {
			boolDisplayLegend = true;
			switchToggleOn('graphlegenddiv');
		} else {
			boolDisplayLegend = false;
			switchToggleOff('graphlegenddiv');
		}
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayLiveGraph' ) {
		if ( mqttpayload == 1) {
			$('#thegraph').show();
			boolDisplayLiveGraph = true;
			switchToggleOn('graphgraphdiv');
		} else {
			$('#thegraph').hide();
			boolDisplayLiveGraph = false;
			switchToggleOff('graphgraphdiv');
		}
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayEvu' ) {
		if ( mqttpayload == 1) {
			boolDisplayEvu = false;
			hideevu = 'foo';
			switchToggleOn('graphevudiv');
		} else {
			boolDisplayEvu = true;
			hideevu = 'Bezug';
			switchToggleOff('graphevudiv');
		}
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayPv' ) {
		if ( mqttpayload == 1) {
			boolDisplayPv = false;
			hidepv = 'foo';
			switchToggleOn('graphpvdiv');
		} else {
			boolDisplayPv = true;
			hidepv = 'PV';
			switchToggleOff('graphpvdiv');
		}
	}
	else if ( mqttmsg.match( /^openwb\/graph\/booldisplaylp[1-9][0-9]*$/i ) ) {
		// matches to all messages containing 'openwb/graph/booldisplaylp#'
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		// now call functions or set variables corresponding to the index
		if ( mqttpayload == 1) {
			window['boolDisplayLp'+index] = false;
			window['hidelp'+index] = 'foo';
			switchToggleOn('graphlp'+index+'div');
		} else {
			window['boolDisplayLp'+index] = true;
			window['hidelp'+index] = 'Lp' + index;
			switchToggleOff('graphlp'+index+'div');
		}
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayLpAll' ) {
		if ( mqttpayload == 1) {
			boolDisplayLpAll = false;
			hidelpa = 'foo';
			switchToggleOn('graphlpalldiv');
		} else {
			boolDisplayLpAll = true;
			hidelpa = 'LP Gesamt';
			switchToggleOff('graphlpalldiv');
		}
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplaySpeicher' ) {
		if ( mqttpayload == 1) {
			boolDisplaySpeicher = false;
			hidespeicher = 'foo';
			switchToggleOn('graphspeicherdiv');
		} else {
			hidespeicher = 'Speicherleistung';
			boolDisplaySpeicher = true;
			switchToggleOff('graphspeicherdiv');
		}
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplaySpeicherSoc' ) {
		if ( mqttpayload == 1) {
			hidespeichersoc = 'foo';
			boolDisplaySpeicherSoc = false;
			switchToggleOn('graphspeichersocdiv');
		} else {
			hidespeichersoc = 'Speicher SoC';
			boolDisplaySpeicherSoc = true;
			switchToggleOff('graphspeichersocdiv');
		}
	}
	else if ( mqttmsg.match( /^openwb\/graph\/booldisplaylp[1-9][0-9]*soc$/i ) ) {
		// matches to all messages containing 'openwb/graph/booldisplaylp#soc'
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		if ( mqttpayload == 1) {
			$('#socenabledlp'+index).show();
			window['boolDisplayLp'+index+'Soc'] = false;
			window['hidelp'+index+'soc'] = 'foo';
			switchToggleOn('graphlp'+index+'socdiv');
		} else {
			$('#socenabledlp'+index).hide();
			window['boolDisplayLp'+index+'Soc'] = true;
			window['hidelp'+index+'soc'] = 'LP'+index+' SoC';
			switchToggleOff('graphlp'+index+'socdiv');
		}
	}
	else if ( mqttmsg.match( /^openwb\/graph\/booldisplayload[1-9][0-9]*$/i ) ) {
		// matches to all messages containing 'openwb/graph/booldisplayload#'
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		// now call functions or set variables corresponding to the index
		if ( mqttpayload == 1) {
			window['hideload'+index] = 'foo';
			window['boolDisplayLoad'+index] = false;
			switchToggleOn('graphload'+index+'div');
		} else {
			window['hideload'+index] = 'Verbraucher ' + index;
			window['boolDisplayLoad'+index] = true;
			switchToggleOff('graphload'+index+'div');
		}
	}
	else if ( mqttmsg.match( /^openwb\/graph\/[1-9][0-9]*alllivevalues$/i ) ) {
		// matches to all messages containing 'openwb/graph/#alllivevalues'
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d/g)[0];  // extract first match = number from mqttmsg
		// now call functions or set variables corresponding to the index
		if (initialread == 0) {
			window['all'+index+'p'] = mqttpayload;
			window['all'+index] = 1;
			putgraphtogether();
		}
	}
	else if ( mqttmsg == 'openWB/graph/lastlivevalues' ) {
		if ( initialread > 0) {
			var lines = mqttpayload.split('\n');
			for (var i = 0; i < lines.length; i++) {
				var ldate = lines[i].split(',')[0];
				var lbezug = lines[i].split(',')[1];
				var lpv = lines[i].split(',')[3];
				var llp2 = lines[i].split(',')[5];
				var lspeicherl = lines[i].split(',')[7];
				var lsoc = lines[i].split(',')[9];
				var lspeichersoc = lines[i].split(',')[8];
				var lpa = lines[i].split(',')[2];
				var llp1 = lines[i].split(',')[4];
				var lsoc1 = lines[i].split(',')[10];
				var lhausverbrauch = lines[i].split(',')[11];
				var lverbraucher1 = lines[i].split(',')[12];
				var lverbraucher2 = lines[i].split(',')[13];
				var lp3 = lines[i].split(',')[14];
				var lp4 = lines[i].split(',')[15];
				var lp5 = lines[i].split(',')[16];
				var lp6 = lines[i].split(',')[17];
				var lp7 = lines[i].split(',')[18];
				var lp8 = lines[i].split(',')[19];
			}
			myLine.data.labels.push(ldate.substring(0, ldate.length -3));
			myLine.data.datasets[2].data.push(lbezug / 1000);
			myLine.data.datasets[3].data.push(lpv / 1000);
			myLine.data.datasets[4].data.push(lspeicherl / 1000);
			myLine.data.datasets[5].data.push(lspeichersoc);
			myLine.data.datasets[6].data.push(lsoc);
			myLine.data.datasets[0].data.push(llp1 / 1000);
			myLine.data.datasets[1].data.push(llp2 / 1000);
			myLine.data.datasets[7].data.push(lsoc1);
			myLine.data.datasets[8].data.push(lhausverbrauch / 1000);
			myLine.data.datasets[9].data.push(lverbraucher1 / 1000);
			myLine.data.datasets[10].data.push(lverbraucher2 / 1000);
			myLine.data.datasets[11].data.push(lpa / 1000);
			myLine.data.datasets[12].data.push(lp3 / 1000);
			myLine.data.datasets[13].data.push(lp4 / 1000);
			myLine.data.datasets[14].data.push(lp5 / 1000);
			myLine.data.datasets[15].data.push(lp6 / 1000);
			myLine.data.datasets[16].data.push(lp7 / 1000);
			myLine.data.datasets[17].data.push(lp8 / 1000);
			myLine.data.labels.splice(0, 1);
			myLine.data.datasets.forEach(function(dataset) {
				dataset.data.splice(0, 1);
			});
			myLine.update();
		}
	}
}  // end processMessages