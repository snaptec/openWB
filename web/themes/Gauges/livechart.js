var style = getComputedStyle(document.body);
var fontCol = style.getPropertyValue('--fontCol');
var gridCol = style.getPropertyValue('--gridCol');
var xgridCol = style.getPropertyValue('--xgridCol');
var gridSocCol = style.getPropertyValue('--gridSocCol');
var tickCol = style.getPropertyValue('--tickCol');
var lp1Col = style.getPropertyValue('--lp1Col');
var lp1bgCol = style.getPropertyValue('--lp1bgCol');
var lp2Col = style.getPropertyValue('--lp2Col');
var lp2bgCol = style.getPropertyValue('--lp2bgCol');
var evuCol = style.getPropertyValue('--evuCol');
var evubgCol = style.getPropertyValue('--evubgCol');
var pvCol = style.getPropertyValue('--pvCol');
var pvbgCol = style.getPropertyValue('--pvbgCol');
var speicherCol = style.getPropertyValue('--speicherCol');
var speicherSocCol = style.getPropertyValue('--speicherSocCol');
var speicherbgCol = style.getPropertyValue('--speicherbgCol');
var speicherSocbgCol = style.getPropertyValue('--speicherSocbgCol');
var lp1SocCol = style.getPropertyValue('--lp1SocCol');
var lp2SocCol = style.getPropertyValue('--lp2SocCol');
var hausverbrauchCol = style.getPropertyValue('--hausverbrauchCol');
var hausverbrauchbgCol = style.getPropertyValue('--hausverbrauchbgCol');
var lpgesamtCol = style.getPropertyValue('--lpgesamtCol');
var lpgesamtbgCol = style.getPropertyValue('--lpgesamtbgCol');
var lp3Col = style.getPropertyValue('--lp3Col');
var lp3bgCol = style.getPropertyValue('--lp3bgCol');
var lp4Col = style.getPropertyValue('--lp4Col');
var lp4bgCol = style.getPropertyValue('--lp4bgCol');
var lp5Col = style.getPropertyValue('--lp5Col');
var lp5bgCol = style.getPropertyValue('--lp5bgCol');
var lp6Col = style.getPropertyValue('--lp6Col');
var lp6bgCol = style.getPropertyValue('--lp6bgCol');
var lp7Col = style.getPropertyValue('--lp7Col');
var lp7bgCol = style.getPropertyValue('--lp7bgCol');
var lp8Col = style.getPropertyValue('--lp8Col');
var lp8bgCol = style.getPropertyValue('--lp8bgCol');
var verbraucher1Col = style.getPropertyValue('--verbraucher1Col');
var verbraucher1bgCol = style.getPropertyValue('--verbraucher1bgCol');
var verbraucher2Col = style.getPropertyValue('--verbraucher2Col');
var verbraucher2bgCol = style.getPropertyValue('--verbraucher2bgCol');
var d1Col = style.getPropertyValue('--d1Col');
var d1bgCol = style.getPropertyValue('--d1bgCol');
var d2Col = style.getPropertyValue('--d2Col');
var d2bgCol = style.getPropertyValue('--d2bgCol');
var d3Col = style.getPropertyValue('--d3Col');
var d3bgCol = style.getPropertyValue('--d3bgCol');
var d4Col = style.getPropertyValue('--d4Col');
var d4bgCol = style.getPropertyValue('--d4bgCol');
var d5Col = style.getPropertyValue('--d5Col');
var d5bgCol = style.getPropertyValue('--d5bgCol');
var d6Col = style.getPropertyValue('--d6Col');
var d6bgCol = style.getPropertyValue('--d6bgCol');
var d7Col = style.getPropertyValue('--d7Col');
var d7bgCol = style.getPropertyValue('--d7bgCol');
var d8Col = style.getPropertyValue('--d8Col');
var d8bgCol = style.getPropertyValue('--d8bgCol');
var d9Col = style.getPropertyValue('--d9Col');
var d9bgCol = style.getPropertyValue('--d9bgCol');

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
var boolDisplayshd1;
var boolDisplayshd2;
var boolDisplayshd3;
var boolDisplayshd4;
var boolDisplayshd5;
var boolDisplayshd6;
var boolDisplayshd7;
var boolDisplayshd8;
var boolDisplayshd9;
var d1name = 'Device 1';
var d2name = 'Device 2';
var d3name = 'Device 3';
var d4name = 'Device 4';
var d5name = 'Device 5';
var d6name = 'Device 6';
var d7name = 'Device 7';
var d8name = 'Device 8';
var d9name = 'Device 9';
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
var all13 = 0;
var all14 = 0;
var all15 = 0;
var all16 = 0;
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
var all13p;
var all14p;
var all15p;
var all16p;

