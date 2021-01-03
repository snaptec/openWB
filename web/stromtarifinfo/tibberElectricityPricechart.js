function loadElectricityPricechart(priceDataToday, priceDataTomorrow) {
	/**
	 * creates chart for price information
	 * chart starts today at current hour and includes tomorrows data if available
	 *
	 * @function loadElectricityPricechart
	 * @author Michael Ortenstein
	 * @param {object} priceTodayData as JSON object
	 * @param {object} priceTomorrowData as JSON object
	 */

	var labels = [];
	var data = [];

	// get current timestamp but at full hour
	var now = new Date;
	now.setMinutes(0, 0, 0);

	// chart should beginn at current hour, so
	// copy only prices at or after full hour in arrays for the chart
	for (i=0; i<priceDataToday.length; i++) {
		var startsAtDate = new Date(priceDataToday[i].startsAt);
		if (startsAtDate.valueOf() >= now.valueOf()){
			data.push((priceDataToday[i].total*100).toFixed(2));
			labels.push(createXLabel(priceDataToday[i].startsAt));
		}
	}
	for (i=0; i<priceDataTomorrow.length; i++) {
		data.push((priceDataTomorrow[i].total*100).toFixed(2));
		labels.push(createXLabel(priceDataTomorrow[i].startsAt));
	}

	var ctxElectricityPricechart = $('#electricityPricechartCanvas')[0].getContext('2d');

	var config = {
		type: 'line',
		data: {
		  	labels: labels,
			datasets: [{
				label: 'Strompreis Cent/kWh',
				yAxisID: 'y-axis-1',
				data: data,
				borderColor: "rgba(255, 155, 155, 0.9)",
				backgroundColor: "rgba(0, 0, 255, 0.7)",
				borderWidth: 2,
				fill: false,
				steppedLine: true
			}]
		},
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
						labelString: 'Preis Cent/kWh',
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

	var priceChart = new Chart(ctxElectricityPricechart, config);

}  // end loadElectricityPricechart
