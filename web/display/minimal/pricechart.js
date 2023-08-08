class PriceChart {

	constructor() {
		this.width = 400;
		this.height = 80;
		this.margin = { top: 5, bottom: 15, left: 30, right: 20 };
	}

	// initialize when application is loaded
	init() {
		const figure = d3.select("figure#priceChart");
		this.svg = figure.append("svg").attr("viewBox", `0 0 400 80`);
		this.bgColor = 'var(--color-bg)';
		this.gridColor = 'var(--color-grid)';
		this.axisColor = 'var(--color-axis)';
		this.chargeColor = 'var(--color-charging)';
		this.noChargeColor = 'var(--color-axis)';
		etPriceList = '';
	}

	// update the view
	update() {
		var svg = this.createOrUpdateSvg();
		if (etPriceList != "") {
			this.plotdata = etPriceList.split(/\r?\n|\r/);        // split into lines
			this.plotdata.shift();                                // remove first line
			this.plotdata = this.plotdata.map((line, i) => {      // split lines into tuples [time,price]
				return line.split(',')
		}) .map(line => [line[0] * 1000, +line[1]]);              // multiply timestamps by 1000
			this.drawGraph(svg);
		}
	}

	// clear the display area
	createOrUpdateSvg() {
		this.svg.selectAll("*").remove();
		const g = this.svg.append("g").attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
		return g
	}

	// draw the graph
	drawGraph(svg) {
		let etMaxPriceMax = Math.max.apply(null, etMaxPricesFinal);
		let etMaxPriceMin = Math.min.apply(null, etMaxPricesFinal);

		const height = this.height - this.margin.top - this.margin.bottom;
		const width = this.width - this.margin.left - this.margin.right;
		const barwidth = width / this.plotdata.length - 1;

		const xdomain = d3.extent(this.plotdata, (d) => d[0]);
		const ydomain = d3.extent(this.plotdata, (d) => d[1]);

		xdomain[1] = xdomain[1] + 3600000;
		ydomain[0] = Math.min(ydomain[0], etMaxPriceMin, 0);
		ydomain[1] = Math.max(ydomain[1], etMaxPriceMax);
		ydomain[1] = Math.floor(ydomain[1] + 1);

		this.xScale = d3.scaleTime().range([0, width]).domain(xdomain);
		this.yScale = d3.scaleLinear().range([height, 0]).domain(ydomain);

		const bargroups = svg.selectAll("bar").data(this.plotdata).enter().append("g");
		bargroups.append("rect")
					.attr("class", "bar")
					.attr("x", (d) => this.xScale(d[0]))
					.attr("y", (d) => this.yScale(d[1]))
					.attr("width", barwidth)
					.attr("height", (d) => height - this.yScale(d[1]))
					.attr("fill", (d) => (d[1] <= etMaxPriceMax) ? this.chargeColor : this.noChargeColor);

		const generators = [];
		const points = [];
		const paths = [];
		const lineColors = ["orange", "#FF4500"];
		for (let i = 0; i < etModes.length; i++) {
			if (etModes[i] != 0) {
				// Line for max price
				generators[i] = d3.line();
				points[i] = [[0, this.yScale(etMaxPricesFinal[i])], [width, this.yScale(etMaxPricesFinal[i])]];
				paths[i] = generators[i](points[i]);
				svg.append("path").attr('d', paths[i]).attr("stroke", lineColors[i]);
			}
		}

		// X Axis
		const xAxisGenerator = d3.axisBottom(this.xScale)
									.ticks(4)
									.tickFormat(d3.timeFormat("%H:%M"));
		const xAxis = this.svg.append("g").attr("class", "axis").call(xAxisGenerator);
		xAxis.attr("transform", "translate(" + this.margin.left + "," + (height + this.margin.top) + ")");
		xAxis.selectAll(".tick").attr("font-size", 8).attr("color", "white");

		// Y Axis
		const yAxisGenerator = d3.axisLeft(this.yScale)
									.ticks(6)
									.tickSizeInner(-(this.width - this.margin.right - this.margin.left))
									.tickFormat((d) => d);

		const yAxis = this.svg.append("g").attr("class", "axis").call(yAxisGenerator);
		yAxis.attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
		yAxis.selectAll(".tick").attr("font-size", 8).attr("color", "white");
		yAxis.selectAll(".tick line").attr("stroke", this.bgColor).attr("stroke-width", "0.5");
		yAxis.select(".domain").attr("stroke", this.bgColor);
	}
}

