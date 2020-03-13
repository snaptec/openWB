var overallhausverbrauch = 0;
var hideload2;
var hidespeichersoc;
var hidelpa;
var hidelp1;
var hidelp2;
var hidelp3;
var hidelp4;
var hidelp5;
var hidelp6;
var hidelp7;
var hidelp8;
var atime;
var boolDisplayLp1 = false;
var boolDisplayLp2 = false;
var boolDisplayLp3 = false;
var boolDisplayLp4 = false;
var boolDisplayLp5 = false;
var boolDisplayLp6 = false;
var boolDisplayLp7 = false;
var boolDisplayLp8 = false;
var boolDisplayEvu = false;
var boolDisplayPv = false;
var boolDisplaySpeicheri = false;
var boolDisplaySpeichere = false;
var boolDisplayLp1Soc = false;
var boolDisplayLp2Soc = false;
var boolDisplayLoad1i = false;
var boolDisplayLoad1e = false;
var boolDisplayLoad2i = false;
var boolDisplayLoad2e = false;
var boolDisplayHouseConsumption = false;
var alp1 = new Array();
var alp2 = new Array();
var alp3 = new Array();
var alp4 = new Array();
var alp5 = new Array();
var alp6 = new Array();
var alp7 = new Array();
var alp8 = new Array();
var abezug = new Array();
var aeinspeisung = new Array();
var lp1soc;
var lp2soc;
var lp1enabled;
var lp2enabled;
var lp3enabled;
var initialread = 0;
var graphloaded = 0;
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
var boolDisplayEvu;
var boolDisplayPv;
var boolDisplayLegend = true;
var boolDisplayLiveGraph;
var datasend = 0;
var allValuesPresent = new Array(12).fill(0);  // flag if all data segments were received
var graphDataSegments = new Array(12).fill('');  // all data segments
var graphDataStr = '';
var overalllp1wh = new Array();
var overalllp2wh = new Array();

var apv = new Array();
var aspeicheri = new Array();
var aspeichere = new Array();
var aspeichersoc = new Array();
var asoc = new Array();
var asoc1 = new Array();
var averbraucher2i = new Array();
var averbraucher2e = new Array();
var averbraucher1i = new Array();
var averbraucher1e = new Array();
var ahausverbrauch = new Array();
var alpa = new Array();
var thevalues = [
	["openWB/system/MonthGraphData1", "#"],
	["openWB/system/MonthGraphData2", "#"],
	["openWB/system/MonthGraphData3", "#"],
	["openWB/system/MonthGraphData4", "#"],
	["openWB/system/MonthGraphData5", "#"],
	["openWB/system/MonthGraphData6", "#"],
	["openWB/system/MonthGraphData7", "#"],
	["openWB/system/MonthGraphData8", "#"],
	["openWB/system/MonthGraphData9", "#"],
	["openWB/system/MonthGraphData10", "#"],
	["openWB/system/MonthGraphData11", "#"],
	["openWB/system/MonthGraphData12", "#"],
]
var clientuid = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
var client = new Messaging.Client(location.host, 9001, clientuid);

function handlevar(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	if ( mqttmsg.match( /^openwb\/system\/monthgraphdata[1-9][0-9]*$/i ) ) {
		// matches to all messages containing "openwb/graph/monthgraphdata#"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d+/)[0];  // extract first match = number from mqttmsg
		if ( index < 13 && initialread == 0 && (mqttpayload != "empty")) {
			index -= 1;  // adjust to array starting at index 0
			graphDataStr += ('\n') + mqttpayload;
			graphDataSegments[index] = mqttpayload;
			allValuesPresent[index] = 1;
			if ( !allValuesPresent.includes(0) ) {
				// all segments received, so process data and display graph
				loadgraph();
			}
		}
	}
}

//Gets  called if the websocket/mqtt connection gets disconnected for any reason
client.onConnectionLost = function (responseObject) {
	client.connect(options);
}

//Gets called whenever you receive a message
client.onMessageArrived = function (message) {
	handlevar(message.destinationName, message.payloadString, thevalues[0], thevalues[1]);
}

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
		requestmonthgraph();
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

var url_string = window.location.href
var url = new URL(url_string);
var graphdate = url.searchParams.get("date");
if ( graphdate == null) {
	var today = new Date();
	var dd = String(today.getDate()).padStart(2, '0');
	var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
	var yyyy = today.getFullYear();
	graphdate = yyyy + mm;
} else {
	graphdate = graphdate.replace('-','');
}

function requestmonthgraph() {
	publish(graphdate, "openWB/set/graph/RequestMonthGraph");
}

function getCol(matrix, col){
	var column = [];
	for(var i=0; i<matrix.length; i++){
    	column.push(matrix[i][col]);
    }
    return column;
}

