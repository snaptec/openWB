/**
 * reads longtime logging data and displays graph
 *
 * @author: Kevin Wieland, Michael Ortenstein
 *
 * generally fills data-gaps in timeline with zero values,
 * fills data-gap-columns indicated by "socValues" as their index with 50% so lines dont jump
 */

const socValues = [13, 14, 15];  // these columns represent SoC values

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
var alldata;

$.ajax({
	url: "/openWB/ramdisk/all.graph",
	contentType: "text/plain",
	dataType: "text",
	beforeSend: function(xhr) {
		xhr.overrideMimeType( "text/plain; charset=x-user-defined" );
	},
	complete: function(request){
		alldata = request.responseText;
		loadgraph();
	}
});

function getCol(matrix, col){
	var column = [];
	for(var i=0; i<matrix.length; i++){
		column.push(matrix[i][col]);
	}
	return column;
}

function convertToKw(dataColum) {
	var convertedDataColumn = [];
	dataColum.forEach((value) => {
		convertedDataColumn.push(value / 1000);
	});
	return convertedDataColumn;
}

function visibility(datavar,hidevar,hidevalue,boolvar) {
	var vis=0;
	datavar.forEach(function(csvvar){
		if ( csvvar != 0 && typeof csvvar !== 'undefined'){
			vis=1;
		}
	});
	if ( vis == 1 ){
		window[hidevar] = 'foo';
		window[boolvar] = 'flase';
	} else {
		window[hidevar] = hidevalue;
		window[boolvar] = 'true';
	}
}

function prepareNewDataset(length, dataArray) {
	/**
	 * builds an array(length) filled with zeros
	 * to generally fill data-gaps in timeline with zero values,
	 * fills data-gap-columns indicated by "socValues" as their index with 50% so lines dont jump
	 * (but only if other SoC-values exist in dataArray)
	 *
	 * @author: Michael Ortenstein
	 * @param {number} length The desired length of the new array
	 * @param {array} dataArray The complete array of all csv values
	 * @returns {newArray} The dataset to fill the gap
	 */
	var newArray = new Array(length).fill('0');
	if ( socValues.length > 0 ) {
		// there are columns marked as containing SoC values
		socValues.forEach((column) => {
			var dataColumn = getCol(dataArray, column);
			// check how to cover the gaps so lines don't jump
			if ( dataColumn.every( value => value == '0' ) ) {
				newArray[column] = '0';
			} else if ( dataColumn.every( value => value == '' ) ) {
				newArray[column] = '';
			} else {
				newArray[column] = '50';
			}
		});
	}
	return newArray;
}

