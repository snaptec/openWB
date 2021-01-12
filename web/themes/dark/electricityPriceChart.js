function loadElectricityPriceChart() {
	var electricityPriceChartData = {
		labels: electricityPriceTimeline,
		datasets: [{
			yAxisID: 'y-axis-0',
			data: electricityPriceChartline,
			borderColor: "rgba(255, 155, 155, 0.9)",
			backgroundColor: "rgba(0, 0, 255, 0.7)",
			borderWidth: 2,
			fill: false,
			steppedLine: true
		}]
	}

	var ctxa = $('#electricityPriceChartCanvas')[0].getContext('2d');

	window.AwattarLine = new Chart.Line(ctxa, {
		data: electricityPriceChartData,
		options: {
			tooltips: {
				enabled: true
			},
			responsive: true,
			maintainAspectRatio: false,
			hover: {
				mode: 'null'
			},
			stacked: false,
			legend: {
				display: false
			},
			title: {
				display: false
			},
			scales: {
				xAxes: [
					{
					gridLines: {
							// light grey, opacy = 100% (visible)
							color: "rgba(204, 204, 204, 1)",
						},

					ticks: {
							// middle grey, opacy = 100% (visible)
							fontColor: "rgba(153, 153, 153, 1)"
					}
				}],
				yAxes: [{
					// values price
					position: 'left',
					id: 'y-axis-0',
					type: 'linear',
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'Strompreis [Cent/kWh]',
						fontColor: "rgba(153, 153, 153, 1)"
					},
					gridLines: {
						color: "rgba(204, 204, 204, 1)",
					},
					ticks: {
						fontColor: "rgba(153, 153, 153, 1)"
					}
				}]
			},
			plugins:{
						annotation: {
			        annotations: [{
			            type: 'line',
			            mode: 'horizontal',
			            scaleID: 'x-axis-1',
			            value: 26,
			            borderColor: 'tomato',
			            borderWidth: 4
			        }],
			        drawTime: "afterDraw" // (default)
			    }
			}
		}
	});
}
