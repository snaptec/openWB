/**
 * reads monthly logging data and displays graph
 *
 * @author: Kevin Wieland, Michael Ortenstein
 *
 * fills data-gaps in timeline with respective values and hides empty data from being displayed
 */

const DATACOLUMNCOUNT = 59;  // count of native data columns received by mqtt (including timestamp-column)
const LPCOLUMNS = [4, 5, 6, 12, 13, 14, 15, 16];  // column-indexes of LP-entries in csvData-array

var initialread = 0;
var indexb = 0;
var indexc = 0;
var boolDisplayLegend = true;
var allValuesPresent = new Array(12).fill(0);  // flag if all data segments were received
var graphDataSegmentsb= new Array(12).fill('');  // all amount data segments
var graphDataSegments = new Array(12).fill('');  // all counter data segments
var headerSegments = new Array(1).fill('');  // all header description segments
var headerDataSegmentsb = new Array(1).fill('');  // all header amounts data segments (1)
var headerDataSegments = new Array(1).fill('');  // all header counter data segments (1)
var csvData = [];  // holds data as 2d-array after calculating values from graphDataStr
var csvDatab = [];  // holds data as 2d-array after calculating values from graphDataStr

var totalValues = [''];  // holds monthly totals for every data-column from csvData, starting with empty value at index 0 (equals timestamp index at csvData)
var totalHidden = [''];  // holds true or false for each legend item
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
	["openWB/system/MonthGraphDatan1", "#"],
	["openWB/system/MonthGraphDatan2", "#"],
	["openWB/system/MonthGraphDatan3", "#"],
	["openWB/system/MonthGraphDatan4", "#"],
	["openWB/system/MonthGraphDatan5", "#"],
	["openWB/system/MonthGraphDatan6", "#"],
	["openWB/system/MonthGraphDatan7", "#"],
	["openWB/system/MonthGraphDatan8", "#"],
	["openWB/system/MonthGraphDatan9", "#"],
	["openWB/system/MonthGraphDatan10", "#"],
	["openWB/system/MonthGraphDatan11", "#"],
	["openWB/system/MonthGraphDatan12", "#"],
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

var url_string = window.location.href
if (url_string.includes('v1.php') == 1) {
	var callv1 = 1;
	var callv2 = 0;
} else {
	var callv1 = 0;
	var callv2 = 1;
}
//console.log("url_string",url_string,'callv1',callv1,'callv2',callv2);

var url = new URL(url_string);
var graphDate = url.searchParams.get("date");
if ( graphDate == null) {
	var today = new Date();
	var dd = String(today.getDate()).padStart(2, '0');
	var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
	var yyyy = today.getFullYear();
	graphDate = yyyy + mm;
} else {
	graphDate = graphDate.replace('-','');
}
var graphYear = graphDate.substr(0, 4);
var graphMonth = graphDate.substring(4);
// day 0 is the last day in the previous month
// Date-object expects month January = 0, so the var month actually contains number of next month
// therefore no correction to month is needed by getting the # of days in selected month
var daysInMonth = new Date(graphYear, graphMonth, 0).getDate();
var clientuid = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
var client = new Messaging.Client(location.hostname, 9001, clientuid);

