var hourlyConsumptionchart;

function loadHourlyConsumptionchart(labels, dataConsumption, dataPrice) {
	/**
	 * creates chart for hourly consumption
	 *
	 * @function loadHourlyConsumptionchart
	 * @author Michael Ortenstein
	 * @param {array} labels is time
	 * @param {array} dataConsumption is hourly consumption
	 * @param {array} dataPrice is hourly price
	 */

	var ctxHourlyConsumptionchart = $('#consumptionchartCanvas')[0].getContext('2d');

	var config = {
		type: 'line',
		data: {
		  	labels: labels,
			datasets: [{
				yAxisID: 'y-axis-left',
				data: dataPrice,
				borderColor: 'rgba(201, 38, 38, 1)',
				backgroundColor: 'rgba(30, 33, 194, 0.7)',
				borderWidth: 2,
				fill: false,
				steppedLine: true
			}, {
				yAxisID: 'y-axis-right',
				data: dataConsumption,
				type: 'bar',
				borderColor: 'rgba(5, 85, 111, 0.5)',
				backgroundColor: 'rgba(172, 231, 250, 0.75)',
				borderWidth: 2,
			}]
		},
		options: {
			tooltips: {
				enabled: true,
				mode: 'nearest',
				intersect: true,
                callbacks: {
                    label: function(tooltipItem, data) {
						let i = tooltipItem.index;
                        return data.datasets[1].data[i] + ' kWh bezogen zu ' + data.datasets[0].data[i] + ' ct/kWh';
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
				display: false
			},
			title: {
				display: false
			},
			scales: {
				xAxes: [{
					gridLines: {
						color: 'rgba(204, 204, 204, 0.3)',
					},
					ticks: {
						fontColor: 'rgba(153, 153, 153, 1)'
					}
				}],
				yAxes: [{
					// values consumption
					id: 'y-axis-right',
					position: 'right',
					type: 'linear',
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'bezogene Energie [kWh]',
						fontColor: 'rgba(153, 153, 153, 1)'
					},
					gridLines: {
						color: 'rgba(204, 204, 204, 1)',
					},
					ticks: {
						fontColor: 'rgba(153, 153, 153, 1)',
						fontSize: 15
					}
				}, {
					// values price
					id: 'y-axis-left',
					position: 'left',
					type: 'linear',
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'stündl. Preis [ct/kWh]',
						fontColor: 'rgba(153, 153, 153, 1)'
					},
					gridLines: {
						display: false,
					},
					ticks: {
						fontColor: 'rgba(153, 153, 153, 1)',
						fontSize: 15
					}
				}]
			}
		}
	};

	if (hourlyConsumptionchart) {
		// if chart exists refresh chart with new data
		hourlyConsumptionchart.data.datasets[0].data = dataPrice;
		hourlyConsumptionchart.data.datasets[1].data = dataConsumption;
		hourlyConsumptionchart.data.labels = labels;
		//finally update chart var:
		hourlyConsumptionchart.update();
	} else {
		// create new chart from data
		hourlyConsumptionchart = new Chart(ctxHourlyConsumptionchart, config);
	}
}
