function loadgraph() {
var lineChartData = {
	labels: atime,
	datasets: [{
		label: 'Lp1',
		borderColor: "rgba(0, 0, 255, 0.7)",
		backgroundColor: 'blue',
		borderWidth: 1,
		fill: false,
		data: alp1,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Lp2',
		borderColor: "rgba(50, 50, 55, 0.7)",
		backgroundColor: 'blue',
		borderWidth: 1,
		fill: false,
		hidden: boolDisplayLp2,
		data: alp2,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Bezug',
		borderColor: "rgba(255, 0, 0, 0.7)",
		backgroundColor: "rgba(255, 10, 13, 0.3)",
		borderWidth: 1,
		fill: true,
		data: abezug,
		hidden: boolDisplayEvu,
		yAxisID: 'y-axis-1',
	} , {
		label: 'PV',
		borderColor: 'green',
		backgroundColor: "rgba(10, 255, 13, 0.3)",
		fill: true,
		hidden: boolDisplayPv,
		borderWidth: 1,
		data: apv,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Speicherleistung',
		borderColor: 'orange',
		backgroundColor: "rgba(200, 255, 13, 0.3)",
		fill: true,
		borderWidth: 1,
		data: aspeicherl,
		hidden: boolDisplaySpeicher,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Speicher SoC',
		borderColor: 'orange',
		backgroundColor: "rgba(200, 255, 13, 0.5)",
		borderDash: [10,5],
		hidden: boolDisplaySpeicherSoc,
		fill: false,
		borderWidth: 1,
		data: aspeichersoc,
		yAxisID: 'y-axis-2',
	} , {
		label: 'LP1 SoC',
		borderColor: "rgba(0, 0, 255, 0.5)",
		borderDash: [10,5],
		borderWidth: 2,
		hidden: boolDisplayLp1Soc,
		fill: false,
		data: asoc,
		yAxisID: 'y-axis-2',
	} , {
		label: 'LP2 SoC',
		borderColor: "rgba(50, 50, 55, 0.5)",
		borderDash: [10,5],
		fill: false,
		borderWidth: 2,
		hidden: boolDisplayLp2Soc,
		data: asoc1,
		yAxisID: 'y-axis-2',
	} , {
		label: 'Hausverbrauch',
		borderColor: "rgba(150, 150, 150, 0.7)",
		backgroundColor: "rgba(200, 255, 13, 0.3)",
		fill: false,
		borderWidth: 2,
		hidden: boolDisplayHouseConsumption,
		data: ahausverbrauch,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Verbraucher 1',
		borderColor: "rgba(0, 150, 150, 0.7)",
		backgroundColor: "rgba(200, 255, 13, 0.3)",
		fill: false,
		borderWidth: 2,
		hidden: boolDisplayLoad1,
		data: averbraucher1,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Verbraucher 2',
		borderColor: "rgba(150, 150, 0, 0.7)",
		backgroundColor: "rgba(200, 255, 13, 0.3)",
		fill: false,
		borderWidth: 2,
		data: averbraucher2,
		hidden: boolDisplayLoad2,
		yAxisID: 'y-axis-1',
	} , {
		label: 'LP Gesamt',
		borderColor: "rgba(50, 50, 55, 0.1)",
		backgroundColor: "rgba(0, 0, 255, 0.1)",
		fill: false,
		borderWidth: 2,
		data: alpa,
		hidden: boolDisplayLpAll,
		yAxisID: 'y-axis-1',
	} , {
		label: 'Lp3',
		borderColor: "rgba(50, 50, 55, 0.7)",
		backgroundColor: 'blue',
		fill: false,
		borderWidth: 2,
		data: alp2,
		yAxisID: 'y-axis-1',
		hidden: boolDisplayLp3,
	} , {
		label: 'Lp4',
		borderColor: "rgba(50, 50, 55, 0.7)",
		backgroundColor: 'blue',
		fill: false,
		data: alp4,
		borderWidth: 2,
		yAxisID: 'y-axis-1',
		hidden: boolDisplayLp4,
	} , {
		label: 'Lp5',
		borderColor: "rgba(50, 50, 55, 0.7)",
		backgroundColor: 'blue',
		fill: false,
		borderWidth: 2,
		data: alp5,
		yAxisID: 'y-axis-1',
		hidden: boolDisplayLp5,
	} , {
		label: 'Lp6',
		borderColor: "rgba(50, 50, 55, 0.7)",
		backgroundColor: 'blue',
		fill: false,
		borderWidth: 2,
		data: alp6,
		yAxisID: 'y-axis-1',
		hidden: boolDisplayLp6,
	} , {
		label: 'Lp7',
		borderColor: "rgba(50, 50, 55, 0.7)",
		backgroundColor: 'blue',
		fill: false,
		borderWidth: 2,
		data: alp7,
		yAxisID: 'y-axis-1',
		hidden: boolDisplayLp7,
	} , {
		label: 'Lp8',
		borderColor: "rgba(50, 50, 55, 0.7)",
		backgroundColor: 'blue',
		fill: false,
		borderWidth: 2,
		data: alp8,
		yAxisID: 'y-axis-1',
		hidden: boolDisplayLp8,

	}]
};
	var ctx = document.getElementById('canvas').getContext('2d');
	window.myLine = Chart.Line(ctx, {
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
				mode: 'null',
			},
			stacked: false,
			legend: {
				display: boolDisplayLegend
			},
			title: {
				display: false
			},
			scales: {
				yAxes: [{
					type: 'linear', 
					display: true,
					position: 'left',
					id: 'y-axis-1',
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

				}],
			}
		}
	});
};			
function checkgraphload(){
	if (( boolDisplayHouseConsumption == true  ||  boolDisplayHouseConsumption == false) && (boolDisplayLoad1 == true || boolDisplayLoad1 == false ) && (boolDisplayLp1Soc == true || boolDisplayLp1Soc == false ) && (boolDisplayLp2Soc == true || boolDisplayLp2Soc == false ) && (boolDisplayLoad2 == true || boolDisplayLoad2 == false ) && (boolDisplayLp2 == true || boolDisplayLp2 == false ) && (boolDisplayLp3 == true || boolDisplayLp3 == false ) && (boolDisplayLp4 == true || boolDisplayLp4 == false ) && (boolDisplayLp5 == true || boolDisplayLp5 == false ) && (boolDisplayLp6 == true || boolDisplayLp6 == false ) && (boolDisplayLp7 == true || boolDisplayLp7 == false ) && (boolDisplayLp8 == true || boolDisplayLp8 == false ) && (boolDisplayLpAll == true || boolDisplayLpAll == false ) && (boolDisplaySpeicherSoc == true || boolDisplaySpeicherSoc == false ) && (boolDisplaySpeicher == true || boolDisplaySpeicher == false ) && (boolDisplayEvu == true || boolDisplayEvu == false ) && (boolDisplayPv == true || boolDisplayPv == false ) && (boolDisplayLegend == true || boolDisplayLegend == false ))  {
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
};
 window.onload = function(){
	    setTimeout(forcegraphload, 5000)
 };
function forcegraphload() {
	if ( graphloaded == 0 ) {
		loadgraph();
		graphloaded = 1;
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

