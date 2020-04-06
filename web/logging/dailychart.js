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
var graphdata;
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
var boolDisplaySpeicher = false;
var boolDisplayLp1Soc = false;
var boolDisplayLp2Soc = false;
var alp1 = [];
var alp2 = [];
var alp3 = [];
var alp4 = [];
var alp5 = [];
var alp6 = [];
var alp7 = [];
var alp8 = [];
var abezug = [];
var aeinspeisung = [];
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
var boolDisplaySpeicher;
var boolDisplayEvu;
var boolDisplayPv;
var boolDisplayLegend = true;
var boolDisplayLiveGraph;
var datasend = 0;
var allValuesPresent = new Array(12).fill(0);  // flag if all data segments were received
var graphDataSegments = new Array(12).fill('');  // all data segments

var apv = [];
var aspeicheri = [];
var aspeichere = [];
var aspeichersoc = [];
var asoc = [];
var asoc1 = [];
var averbraucher2i = [];
var averbraucher2e = [];
var averbraucher1i = [];
var averbraucher1e = [];
var ahausverbrauch = [];
var alpa = [];
var thevalues = [
	["openWB/system/DayGraphData1", "#"],
	["openWB/system/DayGraphData2", "#"],
	["openWB/system/DayGraphData3", "#"],
	["openWB/system/DayGraphData4", "#"],
	["openWB/system/DayGraphData5", "#"],
	["openWB/system/DayGraphData6", "#"],
	["openWB/system/DayGraphData7", "#"],
	["openWB/system/DayGraphData8", "#"],
	["openWB/system/DayGraphData9", "#"],
	["openWB/system/DayGraphData10", "#"],
	["openWB/system/DayGraphData11", "#"],
	["openWB/system/DayGraphData12", "#"],
];
var clientuid = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
var client = new Messaging.Client(location.host, 9001, clientuid);

function handlevar(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	if ( mqttmsg.match( /^openwb\/system\/daygraphdata[1-9][0-9]*$/i ) ) {
		// matches to all messages containing "openwb/graph/daygraphdata#"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d+/)[0];  // extract first match = number from mqttmsg
		if ( index < 13 && initialread == 0 && (mqttpayload != "empty")) {
			index -= 1;  // adjust to array starting at index 0
			graphDataSegments[index] = mqttpayload;
			allValuesPresent[index] = 1;
			putgraphtogether();
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
		requestdaygraph();
	},
	//Gets Called if the connection could not be established
	onFailure: function (message) {
		client.connect(options);
	}
}

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
	graphdate = yyyy + mm + dd;
} else {
	graphdate = graphdate.replace('-','').replace('-','');
}

function requestdaygraph() {
	publish(graphdate, "openWB/set/graph/RequestDayGraph");
}

function putgraphtogether() {
	if ( !allValuesPresent.includes(0) ) {
		var alldata = graphDataSegments[0] + "\n" + graphDataSegments[1] + "\n" + graphDataSegments[2] + "\n" + graphDataSegments[3] + "\n" + graphDataSegments[4] + "\n" + graphDataSegments[5] + "\n" + graphDataSegments[6] + "\n" + graphDataSegments[7] + "\n" + graphDataSegments[8] + "\n" + graphDataSegments[9] + "\n" + graphDataSegments[10] + "\n" + graphDataSegments[11];
		graphdata = alldata.replace(/^\s*[\n]/gm, '');
		//graphdata = graphDataSegments.join().replace(/^\s*[\n]/gm, '');
		initialread = 1;

		// test if graphdata starts with a timestamp followed by comma like 0745,
		if ( !(/^\d{4},/.test(graphdata)) ) {
			$("#waitforgraphloadingdiv").html('<br>Keine Daten für diesen Zeitraum verfügbar');
			$("#canvasdiv").hide();
		} else {
			formdata(graphdata);
			$("#waitforgraphloadingdiv").hide();
		}
	}
}

function getCol(matrix, col){
	var column = [];
	for(var i=0; i<matrix.length; i++){
        column.push(matrix[i][col]);
    }
    return column;
}

