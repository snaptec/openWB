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
		    beforeSend: function(xhr){  xhr.overrideMimeType( "text/plain; charset=x-user-defined" );},
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
function visibility(datavar,hidevar,hidevalue,boolvar) {
	var vis=0;
	datavar.forEach(function(csvvar){
		if ( csvvar != 0 && typeof csvvar !== 'undefined'){
			vis=1;
		}
	});
	//window[overall] = ((oldcsvvar - firstcsvvar) / 1000).toFixed(2);
	if ( vis == 1 ){
		window[hidevar] = 'foo';
		window[boolvar] = 'flase';
	} else {
		window[hidevar] = hidevalue;
		window[boolvar] = 'true';
	}

}
function loadgraph() {

		alldata = alldata.replace(/^\s*[\n]/gm, '');
		alldata = alldata.replace(/^\s*-[\n]/gm, '');
		var csvData = new Array();
		var rawcsv = alldata.split(/\r?\n|\r/);
		for (var i = 0; i < rawcsv.length; i++) {
			  csvData.push(rawcsv[i].split(','));
		}
		csvData.pop();
		// Retrived data from csv file content
		var splittime = new Array();
		//getCol(csvData, 0).forEach(function(zeit){
		//	splittime.push(zeit.substring(0, zeit.length -3));
		//});
		//atime = splittime;
		atime = getCol(csvData, 0);
		abezug = getCol(csvData, 1);
		alpa = getCol(csvData, 2);
		apv = getCol(csvData, 3);
		alp1 = getCol(csvData, 4);
		alp2 = getCol(csvData, 5);
		alp3 = getCol(csvData, 6);
		alp4 = getCol(csvData, 7);
		alp5 = getCol(csvData, 8);
		alp6 = getCol(csvData, 9);
		alp7 = getCol(csvData, 10);
		alp8 = getCol(csvData, 11);
		aspeicherl = getCol(csvData, 12);
		aspeichersoc = getCol(csvData, 13);
		asoc = getCol(csvData, 14);
		asoc1 = getCol(csvData, 15);
		ahausverbrauch = getCol(csvData, 16);
		averbraucher1 = getCol(csvData, 17);
		averbraucher2 = getCol(csvData, 18);
		visibility(abezug,'hidebezug','Bezug',boolDisplayEvu);
		visibility(alpa,'hidelpa','LP Gesamd',boolDisplayEvu);
		visibility(apv,'hidepv','Bezug',boolDisplayLpAll);
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

		initialread = 1 ;
		//checkgraphload();
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
			yAxisID: 'y-axis-1',
		} , {
			label: 'Lp2',
			borderColor: "rgba(50, 30, 105, 0.7)",
			backgroundColor: "rgba(50, 30, 105, 0.7)",
			borderWidth: 1,
			hidden: boolDisplayLp2,
			fill: false,
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
		}  , {
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
			fill: true,
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
			data: alp3,
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
	}

	var ctx = document.getElementById('canvas').getContext('2d');

	window.myLine = new Chart.Line(ctx, {
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
				display: true,
				//display: boolDisplayLegend,
				labels: {
					// middle grey, opacy = 100% (visible)
					fontColor: "rgba(153, 153, 153, 1)",
					filter: function(item,chart) {
						if ( item.text.includes(hidehaus) || item.text.includes(hideload2) || item.text.includes(hideload1) || item.text.includes(hidelp2soc) || item.text.includes(hidelp1soc) || item.text.includes(hidelp1) || item.text.includes(hidelp2) || item.text.includes(hidelp3) || item.text.includes(hidelp4) || item.text.includes(hidelp5) || item.text.includes(hidelp6) || item.text.includes(hidelp7) || item.text.includes(hidelp8) || item.text.includes(hidespeichersoc) || item.text.includes(hidespeicher) || item.text.includes(hidelpa) || item.text.includes(hidepv) || item.text.includes(hidebezug) ) { return false } else { return true}
					}
				}
			},
			title: {
				display: false
			},
			scales: {
				xAxes: [
					{
         				ticks: {
							// middle grey, opacy = 100% (visible)
							fontColor: "rgba(153, 153, 153, 1)"
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
		        			labelString: 'Leistung [W]',
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
							// middle grey, opacy = 100% (visible)
							fontColor: "rgba(153, 153, 153, 1)"
						},
						gridLines: {
							// black, opacy = 0% (invisible)
							color: "rgba(0, 0, 0, 0)",
						},
						ticks: {
							min: 1,
							suggestedMax: 100,
							// middle grey, opacy = 100% (visible)
							fontColor: "rgba(153, 153, 153, 1)"
						}
					}
				]
			}
		}
	});
	initialread = 1;
	$('#waitforgraphloadingdiv').hide();
}  // end loadgraph
function checkgraphload(){
	if ( graphloaded == 1) {
       	myLine.destroy();
		loadgraph();
	} else {
		if (( boolDisplayHouseConsumption == true  ||  boolDisplayHouseConsumption == false) && (boolDisplayLoad1 == true || boolDisplayLoad1 == false ) && (boolDisplayLp1Soc == true || boolDisplayLp1Soc == false ) && (boolDisplayLp2Soc == true || boolDisplayLp2Soc == false ) && (boolDisplayLoad2 == true || boolDisplayLoad2 == false ) && (boolDisplayLp1 == true || boolDisplayLp1 == false ) && (boolDisplayLp2 == true || boolDisplayLp2 == false ) && (boolDisplayLp3 == true || boolDisplayLp3 == false ) && (boolDisplayLp4 == true || boolDisplayLp4 == false ) && (boolDisplayLp5 == true || boolDisplayLp5 == false ) && (boolDisplayLp6 == true || boolDisplayLp6 == false ) && (boolDisplayLp7 == true || boolDisplayLp7 == false ) && (boolDisplayLp8 == true || boolDisplayLp8 == false ) && (boolDisplayLpAll == true || boolDisplayLpAll == false ) && (boolDisplaySpeicherSoc == true || boolDisplaySpeicherSoc == false ) && (boolDisplaySpeicher == true || boolDisplaySpeicher == false ) && (boolDisplayEvu == true || boolDisplayEvu == false ) && (boolDisplayPv == true || boolDisplayPv == false ) && (boolDisplayLegend == true || boolDisplayLegend == false ))  {
			if ( initialread != 0 ) {
				if ( graphloaded == 0 ) {
					graphloaded += 1;
				} else {
		       		myLine.destroy();
				}
				loadgraph();
	 		}
		}
	}
}