var hidehaus;
var myLine;

function loadgraph(animationDuration = 1000) {
	var lineChartData = {
		labels: atime,
		datasets: [{
			label: 'Lp1',
			borderColor: lp1Col,
			backgroundColor: lp1bgCol,
			borderWidth: 2,
			hidden: boolDisplayLp1,
			fill: false,
			lineTension: 0.2,
			data: alp1,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Lp2',
			borderColor: lp2Col,
			backgroundColor: lp2bgCol,
			borderWidth: 2,
			hidden: boolDisplayLp2,
			fill: false,
			lineTension: 0.2,
			data: alp2,
			yAxisID: 'y-axis-1'
		} , {
			label: 'EVU',
			borderColor: evuCol,
			backgroundColor: evubgCol,
			borderWidth: 1,
			fill: true,
			lineTension: 0.2,
			data: abezug,
			hidden: boolDisplayEvu,
			yAxisID: 'y-axis-1'
		} , {
			label: 'PV',
			borderColor: pvCol,
			backgroundColor: pvbgCol,
			fill: true,
			lineTension: 0.2,
			hidden: boolDisplayPv,
			borderWidth: 1,
			data: apv,
			yAxisID: 'y-axis-1'
		}  , {
			label: 'Speicher',
			borderColor: speicherCol,
			backgroundColor: speicherbgCol,
			fill: true,
			lineTension: 0.2,
			borderWidth: 1,
			data: aspeicherl,
			hidden: boolDisplaySpeicher,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Speicher SoC',
			borderColor: speicherSocCol,
			backgroundColor: speicherSocbgCol,
			borderDash: [10,5],
			hidden: boolDisplaySpeicherSoc,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: aspeichersoc,
			yAxisID: 'y-axis-2'
		} , {
			label: 'LP1 SoC',
			borderColor: lp1SocCol,
			borderDash: [10,5],
			borderWidth: 2,
			hidden: boolDisplayLp1Soc,
			fill: false,
			lineTension: 0.2,
			data: asoc,
			yAxisID: 'y-axis-2'
		} , {
			label: 'LP2 SoC',
			borderColor: lp2SocCol,
			borderDash: [10,5],
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			hidden: boolDisplayLp2Soc,
			data: asoc1,
			yAxisID: 'y-axis-2'
		} , {
			label: 'Hausverbrauch',
			borderColor: hausverbrauchCol,
			backgroundColor: hausverbrauchbgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			hidden: boolDisplayHouseConsumption,
			data: ahausverbrauch,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Verbraucher 1',
			borderColor: verbraucher1Col,
			backgroundColor: verbraucher1bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			hidden: boolDisplayLoad1,
			data: averbraucher1,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Verbraucher 2',
			borderColor: verbraucher2Col,
			backgroundColor: verbraucher2bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: averbraucher2,
			hidden: boolDisplayLoad2,
			yAxisID: 'y-axis-1'
		} , {
			label: 'LP Gesamt',
			borderColor: lpgesamtCol,
			backgroundColor: lpgesamtbgCol,
			fill: true,
			lineTension: 0.2,
			borderWidth: 2,
			data: alpa,
			hidden: boolDisplayLpAll,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Lp3',
			borderColor: lp3Col,
			backgroundColor: lp3bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: alp3,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp3
		} , {
			label: 'Lp4',
			borderColor: lp4Col,
			backgroundColor: lp4bgCol,
			fill: false,
			lineTension: 0.2,
			data: alp4,
			borderWidth: 2,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp4
		} , {
			label: 'Lp5',
			borderColor: lp5Col,
			backgroundColor: lp5bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: alp5,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp5
		} , {
			label: 'Lp6',
			borderColor: lp6Col,
			backgroundColor: lp6bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: alp6,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp6
		} , {
			label: 'Lp7',
			borderColor: lp7Col,
			backgroundColor: lp7bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: alp7,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp7
		} , {
			label: 'Lp8',
			borderColor: lp8Col,
			backgroundColor: lp8bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: alp8,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp8
		}, {
			label: d1name,
			borderColor: d1Col,
			backgroundColor: d1bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: ashd1,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayshd1
		}, {
			label: d2name,
			borderColor: d2Col,
			backgroundColor: d2bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: ashd2,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayshd2
		}, {
			label: d3name,
			borderColor: d3Col,
			backgroundColor: d3bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: ashd3,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayshd3
		}, {
			label: d4name,
			borderColor: d4Col,
			backgroundColor: d4bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: ashd4,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayshd4
		}, {
			label: d5name,
			borderColor: d5Col,
			backgroundColor: d5bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: ashd5,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayshd5
		}, {
			label: d6name,
			borderColor: d6Col,
			backgroundColor: d6bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: ashd6,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayshd6
		}, {
			label: d7name,
			borderColor: d7Col,
			backgroundColor: d7bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: ashd7,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayshd7
		}, {
			label: d8name,
			borderColor: d8Col,
			backgroundColor: d8bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: ashd8,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayshd8
		}, {
			label: d9name,
			borderColor: d9Col,
			backgroundColor: d9bgCol,
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: ashd9,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayshd9
		}/*, {
			label: 'Device 1t0',
			borderColor: "rgba(250, 250, 155, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: ashd1t0,
			yAxisID: 'y-axis-2',
			hidden: boolDisplayLp8
		}, {
			label: 'Device 1t1',
			borderColor: "rgba(150, 250, 255, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: ashd1t1,
			yAxisID: 'y-axis-2',
			hidden: boolDisplayLp8
		}, {
			label: 'Device 1t2',
			borderColor: "rgba(255, 150, 255, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: ashd1t2,
			yAxisID: 'y-axis-2',
			hidden: boolDisplayLp8
		}*/
		]
	}

	function getMaxTicksLimit(width) {
		if ( width < 350 ) {
			return 6;
		} else if ( width < 470 ) {
			return 9;
		} else if ( width < 768 ) {
			return 12;
		} else {
			return 18;
		}
	}

	function setGraphLineBorderWidth(theGraph, newWidth) {
		// sets borderWidth attribute for all single lines without fill
		for ( var index = 0; index < theGraph.config.data.datasets.length; index++) {
			if ( !theGraph.config.data.datasets[index].fill ) {
				theGraph.config.data.datasets[index].borderWidth = newWidth;
			}
		}
	}

	function doGraphResponsive(chartInstance) {
		// changes graph resonding to screen size
		// quantity of x-axis labels
		chartInstance.config.options.scales.xAxes[0].ticks.maxTicksLimit = getMaxTicksLimit(chartInstance.width);
		// other settings
		if ( chartInstance.width > 390 ) {
			setGraphLineBorderWidth(chartInstance, 2);
			chartInstance.config.options.scales.xAxes[0].ticks.fontSize = 12;
			chartInstance.config.options.scales.yAxes[0].ticks.fontSize = 12;
			chartInstance.config.options.scales.yAxes[0].scaleLabel.fontSize = 12;
			chartInstance.config.options.scales.yAxes[1].ticks.fontSize = 12;
			chartInstance.config.options.scales.yAxes[1].scaleLabel.fontSize = 12;
		} else {
			setGraphLineBorderWidth(chartInstance, 1);
			chartInstance.config.options.scales.xAxes[0].ticks.fontSize = 10;
			chartInstance.config.options.scales.yAxes[0].ticks.fontSize = 9;
			chartInstance.config.options.scales.yAxes[0].scaleLabel.fontSize = 10;
			chartInstance.config.options.scales.yAxes[1].ticks.fontSize = 9;
			chartInstance.config.options.scales.yAxes[1].scaleLabel.fontSize = 10;
		}

		chartInstance.update();
	}

	var ctx = document.getElementById('canvas').getContext('2d');

	window.myLine = new Chart.Line(ctx, {
		plugins: {
			afterInit: doGraphResponsive,
			resize: doGraphResponsive
		},
		data: lineChartData,
		options: {
			tooltips: {
				enabled: false
			},
			elements: {
				point: {
					radius: 0
				}
			},
			animation: {
				duration: animationDuration,
				onComplete: function(animation) {
					// if duration was set to 0 to avoid pumping after reload, set back to default
					this.options.animation.duration = 1000
				}
			},
			responsive: true,
			maintainAspectRatio: false,
			hover: {
				mode: 'null'
			},
			stacked: false,
			legend: {
				display: boolDisplayLegend,
				labels: {
					fontColor: fontCol,
					filter: function(item,chart) {
						if ( item.text.includes(hidehaus) || item.text.includes(hideload2) || item.text.includes(hideload1) || item.text.includes(hidelp2soc) || item.text.includes(hidelp1soc) || item.text.includes(hidelp1) || item.text.includes(hidelp2) || item.text.includes(hidelp3) || item.text.includes(hidelp4) || item.text.includes(hidelp5) || item.text.includes(hidelp6) || item.text.includes(hidelp7) || item.text.includes(hidelp8) || item.text.includes(hidespeichersoc) || item.text.includes(hidespeicher) || item.text.includes(hidelpa) || item.text.includes(hidepv) || item.text.includes(hideevu) || item.text.includes(hideshd1)|| item.text.includes(hideshd2)|| item.text.includes(hideshd3)|| item.text.includes(hideshd4)|| item.text.includes(hideshd5)|| item.text.includes(hideshd6) || item.text.includes(hideshd7) || item.text.includes(hideshd8)|| item.text.includes(hideshd9) ) { return false } else { return true}
					}
				}
			},
			title: {
				display: false
			},
			scales: {
				xAxes: [
					{
						gridLines: {
							color: xgridCol
						},
					ticks: {
							fontColor: tickCol,
							maxTicksLimit: 15
					}
				}],
				yAxes: [
					{
						// horizontal line for values displayed on the left side (power)
						position: 'left',
						id: 'y-axis-1',
						type: 'linear',
						display: true,
						scaleLabel: {
						display: true,
						labelString: 'Leistung [kW]',
						fontColor: fontCol
					},
						gridLines: {
							color: gridCol
						},
						ticks: {
							stepSize: 0.2,
							maxTicksLimit: 10,
							fontColor: tickCol
						}
					},{
						// horizontal line for values displayed on the right side (SoC)
						position: 'right',
						id: 'y-axis-2',
						type: 'linear',
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'SoC [%]',
							fontColor: fontCol
						},
						gridLines: {
							// black, opacy = 0% (invisible)
							color: gridSocCol,
						},
						ticks: {
							min: 0,
							suggestedMax: 100,
							fontColor: tickCol
						}
					}
				]
			}
		}
	});
	initialread = 1;
	$('#waitforgraphloadingdiv').hide();
}  // end loadgraph
// Sichtbarkeit für SmartHome Devices im Graph
function setvisibility(datarr,hidevar,hidevalue,booldisplay){
	var arrayLength = datarr.length;
	var vis=0
	for (var i = 0; i < arrayLength; i++) {
		if (( datarr[i] >= 0.010) || (datarr[i] <=- 0.010)) {
			vis=1
		}
	}
	if ( vis == 0){
		window[hidevar] = hidevalue;
		window[booldisplay] = true;
	} else {
		window[hidevar] = 'foo';
		window[booldisplay] = false;

	}
}
function putgraphtogether() {
	if ( (all1 == 1) && (all2 == 1) && (all3 == 1) && (all4 == 1) && (all5 == 1) && (all6 == 1) && (all7 == 1) && (all8 == 1) && (all9 == 1) && (all10 == 1) && (all11 == 1) && (all12 == 1) && (all13 == 1) && (all14 == 1) && (all15 == 1) && (all16 == 1) ){
		var alldata = all1p + "\n" + all2p + "\n" + all3p + "\n" + all4p + "\n" + all5p + "\n" + all6p + "\n" + all7p + "\n" + all8p + "\n" + all9p + "\n" + all10p + "\n" + all11p + "\n" + all12p + "\n" + all13p + "\n" + all14p + "\n" + all15p + "\n" + all16p;
		alldata = alldata.replace(/^\s*[\n]/gm, "");
		alldata = alldata.replace(/^\s*-[\n]/gm, "");
		var csvData = [];
		var rawcsv = alldata.split(/\r?\n|\r/);
		for (var i = 0; i < rawcsv.length; i++) {
			  csvData.push(rawcsv[i].split(","));
		}
		csvData.pop();
		// Retrived data from csv file content
		var splittime = [];
		getCol(csvData, 0).forEach(function(zeit){
			splittime.push(zeit.substring(0, zeit.length -3));
		});
		atime = splittime;
		if ( atime.length >= 30 ) {
			//atime = getCol(csvData, 0);
			abezug = convertToKw(getCol(csvData, 1));
			alpa = convertToKw(getCol(csvData, 2));
			apv = convertToKw(getCol(csvData, 3));
			alp1 = convertToKw(getCol(csvData, 4));
			alp2 = convertToKw(getCol(csvData, 5));
			aspeicherl = convertToKw(getCol(csvData, 7));
			aspeichersoc = getCol(csvData, 8);
			asoc = getCol(csvData, 9);
			asoc1 = getCol(csvData, 10);
			ahausverbrauch = convertToKw(getCol(csvData, 11));
			averbraucher1 = convertToKw(getCol(csvData, 12));
			averbraucher2 = convertToKw(getCol(csvData, 13));
			alp3 = convertToKw(getCol(csvData, 14));
			alp4 = convertToKw(getCol(csvData, 15));
			alp5 = convertToKw(getCol(csvData, 16));
			alp6 = convertToKw(getCol(csvData, 17));
			alp7 = convertToKw(getCol(csvData, 18));
			alp8 = convertToKw(getCol(csvData, 19));
			ashd1 = convertToKw(getCol(csvData, 20));
			ashd2 = convertToKw(getCol(csvData, 21));
			ashd3 = convertToKw(getCol(csvData, 22));
			ashd4 = convertToKw(getCol(csvData, 23));
			ashd5 = convertToKw(getCol(csvData, 24));
			ashd6 = convertToKw(getCol(csvData, 25));
			ashd7 = convertToKw(getCol(csvData, 26));
			ashd8 = convertToKw(getCol(csvData, 27));
			ashd9 = convertToKw(getCol(csvData, 28));
			//ashd1t0 = getCol(csvData, 29);
			//ashd1t1 = getCol(csvData, 30);
			//ashd1t2 = getCol(csvData, 31);
			setvisibility(alp3,'hidelp3','Lp3');
			setvisibility(alp4,'hidelp4','Lp4');
			setvisibility(alp5,'hidelp5','Lp5');
			setvisibility(alp6,'hidelp6','Lp6');
			setvisibility(alp7,'hidelp7','Lp7');
			setvisibility(alp8,'hidelp8','Lp8');
			setvisibility(ashd1,'hideshd1',d1name,'boolDisplayshd1');
			setvisibility(ashd2,'hideshd2',d2name,'boolDisplayshd2');
			setvisibility(ashd3,'hideshd3',d3name,'boolDisplayshd3');
			setvisibility(ashd4,'hideshd4',d4name,'boolDisplayshd4');
			setvisibility(ashd5,'hideshd5',d5name,'boolDisplayshd5');
			setvisibility(ashd6,'hideshd6',d6name,'boolDisplayshd6');
			setvisibility(ashd7,'hideshd7',d7name,'boolDisplayshd7');
			setvisibility(ashd8,'hideshd8',d8name,'boolDisplayshd8');
			setvisibility(ashd9,'hideshd9',d9name,'boolDisplayshd9');

			initialread = 1 ;
			// after receipt of all 8 first data segments, unsubscribe from these topics to save bandwidth
			unsubscribeMqttGraphSegments();

			checkgraphload();
		} else {
			all1 = 0;
			all2 = 0;
			all3 = 0;
			all4 = 0;
			all5 = 0;
			all6 = 0;
			all7 = 0;
			all8 = 0;
			all9 = 0;
			all10 = 0;
			all11 = 0;
			all12 = 0;
			all13 = 0;
			all14 = 0;
			all15 = 0;
			all16 = 0;

			var percent = (atime.length / 60 * 100).toFixed();
			$('#waitforgraphloadingdiv').text('Erst ca. ' + percent + '% der mindestens benötigten Datenpunkte für den Graph seit Neustart vorhanden.');
		}
	}
}  // end putgraphtogether

