function loadHourlyConsumptionchart(labels, data) {
	/**
	 * creates chart for hourly consumption
	 *
	 * @function loadHourlyConsumptionchart
	 * @author Michael Ortenstein
	 * @param {object} priceTodayData as JSON object
	 * @param {object} priceTomorrowData as JSON object
	 */

	var ctxHourlyConsumptionchart = $('#consumptionchartCanvas')[0].getContext('2d');

	var config = {
		type: 'line',
		data: {
		  	labels: labels,
			datasets: [{
				yAxisID: 'y-axis-1',
				data: data,
				borderColor: "rgba(255, 155, 155, 0.9)",
				backgroundColor: "rgba(0, 0, 255, 0.7)",
				borderWidth: 2,
				fill: false
			}]
		},
		options: {
			tooltips: {
				enabled: true,
				mode: 'single',
                callbacks: {
                    label: function(tooltipItems, data) {
                        return tooltipItems.yLabel + ' kWh Tages-Gesamtverbrauch';
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
				xAxes: [
					{
					gridLines: {
							// light grey, opacy = 100% (visible)
							color: "rgba(204, 204, 204, 0.3)",
						},

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
						labelString: 'bezogene kWh',
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

					}]
			}
		}
	};

	var hourlyConsumptionchart = new Chart(ctxHourlyConsumptionchart, config);

}