function handlevar(mqttmsg, mqttpayload, mqtttopic, htmldiv) {
	if ( mqttmsg.match( /^openWB\/config\/get\/SmartHome\/Devices\/[1-9][0-9]*\/device_name$/i ) ) {
		var index = mqttmsg.match(/\d+/)[0];
		window['d'+index+'name']=mqttpayload;
	}
	if ( mqttmsg.match( /^openwb\/system\/monthgraphdatan[1-9][0-9]*$/i ) ) {
		// matches to all messages containing "openwb/graph/monthgraphdata#"
		// where # is an integer > 0
		// search is case insensitive
		// file 1 -> headerst
		// file 2 -> Zaehler summe
		// file 3 -> beträge summe
		// file 4 -> Zaehler detail
		// file 5 -> beträge detail
		// file 6 -> beträge detail
		// file 7 -> Zaehler detail
		var index = mqttmsg.match(/\d+/)[0];  // extract first match = number from mqttmsg

		if (index == 1 && initialread == 0 && (mqttpayload != "empty")) {
			headerSegments [0] = mqttpayload;
		}
		if (index == 2 && initialread == 0 && (mqttpayload != "empty")) {
			headerDataSegments [0] = mqttpayload;
		}
		if (index == 3 && initialread == 0 && (mqttpayload != "empty")) {
			headerDataSegmentsb [0] = mqttpayload;
		}
		if ((index == 4 || index == 7) && initialread == 0 && (mqttpayload != "empty")) {
			graphDataSegments [indexc] = mqttpayload;
			indexc = indexc + 1
		}
		if ((index == 5 || index == 6) && initialread == 0 && (mqttpayload != "empty")) {
			graphDataSegmentsb [indexb] = mqttpayload;
			indexb = indexb + 1
		}
		if ( index < 13 && initialread == 0 && (mqttpayload != "empty")) {
			index -= 1;  // adjust to array starting at index 0
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
		requestmonthgraph();
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

function requestmonthgraph() {
	publish(graphDate, "openWB/set/graph/RequestMonthGraphv1");
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
	var firstDayOfThisMonthDate = new Date(graphYear + '/' + graphMonth + '/01');
	var firstDayOfNextMonthDate = new Date(firstDayOfThisMonthDate.setMonth(firstDayOfThisMonthDate.getMonth() + 1));
	var nextMonth = String(firstDayOfNextMonthDate.getMonth() + 1).padStart(2, '0'); //January is 0!
	var nextMonthYear = firstDayOfNextMonthDate.getFullYear();
	// for calculation of daily values the first day of next month may be included in dataset
	var firstDayOfNextMonthStr = nextMonthYear + nextMonth + '01';
	rawcsv.forEach((rawDataRowStr) => {
		if ( /^\d{8},$/.test(rawDataRowStr.substring(0, 9)) ) {
			// first 9 chars is possible date followed by comma (format YYYYmmdd,)
			// so check if it is valid for selected month
			var dataRowDateStr = rawDataRowStr.substring(0, 8);
			var dataRowDayStr = dataRowDateStr.substr(6, 2);
			var dataRowMonthStr = dataRowDateStr.substr(4, 2);
			var dataRowYearStr = dataRowDateStr.substr(0, 4);
			var dataRowDate = new Date(dataRowYearStr + '/' + dataRowMonthStr + '/' + dataRowDayStr);  // to avoid parsed dates like 20190245 convert string to date and back
			if ( dataRowDate !== "Invalid Date" && !isNaN(dataRowDate) ) {
				// date is a valid date
				var isSelectedMonth = (dataRowDateStr.substr(0, 6) == graphDate);
				var isFirstDayOfNextMonth = (dataRowDateStr == firstDayOfNextMonthStr);
        if ( dataRowDateStr.substr(0, 6) == graphDate || dataRowDateStr == firstDayOfNextMonthStr ) {
					// date falls within selected month or is first day of next month
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
							}
						}
					});
					csvData.push(dataRow);
				}
			}
		}
	});
}