function updateGraph(dataset) {
	var lines = dataset.split("\n");
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
		var shd1 = lines[i].split(",")[20];
		var shd2 = lines[i].split(",")[21];
		var shd3 = lines[i].split(",")[22];
		var shd4 = lines[i].split(",")[23];
		var shd5 = lines[i].split(",")[24];
		var shd6 = lines[i].split(",")[25];
		var shd7 = lines[i].split(",")[26];
		var shd8 = lines[i].split(",")[27];
		var shd9 = lines[i].split(",")[28];
		//var shd1t0 = lines[i].split(",")[29];
		//var shd1t1 = lines[i].split(",")[30];
		//var shd1t2 = lines[i].split(",")[31];

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
	myLine.data.datasets[18].data.push(shd1 / 1000);
	myLine.data.datasets[19].data.push(shd2 / 1000);
	myLine.data.datasets[20].data.push(shd3 / 1000);
	myLine.data.datasets[21].data.push(shd4 / 1000);
	myLine.data.datasets[22].data.push(shd5 / 1000);
	myLine.data.datasets[23].data.push(shd6 / 1000);
	myLine.data.datasets[24].data.push(shd7 / 1000);
	myLine.data.datasets[25].data.push(shd8 / 1000);
	myLine.data.datasets[26].data.push(shd9 / 1000);
	//myLine.data.datasets[27].data.push(shd1t0);
	//myLine.data.datasets[28].data.push(shd1t1);
	//myLine.data.datasets[29].data.push(shd1t2);
	myLine.data.labels.splice(0, 1);
	myLine.data.datasets.forEach(function(dataset) {
		dataset.data.splice(0, 1);
	});
	myLine.update();
}

