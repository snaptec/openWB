var awattartime = [];
var graphawattarprice;
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
var all1 = 0;
var all2 = 0;
var all3 = 0;
var all4 = 0;
var all5 = 0;
var all6 = 0;
var all7 = 0;
var all8 = 0;
var all1p;
var all2p;
var all3p;
var all4p;
var all5p;
var all6p;
var all7p;
var all8p;
var hidehaus;
var myLine;

function loadgraph() {
	var lineChartData = {
		labels: atime,
		datasets: [{
			label: 'Lp1',
			borderColor: "rgba(0, 0, 255, 0.7)",
			backgroundColor: "rgba(0, 0, 255, 0.7)",
			borderWidth: 2,
			hidden: boolDisplayLp1,
			fill: false,
			lineTension: 0.2,
			data: alp1,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Lp2',
			borderColor: "rgba(50, 30, 105, 0.7)",
			backgroundColor: "rgba(50, 30, 105, 0.7)",
			borderWidth: 2,
			hidden: boolDisplayLp2,
			fill: false,
			lineTension: 0.2,
			data: alp2,
			yAxisID: 'y-axis-1'
		} , {
			label: 'EVU',
			borderColor: "rgba(255, 0, 0, 0.7)",
			backgroundColor: "rgba(255, 10, 13, 0.3)",
			borderWidth: 1,
			fill: true,
			lineTension: 0.2,
			data: abezug,
			hidden: boolDisplayEvu,
			yAxisID: 'y-axis-1'
		} , {
			label: 'PV',
			borderColor: 'green',
			backgroundColor: "rgba(10, 255, 13, 0.3)",
			fill: true,
			lineTension: 0.2,
			hidden: boolDisplayPv,
			borderWidth: 1,
			data: apv,
			yAxisID: 'y-axis-1'
		}  , {
			label: 'Speicher',
			borderColor: 'orange',
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: true,
			lineTension: 0.2,
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
			lineTension: 0.2,
			borderWidth: 2,
			data: aspeichersoc,
			yAxisID: 'y-axis-2'
		} , {
			label: 'LP1 SoC',
			borderColor: "rgba(0, 0, 255, 0.5)",
			borderDash: [10,5],
			borderWidth: 2,
			hidden: boolDisplayLp1Soc,
			fill: false,
			lineTension: 0.2,
			data: asoc,
			yAxisID: 'y-axis-2'
		} , {
			label: 'LP2 SoC',
			borderColor: "rgba(50, 50, 55, 0.5)",
			borderDash: [10,5],
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			hidden: boolDisplayLp2Soc,
			data: asoc1,
			yAxisID: 'y-axis-2'
		} , {
			label: 'Hausverbrauch',
			borderColor: "rgba(255,255,204,0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			hidden: boolDisplayHouseConsumption,
			data: ahausverbrauch,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Verbraucher 1',
			borderColor: "rgba(0, 150, 150, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			hidden: boolDisplayLoad1,
			data: averbraucher1,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Verbraucher 2',
			borderColor: "rgba(150, 150, 0, 0.7)",
			backgroundColor: "rgba(200, 255, 13, 0.3)",
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: averbraucher2,
			hidden: boolDisplayLoad2,
			yAxisID: 'y-axis-1'
		} , {
			label: 'LP Gesamt',
			borderColor: "rgba(50, 50, 55, 0.1)",
			backgroundColor: "rgba(0, 0, 255, 0.1)",
			fill: true,
			lineTension: 0.2,
			borderWidth: 2,
			data: alpa,
			hidden: boolDisplayLpAll,
			yAxisID: 'y-axis-1'
		} , {
			label: 'Lp3',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: alp3,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp3
		} , {
			label: 'Lp4',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			lineTension: 0.2,
			data: alp4,
			borderWidth: 2,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp4
		} , {
			label: 'Lp5',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: alp5,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp5
		} , {
			label: 'Lp6',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: alp6,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp6
		} , {
			label: 'Lp7',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: alp7,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp7
		} , {
			label: 'Lp8',
			borderColor: "rgba(50, 50, 55, 0.7)",
			backgroundColor: 'blue',
			fill: false,
			lineTension: 0.2,
			borderWidth: 2,
			data: alp8,
			yAxisID: 'y-axis-1',
			hidden: boolDisplayLp8
		}]
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
			responsive: true,
			maintainAspectRatio: false,
			hover: {
				mode: 'null'
			},
			stacked: false,
			legend: {
				display: boolDisplayLegend,
				labels: {
					fontColor: "rgba(255, 255, 255, 0.82)",
					filter: function(item,chart) {
						if ( item.text.includes(hidehaus) || item.text.includes(hideload2) || item.text.includes(hideload1) || item.text.includes(hidelp2soc) || item.text.includes(hidelp1soc) || item.text.includes(hidelp1) || item.text.includes(hidelp2) || item.text.includes(hidelp3) || item.text.includes(hidelp4) || item.text.includes(hidelp5) || item.text.includes(hidelp6) || item.text.includes(hidelp7) || item.text.includes(hidelp8) || item.text.includes(hidespeichersoc) || item.text.includes(hidespeicher) || item.text.includes(hidelpa) || item.text.includes(hidepv) || item.text.includes(hideevu) ) { return false } else { return true}
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
							color: "rgba(255, 255, 255, 0.1)"
						},
         				ticks: {
							fontColor: "rgba(255, 255, 255, 0.82)",
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
							fontColor: "rgba(255, 255, 255, 0.82)"
		      			},
						gridLines: {
							color: "rgba(255, 255, 255, 0.82)"
						},
						ticks: {
							stepSize: 0.2,
							maxTicksLimit: 10,
							fontColor: "rgba(255, 255, 255, 0.82)"
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
							fontColor: "rgba(255, 255, 255, 0.82)"
						},
						gridLines: {
							// black, opacy = 0% (invisible)
							color: "rgba(0, 0, 0, 0)",
						},
						ticks: {
							min: 0,
							suggestedMax: 100,
							fontColor: "rgba(255, 255, 255, 0.82)"
						}
					}
				]
			}
		}
	});
	initialread = 1;
	$('#waitforgraphloadingdiv').hide();
}  // end loadgraph

function putgraphtogether() {
	if ( (all1 == 1) && (all2 == 1) && (all3 == 1) && (all4 == 1) && (all5 == 1) && (all6 == 1) && (all7 == 1) && (all8 == 1) ){
		var alldata = all1p + "\n" + all2p + "\n" + all3p + "\n" + all4p + "\n" + all5p + "\n" + all6p + "\n" + all7p + "\n" + all8p;
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
		initialread = 1 ;

		// after receipt of all 8 first data segments, unsubscribe from these topics to save bandwidth
		unsubscribeMqttGraphSegments();

		checkgraphload();
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

window.onload = function(){
	setTimeout(forcegraphload, 15000)
}

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
	for (var segments = 1; segments < 9; segments++) {
		topic = "openWB/graph/" + segments + "alllivevalues";
		client.subscribe(topic, {qos: 0});
	}
}

function unsubscribeMqttGraphSegments() {
	for (var segments = 1; segments < 9; segments++) {
		topic = "openWB/graph/" + segments + "alllivevalues";
		client.unsubscribe(topic);
	}
}