function convertdata(csvData,csvrow,pushdataset,hidevar,hidevalue,overall,hideline) {
	var oldcsvvar;
	var fincsvvar;
	var oldfincsvvar;
	var firstcsvvar;
	getCol(csvData, csvrow).forEach(function(csvvar, index){
		if (index > 0) {
			var fincsvvar=(csvvar - oldcsvvar);
			if (fincsvvar > 150000){
				fincsvvar=oldfincsvvar;
			}
			if (fincsvvar < -0){
				fincsvvar=oldfincsvvar;
	 		}
			if ( isNaN(fincsvvar)) {
				fincsvvar=0 }
			pushdataset.push(parseFloat((fincsvvar/1000).toFixed(2)));
			if ( csvrow == 4 || csvrow == 5) {
				window[overall+"wh"].push(csvvar/1000);
			}
	 	} else {
		 	firstcsvvar = csvvar;
			if ( csvrow == 4 || csvrow == 5 ) {
				window[overall+"wh"].push(csvvar/1000);
			}
	 	}
		oldfincsvvar=fincsvvar;
		if (csvvar > 100 ) {
			oldcsvvar = csvvar;
		}
	});
	window[overall] = ((oldcsvvar - firstcsvvar) / 1000).toFixed(2);
	if (window[overall] == 0 || isNaN(window[overall]) || window[overall] < 0) {
		window[hidevar] = hidevalue;
		window[hideline] = true;
	} else {
		window[hidevar] = 'foo';
		window[hideline] = false;
	}
	pushdataset.pop();
}