function checkgraphload(){
	if ( graphloaded == 1 ) {
		myLine.destroy();
		loadgraph();
		return;
	}
	if ( typeof boolDisplayHouseConsumption === "boolean" &&
		typeof boolDisplayLoad1 === "boolean" &&
		typeof boolDisplayLp1Soc === "boolean" &&
		typeof boolDisplayLp2Soc === "boolean" &&
		typeof boolDisplayLoad2 === "boolean" &&
		typeof boolDisplayLp1 === "boolean" &&
		typeof boolDisplayLp2 === "boolean" &&
		typeof boolDisplayLp3 === "boolean" &&
		typeof boolDisplayLp4 === "boolean" &&
		typeof boolDisplayLp5 === "boolean" &&
		typeof boolDisplayLp6 === "boolean" &&
		typeof boolDisplayLp7 === "boolean" &&
		typeof boolDisplayLp8 === "boolean" &&
		typeof boolDisplayLpAll === "boolean" &&
		typeof boolDisplaySpeicherSoc === "boolean" &&
		typeof boolDisplaySpeicher === "boolean" &&
		typeof boolDisplayEvu === "boolean" &&
		typeof boolDisplayPv === "boolean" &&
		typeof boolDisplayLegend === "boolean" ) {
		if ( initialread != 0 ) {
			if ( graphloaded == 0 ) {
				graphloaded = 1;
			} else {
				myLine.destroy();
			}
			loadgraph();
		}
	}
}

