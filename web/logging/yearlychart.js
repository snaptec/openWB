/**
 * reads monthly logging data and displays graph
 *
 * @author: Kevin Wieland, Michael Ortenstein
 *
 * fills data-gaps in timeline with respective values and hides empty data from being displayed
 */

const DATACOLUMNCOUNT = 28;  // count of native data columns received by mqtt (including timestamp-column)
const LPCOLUMNS = [4, 5, 6, 12, 13, 14, 15, 16];  // column-indexes of LP-entries in csvData-array

var initialread = 0;
var boolDisplayLegend = true;
var allValuesPresent = new Array(12).fill(0);  // flag if all data segments were received
var graphDataSegments = new Array(12).fill('');  // all data segments
var csvData = [];  // holds data as 2d-array after calculating values from graphDataStr
var totalValues = [''];  // holds yearly totals for every data-column from csvData, starting with empty value at index 0 (equals timestamp index at csvData)
var lpCounterValues = [];  // holds all counter values transformed to kWh
var d1name = 'Device 1';
var d2name = 'Device 2';
var d3name = 'Device 3';
var d4name = 'Device 4';
var d5name = 'Device 5';
var d6name = 'Device 6';
var d7name = 'Device 7';
var d8name = 'Device 8';
var d9name = 'Device 9';
var d10name = 'Device 10';
var thevalues = [
	["openWB/system/YearGraphData1", "#"],
	["openWB/system/YearGraphData2", "#"],
	["openWB/system/YearGraphData3", "#"],
	["openWB/system/YearGraphData4", "#"],
	["openWB/system/YearGraphData5", "#"],
	["openWB/system/YearGraphData6", "#"],
	["openWB/system/YearGraphData7", "#"],
	["openWB/system/YearGraphData8", "#"],
	["openWB/system/YearGraphData9", "#"],
	["openWB/system/YearGraphData10", "#"],
	["openWB/system/YearGraphData11", "#"],
	["openWB/system/YearGraphData12", "#"],
	["openWB/config/get/SmartHome/Devices/1/device_name", "#"],
	["openWB/config/get/SmartHome/Devices/2/device_name", "#"],
	["openWB/config/get/SmartHome/Devices/3/device_name", "#"],
	["openWB/config/get/SmartHome/Devices/4/device_name", "#"],
	["openWB/config/get/SmartHome/Devices/5/device_name", "#"],
	["openWB/config/get/SmartHome/Devices/6/device_name", "#"],
	["openWB/config/get/SmartHome/Devices/7/device_name", "#"],
	["openWB/config/get/SmartHome/Devices/8/device_name", "#"],
	["openWB/config/get/SmartHome/Devices/9/device_name", "#"],
	["openWB/config/get/SmartHome/Devices/10/device_name", "#"],
]
var monthName = new Array(13).fill(''); // + 1 for direkt access with month
var url_string = window.location.href
var url = new URL(url_string);
var graphDate = url.searchParams.get("date");
if ( graphDate == null) {
	var today = new Date();
	var dd = String(today.getDate()).padStart(2, '0');
	var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
	var yyyy = today.getFullYear();
	graphDate = String(yyyy);
}
var graphYear = Number(graphDate);
var graphNextYear = Number(graphDate) + 1;
// day 0 is the last day in the previous month
// Date-object expects month January = 0, so the var month actually contains number of next month
// therefore no correction to month is needed by getting the # of days in selected month
var monthsInYear = 12;

var clientuid = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
var client = new Messaging.Client(location.hostname, 9001, clientuid);

