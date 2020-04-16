/**
 * functions to setup graph via MQTT-messages
 *
 * @author Michael Ortenstein
 */

 function processMessages(mqttmsg, mqttpayload) {
	if ( mqttmsg == 'openWB/graph/boolDisplayHouseConsumption' ) {
		if ( mqttpayload == 1) {
			boolDisplayHouseConsumption = false;
			hidehaus = 'foo';
			document.getElementById('graphhausdiv').setAttribute('style', 'color: green;');
			graphhausdiv.classList.remove('fa-toggle-off');
			graphhausdiv.classList.add('fa-toggle-on');

		} else {
			boolDisplayHouseConsumption = true;
			document.getElementById('graphhausdiv').setAttribute('style', 'color: red;');
			graphhausdiv.classList.remove('fa-toggle-on');
			graphhausdiv.classList.add('fa-toggle-off');
			hidehaus = 'Hausverbrauch';
		}

	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayLegend' ) {
		if ( mqttpayload == 0) {
			boolDisplayLegend = false;
			document.getElementById('graphlegenddiv').setAttribute('style', 'color: red;');
			graphlegenddiv.classList.remove('fa-toggle-on');
			graphlegenddiv.classList.add('fa-toggle-off');
		} else {
			boolDisplayLegend = true;
			document.getElementById('graphlegenddiv').setAttribute('style', 'color: green;');
			graphlegenddiv.classList.remove('fa-toggle-off');
			graphlegenddiv.classList.add('fa-toggle-on');

		}

	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayLiveGraph' ) {
		if ( mqttpayload == 0) {
			$('#thegraph').hide();
			boolDisplayLiveGraph = false;
			document.getElementById('graphgraphdiv').setAttribute('style', 'color: red;');
			graphgraphdiv.classList.remove('fa-toggle-on');
			graphgraphdiv.classList.add('fa-toggle-off');
		} else {
			$('#thegraph').show();
			boolDisplayLiveGraph = true;
			document.getElementById('graphgraphdiv').setAttribute('style', 'color: green;');
			graphgraphdiv.classList.remove('fa-toggle-off');
			graphgraphdiv.classList.add('fa-toggle-on');
		}
	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayEvu' ) {
		if ( mqttpayload == 1) {
			boolDisplayEvu = false;
			hideevu = 'foo';
			document.getElementById('graphevudiv').setAttribute('style', 'color: green;');
			graphevudiv.classList.remove('fa-toggle-off');
			graphevudiv.classList.add('fa-toggle-on');

		} else {
			boolDisplayEvu = true;
			hideevu = 'Bezug';
			document.getElementById('graphevudiv').setAttribute('style', 'color: red;');
			graphevudiv.classList.remove('fa-toggle-on');
			graphevudiv.classList.add('fa-toggle-off');

		}

	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayPv' ) {
		if ( mqttpayload == 1) {
			boolDisplayPv = false;
			hidepv = 'foo';
			document.getElementById('graphpvdiv').setAttribute('style', 'color: green;');
			graphpvdiv.classList.remove('fa-toggle-off');
			graphpvdiv.classList.add('fa-toggle-on');
		} else {
			boolDisplayPv = true;
			hidepv = 'PV';
			document.getElementById('graphpvdiv').setAttribute('style', 'color: red;');
			graphpvdiv.classList.remove('fa-toggle-on');
			graphpvdiv.classList.add('fa-toggle-off');
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
			document.getElementById('graphlp'+index+'div').setAttribute('style', 'color: green;');
			window['graphlp'+index+'div'].classList.remove('fa-toggle-off');
			window['graphlp'+index+'div'].classList.add('fa-toggle-on');
		} else {
			window['boolDisplayLp'+index] = true;
			window['hidelp'+index] = 'Lp' + index;
			document.getElementById('graphlp'+index+'div').setAttribute('style', 'color: red;');
			window['graphlp'+index+'div'].classList.remove('fa-toggle-on');
			window['graphlp'+index+'div'].classList.add('fa-toggle-off');
		}

	}
	else if ( mqttmsg == 'openWB/graph/boolDisplayLpAll' ) {
		if ( mqttpayload == 1) {
			boolDisplayLpAll = false;
			hidelpa = 'foo';
			var element = document.getElementById('graphlpalldiv');
			graphlpalldiv.classList.remove('fa-toggle-off');
			graphlpalldiv.classList.add('fa-toggle-on');
			element.setAttribute('style', 'color: green;');
		} else {
			boolDisplayLpAll = true;
			hidelpa = 'LP Gesamt';
			var element = document.getElementById('graphlpalldiv');
			graphlpalldiv.classList.remove('fa-toggle-on');
			graphlpalldiv.classList.add('fa-toggle-off');
			element.setAttribute('style', 'color: red;');

		}

	}
	else if ( mqttmsg == 'openWB/graph/boolDisplaySpeicher' ) {
		if ( mqttpayload == 1) {
			boolDisplaySpeicher = false;
			hidespeicher = 'foo';
			document.getElementById('graphspeicherdiv').setAttribute('style', 'color: green;');
			graphspeicherdiv.classList.remove('fa-toggle-off');
			graphspeicherdiv.classList.add('fa-toggle-on');
		} else {
			hidespeicher = 'Speicherleistung';
			boolDisplaySpeicher = true;
			document.getElementById('graphspeicherdiv').setAttribute('style', 'color: red;');
			graphspeicherdiv.classList.remove('fa-toggle-on');
			graphspeicherdiv.classList.add('fa-toggle-off');

		}

	}
	else if ( mqttmsg == 'openWB/graph/boolDisplaySpeicherSoc' ) {
		if ( mqttpayload == 1) {
			hidespeichersoc = 'foo';
			boolDisplaySpeicherSoc = false;
			document.getElementById('graphspeichersocdiv').setAttribute('style', 'color: green;');
			graphspeichersocdiv.classList.remove('fa-toggle-off');
			graphspeichersocdiv.classList.add('fa-toggle-on');
		} else {
			hidespeichersoc = 'Speicher SoC';
			boolDisplaySpeicherSoc = true;
			document.getElementById('graphspeichersocdiv').setAttribute('style', 'color: red;');
			graphspeichersocdiv.classList.remove('fa-toggle-on');
			graphspeichersocdiv.classList.add('fa-toggle-off');

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
			document.getElementById('graphlp'+index+'socdiv').setAttribute('style', 'color: green;');
			window['graphlp'+index+'socdiv'].classList.remove('fa-toggle-off');
			window['graphlp'+index+'socdiv'].classList.add('fa-toggle-on');
		} else {
			$('#socenabledlp'+index).hide();
			window['boolDisplayLp'+index+'Soc'] = true;
			window['hidelp'+index+'soc'] = 'LP'+index+' SoC';
			document.getElementById('graphlp'+index+'socdiv').setAttribute('style', 'color: red;');
			window['graphlp'+index+'socdiv'].classList.remove('fa-toggle-on');
			window['graphlp'+index+'socdiv'].classList.add('fa-toggle-off');
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
			document.getElementById('graphload'+index+'div').setAttribute('style', 'color: green;');
			window['graphload'+index+'div'].classList.remove('fa-toggle-off');
			window['graphload'+index+'div'].classList.add('fa-toggle-on');
		} else {
			window['hideload'+index] = 'Verbraucher ' + index;
			window['boolDisplayLoad'+index] = true;
			document.getElementById('graphload'+index+'div').setAttribute('style', 'color: red;');
			window['graphload'+index+'div'].classList.remove('fa-toggle-on');
			window['graphload'+index+'div'].classList.add('fa-toggle-off');
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