$(document).ready(function(){
	setTimeout(forcegraphload, 15000);
});

function forcegraphload() {
	if ( graphloaded == 0 ) {
		if ( !(typeof boolDisplayHouseConsumption === "boolean") ) {
			showhidedataset('boolDisplayHouseConsumption');
		}
		if ( !(typeof boolDisplayLoad1 === "boolean") ) {
			showhidedataset('boolDisplayLoad1');
		}
		if ( !(typeof boolDisplayLp1Soc === "boolean") ) {
			showhidedataset('boolDisplayLp1Soc');
		}
		if ( !(typeof boolDisplayLp2Soc === "boolean") ) {
			showhidedataset('boolDisplayLp2Soc');
		}
		if ( !(typeof boolDisplayLoad2 === "boolean") ) {
			showhidedataset('boolDisplayLoad2');
		}
		if ( !(typeof boolDisplayLp1 === "boolean") ) {
			showhidedataset('boolDisplayLp1');
		}
		if ( !(typeof boolDisplayLp2 === "boolean") ) {
			showhidedataset('boolDisplayLp2');
		}
		if ( !(typeof boolDisplayLp3 === "boolean") ) {
			showhidedataset('boolDisplayLp3');
		}
		if ( !(typeof boolDisplayLp4 === "boolean") ) {
			showhidedataset('boolDisplayLp4');
		}
		if ( !(typeof boolDisplayLp5 === "boolean") ) {
			showhidedataset('boolDisplayLp5');
		}
		if ( !(typeof boolDisplayLp6 === "boolean") ) {
			showhidedataset('boolDisplayLp6');
		}
		if ( !(typeof boolDisplayLp7 === "boolean") ) {
			showhidedataset('boolDisplayLp7');
		}
		if ( !(typeof boolDisplayLp8 === "boolean") ) {
			showhidedataset('boolDisplayLp8');
		}
		if ( !(typeof boolDisplayLpAll === "boolean") ) {
			showhidedataset('boolDisplayLpAll');
		}
		if ( !(typeof boolDisplaySpeicherSoc === "boolean") ) {
			showhidedataset('boolDisplaySpeicherSoc');
		}
		if ( !(typeof boolDisplaySpeicher === "boolean") ) {
			showhidedataset('boolDisplaySpeicher');
		}
		if ( !(typeof boolDisplayEvu === "boolean") ) {
			showhidedataset('boolDisplayEvu');
		}
		if ( !(typeof boolDisplayPv === "boolean") ) {
			showhidedataset('boolDisplayPv');
		}
		if ( !(typeof boolDisplayLegend === "boolean") ) {
			showhidedataset('boolDisplayLegend');
		}
		checkgraphload();
	}
}  // end forcegraphload

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

function subscribeMqttGraphSegments() {
	for (var segments = 1; segments < 17; segments++) {
		topic = "openWB/graph/" + segments + "alllivevalues";
		client.subscribe(topic, {qos: 0});
	}
}

function unsubscribeMqttGraphSegments() {
	for (var segments = 1; segments < 17; segments++) {
		topic = "openWB/graph/" + segments + "alllivevalues";
		client.unsubscribe(topic);
	}
}