function updateSetPriceLabels() {
	if (etEnabled == 1) { // show dynamic prices		
		if (configuredChargePoints == 1) { // not a DUO
			$('#etCombineSelection').addClass("hide");
			$('#etPriceSetLp2').addClass("hide");
			if (etModes[0] == 0) {  // price based charging disabled
				$('#etPriceSetLp1').addClass("hide");
			} else { // etModeLp1 != 0
				$('#etPriceSetLp1').removeClass("hide");
				if (etModes[0] == 1) { // global price based charging
					$('label[for="maxPriceLp1"].maxPriceLabelName').text("max. Preis (G):");
					etMaxPricesFinal[0] = etMaxPriceGlobal;
				} else { // individual price based charging
					$('label[for="maxPriceLp1"].maxPriceLabelName').text("max. Preis (L):");
					etMaxPricesFinal[0] = etMaxPricesLocal[0];
				}
			}
		} else { // configuredChargePoints > 1 i.e. DUO			
			if (etModes[0] == 1 && etModes[1] == 1) { // global price based charging on both -> only one selector
				$('#etPriceSetLp1').removeClass("hide");
				$('#etPriceSetLp2').addClass("hide");
				$('label[for="maxPriceLp1"].maxPriceLabelName').text("Global:");
				etMaxPricesFinal[0] = etMaxPriceGlobal;
			} else {
				if (etModes[0] != 0 && etModes[1] != 0) {
					$('#etCombineSelection').removeClass("hide");
				} else {
					$('#etCombineSelection').addClass("hide");
				}
				for (let i = 0; i < etModes.length; i++) {
					let ipp = i + 1;
					if (etModes[i] == 0) { // price based charging disabled			
						$('#etPriceSetLp' + ipp).addClass("hide");
					} else { // etModeLp1 != 0
						$('#etPriceSetLp' + ipp).removeClass("hide");
						if (etModes[i] == 1) { // global price based charging
							$('label[for="maxPriceLp' + ipp + '"].maxPriceLabelName').text("LP" + ipp + " (G):");
							etMaxPricesFinal[i] = etMaxPriceGlobal;
						} else { // individual price based charging
							$('label[for="maxPriceLp' + ipp + '"].maxPriceLabelName').text("LP" + ipp + " (L):");
							etMaxPricesFinal[i] = etMaxPricesLocal[i];
						}
					}
				}				
			}			
		}
		for (let i = 0; i < Math.min(etModes.length, configuredChargePoints); i++) {
			let ipp = i + 1;
			$('label[for="maxPriceLp' + ipp + '"].maxPriceLabelValue').text(etMaxPricesFinal[i] + " ct");
			if ($('#maxPriceLp' + ipp).val() != etMaxPricesFinal[i]) {
				$('#maxPriceLp' + ipp).val(etMaxPricesFinal[i]);
			}
		}
	}
	priceChart.update();
}

function updateMainPriceLabels() {
	let identifyer = "";
	if (showPrice == 1) {  // if price display is off, none of these will exist
		$('#currentPrice').removeClass("hide");
		$('#etsetprice').removeClass("hide");
		if (etEnabled == 1) { // show dynamic prices
			$('#currentPrice').html("Preis: " + etCurrentPrice + " ct/kWh");
			if (configuredChargePoints == 1) { // not a DUO				
				$('#etPriceLimitLp2').addClass("hide");
				if (etModes[0] == 0) {  // price based charging disabled
					$('#etPriceLimitLp1').addClass("hide");
				} else { // etModeLp1 != 0
					$('#etPriceLimitLp1').removeClass("hide");
					if (etModes[0] == 1) {
						etMaxPricesFinal[0] = etMaxPriceGlobal;
					} else {
						etMaxPricesFinal[0] = etMaxPricesLocal[0];
					}
					$('#etPriceLimitLp1').html("Limit: " + etMaxPricesFinal[0] + " ct/kWh");
				}
			} else { // configuredChargePoints > 1 i.e. DUO
				if (etModes[0] == 1 && etModes[1] == 1) { // global price based charging on both -> only one selector
					$('#etPriceLimitLp1').removeClass("hide");
					$('#etPriceLimitLp2').addClass("hide");
					$('#etPriceLimitLp1').html("Limit: " + etMaxPriceGlobal + " ct/kWh");
				} else {
					for (let i = 0; i < etModes.length; i++) {
						let ipp = i + 1;
						if (etModes[i] == 0) { // price based charging disabled
							$('#etPriceLimitLp' + ipp).addClass("hide");
						} else { // etMode != 0
							$('#etPriceLimitLp' + ipp).removeClass("hide");
							if (etModes[i] == 1) {
								etMaxPricesFinal[i] = etMaxPriceGlobal;
							} else {
								etMaxPricesFinal[i] = etMaxPricesLocal[i];
							}
							$('#etPriceLimitLp' + ipp).html("Limit LP" + ipp + ": " + etMaxPricesFinal[i] + " ct/kWh");
						}
					}
				}
			}
			for (let i = 0; i < Math.min(etModes.length, configuredChargePoints); i++) {
				let ipp = i + 1;
				if ( etCurrentPrice > etMaxPricesFinal[i] ) {
					$('#etPriceLimitLp' + ipp).addClass('text-danger');
				} else {			
					$('#etPriceLimitLp' + ipp).removeClass('text-danger');
				}
			}
		} else { // we show preset value
			$('#etPriceLimitLp1').addClass("hide");
			$('#etPriceLimitLp2').addClass("hide");
			$('#etsetprice').addClass("hide");
			$('#currentPrice').html("Preis: " + parseFloat(defaultPrice).toFixed(2) + " ct/kWh");
		}
	}
}

var priceChart = new PriceChart();