function formdata(graphdata){
	var csvData = [];
	var rawcsv = graphdata.split(/\r?\n|\r/);
	rawcsv.forEach((dataset) => {
		csvData.push(dataset.split(','));
	});
	var splittime = [];
	getCol(csvData, 0).forEach(function(zeit){
		splittime.push(zeit.substring(0, zeit.length -2)+':'+zeit.substring(2));
	});
	splittime.shift();
	atime = splittime.slice(0,-1);
	convertdata(csvData,'1',abezug,'hidebezug','Bezug','overallbezug');
	convertdata(csvData,'2',aeinspeisung,'hideeinspeisung','Einspeisung','overalleinspeisung');
	convertdata(csvData,'3',apv,'hidepv','PV','overallpv');
	convertdata(csvData,'8',aspeicheri,'hidespeicheri','Speicher I','overallspeicheri');
	convertdata(csvData,'9',aspeichere,'hidespeichere','Speicher E','overallspeichere');
	convertdata(csvData,'7',alpa,'hidelpa','Lp Gesamt','overalllpgesamt');
	convertdata(csvData,'4',alp1,'hidelp1','Lp1','overalllp1');
	convertdata(csvData,'5',alp2,'hidelp2','Lp2','overalllp2');
	convertdata(csvData,'6',alp3,'hidelp3','Lp3','overalllp3');
	convertdata(csvData,'15',alp4,'hidelp4','Lp4','overalllp4');
	convertdata(csvData,'16',alp5,'hidelp5','Lp5','overalllp5');
	convertdata(csvData,'17',alp6,'hidelp6','Lp6','overalllp6');
	convertdata(csvData,'18',alp7,'hidelp7','Lp7','overalllp7');
	convertdata(csvData,'19',alp8,'hidelp8','Lp8','overalllp8');
	convertdata(csvData,'10',averbraucher1i,'hideload1i','Verbraucher 1 I','overallload1i');
	convertdata(csvData,'11',averbraucher1e,'hideload1e','Verbraucher 1 E','overallload1e');
	convertdata(csvData,'12',averbraucher2i,'hideload2i','Verbraucher 2 I','overallload2i');
	convertdata(csvData,'13',averbraucher2e,'hideload2e','Verbraucher 2 E','overallload2e');
	convertsoc(csvData,'21',asoc,'hidesoc','SoC Lp 1','overalllp1soc');
	convertsoc(csvData,'22',asoc1,'hidesoc1','SoC Lp 2','overalllp2soc');
	convertsoc(csvData,'20',aspeichersoc,'hidespeichersoc','Speicher SoC','overallspeichersoc');
	for (i = 0; i < abezug.length; i += 1) {

		var hausverbrauch = abezug[i] + apv[i] - alpa[i] + aspeichere[i] - aspeicheri[i] - aeinspeisung[i];
		
		if ( hausverbrauch >= 0) {
		    ahausverbrauch.push(hausverbrauch);
		    overallhausverbrauch += hausverbrauch;
		} else {
			ahausverbrauch.push('0');
		}
	}
	overallhausverbrauch = (overallhausverbrauch / 12 / 1000).toFixed(2);
	ahausverbrauch.pop();
	loadgraph();
}

function convertdata(csvData,csvrow,pushdataset,hidevar,hidevalue,overall) {
	var counter = 0;
	var oldcsvvar;
	var fincsvvar;
	var oldfincsvvar;
	var firstcsvvar;
	getCol(csvData, csvrow).forEach(function(csvvar){
		if (counter > 0) {
			var fincsvvar=(csvvar - oldcsvvar) * 12;
			if (fincsvvar > 150000){
				fincsvvar=oldfincsvvar;
			}
			if (fincsvvar < -0){
				fincsvvar=oldfincsvvar;
	 		}
			if (!isNaN(fincsvvar)) {
				pushdataset.push(fincsvvar);
			} else {
				fincsvvar=0
				pushdataset.push(fincsvvar);
			
			}
	 	} else {
			if (!isNaN(csvvar)) {
		 		firstcsvvar = csvvar;
			} else {
				firstcsvvar = 0;
			}

	 	}
		oldfincsvvar=fincsvvar;
		counter++;
		if (csvvar > 100 ) {
			oldcsvvar = csvvar;
		}
	});
	window[overall] = ((oldcsvvar - firstcsvvar) / 1000).toFixed(2);
	if (isNaN(window[overall])) {
	//if (window[overall] == 0 || window[overall] == "NaN" || window[overall] < 0) {
		window[hidevar] = hidevalue;
	} else {
		window[hidevar] = 'foo';
	}
}

function convertsoc(csvData,csvrow,pushdataset,hidevar,hidevalue,overall) {
	var counter = 0;
	var oldcsvvar;
	var fincsvvar;
	var oldfincsvvar;
	var firstcsvvar;
	var vis=0;
	getCol(csvData, csvrow).forEach(function(csvvar){
		if (counter > 0) {
	 		pushdataset.push(csvvar);
	 	} else {
		 	firstcsvvar = csvvar;
	 	}
		oldfincsvvar=fincsvvar;
		if ( csvvar != 0 && typeof csvvar !== 'undefined'){
			vis=1;
		}
		counter++;
	});
	//window[overall] = ((oldcsvvar - firstcsvvar) / 1000).toFixed(2);
	if ( vis == 1 ){
		window[hidevar] = 'foo';
	} else {
		window[hidevar] = hidevalue;
	}
}