function loadgraph() {
	var selectedGraphMonth = parseInt(graphdate.slice(4, 6));  // last 2 digits is month
	graphDataStr = graphDataStr.replace(/^\s*[\n]/gm, '');
	// test if graphdata starts with a date followed by comma like 20191201,
	if ( !(/^\d{8},/.test(graphDataStr)) ) {
		$("#waitforgraphloadingdiv").html('<br>Keine Daten für diesen Zeitraum verfügbar');
		$('#canvasdiv').hide();
		return;
	}

	// build array for graph from data-string
	var csvData = new Array();
	var rawcsv = graphDataStr.split(/\r?\n|\r/);
	rawcsv.forEach((dataset) => {
		var datasetArray = dataset.split(',');
		var datasetDateStr = datasetArray[0];
		if ( /^\d{8}$/.test(datasetDateStr) ) {
			// test if first column is possible date and format correctly
			datasetDateStr = datasetDateStr.slice(0, 4) + "/" + datasetDateStr.slice(4, 6) + "/" + datasetDateStr.slice(6, 8);
			datasetDate = new Date(datasetDateStr);
			if ( datasetDateStr.length > 0 && datasetDate !== "Invalid Date" && !isNaN(datasetDate) ) {
				// date string is not undefined or empty and date string is a date and dataset is for selected month
				datasetArray[0] = datasetDateStr;
				for (var index=1; index<datasetArray.length; index++) {
					// make sure all fields are numbers
					if ( isNaN(datasetArray[index]) ) {
						datasetArray[index] = '0';
					}
				}
				csvData.push(datasetArray);
			}
		}
	});
	console.log(csvData);
	atime = getCol(csvData, 0);
	convertdata(csvData,'1',abezug,'hidebezug','Bezug','overallbezug','boolDisplayEvu');
	convertdata(csvData,'2',aeinspeisung,'hideeinspeisung','Einspeisung','overalleinspeisung');
	convertdata(csvData,'3',apv,'hidepv','PV','overallpv');
	convertdata(csvData,'4',alp1,'hidelp1','Lp1','overalllp1','boolDisplayLp1');
	convertdata(csvData,'5',alp2,'hidelp2','Lp2','overalllp2','boolDisplayLp2');
	convertdata(csvData,'6',alp3,'hidelp3','Lp3','overalllp3','boolDisplayLp3');
	convertdata(csvData,'7',alpa,'hidelpa','Lp Gesamt','overalllpgesamt');
	convertdata(csvData,'8',averbraucher1i,'hideload1i','Verbraucher 1 I','overallload1i','boolDisplayLoad1i');
	convertdata(csvData,'9',averbraucher1e,'hideload1e','Verbraucher 1 E','overallload1e','boolDisplayLoad1e');
	convertdata(csvData,'10',averbraucher2i,'hideload2i','Verbraucher 2 I','overallload2i','boolDisplayLoad2i');
	convertdata(csvData,'11',averbraucher2e,'hideload2e','Verbraucher 2 E','overallload2e','boolDisplayLoad2e');
	convertdata(csvData,'12',alp4,'hidelp4','Lp4','overalllp4','boolDisplayLp4');
	convertdata(csvData,'13',alp5,'hidelp5','Lp5','overalllp5','boolDisplayLp5');
	convertdata(csvData,'14',alp6,'hidelp6','Lp6','overalllp6','boolDisplayLp6');
	convertdata(csvData,'15',alp7,'hidelp7','Lp7','overalllp7','boolDisplayLp7');
	convertdata(csvData,'16',alp8,'hidelp8','Lp8','overalllp8','boolDisplayLp8');
	convertdata(csvData,'17',aspeicheri,'hidespeicheri','Speicher I','overallspeicheri','boolDisplaySpeicheri');
	convertdata(csvData,'18',aspeichere,'hidespeichere','Speicher E','overallspeichere','boolDisplaySpeichere');

	console.log(abezug);
	for (i = 0; i < abezug.length; i += 1) {
		var hausverbrauch = abezug[i] + apv[i] - alpa[i] + aspeichere[i] - aspeicheri[i] - aeinspeisung[i];
		if ( hausverbrauch >= 0) {
		    ahausverbrauch.push((hausverbrauch).toFixed(2));
		    overallhausverbrauch += hausverbrauch;
		} else {
			ahausverbrauch.push('0');
		}
	}
	overallhausverbrauch = (overallhausverbrauch).toFixed(2);

	var lineChartData = {
		labels: atime,
		datasets: [{
			label: 'Bezug ' + overallbezug + ' kWh',
			borderColor: "rgba(255, 0, 0, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 1,
			fill: true,
			data: abezug,
			hidden: boolDisplayEvu,
			yAxisID: 'y-axis-1',
			lineTension: 0.2
		} , {
			label: 'Einspeisung ' + overalleinspeisung + ' kWh',
			borderColor: "rgba(0, 255, 105, 0.9)",
			backgroundColor: "rgba(0, 255, 255, 0.3)",
			borderWidth: 2,
			fill: true,
			data: aeinspeisung,
			hidden: boolDisplayEvu,
			yAxisID: 'y-axis-1',
			lineTension: 0.2
		} , {
			label: 'PV ' + overallpv + ' kWh',
			borderColor: 'green',
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: true,
			hidden: boolDisplayPv,
			borderWidth: 1,
			data: apv,
			yAxisID: 'y-axis-1',
			lineTension: 0.2
		}  , {
			label: 'Speicher I ' + overallspeicheri + ' kWh',
			borderColor: 'orange',
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: true,
			borderWidth: 1,
			data: aspeicheri,
			hidden: boolDisplaySpeicheri,
			yAxisID: 'y-axis-1',
			lineTension: 0.2
		} , {
			label: 'Speicher E ' + overallspeichere + ' kWh',
			borderColor: 'orange',
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: true,
			borderWidth: 1,
			data: aspeichere,
			hidden: boolDisplaySpeichere,
			yAxisID: 'y-axis-1',
			lineTension: 0.2
		} , {
			label: 'Lp Gesamt ' + overalllpgesamt + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.1)",
			backgroundColor: "rgba(0, 0, 255, 0.1)",
			fill: true,
			borderWidth: 2,
			data: alpa,
			hidden: boolDisplayLpAll,
			yAxisID: 'y-axis-1',
			lineTension: 0.2
		} , {
			label: 'Lp1 ' + overalllp1 + ' kWh',
			borderColor: "rgba(0, 0, 255, 0.7)",
			backgroundColor: "rgba(0, 0, 255, 0.7)",
			borderWidth: 1,
			hidden: boolDisplayLp1,
			fill: false,
			data: alp1,
			yAxisID: 'y-axis-1',
			lineTension: 0.2
		} , {
			label: 'Lp2 ' + overalllp2 + ' kWh',
			borderColor: "rgba(50, 30, 105, 0.7)",
			backgroundColor: "rgba(50, 30, 105, 0.7)",
			borderWidth: 1,
			hidden: boolDisplayLp2,
			fill: false,
			data: alp2,
			yAxisID: 'y-axis-1',
			lineTension: 0.2
		} , {
			label: 'Lp3 ' + overalllp3 + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp3,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp3,
			lineTension: 0.2
		} , {
			label: 'Lp4 ' + overalllp4 + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			data: alp4,
			borderWidth: 2,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp4,
			lineTension: 0.2
		} , {
			label: 'Lp5 ' + overalllp5 + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp5,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp5,
			lineTension: 0.2
		} , {
			label: 'Lp6 ' + overalllp6 + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp6,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp6,
			lineTension: 0.2
		} , {
			label: 'Lp7 ' + overalllp7 + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp7,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp7,
			lineTension: 0.2
		} , {
			label: 'Lp8 ' + overalllp8 + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp8,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp8,
			lineTension: 0.2
		} , {
			label: 'Verbraucher 1 I ' + overallload1i + ' kWh',
			borderColor: "rgba(0, 150, 150, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			hidden: boolDisplayLoad1i,
			data: averbraucher1i,
			yAxisID: 'y-axis-1',
			lineTension: 0.2
		} , {
			label: 'Verbraucher 1 E ' + overallload1e + ' kWh',
			borderColor: "rgba(0, 150, 150, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			hidden: boolDisplayLoad1e,
			data: averbraucher1e,
			yAxisID: 'y-axis-1',
			lineTension: 0.2
		} , {
			label: 'Verbraucher 2 I ' + overallload2i + ' kWh',
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: averbraucher2i,
			hidden: boolDisplayLoad2i,
			yAxisID: 'y-axis-1',
			lineTension: 0.2
		} , {
			label: 'Verbraucher 2 E ' + overallload2e + ' kWh',
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: averbraucher2e,
			hidden: boolDisplayLoad2e,
			yAxisID: 'y-axis-1',
			lineTension: 0.2
		} , {
			label: 'Hausverbrauch ' + overallhausverbrauch + ' kWh',
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: ahausverbrauch,
			hidden: boolDisplayHouseConsumption,
			yAxisID: 'y-axis-1',
			lineTension: 0.2
		}]
	};
	var ctx = document.getElementById('canvas').getContext('2d');
	window.myLine = new Chart(ctx, {
		type: 'line',
		data: lineChartData,
		options: {
			tooltips: {
				enabled: true,
				mode: 'index',
				callbacks: {
					label: function(t, d) {
			   			if ( t.datasetIndex == 6 ) {
							var xLabel = d.datasets[t.datasetIndex].label + ", Zählerstand: " + overalllp1wh[t.index] + " kWh";
						} else if ( t.datasetIndex == 7) {
							var xLabel = d.datasets[t.datasetIndex].label + ", Zählerstand: " + overalllp2wh[t.index] + " kWh";
						} else {
							var xLabel = d.datasets[t.datasetIndex].label;
						}
			   			var yLabel = t.yLabel;
			   			return xLabel + ', Wert: ' + yLabel + 'kWh';
					}
				}
			},
			responsive: true,
			maintainAspectRatio: false,
			hover: {
				mode: 'null',
			},
			stacked: false,
			legend: {
				display: boolDisplayLegend,
				position: 'bottom',
				labels: {
			        filter: function(item, chart) {
						if ( item.text.includes(hidelpa) || item.text.includes(hideload2) || item.text.includes(hidelp1)|| item.text.includes(hidespeicheri)|| item.text.includes(hidespeichere) || item.text.includes(hidelp2)|| item.text.includes(hidelp3)|| item.text.includes(hidelp4)|| item.text.includes(hidelp5)|| item.text.includes(hidelp6)|| item.text.includes(hidelp7)|| item.text.includes(hidelp8)|| item.text.includes(hideload2i)|| item.text.includes(hideload2e)|| item.text.includes(hideload1i)|| item.text.includes(hideload1e)) {
							return false
						} else {
							return true
						}
					}
				}
			},
			title: {
				display: false
			},
			scales: {
				xAxes: [{
					type: 'category'
				}],
				yAxes: [{
					type: 'linear',
					display: true,
					position: 'left',
					id: 'y-axis-1',
					scaleLabel: {
						display: true,
						labelString: 'Energie [kWh]',
						// middle grey, opacy = 100% (visible)
						fontColor: "rgba(153, 153, 153, 1)"
					}
				}]
			}
		}
	});
	$('#canvas').click (function(evt) {
		// on click of datapoint, jump to day view
		var activePoint = myLine.getElementAtEvent(event);
		if (activePoint.length > 0) {
			var clickedElementindex = activePoint[0]._index;
			var jumpToDate = myLine.data.labels[clickedElementindex];
			window.location.href = "daily.php?date=" + jumpToDate;
		}
	});

	initialread = 1;
	$('#waitforgraphloadingdiv').hide();
}

function showhidedataset(thedataset) {
	if ( window[thedataset] == true ) {
		publish("1","openWB/graph/"+thedataset);
	} else if ( window[thedataset] == false ) {
		publish("0","openWB/graph/"+thedataset);
	} else {
		publish("1","openWB/graph/"+thedataset);
	}
}

function showhidelegend(thedataset) {
	if ( window[thedataset] == true ) {
		publish("0","openWB/graph/"+thedataset);
	} else if ( window[thedataset] == false ) {
		publish("1","openWB/graph/"+thedataset);
	} else {
		publish("0","openWB/graph/"+thedataset);
	}
}

function showhide(thedataset) {
	if ( window[thedataset] == 0 ) {
		publish("1","openWB/graph/"+thedataset);
	} else if ( window[thedataset] == 1 ) {
		publish("0","openWB/graph/"+thedataset);
	} else {
		publish("1","openWB/graph/"+thedataset);
	}
}