function handlevar(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	if ( mqttmsg.match( /^openWB\/config\/get\/SmartHome\/Devices\/[1-9][0-9]*\/device_name$/i ) ) {
		var index = mqttmsg.match(/\d+/)[0];
		window['d'+index+'name']=mqttpayload;
	}
	if ( mqttmsg.match( /^openwb\/system\/yeargraphdata[1-9][0-9]*$/i ) ) {
		// matches to all messages containing "openwb/graph/monthgraphdata#"
		// where # is an integer > 0
		// search is case insensitive
		var index = mqttmsg.match(/\d+/)[0];  // extract first match = number from mqttmsg
		if ( index < 13 && initialread == 0 && (mqttpayload != "empty")) {
			index -= 1;  // adjust to array starting at index 0
			graphDataSegments[index] = mqttpayload;
			allValuesPresent[index] = 1;
			if ( !allValuesPresent.includes(0) ) {
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
		requestyeargraph();
	},
	//Gets Called if the connection could not be established
	onFailure: function (message) {
		client.connect(options);
	}
};

client.connect(options);

//Creates a new Messaging.Message Object and sends it
var publish = function (payload, topic) {
	var message = new Messaging.Message(payload);
	message.destinationName = topic;
	message.qos = 2;
	message.retained = true;
	client.send(message);
}

function requestyeargraph() {
	publish(graphDate, "openWB/set/graph/RequestYearGraph");
}

function getCol(matrix, col) {
	var column = [];
	for( var i = 0; i < matrix.length; i++) {
		column.push(matrix[i][col]);
	}
	return column;
}

function buildCsvDataArray() {
	// build array for graph from data-segments
	var rawcsv = [];
	// first put lines containing data from received segments into raw-data-array
	graphDataSegments.forEach((segment, i) => {
		var trimmedSegment = segment.trim();
		var splitSegment = trimmedSegment.split(/\r?\n|\r/);
		splitSegment.forEach((splitSegmentRow) => {
		var trimmedSplitSegmentRow = splitSegmentRow.trim();
		if ( trimmedSplitSegmentRow != '' ) {
			rawcsv.push(trimmedSplitSegmentRow);
			}
		});
	});

	// rawdata date format is YYYYmmdd, so use this for comparison
	// for calculation of daily values the first day of next year must be included in dataset
	rawcsv.forEach((rawDataRowStr) => {
		if ( /^\d{8},$/.test(rawDataRowStr.substring(0, 9)) ) {
			// first 9 chars is possible date followed by comma (format YYYYmmdd,)
			// so check if it is valid for selected month
			var dataRowDateStr = rawDataRowStr.substring(0, 8);
			var dataRowDayStr = dataRowDateStr.substr(6, 2);
			var dataRowMonthStr = dataRowDateStr.substr(4, 2);
			var dataRowYearStr = dataRowDateStr.substr(0, 4);
			var dataRowDate = new Date(dataRowYearStr + '/' + dataRowMonthStr + '/' + dataRowDayStr);  // to avoid parsed dates like 20190245 convert string to date and back
			var totalcounter = 0;
			if ( dataRowDate !== "Invalid Date" && !isNaN(dataRowDate) ) {
				// date is a valid date
				var dataRowyyyy = dataRowDate.getFullYear();
				//console.log("buildCsvDataArray" + dataRowDateStr + "Index" + csvData.length );
				if ( dataRowyyyy == graphYear ||  dataRowyyyy == graphNextYear  ) {
					// date falls within selected year or next year
					dataRowDateStr = dataRowYearStr + '/' + dataRowMonthStr + '/' + dataRowDayStr;
					var dataRow = rawDataRowStr.split(',');  // now split row into csv-array
					dataRow[0] = dataRowDateStr;  // replace first element with date in new format
					// now format the array
					var columnCountDifference = DATACOLUMNCOUNT - dataRow.length;
					if ( columnCountDifference > 0 ) {
						// not enough columns in dataset, maybe due to older logfile, so add zero-fields
						while ( columnCountDifference > 0 ) {
							dataRow.push(0);
							columnCountDifference--;
						}
					} else if ( columnCountDifference < 0 ) {
						// too many columns in dataset, maybe due to read-errors of logfiles, so delete fields
						while ( columnCountDifference < 0 ) {
							dataRow.pop();
							columnCountDifference++;
						}
					}
					dataRow.forEach((value, columnIndex, theArray) => {
						// make sure all fields (except index 0 = timestamp) are numbers with two decimal places
						if ( columnIndex > 0 ) {
							if ( isNaN(value) ) {
								theArray[columnIndex] = 0;
							} else {
								theArray[columnIndex] = parseFloat(value);
								totalcounter = totalcounter + parseFloat(value); 
							}
						}
					});
					if (totalcounter > 0) {
						csvData.push(dataRow);
					}
				}
			}
		}
	});
}

function fillLpCounterValuesArray() {
	// fills an array with same size as csvData but holding counter values of all lp in kWh
	// these values will be displayed at the graph tooltips
	csvData.forEach((dataRow, rowIndex) => {
		// process every day
		var lpCounterValuesRow = [];  // row to hold the counter values of the day in kWh
		if ( rowIndex < (csvData.length -1) ) {  // skipt last row of csvData-array, it is just needed for calculation
			dataRow.forEach((value, columnIndex) => {
				if ( LPCOLUMNS.includes(columnIndex) ) {
					// current column is a LP-counter-value
					lpCounterValuesRow.push(', Zählerstand: ' + (value/1000).toFixed(2) + ' kWh');
				} else {
					// no LP-counter-value so nothing to display
					lpCounterValuesRow.push('');
				}
			});
			lpCounterValues.push(lpCounterValuesRow);
		}
	});
}

function calcMonthlyValues() {
	// values in logfile are stored as counter values
	// calculates daily values by substracting two consecutive counter values from data array
	// stores results in same array
	for ( var column = 1; column < csvData[0].length; column++ ) {
		// process every column after date-column
		var dataColumn = getCol(csvData, column);
		if ( dataColumn.some(value => value > 0) ) {
			// don't process column if all values are zero
			var prevValue = dataColumn[0];
			var dailyValue = 0;
			var prevDailyValue = 0;
			dataColumn.forEach((value, row) => {
				if ( row > 0 ) {  // start calculation with second row
					dailyValue=(value - prevValue);
					if ( dailyValue > 4650000 || dailyValue < 0 ) { // daily Wert für spikes mal 31
						// avoid large spikes or negative values
						dailyValue=prevDailyValue;
					}
					csvData[row-1][column] = dailyValue/1000;
				}
				prevDailyValue = dailyValue;
				if ( value > 100 ) {
					prevValue = value;
				}
			});
		}
	}
}

function formatDateColumn() {
	// formats the first csvdata-column so date is displayed at labels like 'Jan'
	for ( var rowIndex = 0; rowIndex < csvData.length; rowIndex++ ) {
		var theDate = new Date(csvData[rowIndex][0]);
		var monthstr = theDate.toLocaleDateString('de-DE', { month: 'short'});
		var month = String(theDate.getMonth() + 1).padStart(2, '0'); 
		var theDatestr = monthstr;
		monthName[(theDate.getMonth() + 1)] = monthstr;
		csvData[rowIndex][0] = theDatestr;
	}
}

function lpCount() {
	// returns amount of LP containing other values than zero
	var count = 0;
	for ( var i = 0; i < LPCOLUMNS.length; i++ ) {
		var dataColumn = getCol(csvData, LPCOLUMNS[i]);
		if ( dataColumn.every( value => value !== 0 ) ) {
			count++;
		}
	}
	return count;
}

function loadgraph() {
	buildCsvDataArray();
	console.log('CsvDataLength: '+csvData.length);
	if ( csvData.length < 2 ) {
		// not enough data rows: nothing to display
		$("#waitforgraphloadingdiv").html('<br>Nicht genügend Daten für diesen Zeitraum verfügbar.');
		$('#canvasdiv').hide();
		return;
	}
	if ( csvData.length > ((monthsInYear*2) + 1) ) {
		// too many data-rows have been transmitted, data may be corrupt
		$("#waitforgraphloadingdiv").html('<br>Fehler bei der Übertragung der Daten für dieses Jahr, bitte erneut versuchen.');
		$('#canvasdiv').hide();
		return;
	}

	// sort array by date
	csvData.sort((date1, date2) => date1[0].localeCompare(date2[0]));

	// for ( var rowIndex = 0; rowIndex < csvData.length; rowIndex++ ) {
	// 	console.log("nach Sort " + rowIndex  + " Datum " + csvData[rowIndex][0]  + " Bezug " + csvData[rowIndex][1] );
	// }

	fillLpCounterValuesArray();  // fills an array containg all counter values for every lp
	calcMonthlyValues();  // sum up values for totals
	// for ( var rowIndex = 0; rowIndex < csvData.length; rowIndex++ ) {
	// 	console.log("nach Sum " + rowIndex  + " Datum " + csvData[rowIndex][0]  + " Bezug " + csvData[rowIndex][1] );
	// }
	csvData.pop();  // discard last row in csvData-array, it was just needed for calculation of daily values from original counter-values

	formatDateColumn();  // format date for labels

	for ( var rowIndex = 0; rowIndex < csvData.length; rowIndex++ ) {
		// calculate daily 'Hausverbrauch [kWh]' from row-values
		// and extend csvData by these values
		// tägl. Hausverbrauch = Bezug - Einspeisung + PV - alle LP + Speicherentladung - Speicherladung ;
		var homeConsumption = csvData[rowIndex][1] - csvData[rowIndex][2] + csvData[rowIndex][3] - csvData[rowIndex][7] - csvData[rowIndex][8] + csvData[rowIndex][9] - csvData[rowIndex][10] + csvData[rowIndex][11] + csvData[rowIndex][18] - csvData[rowIndex][17] - csvData[rowIndex][19] - csvData[rowIndex][20] - csvData[rowIndex][21] - csvData[rowIndex][22] - csvData[rowIndex][23] - csvData[rowIndex][24] - csvData[rowIndex][25] - csvData[rowIndex][26] - csvData[rowIndex][27];
		if ( homeConsumption >= 0) {
			csvData[rowIndex].push(homeConsumption);
		} else {
			csvData[rowIndex].push(0);
		}
	}

	for ( var columnIndex = 1; columnIndex < csvData[0].length; columnIndex++ ) {
		// summarize all columns for monthly totals
		var dataColumn = getCol(csvData, columnIndex);
		var total = 0;
		dataColumn.forEach((value) => {
			total+=value;
		});
		totalValues.push(total);
	}

	//build array containing all available data from csvData
	var lineChartDataSets = [
		'', // first entry with index 0 is empty and later removed just needed to sync array index with respective csvData index
		{
			label: 'Bezug ' + totalValues[1].toFixed(2) + ' kWh',
			borderColor: "rgba(255, 0, 0, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 1,
			fill: true,
			data: getCol(csvData, 1),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 1)  // custom added field, holds counter values or empty string
		} , {
			label: 'Einspeisung ' + totalValues[2].toFixed(2) + ' kWh',
			borderColor: "rgba(0, 255, 105, 0.9)",
			backgroundColor: "rgba(0, 255, 255, 0.3)",
			borderWidth: 2,
			fill: true,
			data: getCol(csvData, 2),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 2)  // custom added field, holds counter values or empty string
		} , {
			label: 'PV ' + totalValues[3].toFixed(2) + ' kWh',
			borderColor: 'green',
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: true,
			borderWidth: 1,
			data: getCol(csvData, 3),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 3)  // custom added field, holds counter values or empty string
		} , {
			label: 'Lp1 ' + totalValues[4].toFixed(2) + ' kWh',
			borderColor: "rgba(0, 0, 255, 0.7)",
			backgroundColor: "rgba(0, 0, 255, 0.7)",
			borderWidth: 1,
			fill: false,
			data: getCol(csvData, 4),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 4)  // custom added field, holds counter values or empty string
		} , {
			label: 'Lp2 ' + totalValues[5].toFixed(2) + ' kWh',
			borderColor: "rgba(50, 30, 105, 0.7)",
			backgroundColor: "rgba(50, 30, 105, 0.7)",
			borderWidth: 1,
			fill: false,
			data: getCol(csvData, 5),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 5)  // custom added field, holds counter values or empty string
		} , {
			label: 'Lp3 ' + totalValues[6].toFixed(2) + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 6),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 6)  // custom added field, holds counter values or empty string
		} , {
			label: 'Lp Gesamt ' + totalValues[7].toFixed(2) + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.1)",
			backgroundColor: "rgba(0, 0, 255, 0.1)",
			fill: true,
			borderWidth: 2,
			data: getCol(csvData, 7),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 7)  // custom added field, holds counter values or empty string
		} , {
			label: 'Verbraucher 1 in ' + totalValues[8].toFixed(2) + ' kWh',
			borderColor: "rgba(0, 150, 150, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 8),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 8)  // custom added field, holds counter values or empty string
		} , {
			label: 'Verbraucher 1 out ' + totalValues[9].toFixed(2) + ' kWh',
			borderColor: "rgba(0, 150, 150, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 9),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 9)  // custom added field, holds counter values or empty string
		} , {
			label: 'Verbraucher 2 in ' + totalValues[10].toFixed(2) + ' kWh',
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 10),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 10)  // custom added field, holds counter values or empty string
		} , {
			label: 'Verbraucher 2 out ' + totalValues[11].toFixed(2) + ' kWh',
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 11),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 11)  // custom added field, holds counter values or empty string
		} , {
			label: 'Lp4 ' + totalValues[12].toFixed(2) + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			data: getCol(csvData, 12),
			borderWidth: 2,
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 12)  // custom added field, holds counter values or empty string
		} , {
			label: 'Lp5 ' + totalValues[13].toFixed(2) + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 13),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 13)  // custom added field, holds counter values or empty string
		} , {
			label: 'Lp6 ' + totalValues[14].toFixed(2) + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 14),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 14)  // custom added field, holds counter values or empty string
		} , {
			label: 'Lp7 ' + totalValues[15].toFixed(2) + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 15),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 15)  // custom added field, holds counter values or empty string
		} , {
			label: 'Lp8 ' + totalValues[16].toFixed(2) + ' kWh',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 16),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 16)  // custom added field, holds counter values or empty string
		} , {
			label: 'Speicherladung ' + totalValues[17].toFixed(2) + ' kWh',
			borderColor: 'orange',
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: true,
			borderWidth: 1,
			data: getCol(csvData, 17),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 17)  // custom added field, holds counter values or empty string
		} , {
			label: 'Speicherentladung ' + totalValues[18].toFixed(2) + ' kWh',
			borderColor: 'orange',
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: true,
			borderWidth: 1,
			data: getCol(csvData, 18),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 18)  // custom added field, holds counter values or empty string
		} , {
			label: d1name + ' Import ' + totalValues[19].toFixed(2) + ' kWh',
			borderColor:"rgba(200, 150, 200, 0.7)",
			backgroundColor: "rgba(200, 150, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 19),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 19)  // custom added field, holds counter values or empty string
		} , {
			label: d2name + ' Import ' + totalValues[20].toFixed(2) + ' kWh',
			borderColor: "rgba(200, 100, 200, 0.7)",
			backgroundColor: "rgba(200, 100, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 20),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 20)  // custom added field, holds counter values or empty string
		} , {
			label: d3name + ' Import ' + totalValues[21].toFixed(2) + ' kWh',
			borderColor: "rgba(200, 50, 200, 0.7)",
			backgroundColor: "rgba(200, 50, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 21),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 21)  // custom added field, holds counter values or empty string
		} , {
			label: d4name + ' Import ' + totalValues[22].toFixed(2) + ' kWh',
			borderColor: "rgba(200, 0, 200, 0.7)",
			backgroundColor: "rgba(200, 0, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 22),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 22)  // custom added field, holds counter values or empty string
		} , {
			label: d5name + ' Import ' + totalValues[23].toFixed(2) + ' kWh',
			borderColor: "rgba(150, 200, 200, 0.7)",
			backgroundColor: "rgba(150, 200, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 23),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 23)  // custom added field, holds counter values or empty string
		} , {
			label: d6name + ' Import ' + totalValues[24].toFixed(2) + ' kWh',
			borderColor: "rgba(100, 200, 200, 0.7)",
			backgroundColor: "rgba(100, 200, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 24),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 24)  // custom added field, holds counter values or empty string
		} , {
			label: d7name + ' Import ' + totalValues[25].toFixed(2) + ' kWh',
			borderColor: "rgba(50, 200, 200, 0.7)",
			backgroundColor: "rgba(50, 200, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 25),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 25)  // custom added field, holds counter values or empty string
		} , {
			label: d8name + ' Import ' + totalValues[26].toFixed(2) + ' kWh',
			borderColor: "rgba(0, 200, 200, 0.7)",
			backgroundColor: "rgba(0, 200, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 26),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 26)  // custom added field, holds counter values or empty string
		} , {
			label: d9name + ' Import ' + totalValues[27].toFixed(2) + ' kWh',
			borderColor: "rgba(200, 200, 200, 0.7)",
			backgroundColor: "rgba(200, 200, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 27),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 27)  // custom added field, holds counter values or empty string
		} , {
			label: 'Hausverbrauch ' + totalValues[28].toFixed(2) + ' kWh',
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 28),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			toolTipData: getCol(lpCounterValues, 0)  // custom added field, always empty string at index 0
		}
	];

	// check if other LP than #1 has data !== 0 and if not, set all LP Gesamt to 0 so it will not be displayed
	if ( lpCount() < 2 ) {
		for ( var rowIndex = 0; rowIndex < csvData.length; rowIndex++ ) {
			csvData[rowIndex][7] = 0;
		}
	}

	// now delete all graph lines containing only zero values
	// by deleting the respective field in the linChartDataSets-array
	for ( var column = 1; column < csvData[0].length; column++ ) {
		// process all data-columns except the date
		// column in csvData is represented by column-entry in linChartData
		var dataColumn = getCol(csvData, column);
		if ( dataColumn.every( value => value === 0 ) ) {
			lineChartDataSets[column] = '';  // mark entry for removal of line if data is all zero
		}
	}
	// now remove lines marked by '' for removal
	lineChartDataSets = lineChartDataSets.filter((element) => element !== '');

	var ctx = document.getElementById('canvas').getContext('2d');
	window.myLine = new Chart(ctx, {
		type: 'line',
		data: {
			labels: getCol(csvData, 0),
			datasets: lineChartDataSets
		},
		options: {
			tooltips: {
				enabled: true,
				mode: 'index',
				callbacks: {
					title: function(dataPoint, graphData) {
						// return complete data as title
						return dataPoint[0].xLabel + ' ' + graphYear;
					},
					label: function(dataPoint, graphData) {
						// get only the name of the respective dataline since total value is visible at legend
						var xLabel = graphData.datasets[dataPoint.datasetIndex].label.split(' ', 1)[0];
						// get value for the tooltip-day
						var yLabel = ', Monatswert: ' + dataPoint.yLabel.toFixed(2) + ' kWh';
						// get counter value for the day (or empty string if not apliccable)
						var counter = graphData.datasets[dataPoint.datasetIndex].toolTipData[dataPoint.index];
						return xLabel + counter + yLabel;
					}
				}
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
					// middle grey, opacy = 100% (visible)
					fontColor: "rgba(153, 153, 153, 1)",
				}
			},
			title: {
				display: false
			},
			scales: {
				xAxes: [{
					type: 'category',
					ticks: {
						//source: 'data',
						fontColor: "rgba(153, 153, 153, 1)"  // middle grey, opacy = 100% (visible)
					}
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
					},
					gridLines: {
						// light grey, opacy = 100% (visible)
						color: "rgba(204, 204, 204, 1)",
					},
					ticks: {
						// middle grey, opacy = 100% (visible)
						fontColor: "rgba(153, 153, 153, 1)"
					},
				}]
			}
		}
	});
	$('#canvas').click (function(evt) {
		// on click of datapoint, jump to day view
		var activePoint = myLine.getElementAtEvent(event);
		if ( activePoint.length > 0) {
			var clickedElementindex = activePoint[0]._index;
			var monthstr = myLine.data.labels[clickedElementindex];  // get complete label of day clicked
			// and format the string as needed to call monthly graph: YYYYmm
			monthstr = monthstr.substring(0,3); // get month in short description
			var month = monthName.indexOf(monthstr);
			var jumpToDate = String(graphYear) + '-' + String(month).padStart(2, '0');  // month with leading zero
			window.location.href = "logging/monthly.php?date=" + jumpToDate;
	 	}
	});

	initialread = 1;
	$('#waitforgraphloadingdiv').hide();
}
