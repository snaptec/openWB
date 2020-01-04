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
var all1 = 0;
var all2 = 0;
var all3 = 0;
var all4 = 0;
var all5 = 0;
var all6 = 0;
var all7 = 0;
var all8 = 0;
var all9 = 0;
var all10 = 0;
var all11 = 0;
var all12 = 0;
var all1p; 
var all2p; 
var all3p; 
var all4p; 
var all5p; 
var all6p; 
var all7p; 
var all8p;
var all9p; 
var all10p; 
var all11p; 
var all12p;

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
	if ( mqttmsg == "openWB/system/MonthGraphData1" ) {
		if (initialread == 0 && (mqttpayload != "empty")) {
			all1p = mqttpayload;
			all1 = 1;
		putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/system/MonthGraphData1" ) {
		if (initialread == 0 && (mqttpayload != "empty")) {
			all1p = mqttpayload;
			all1 = 1;
		putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/system/MonthGraphData2" ) {
		if (initialread == 0 && (mqttpayload != "empty")) {
			all2p = mqttpayload;
			all2 = 1;
		putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/system/MonthGraphData3" ) {
		if (initialread == 0 && (mqttpayload != "empty")) {
			all3p = mqttpayload;
			all3 = 1;
		putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/system/MonthGraphData4" ) {
		if (initialread == 0 && (mqttpayload != "empty")) {
			all4p = mqttpayload;
			all4 = 1;
		putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/system/MonthGraphData5" ) {
		if (initialread == 0 && (mqttpayload != "empty")) {
			all5p = mqttpayload;
			all5 = 1;
		putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/system/MonthGraphData6" ) {
		if (initialread == 0 && (mqttpayload != "empty")) {
			all6p = mqttpayload;
			all6 = 1;
		putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/system/MonthGraphData7" ) {
		if (initialread == 0 && (mqttpayload != "empty")) {
			all7p = mqttpayload;
			all7 = 1;
		putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/system/MonthGraphData8" ) {
		if (initialread == 0 && (mqttpayload != "empty")) {
			all8p = mqttpayload;
			all8 = 1;
		putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/system/MonthGraphData9" ) {
		if (initialread == 0 && (mqttpayload != "empty")) {
			all9p = mqttpayload;
			all9 = 1;
		putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/system/MonthGraphData10" ) {
		if (initialread == 0 && (mqttpayload != "empty")) {
			all10p = mqttpayload;
			all10 = 1;
		putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/system/MonthGraphData11" ) {
		if (initialread == 0 && (mqttpayload != "empty")) {
			all11p = mqttpayload;
			all11 = 1;
		putgraphtogether();
		}
	}
	else if ( mqttmsg == "openWB/system/MonthGraphData12" ) {
		if (initialread == 0 && (mqttpayload != "empty")) {
			all12p = mqttpayload;
			all12 = 1;
		putgraphtogether();
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
var options = {
	timeout: 5,
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
function requestdaygraph() {
	        publish(graphdate, "openWB/set/graph/RequestMonthGraph");
}

function putgraphtogether() {
	if ( (all1 == 1) && (all2 == 1) && (all3 == 1) && (all4 == 1) && (all5 == 1) && (all6 == 1) && (all7 == 1) && (all8 == 1) && (all9 == 1) && (all10 == 1) && (all11 == 1) && (all12 == 1) ){
		var alldata = all1p + "\n" + all2p + "\n" + all3p + "\n" + all4p + "\n" + all5p + "\n" + all6p + "\n" + all7p + "\n" + all8p + "\n" + all9p + "\n" + all10p + "\n" + all11p + "\n" + all12p;
		graphdata = alldata.replace(/^\s*[\n]/gm, '');
		initialread = 1 ;
		//checkgraphload();
		if ( graphdata.length < 5 ) {
			$("#loadlivegraph").html("Keine Daten für diesen Zeitraum verfügbar");
			$("#dailygraphvis").hide();
		} else {
		formdata(graphdata);
		$("#loadlivegraph").hide();
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
	graphdata = graphdata.replace(/^\s*[\n]/gm, '');
	var csvData = new Array();
	var rawcsv = graphdata.split(/\r?\n|\r/);
	for (var i = 0; i < rawcsv.length; i++) {
		csvData.push(rawcsv[i].split(',')); 
        } 
	var splittime = new Array();
	getCol(csvData, 0).forEach(function(zeit){
		splittime.push(zeit.substring(0, zeit.length-4)+'-'+zeit.substring(4, zeit.length-2)+'-'+zeit.substring(6));
	})
	splittime.pop();
	splittime.pop();
	for (i = splittime.length; i < 28 ; i += 1) {
		splittime.push("");
	}
	atime = splittime;
	
	convertdata(csvData,'1',abezug,'hidebezug','Bezug','overallbezug','boolDisplayEvu');
	convertdata(csvData,'2',aeinspeisung,'hideeinspeisung','Einspeisung','overalleinspeisung');
	convertdata(csvData,'3',apv,'hidepv','PV','overallpv');
	convertdata(csvData,'17',aspeicheri,'hidespeicheri','Speicher I','overallspeicheri','boolDisplaySpeicheri');
	convertdata(csvData,'18',aspeichere,'hidespeichere','Speicher E','overallspeichere','boolDisplaySpeichere');
	convertdata(csvData,'7',alpa,'hidelpa','Lp Gesamt','overalllpgesamt');
	convertdata(csvData,'4',alp1,'hidelp1','Lp1','overalllp1','boolDisplayLp1');
	convertdata(csvData,'5',alp2,'hidelp2','Lp2','overalllp2','boolDisplayLp2');
	convertdata(csvData,'6',alp3,'hidelp3','Lp3','overalllp3','boolDisplayLp3');
	convertdata(csvData,'12',alp4,'hidelp4','Lp4','overalllp4','boolDisplayLp4');
	convertdata(csvData,'13',alp5,'hidelp5','Lp5','overalllp5','boolDisplayLp5');
	convertdata(csvData,'14',alp6,'hidelp6','Lp6','overalllp6','boolDisplayLp6');
	convertdata(csvData,'15',alp7,'hidelp7','Lp7','overalllp7','boolDisplayLp7');
	convertdata(csvData,'16',alp8,'hidelp8','Lp8','overalllp8','boolDisplayLp8');
	convertdata(csvData,'8',averbraucher1i,'hideload1i','Verbraucher 1 I','overallload1i','boolDisplayLoad1i');
	convertdata(csvData,'9',averbraucher1e,'hideload1e','Verbraucher 1 E','overallload1e','boolDisplayLoad1e');
	convertdata(csvData,'10',averbraucher2i,'hideload2i','Verbraucher 2 I','overallload2i','boolDisplayLoad2i');
	convertdata(csvData,'11',averbraucher2e,'hideload2e','Verbraucher 2 E','overallload2e','boolDisplayLoad2e');
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
	loadgraph();
}

function convertdata(csvData,csvrow,pushdataset,hidevar,hidevalue,overall,hideline) {
	var counter = 0;
	var oldcsvvar;
	var fincsvvar;
	var oldfincsvvar;
	var firstcsvvar;
	getCol(csvData, csvrow).forEach(function(csvvar){
		if (counter > 0) {
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
	 	} else {
		 	firstcsvvar = csvvar;
	 	}
		oldfincsvvar=fincsvvar;
		counter++;
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
		yAxisID: 'y-axis-1',
	} , {
		label: 'Einspeisung ' + overalleinspeisung + ' kWh',
		borderColor: "rgba(0, 255, 105, 0.9)",
		backgroundColor: "rgba(0, 255, 255, 0.3)",
		borderWidth: 2,
		fill: true,
		data: aeinspeisung,
		hidden: boolDisplayEvu,
		yAxisID: 'y-axis-1',
	} , {
		label: 'PV ' + overallpv + ' kWh',
		borderColor: 'green',
		backgroundColor: "rgba(10, 255, 13, 0.3)",
		fill: true,
		hidden: boolDisplayPv,
		borderWidth: 1,
		data: apv,
		yAxisID: 'y-axis-1',
	}  , {
		label: 'Speicher I ' + overallspeicheri + ' kWh',
		borderColor: 'orange',
		backgroundColor: "rgba(200, 255, 13, 0.3)",
		fill: true,
		borderWidth: 1,
		data: aspeicheri,
		hidden: boolDisplaySpeicheri,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Speicher E ' + overallspeichere + ' kWh',
		borderColor: 'orange',
		backgroundColor: "rgba(255, 155, 13, 0.3)",
		fill: true,
		borderWidth: 1,
		data: aspeichere,
		hidden: boolDisplaySpeichere,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Lp Gesamt ' + overalllpgesamt + ' kWh',
		borderColor: "rgba(50, 50, 55, 0.1)",
		backgroundColor: "rgba(0, 0, 255, 0.1)",
		fill: true,
		borderWidth: 2,
		data: alpa,
		hidden: boolDisplayLpAll,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Lp1 ' + overalllp1 + ' kWh',
		borderColor: "rgba(0, 0, 255, 0.7)",
		backgroundColor: "rgba(0, 0, 255, 0.7)",
		borderWidth: 1,
		hidden: boolDisplayLp1,
		fill: false,
		data: alp1,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Lp2 ' + overalllp2 + ' kWh',
		borderColor: "rgba(50, 30, 105, 0.7)",
		backgroundColor: "rgba(50, 30, 105, 0.7)",
		borderWidth: 1,
		hidden: boolDisplayLp2,
		fill: false,
		data: alp2,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Lp3 ' + overalllp3 + ' kWh',
		borderColor: "rgba(50, 50, 55, 0.7)",
		backgroundColor: 'blue',
		fill: false,
		borderWidth: 2,
		data: alp3,
		yAxisID: 'y-axis-1',
		hidden: boolDisplayLp3,
	} , {
		label: 'Lp4 ' + overalllp4 + ' kWh',
		borderColor: "rgba(50, 50, 55, 0.7)",
		backgroundColor: 'blue',
		fill: false,
		data: alp4,
		borderWidth: 2,
		yAxisID: 'y-axis-1',
		hidden: boolDisplayLp4,
	} , {
		label: 'Lp5 ' + overalllp5 + ' kWh',
		borderColor: "rgba(50, 50, 55, 0.7)",
		backgroundColor: 'blue',
		fill: false,
		borderWidth: 2,
		data: alp5,
		yAxisID: 'y-axis-1',
		hidden: boolDisplayLp5,
	} , {
		label: 'Lp6 ' + overalllp6 + ' kWh',
		borderColor: "rgba(50, 50, 55, 0.7)",
		backgroundColor: 'blue',
		fill: false,
		borderWidth: 2,
		data: alp6,
		yAxisID: 'y-axis-1',
		hidden: boolDisplayLp6,
	} , {
		label: 'Lp7 ' + overalllp7 + ' kWh',
		borderColor: "rgba(50, 50, 55, 0.7)",
		backgroundColor: 'blue',
		fill: false,
		borderWidth: 2,
		data: alp7,
		yAxisID: 'y-axis-1',
		hidden: boolDisplayLp7,
	} , {
		label: 'Lp8 ' + overalllp8 + ' kWh',
		borderColor: "rgba(50, 50, 55, 0.7)",
		backgroundColor: 'blue',
		fill: false,
		borderWidth: 2,
		data: alp8,
		yAxisID: 'y-axis-1',
		hidden: boolDisplayLp8,
	} , {
		label: 'Verbraucher 1 I ' + overallload1i + ' kWh',
		borderColor: "rgba(0, 150, 150, 0.7)",
		backgroundColor: "rgba(200, 255, 13, 0.3)",
		fill: false,
		borderWidth: 2,
		hidden: boolDisplayLoad1i,
		data: averbraucher1i,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Verbraucher 1 E ' + overallload1e + ' kWh',
		borderColor: "rgba(0, 150, 150, 0.7)",
		backgroundColor: "rgba(200, 255, 13, 0.3)",
		fill: false,
		borderWidth: 2,
		hidden: boolDisplayLoad1e,
		data: averbraucher1e,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Verbraucher 2 I ' + overallload2i + ' kWh',
		borderColor: "rgba(150, 150, 0, 0.7)",
		backgroundColor: "rgba(200, 255, 13, 0.3)",
		fill: false,
		borderWidth: 2,
		data: averbraucher2i,
		hidden: boolDisplayLoad2i,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Verbraucher 2 E ' + overallload2e + ' kWh',
		borderColor: "rgba(150, 150, 0, 0.7)",
		backgroundColor: "rgba(200, 255, 13, 0.3)",
		fill: false,
		borderWidth: 2,
		data: averbraucher2e,
		hidden: boolDisplayLoad2e,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Hausverbrauch ' + overallhausverbrauch + ' kWh',
		borderColor: "rgba(150, 150, 0, 0.7)",
		backgroundColor: "rgba(200, 255, 13, 0.3)",
		fill: false,
		borderWidth: 2,
		data: ahausverbrauch,
		hidden: boolDisplayHouseConsumption,
		yAxisID: 'y-axis-1',
	}]
};
	var ctx = document.getElementById('canvas').getContext('2d');
	window.myLine = Chart.Line(ctx, {
		data: lineChartData,
		options: {
			tooltips: {
				enabled: true,
				mode: 'index'
			},
			elements: {
				point: {
					radius: 4
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
				labels: {
				        filter: function(item, chart) {
						if ( item.text.includes(hidelpa) || item.text.includes(hideload2) || item.text.includes(hidelp1)|| item.text.includes(hidespeicheri)|| item.text.includes(hidespeichere) || item.text.includes(hidelp2)|| item.text.includes(hidelp3)|| item.text.includes(hidelp4)|| item.text.includes(hidelp5)|| item.text.includes(hidelp6)|| item.text.includes(hidelp7)|| item.text.includes(hidelp8)|| item.text.includes(hideload2i)|| item.text.includes(hideload2e)|| item.text.includes(hideload1i)|| item.text.includes(hideload1e)) { return false } else { return true }	
				                }
				        }
			},
			title: {
				display: false
			},
			scales: {
				xAxes: [{
				        type: 'category',
				}, ],
				yAxes: [{
					type: 'linear',
					display: true,
					position: 'left',
					id: 'y-axis-1',
				 
					  }],
			
			
			},
			/*
			pan: {
			enabled: true,
			mode: 'x',
			},
			zoom: {
				enabled: true,
				drag: true,
				mode: 'x',

			},
			*/
		}
	});
document.getElementById("canvas").onclick = function(evt) {
	var activePoint = myLine.getElementAtEvent(event);
	if (activePoint.length > 0) {
		var clickedDatasetIndex = activePoint[0]._datasetIndex;
	        var clickedElementindex = activePoint[0]._index;
	        var label = myLine.data.labels[clickedElementindex];
	        var value = myLine.data.datasets[clickedDatasetIndex].data[clickedElementindex];     
	        var newloc = "/openWB/web/logging/daily.php?date=" + label;            
		window.location.href = newloc;
	 }
};


initialread = 1;
$('#loadlivegraph').hide();
};			
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