function buildCsvDataArrayb() {
	// build array for graph from data-segments
	var rawcsv = [];
	// first put lines containing data from received segments into raw-data-array
	graphDataSegmentsb.forEach((segment, i) => {
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
	var firstDayOfThisMonthDate = new Date(graphYear + '/' + graphMonth + '/01');
	var firstDayOfNextMonthDate = new Date(firstDayOfThisMonthDate.setMonth(firstDayOfThisMonthDate.getMonth() + 1));
	var nextMonth = String(firstDayOfNextMonthDate.getMonth() + 1).padStart(2, '0'); //January is 0!
	var nextMonthYear = firstDayOfNextMonthDate.getFullYear();
	// for calculation of daily values the first day of next month may be included in dataset
	var firstDayOfNextMonthStr = nextMonthYear + nextMonth + '01';
	rawcsv.forEach((rawDataRowStr) => {
		if ( /^\d{8},$/.test(rawDataRowStr.substring(0, 9)) ) {
			// first 9 chars is possible date followed by comma (format YYYYmmdd,)
			// so check if it is valid for selected month
			var dataRowDateStr = rawDataRowStr.substring(0, 8);
			var dataRowDayStr = dataRowDateStr.substr(6, 2);
			var dataRowMonthStr = dataRowDateStr.substr(4, 2);
			var dataRowYearStr = dataRowDateStr.substr(0, 4);
			var dataRowDate = new Date(dataRowYearStr + '/' + dataRowMonthStr + '/' + dataRowDayStr);  // to avoid parsed dates like 20190245 convert string to date and back
			if ( dataRowDate !== "Invalid Date" && !isNaN(dataRowDate) ) {
				// date is a valid date
				var isSelectedMonth = (dataRowDateStr.substr(0, 6) == graphDate);
				var isFirstDayOfNextMonth = (dataRowDateStr == firstDayOfNextMonthStr);
				if ( dataRowDateStr.substr(0, 6) == graphDate || dataRowDateStr == firstDayOfNextMonthStr ) {
				//if ( dataRowDateStr.substr(0, 6) == graphDate ) {
					// date falls within selected month or is first day of next month
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
							}
						}
					});
					csvDatab.push(dataRow);
				}
			}
		}
	});
}
function fillDataGaps() {
	// fills data-gaps between logged dates for selected month with respective values
	const oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
	for ( var rowIndex = 1; rowIndex < csvData.length; rowIndex++ ) {
		var firstDateStr = csvData[rowIndex-1][0];
		var firstDate = new Date(firstDateStr + ' 00:00:00');
		var secondDateStr = csvData[rowIndex][0];
		var secondDate = new Date(secondDateStr + ' 00:00:00');
		var diffDays = Math.round(Math.abs((firstDate.getTime() - secondDate.getTime()) / (oneDay)));
		if ( diffDays > 1 ) {
			// difference between 2 datasets is more than 1 day
			var dd = String(firstDate.getDate() + 1).padStart(2, '0');  // day to insert
			var newDatasetDateStr = firstDateStr.substr(0, 8) + dd;
			var newDataSet = [newDatasetDateStr];  // insert new date in new array-row
			var newDataSetb = [newDatasetDateStr];  // insert new date in new array-row
			for ( var colIndex = 1; colIndex < csvData[rowIndex-1].length; colIndex++ ) {
				newDataSet.push(csvData[rowIndex-1][colIndex]);  // copy data from older date
				newDataSetb.push(0);
			}
			csvData.splice(rowIndex, 0, newDataSet);  // insert row
			csvDatab.splice(rowIndex, 0, newDataSetb);  // insert row
		}
	}
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

function calcDailyValuesNew() {
	for ( var column = 1; column < csvData[0].length; column++ ) {
		// process every column after date-column
		var dataColumn = getCol(csvData, column);
		dataColumn.forEach((value, row) => {
		if ( row > 0 ) {  // copy data only
			csvData[row-1][column] = csvDatab[row-1][column];
		}
		});
	}
}

function completeMonth() {
	// makes sure graph-length is always all days of the selected month
	// no matter what day contains first or last logged data
	// need to fill csvData and the lpCounterValues-array
	var day;
	var dayAtIndex;
	var newDayStr;
	var newDatasetDateStr;
	var dateStrPart = graphYear + '/' + graphMonth + '/';
	for ( var dayIndex = 0; dayIndex < daysInMonth; dayIndex++) {
		// iterate over all days of the selected months
		day = dayIndex + 1;
		if ( typeof csvData[dayIndex] === 'undefined' ) {
			// day-element does not exist, so array needs to be extended at the end
			newDayStr = String(day).padStart(2, '0');  // day with leading zero
			newDatasetDateStr = dateStrPart + newDayStr;
			csvData.push(Array(DATACOLUMNCOUNT + 1).fill(0));  // add row to csvData
			csvData[dayIndex][0] = newDatasetDateStr;  // and set correct date
      csvDatab.push(Array(DATACOLUMNCOUNT + 1).fill(0));  // add row to csvData
			csvDatab[dayIndex][0] = newDatasetDateStr;  // and set correct date
			lpCounterValues.push(Array(DATACOLUMNCOUNT + 1).fill(''));  // add row to lp-counter-values
		} else {
			// day-element does exist
			dayAtIndex = parseInt(csvData[dayIndex][0].substring(8));
			if ( dayAtIndex !== day ) {
				// but day doesn't match the array position so array needs to be extended at the front
				day = dayAtIndex - 1;  //
				newDayStr = String(day).padStart(2, '0');  // day with leading zero
				newDatasetDateStr = dateStrPart + newDayStr;
				csvData.unshift(Array(DATACOLUMNCOUNT + 1).fill(0));  // add row to csvData
				csvData[dayIndex][0] = newDatasetDateStr;  // and set correct date
        csvDatab.unshift(Array(DATACOLUMNCOUNT + 1).fill(0));  // add row to csvData
				csvDatab[dayIndex][0] = newDatasetDateStr;  // and set correct date
				lpCounterValues.unshift(Array(DATACOLUMNCOUNT + 1).fill(''));  // add row to lp-counter-values
				dayIndex--;
			}
		}
	}
}

function formatDateColumn() {
	// formats the first csvdata-column so date is displayed at labels like 'Mo, 16.03.20'
	for ( var rowIndex = 0; rowIndex < csvData.length; rowIndex++ ) {
		var theDate = new Date(csvData[rowIndex][0]);
		var day = String(theDate.getDate()).padStart(2, '0');  // format with leading zeros
		var dayOfWeek = theDate.toLocaleDateString('de-DE', { weekday: 'short'});
		// old variant... just keep in case this format is wanted
		// var theDateStr = dayOfWeek + ', ' + day + '.' + graphMonth + '.' + graphYear;
		var theDateStr = dayOfWeek + ', ' + day + '.';
		csvData[rowIndex][0] = theDateStr;
	}
}

function lpCount() {
	// returns amount of LP containing other values than zero
	var count = 0;
	for ( var i = 0; i < LPCOLUMNS.length; i++ ) {
		var dataColumn = getCol(csvData, LPCOLUMNS[i]);
		if ( dataColumn.some( value => value !== 0 ) ) {
			count++;
		}
	}
	return count;
}

function loadgraph() {
	buildCsvDataArray();
  buildCsvDataArrayb();

	if ( csvData.length < 2 ) {
		// not enough data rows: nothing to display
  //  alert(" indexb "+ indexb+ " indexc " + indexc);
  //  alert(" csvData.length "+ csvData [0]);
		$("#waitforgraphloadingdiv").html('<br>Nicht genügend Daten für diesen Zeitraum verfügbar.');
		$('#canvasdiv').hide();
		return;
	}
	if ( csvData.length > (daysInMonth + 1) ) {
		// too many data-rows have been transmitted, data may be corrupt
		$("#waitforgraphloadingdiv").html('<br>Fehler bei der Übertragung der Daten für diesen Monat, bitte erneut versuchen.');
		$('#canvasdiv').hide();
		return;
	}
	// sort array by date
	csvData.sort((date1, date2) => date1[0].localeCompare(date2[0]));
  csvDatab.sort((date1, date2) => date1[0].localeCompare(date2[0]));
	// and process array
	fillDataGaps();  // completes gaps in data
	fillLpCounterValuesArray();  // fills an array containg all counter values for every lp
	//calcDailyValues();  // sum up values for totals
  calcDailyValuesNew();
	csvData.pop();  // discard last row in csvData-array, it was just needed for calculation of daily values from original counter-values
	csvDatab.pop();  // discard last row in csvData-array, it was just needed for calculation of daily values from original counter-values
//alert(" csvData.length "+ csvData.length);
//console.log("csvData 1",csvData[1]);

	if ( csvData.length != daysInMonth ) {
		// not all days of selected month have been logged,
		// complete monthly csvData and counter values before/after first/last day logged
		completeMonth();
	}

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
		if (total <= 2) {  // set data total less then 2 kw to disabled
			totalHidden.push(1);
	} else {
			totalHidden.push(0)
	}
	}

	//build array containing all available data from csvData
  //build array containing all available data from csvData
	var lineChartDataSets = [
		'', // first entry with index 0 is empty and later removed just needed to sync array index with respective csvData index
		{
			label: 'Bezug ' + totalValues[1].toFixed(2) + ' kWh',
			hidden: totalHidden[1],
			borderColor: "rgba(255, 0, 0, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 1,
			fill: true,
			data: getCol(csvData, 1),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 1)
		} ,
		{
			label: 'Einspeisung ' + totalValues[2].toFixed(2) + ' kWh',
			hidden: totalHidden[2],
			borderColor: "rgba(0, 255, 105, 0.9)",
			backgroundColor: "rgba(0, 255, 255, 0.3)",
			borderWidth: 2,
			fill: true,
			data: getCol(csvData, 2),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 2)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'PV ' + totalValues[3].toFixed(2) + ' kWh',
			hidden: totalHidden[3],
			borderColor: 'green',
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: true,
			borderWidth: 1,
			data: getCol(csvData, 3),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 3)  // custom added field, holds counter values or empty string
		} ,

		{
			label: 'Lp1 ' + totalValues[4].toFixed(2) + ' kWh',
			hidden: totalHidden[4],
			borderColor: "rgba(0, 0, 255, 0.7)",
			backgroundColor: "rgba(0, 0, 255, 0.7)",
			borderWidth: 1,
			fill: false,
			data: getCol(csvData, 4),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 4)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Lp2 ' + totalValues[5].toFixed(2) + ' kWh',
			hidden: totalHidden[5],
			borderColor: "rgba(50, 30, 105, 0.7)",
			backgroundColor: "rgba(50, 30, 105, 0.7)",
			borderWidth: 1,
			fill: false,
			data: getCol(csvData, 5),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 5)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Lp3 ' + totalValues[6].toFixed(2) + ' kWh',
			hidden: totalHidden[6],
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 6),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 6)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Lp Gesamt ' + totalValues[7].toFixed(2) + ' kWh',
			hidden: totalHidden[7],
			borderColor: "rgba(50, 50, 55, 0.1)",
			backgroundColor: "rgba(0, 0, 255, 0.1)",
			fill: true,
			borderWidth: 2,
			data: getCol(csvData, 7),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 7)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Verbraucher 1 in ' + totalValues[8].toFixed(2) + ' kWh',
			hidden: totalHidden[8],
			borderColor: "rgba(0, 150, 150, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 8),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 8)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Verbraucher 1 out ' + totalValues[9].toFixed(2) + ' kWh',
			hidden: totalHidden[9],
			borderColor: "rgba(0, 150, 150, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 9),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 9)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Verbraucher 2 in ' + totalValues[10].toFixed(2) + ' kWh',
			hidden: totalHidden[10],
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 10),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 10)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Verbraucher 2 out ' + totalValues[11].toFixed(2) + ' kWh',
			hidden: totalHidden[11],
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 11),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 11)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Lp4 ' + totalValues[12].toFixed(2) + ' kWh',
			hidden: totalHidden[12],
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			data: getCol(csvData, 12),
			borderWidth: 2,
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 12)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Lp5 ' + totalValues[13].toFixed(2) + ' kWh',
			hidden: totalHidden[13],
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 13),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 13)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Lp6 ' + totalValues[14].toFixed(2) + ' kWh',
			hidden: totalHidden[14],
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 14),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 14)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Lp7 ' + totalValues[15].toFixed(2) + ' kWh',
			hidden: totalHidden[15],
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 15),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 15)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Lp8 ' + totalValues[16].toFixed(2) + ' kWh',
			hidden: totalHidden[16],
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 16),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 16)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Speicherladung ' + totalValues[17].toFixed(2) + ' kWh',
			hidden: totalHidden[17],
			borderColor: 'orange',
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: true,
			borderWidth: 1,
			data: getCol(csvData, 17),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 17)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Speicherentladung ' + totalValues[18].toFixed(2) + ' kWh',
			hidden: totalHidden[18],
			borderColor: 'orange',
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: true,
			borderWidth: 1,
			data: getCol(csvData, 18),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 18)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d1name + ' Import ' + totalValues[19].toFixed(2) + ' kWh',
			hidden: totalHidden[19],
			borderColor:"rgba(200, 150, 200, 0.7)",
			backgroundColor: "rgba(200, 150, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 19),
			lineTension: 0.2,
			yAxisID: 'y-axis-1',
			callv1:1,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 19)  // custom added field, holds counter values or empty string
		}  ,
		{
			label: d2name + ' Import ' + totalValues[20].toFixed(2) + ' kWh',
			hidden: totalHidden[20],
			borderColor: "rgba(200, 100, 200, 0.7)",
			backgroundColor: "rgba(200, 100, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 20),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 20)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d3name + ' Import ' + totalValues[21].toFixed(2) + ' kWh',
			hidden: totalHidden[21],
			borderColor: "rgba(200, 50, 200, 0.7)",
			backgroundColor: "rgba(200, 50, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 21),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 21)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d4name + ' Import ' + totalValues[22].toFixed(2) + ' kWh',
			hidden: totalHidden[22],
			borderColor: "rgba(200, 0, 200, 0.7)",
			backgroundColor: "rgba(200, 0, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 22),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 22)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d5name + ' Import ' + totalValues[23].toFixed(2) + ' kWh',
			hidden: totalHidden[23],
			borderColor: "rgba(150, 200, 200, 0.7)",
			backgroundColor: "rgba(150, 200, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 23),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 23)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d6name + ' Import ' + totalValues[24].toFixed(2) + ' kWh',
			hidden: totalHidden[24],
			borderColor: "rgba(100, 200, 200, 0.7)",
			backgroundColor: "rgba(100, 200, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 24),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 24)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d7name + ' Import ' + totalValues[25].toFixed(2) + ' kWh',
			hidden: totalHidden[25],
			borderColor: "rgba(50, 200, 200, 0.7)",
			backgroundColor: "rgba(50, 200, 200, 0.7)",
			fill: false,
			data: getCol(csvData, 25),
			borderWidth: 1,
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 25)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d8name + ' Import ' + totalValues[26].toFixed(2) + ' kWh',
			hidden: totalHidden[26],
			borderColor: "rgba(0, 200, 200, 0.7)",
			backgroundColor: "rgba(0, 200, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 26),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 26)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d9name + ' Import ' + totalValues[27].toFixed(2) + ' kWh',
			hidden: totalHidden[27],
			borderColor: "rgba(200, 200, 200, 0.7)",
			backgroundColor: "rgba(200, 200, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 27),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 27)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d10name + ' Import ' + totalValues[28].toFixed(2) + ' kWh',
			hidden: totalHidden[28],
			borderColor: "rgba(200, 200, 200, 0.7)",
			backgroundColor: "rgba(200, 200, 200, 0.7)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 28),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:0,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 28)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'LP Gesamt PV ' + totalValues[29].toFixed(2) + ' kWh',
			hidden: totalHidden[29],
			borderColor: 'green',
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 29),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'LP-Gesamt',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 29)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'LP Gesamt Speicherentladung ' + totalValues[30].toFixed(2) + ' kWh',
			hidden: totalHidden[30],
			borderColor: 'orange',
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: false,
			borderWidth: 1,
			data: getCol(csvData, 30),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'LP-Gesamt',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 30)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'LP Gesamt Bezug ' + totalValues[31].toFixed(2) + ' kWh',
			hidden: totalHidden[31],
			borderColor: "rgba(255, 0, 0, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 1,
			fill: false,
			data: getCol(csvData, 31),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'LP-Gesamt',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 31)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d1name + ' PV ' + totalValues[32].toFixed(2) + ' kWh',
			hidden: totalHidden[32],
			borderColor:"rgba(200, 150, 200, 0.7)",
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 32),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd1',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 32)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d1name + ' Speicherentladung ' + totalValues[33].toFixed(2) + ' kWh',
			hidden: totalHidden[33],
			borderColor:"rgba(200, 150, 200, 0.7)",
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 33),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd1',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 33)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d1name + ' Bezug ' + totalValues[34].toFixed(2) + ' kWh',
			hidden: totalHidden[34],
			borderColor:"rgba(200, 150, 200, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 2,
			fill: false,
			data: getCol(csvData, 34),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd1',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 34)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d2name + ' PV ' + totalValues[35].toFixed(2) + ' kWh',
			hidden: totalHidden[35],
			borderColor: "rgba(200, 100, 200, 0.7)",
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 35),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd2',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 35)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d2name + ' Speicherentladung ' + totalValues[36].toFixed(2) + ' kWh',
			hidden: totalHidden[36],
			borderColor: "rgba(200, 100, 200, 0.7)",
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 36),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd2',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 36)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d2name + ' Bezug ' + totalValues[37].toFixed(2) + ' kWh',
			hidden: totalHidden[37],
			borderColor: "rgba(200, 100, 200, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 2,
			fill: false,
			data: getCol(csvData, 37),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd2',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 37)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d3name + ' PV ' + totalValues[38].toFixed(2) + ' kWh',
			hidden: totalHidden[38],
			borderColor: "rgba(200, 50, 200, 0.7)",
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 38),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd3',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 38)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d3name + ' Speicherentladung ' + totalValues[39].toFixed(2) + ' kWh',
			hidden: totalHidden[39],
			borderColor: "rgba(200, 50, 200, 0.7)",
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 39),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd3',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 39)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d3name + ' Bezug ' + totalValues[40].toFixed(2) + ' kWh',
			hidden: totalHidden[40],
			borderColor: "rgba(200, 50, 200, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 2,
			fill: false,
			data: getCol(csvData, 40),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd3',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 40)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d4name + ' PV ' + totalValues[41].toFixed(2) + ' kWh',
			hidden: totalHidden[41],
			borderColor: "rgba(200, 0, 200, 0.7)",
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 41),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd4',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 41)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d4name + ' Speicherentladung ' + totalValues[42].toFixed(2) + ' kWh',
			hidden: totalHidden[42],
			borderColor: "rgba(200, 0, 200, 0.7)",
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 42),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd4',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 42)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d4name + ' Bezug ' + totalValues[43].toFixed(2) + ' kWh',
			hidden: totalHidden[43],
			borderColor: "rgba(200, 0, 200, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 2,
			fill: false,
			data: getCol(csvData, 43),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd4',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 43)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d5name + ' PV ' + totalValues[44].toFixed(2) + ' kWh',
			hidden: totalHidden[44],
			borderColor: "rgba(150, 200, 200, 0.7)",
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 44),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd5',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 44)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d5name + ' Speicherentladung ' + totalValues[45].toFixed(2) + ' kWh',
			hidden: totalHidden[45],
			borderColor: "rgba(150, 200, 200, 0.7)",
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 45),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd5',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 45)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d5name + ' Bezug ' + totalValues[46].toFixed(2) + ' kWh',
			hidden: totalHidden[46],
			borderColor: "rgba(150, 200, 200, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 2,
			fill: false,
			data: getCol(csvData, 46),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd5',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 46)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d6name + ' PV ' + totalValues[47].toFixed(2) + ' kWh',
			hidden: totalHidden[47],
			borderColor: "rgba(100, 200, 200, 0.7)",
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 47),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd6',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 47)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d6name + ' Speicherentladung ' + totalValues[48].toFixed(2) + ' kWh',
			hidden: totalHidden[48],
			borderColor: "rgba(100, 200, 200, 0.7)",
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 48),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd6',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 48)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d6name + ' Bezug ' + totalValues[49].toFixed(2) + ' kWh',
			hidden: totalHidden[49],
			borderColor: "rgba(100, 200, 200, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 2,
			fill: false,
			data: getCol(csvData, 49),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd6',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 49)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d7name + ' PV ' + totalValues[50].toFixed(2) + ' kWh',
			hidden: totalHidden[50],
			borderColor: "rgba(50, 200, 200, 0.7)",
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 50),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd7',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 50)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d7name + ' Speicherentladung ' + totalValues[51].toFixed(2) + ' kWh',
			hidden: totalHidden[51],
			borderColor: "rgba(50, 200, 200, 0.7)",
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 51),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd7',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 51)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d7name + ' Bezug ' + totalValues[52].toFixed(2) + ' kWh',
			hidden: totalHidden[52],
			borderColor: "rgba(50, 200, 200, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 2,
			fill: false,
			data: getCol(csvData, 52),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd7',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 52)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d8name + ' PV ' + totalValues[53].toFixed(2) + ' kWh',
			hidden: totalHidden[53],
			borderColor: "rgba(0, 200, 200, 0.7)",
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 53),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd8',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 53)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d8name + ' Speicherentladung ' + totalValues[54].toFixed(2) + ' kWh',
			hidden: totalHidden[54],
			borderColor: "rgba(0, 200, 200, 0.7)",
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 54),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd8',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 54)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d8name + ' Bezug ' + totalValues[55].toFixed(2) + ' kWh',
			hidden: totalHidden[55],
			borderColor: "rgba(0, 200, 200, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 2,
			fill: false,
			data: getCol(csvData, 55),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd8',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 55)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d9name + ' PV ' + totalValues[56].toFixed(2) + ' kWh',
			hidden: totalHidden[56],
			borderColor: "rgba(200, 200, 200, 0.7)",
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 56),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd9',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 56)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d9name + ' Speicherentladung ' + totalValues[57].toFixed(2) + ' kWh',
			hidden: totalHidden[57],
			borderColor: "rgba(200, 200, 200, 0.7)",
			backgroundColor: "rgba(255, 155, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 57),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd9',
			type: 'bar',
			callv1:0,
			callv2:1,
			toolTipData: getCol(lpCounterValues, 57)  // custom added field, holds counter values or empty string
		} ,
		{
			label: d9name + ' Bezug ' + totalValues[58].toFixed(2) + ' kWh',
			hidden: totalHidden[58],
			borderColor: "rgba(200, 200, 200, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 2,
			fill: false,
			data: getCol(csvData, 58),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			stack: 'd9',
			type: 'bar',
			callv1:0,
			callv2:1,
		toolTipData: getCol(lpCounterValues, 58)  // custom added field, holds counter values or empty string
		} ,
		{
			label: 'Hausverbrauch ' + totalValues[59].toFixed(2) + ' kWh',
			hidden: totalHidden[59],
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: getCol(csvData, 59),
			yAxisID: 'y-axis-1',
			lineTension: 0.2,
			callv1:1,
			callv2:0,
			toolTipData: getCol(lpCounterValues, 0)  // custom added field, always empty string at index 0
		}
 ];
	// check if other LP than #1 has data !== 0 and if not, set all LP Gesamt to 0 so it will not be displayed