function loadgraph() {
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
			yAxisID: 'y-axis-1'
		} , {
			label: 'Einspeisung ' + overalleinspeisung + ' kWh',
			borderColor: "rgba(0, 255, 105, 0.7)",
			backgroundColor: "rgba(0, 255, 255, 0.3)",
			borderWidth: 1,
			fill: true,
			data: aeinspeisung,
			hidden: boolDisplayEvu,
			yAxisID: 'y-axis-1'
		} , {
			label: 'PV ' + overallpv + ' kWh',
			borderColor: 'green',
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: true,
			hidden: boolDisplayPv,
			borderWidth: 1,
			data: apv,
			yAxisID: 'y-axis-1'
		}  , {
			label: 'Speicher I ' + overallspeicheri + ' kWh',
			borderColor: 'orange',
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: true,
			borderWidth: 1,
			data: aspeicheri,
			hidden: boolDisplaySpeicher,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Speicher E ' + overallspeichere + ' kWh',
			borderColor: 'orange',
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: true,
			borderWidth: 1,
			data: aspeichere,
			hidden: boolDisplaySpeicher,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Speicher SoC',
			borderColor: 'orange',
			backgroundColor: "rgba(200, 255, 13, 0.5)",
			borderDash: [10,5],
			hidden: boolDisplaySpeicherSoc,
			fill: false,
			borderWidth: 1,
			data: aspeichersoc,
			yAxisID: 'y-axis-2'
		} , {
			label: 'Lp Gesamt ' + overalllpgesamt + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.1)",
			backgroundColor: "rgba(0, 0, 255, 0.1)",
			fill: true,
			borderWidth: 2,
			data: alpa,
			hidden: boolDisplayLpAll,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Lp1 ' + overalllp1 + ' kWh',
			borderColor: "rgba(0, 0, 255, 0.7)",
			backgroundColor: "rgba(0, 0, 255, 0.7)",
			borderWidth: 1,
			hidden: boolDisplayLp1,
			fill: false,
			data: alp1,
			yAxisID: 'y-axis-1'
		} , {
			label: 'SoC Lp 1',
			borderColor: "rgba(0, 0, 255, 0.5)",
			borderDash: [10,5],
			borderWidth: 2,
			hidden: boolDisplayLp1Soc,
			fill: false,
			data: asoc,
			yAxisID: 'y-axis-2'
		} , {
			label: 'Lp2 ' + overalllp2 + ' kWh',
			borderColor: "rgba(50, 30, 105, 0.7)",
			backgroundColor: "rgba(50, 30, 105, 0.7)",
			borderWidth: 1,
			hidden: boolDisplayLp2,
			fill: false,
			data: alp2,
			yAxisID: 'y-axis-1'
		} , {
			label: 'SoC Lp 2',
			borderColor: "rgba(50, 50, 55, 0.5)",
			borderDash: [10,5],
			fill: false,
			borderWidth: 2,
			hidden: boolDisplayLp2Soc,
			data: asoc1,
			yAxisID: 'y-axis-2'
		} , {
			label: 'Lp3 ' + overalllp3 + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp3,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp3
		} , {
			label: 'Lp4 ' + overalllp4 + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			data: alp4,
			borderWidth: 2,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp4
		} , {
			label: 'Lp5 ' + overalllp5 + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp5,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp5
		} , {
			label: 'Lp6 ' + overalllp6 + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp6,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp6
		} , {
			label: 'Lp7 ' + overalllp7 + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp7,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp7
		} , {
			label: 'Lp8 ' + overalllp8 + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp8,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp8
		} , {
			label: 'Verbraucher 1 I ' + overallload1i + ' kWh',
			borderColor: "rgba(0, 150, 150, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			hidden: boolDisplayLoad1,
			data: averbraucher1i,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Verbraucher 1 E ' + overallload1e + ' kWh',
			borderColor: "rgba(0, 150, 150, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			hidden: boolDisplayLoad1,
			data: averbraucher1e,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Verbraucher 2 I ' + overallload2i + ' kWh',
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: averbraucher2i,
			hidden: boolDisplayLoad2,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Verbraucher 2 E ' + overallload2e + ' kWh',
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: averbraucher2e,
			hidden: boolDisplayLoad2,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Hausverbrauch ' + overallhausverbrauch + ' kWh',
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: ahausverbrauch,
			hidden: boolDisplayLoad2,
			yAxisID: 'y-axis-1'
		}]
	}
	var ctx = document.getElementById('canvas').getContext('2d');
	window.myLine = new Chart(ctx, {
		type: 'line',
		data: lineChartData,
		options: {
			tooltips: {
				enabled: false
			},
			 plugins: {
				    zoom: {
					// Container for pan options
					pan: {
					    // Boolean to enable panning
					    enabled: true,

					    // Panning directions. Remove the appropriate direction to disable 
					    // Eg. 'y' would only allow panning in the y direction
					    mode: 'x',
					    rangeMin: {
						    x: null
					    },
					    rangeMax: {
						    x: null
					    },
					    speed: 1000
					},

					// Container for zoom options
					zoom: {
					    // Boolean to enable zooming
					    enabled: true,

					    // Zooming directions. Remove the appropriate direction to disable 
					    // Eg. 'y' would only allow zooming in the y direction
					    mode: 'x',

					    sensitivity: 0.01
					   
					}
				    }
			 },
			elements: {
				point: {
					radius: 0
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
						if ( item.text.includes(hidelpa) || item.text.includes(hideload2) || item.text.includes(hidespeicheri) || item.text.includes(hidespeichere) || item.text.includes(hidespeichersoc) || item.text.includes(hidesoc) || item.text.includes(hidesoc1) || item.text.includes(hidelp1) || item.text.includes(hidelp2)|| item.text.includes(hidelp3)|| item.text.includes(hidelp4)|| item.text.includes(hidelp5)|| item.text.includes(hidelp6)|| item.text.includes(hidelp7)|| item.text.includes(hidelp8)|| item.text.includes(hideload2i)|| item.text.includes(hideload2e)|| item.text.includes(hideload1i)|| item.text.includes(hideload1e)) {
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
					type: 'category',
				}],
				yAxes: [{
					type: 'linear',
					display: true,
					position: 'left',
					id: 'y-axis-1',
					scaleLabel: {
						display: true,
						labelString: 'Leistung [W]',
						// middle grey, opacy = 100% (visible)
						fontColor: "rgba(153, 153, 153, 1)"
					}
				} , {
					type: 'linear',
					display: true,
					gridLines: {
						color: "rgba(0, 0, 0, 0)",
					},
					ticks: {
						min: 1,
						suggestedMax: 100
					},
					position: 'right',
					id: 'y-axis-2',
					scaleLabel: {
						display: true,
						labelString: 'SoC [%]',
						// middle grey, opacy = 100% (visible)
						fontColor: "rgba(153, 153, 153, 1)"
					}
				}]
			}
		}
	});
	initialread = 1;
	$('#waitforgraphloadingdiv').hide();
}