function loadgraph() {
	alldata = alldata.replace(/^\s*[\n]/gm, '');
	alldata = alldata.replace(/^\s*-[\n]/gm, '');
	var csvData = [];
	var rawcsv = alldata.split(/\r?\n|\r/);  // split line in array
	rawcsv.forEach((dataset) => {
		var datasetArray = dataset.split(',');
		var datasetDateStr = datasetArray[0];
		if ( datasetDateStr.length > 0 && new Date(datasetDateStr) !== "Invalid Date" && !isNaN(new Date(datasetDateStr)) ) {
			// date string is not undefined or empty and date string is a date
			csvData.push(datasetArray);
		}
	});

	if ( csvData.length < 30 ) {
		// is less than 30 datasets: don't draw graph
		$('#displayedTimePeriodSpan').html('<br>Anzahl Messpunkte nicht ausreichend zur Darstellung.');
		$('#waitforgraphloadingdiv').hide();
		$('#canvasdiv').hide();
		return;
	} else {
		// scan array for time-gaps in dataset and fill with zero values
		var lastScannedTimestampStr = csvData[0][0];
		const DATAFIELDS = csvData[0].length;
		for (var index=1; index < csvData.length; index++) {
			let currentTimestampStr = csvData[index][0];
			let lastScannedTimestamp = new Date(lastScannedTimestampStr);
			let currentTimestamp = new Date(currentTimestampStr);
			let diffSeconds = Math.round((currentTimestamp - lastScannedTimestamp) / 1000); // seconds between datasets
			if ( diffSeconds > 300 ) {
				// gap between datasets > 300 seconds,
				// add 2 datasets inbetween filled with zeros to flatten graph line
				// since quantity of values may change with development of project
				// build new dataset with zeros dynamically from length of dataset
				let valueArrayLeft = prepareNewDataset(DATAFIELDS, csvData);
				let valueArrayRight = prepareNewDataset(DATAFIELDS, csvData);

				// build timestamp left gap
				let dd = String(lastScannedTimestamp.getDate()).padStart(2, '0');  // format with leading zeros
				let mm = String(lastScannedTimestamp.getMonth() + 1).padStart(2, '0'); //January is 0!
				let HH = String(lastScannedTimestamp.getHours()).padStart(2, '0');
				let MM = String(lastScannedTimestamp.getMinutes()).padStart(2, '0');
				let SS = String(lastScannedTimestamp.getSeconds() + 1).padStart(2, '0');  // add a second to last timestamp
				// set timestamp
				valueArrayLeft[0] = lastScannedTimestamp.getFullYear() + '/' + mm + '/' + dd + ' ' + HH + ':' + MM + ':' + SS;
				// insert into csvData
				csvData.splice(index++, 0, valueArrayLeft);
				// build timestamp right gap
				//
				dd = String(currentTimestamp.getDate()).padStart(2, '0');  // format with leading zeros
				mm = String(currentTimestamp.getMonth() + 1).padStart(2, '0'); //January is 0!
				HH = String(currentTimestamp.getHours()).padStart(2, '0');
				MM = String(currentTimestamp.getMinutes()).padStart(2, '0');
				SS = String(currentTimestamp.getSeconds() - 1).padStart(2, '0');  // // subtract a second from current timestamp
				// set timestamp
				valueArrayRight[0] = currentTimestamp.getFullYear() + '/' + mm + '/' + dd + ' ' + HH + ':' + MM + ':' + SS;
				// insert into csvData
				csvData.splice(index++, 0, valueArrayRight);
			}
			lastScannedTimestampStr = currentTimestampStr;
		}
	}
	// Retrived data from csv file content
	atime = getCol(csvData, 0);
	abezug = convertToKw(getCol(csvData, 1));
	alpa = convertToKw(getCol(csvData, 2));
	apv = convertToKw(getCol(csvData, 3));
	alp1 = convertToKw(getCol(csvData, 4));
	alp2 = convertToKw(getCol(csvData, 5));
	alp3 = convertToKw(getCol(csvData, 6));
	alp4 = convertToKw(getCol(csvData, 7));
	alp5 = convertToKw(getCol(csvData, 8));
	alp6 = convertToKw(getCol(csvData, 9));
	alp7 = convertToKw(getCol(csvData, 10));
	alp8 = convertToKw(getCol(csvData, 11));
	aspeicherl = convertToKw(getCol(csvData, 12));
	aspeichersoc = getCol(csvData, 13);
	asoc = getCol(csvData, 14);
	asoc1 = getCol(csvData, 15);
	ahausverbrauch = convertToKw(getCol(csvData, 16));
	averbraucher1 = convertToKw(getCol(csvData, 17));
	averbraucher2 = convertToKw(getCol(csvData, 18));
	visibility(abezug,'hidebezug','Bezug',boolDisplayEvu);
	visibility(alpa,'hidelpa','LP Gesamt',boolDisplayLpAll);
	visibility(apv,'hidepv','PV',boolDisplayPv);
	visibility(alp1,'hidelp1','Lp1',boolDisplayLp1);
	visibility(alp2,'hidelp2','Lp2',boolDisplayLp2);
	visibility(alp3,'hidelp3','Lp3',boolDisplayLp3);
	visibility(alp4,'hidelp4','Lp4',boolDisplayLp4);
	visibility(alp5,'hidelp5','Lp5',boolDisplayLp5);
	visibility(alp6,'hidelp6','Lp6',boolDisplayLp6);
	visibility(alp7,'hidelp7','Lp7',boolDisplayLp7);
	visibility(alp8,'hidelp8','Lp8',boolDisplayLp8);
	visibility(aspeicherl,'hidespeicher','Speicherleistung',boolDisplaySpeicher);
	visibility(aspeichersoc,'hidespeichersoc','Speicher SoC',boolDisplaySpeicherSoc);
	visibility(asoc,'hidelp1soc','LP1 SoC',boolDisplayLp1Soc);
	visibility(asoc1,'hidelp2soc','LP2 SoC',boolDisplayLp2Soc);
	visibility(ahausverbrauch,'hidehaus','Hausverbrauch',boolDisplayHouseConsumption);
	visibility(averbraucher1,'hideload1','Verbraucher 1',boolDisplayLoad1);
	visibility(averbraucher2,'hideload2','Verbraucher 2',boolDisplayLoad2);

	var lineChartData = {
		labels: atime,
		datasets: [{
			label: 'Lp1',
			borderColor: "rgba(0, 0, 255, 0.7)",
			backgroundColor: "rgba(0, 0, 255, 0.7)",
			borderWidth: 1,
			hidden: boolDisplayLp1,
			fill: false,
			data: alp1,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Lp2',
			borderColor: "rgba(50, 30, 105, 0.7)",
			backgroundColor: "rgba(50, 30, 105, 0.7)",
			borderWidth: 1,
			hidden: boolDisplayLp2,
			fill: false,
			data: alp2,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Bezug',
			borderColor: "rgba(255, 0, 0, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 1,
			fill: true,
			data: abezug,
			hidden: boolDisplayEvu,
			yAxisID: 'y-axis-1'
		} , {
			label: 'PV',
			borderColor: 'green',
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: true,
			hidden: boolDisplayPv,
			borderWidth: 1,
			data: apv,
			yAxisID: 'y-axis-1'
		}  , {
			label: 'Speicherleistung',
			borderColor: 'orange',
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: true,
			borderWidth: 1,
			data: aspeicherl,
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
			label: 'LP1 SoC',
			borderColor: "rgba(0, 0, 255, 0.5)",
			borderDash: [10,5],
			borderWidth: 2,
			hidden: boolDisplayLp1Soc,
			fill: false,
			data: asoc,
			yAxisID: 'y-axis-2'
		} , {
			label: 'LP2 SoC',
			borderColor: "rgba(50, 50, 55, 0.5)",
			borderDash: [10,5],
			fill: false,
			borderWidth: 2,
			hidden: boolDisplayLp2Soc,
			data: asoc1,
			yAxisID: 'y-axis-2'
		} , {
			label: 'Hausverbrauch',
			borderColor: "rgba(150, 150, 150, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			hidden: boolDisplayHouseConsumption,
			data: ahausverbrauch,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Verbraucher 1',
			borderColor: "rgba(0, 150, 150, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			hidden: boolDisplayLoad1,
			data: averbraucher1,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Verbraucher 2',
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			borderWidth: 2,
			data: averbraucher2,
			hidden: boolDisplayLoad2,
			yAxisID: 'y-axis-1'
		} , {
			label: 'LP Gesamt',
			borderColor: "rgba(50, 50, 55, 0.1)",
			backgroundColor: "rgba(0, 0, 255, 0.1)",
			fill: true,
			borderWidth: 2,
			data: alpa,
			hidden: boolDisplayLpAll,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Lp3',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp3,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp3
		} , {
			label: 'Lp4',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			data: alp4,
			borderWidth: 2,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp4
		} , {
			label: 'Lp5',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp5,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp5
		} , {
			label: 'Lp6',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp6,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp6
		} , {
			label: 'Lp7',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp7,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp7
		} , {
			label: 'Lp8',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			borderWidth: 2,
			data: alp8,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp8
		}]
	}
	var canvas = $('#canvas').get(0);
    var ctx = canvas.getContext('2d');
	var longlivechart = new Chart(ctx, {
		type: 'line',
		data: lineChartData,
		options: {
			tooltips: {
				enabled: false
			},
			elements: {
				point: {
					radius: 0
				},
				line: {
					tension: 0
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
				mode: 'null'
			},
			stacked: false,
			legend: {
				display: true,
				position: 'bottom',
				labels: {
					// middle grey, opacity = 100% (visible)
					fontColor: "rgba(153, 153, 153, 1)",
					filter: function(item,chart) {
						if ( item.text.includes(hidehaus) || item.text.includes(hideload2) || item.text.includes(hideload1) || item.text.includes(hidelp2soc) || item.text.includes(hidelp1soc) || item.text.includes(hidelp1) || item.text.includes(hidelp2) || item.text.includes(hidelp3) || item.text.includes(hidelp4) || item.text.includes(hidelp5) || item.text.includes(hidelp6) || item.text.includes(hidelp7) || item.text.includes(hidelp8) || item.text.includes(hidespeichersoc) || item.text.includes(hidespeicher) || item.text.includes(hidelpa) || item.text.includes(hidepv) || item.text.includes(hidebezug) ) {
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
				xAxes: [
					{
						type: 'time',
						time: {
							parser: 'YYYY/MM/DD HH:mm:ss',
							unit: 'minute',
							displayFormats: {
								'minute': 'DD.MM.YY - HH:mm',
							},
							distribution: 'linear',
							precision: 60
						},
						ticks: {
							//source: 'data',
							maxTicksLimit: 25,
							fontColor: "rgba(153, 153, 153, 1)"  // middle grey, opacity = 100% (visible)
						}
					}
				],
				yAxes: [
					{
						// horizontal line for values displayed on the left side (power)
						position: 'left',
						id: 'y-axis-1',
						type: 'linear',
						avoidFirstLastClippingEnabled: true,
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Leistung [kW]',
							// middle grey, opacity = 100% (visible)
							fontColor: "rgba(153, 153, 153, 1)"
						},
						gridLines: {
							// light grey, opacity = 100% (visible)
							color: "rgba(204, 204, 204, 1)",
						},
						ticks: {
							// middle grey, opacity = 100% (visible)
							fontColor: "rgba(153, 153, 153, 1)"
						}
					},
					{
						// horizontal line for values displayed on the right side (SoC)
						position: 'right',
						id: 'y-axis-2',
						type: 'linear',
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'SoC [%]',
							// middle grey, opacity = 100% (visible)
							fontColor: "rgba(153, 153, 153, 1)"
						},
						gridLines: {
							// black, opacity = 0% (invisible)
							color: "rgba(0, 0, 0, 0)",
						},
						ticks: {
							min: 1,
							suggestedMax: 100,
							// middle grey, opacity = 100% (visible)
							fontColor: "rgba(153, 153, 153, 1)"
						}
					}
				]
			}
		}
	});
	initialread = 1;

	let startDate = new Date(atime[0]);
	let endDate = new Date(atime[atime.length - 1]);
	let dd = String(startDate.getDate()).padStart(2, '0');  // format with leading zeros
	let mm = String(startDate.getMonth() + 1).padStart(2, '0'); //January is 0!
	let dayOfWeek = startDate.toLocaleDateString('de-DE', { weekday: 'short'});
	let HH = String(startDate.getHours()).padStart(2, '0');
	let MM = String(startDate.getMinutes()).padStart(2, '0');
	let SS = String(startDate.getSeconds() + 1).padStart(2, '0');  // add a second to last timestamp
	var startDateStr = dayOfWeek + ', ' + dd + '.' + mm + '.' + startDate.getFullYear() + ' (' + HH + ':' + MM + ':' + SS + ')';

	dd = String(endDate.getDate()).padStart(2, '0');  // format with leading zeros
	mm = String(endDate.getMonth() + 1).padStart(2, '0'); //January is 0!
	dayOfWeek = endDate.toLocaleDateString('de-DE', { weekday: 'short'});
	HH = String(endDate.getHours()).padStart(2, '0');
	MM = String(endDate.getMinutes()).padStart(2, '0');
	SS = String(endDate.getSeconds() + 1).padStart(2, '0');  // add a second to last timestamp
	var endDateStr = dayOfWeek + ', ' + dd + '.' + mm + '.' + endDate.getFullYear() + ' (' + HH + ':' + MM + ':' + SS + ')';

	var displayedTimePeriodStr = startDateStr + ' bis ' + endDateStr;

	$('#displayedTimePeriodSpan').text(displayedTimePeriodStr);
	$('#waitforgraphloadingdiv').hide();
}  // end loadgraph