//	if ( lpCount() < 2 ) {
//for ( var rowIndex = 0; rowIndex < csvData.length; rowIndex++ ) {
//	csvData[rowIndex][7] = 0;
//		}
//	}

	// now delete all graph lines containing only zero values
	// by deleting the respective field in the linChartDataSets-array
	for ( var column = 1; column < csvData[0].length; column++ ) {
		// process all data-columns except the date
		// column in csvData is represented by column-entry in linChartData
		var dataColumn = getCol(csvData, column);
		if ( dataColumn.every( value => value === 0 ) ) {
			lineChartDataSets[column] = '';  // mark entry for removal of line if data is all zero
		}
		// delete all totals which are less then 1
		if (totalValues [column] <= 1) {
			lineChartDataSets[column] = '';  // mark entry for removal of line if total is < 1
		}
	}
	// now remove lines marked by '' for removal
	lineChartDataSets = lineChartDataSets.filter((element) => element !== '');
	// Filtern aufgrund programmaufruf
	if (callv1 == 1) {
		lineChartDataSets = lineChartDataSets.filter(function (e) {return e.callv1 == 1;  });
	} ;
	if (callv2 == 1) {
		lineChartDataSets = lineChartDataSets.filter(function (e) {return e.callv2 == 1;  });
	} ;
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
						return dataPoint[0].xLabel + graphMonth + '.' + graphYear;
					},
					label: function(dataPoint, graphData) {
						// get only the name of the respective dataline since total value is visible at legend
						var xLabel = graphData.datasets[dataPoint.datasetIndex].label.split(' ', 1)[0];
						// get value for the tooltip-day
						var yLabel = ', Tageswert: ' + dataPoint.yLabel.toFixed(2) + ' kWh';
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
			var day = myLine.data.labels[clickedElementindex];  // get complete label of day clicked
			// and format the string as needed to call daily graph: YYYY-mm-dd
			day = day.replace(/[^\d]/g,'');  // only day as number left
			var jumpToDate = graphYear + '-' + graphMonth + '-' + day;
			window.location.href = "logging/daily.php?date=" + jumpToDate;
		}
	});

	initialread = 1;
	$('#waitforgraphloadingdiv').hide();
}