function checkgraphload(){
	if ( graphloaded == 1) {
       	myLine.destroy();
		loadgraph();
	} else {
		if (( boolDisplayHouseConsumption == true  ||  boolDisplayHouseConsumption == false) && (boolDisplayLoad1 == true || boolDisplayLoad1 == false ) && (boolDisplayLp1Soc == true || boolDisplayLp1Soc == false ) && (boolDisplayLp2Soc == true || boolDisplayLp2Soc == false ) && (boolDisplayLoad2 == true || boolDisplayLoad2 == false ) && (boolDisplayLp1 == true || boolDisplayLp1 == false ) && (boolDisplayLp2 == true || boolDisplayLp2 == false ) && (boolDisplayLp3 == true || boolDisplayLp3 == false ) && (boolDisplayLp4 == true || boolDisplayLp4 == false ) && (boolDisplayLp5 == true || boolDisplayLp5 == false ) && (boolDisplayLp6 == true || boolDisplayLp6 == false ) && (boolDisplayLp7 == true || boolDisplayLp7 == false ) && (boolDisplayLp8 == true || boolDisplayLp8 == false ) && (boolDisplayLpAll == true || boolDisplayLpAll == false ) && (boolDisplaySpeicherSoc == true || boolDisplaySpeicherSoc == false ) && (boolDisplaySpeicher == true || boolDisplaySpeicher == false ) && (boolDisplayEvu == true || boolDisplayEvu == false ) && (boolDisplayPv == true || boolDisplayPv == false ) && (boolDisplayLegend == true || boolDisplayLegend == false ))  {
			if ( initialread != 0 ) {
				if ( graphloaded == 0) {
					loadgraph();
					graphloaded += 1;
				} else {
			       	myLine.destroy();
					loadgraph();
				}
		 	}
		}
	}
};

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
