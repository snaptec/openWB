/**
 * Show the daily yield and consumption in a bar graph
 *
 * @author Claus Hagen
 */

class YieldMeter {
	bardata;
	xScale;
	yScale;
	svg;

	constructor() {
		this.width = 500;
		this.height = 500;
		this.margin = {
			top: 25, bottom: 30, left: 25, right: 0
		};
		this.labelfontsize = 16;
		this.axisFontSize = 12;
		this.textLength = 12;
	}

	// to be called when the document is loaded
	init() {
		const figure = d3.select("figure#energymeter");
		this.svg = figure.append("svg")
			.attr("viewBox", `0 0 500 500`);
		const style = getComputedStyle(document.body);
		this.houseColor = 'var(--color-house)';
		this.pvColor = 'var(--color-pv)';
		this.exportColor = 'var(--color-export)';
		this.evuColor = 'var(--color-evu)';
		this.bgColor = 'var(--color-bg)';
		this.chargeColor = 'var(--color-charging)';
		this.axisColor = 'var(--color-axis)';
		this.gridColor = 'var(--color-grid)';
		this.batColor = 'var(--color-battery)';
		d3.select("button#energyLeftButton")
			.on("click", shiftLeft)
		d3.select("button#energyRightButton")
			.on("click", shiftRight)
		d3.select("button#calendarButton")
			.on("click", toggleMonthView)
	}

	// to be called when values have changed
	update() {
		let importedEnergy = 0
		let exportedEnergy = 0
		let generatedEnergy = 0
		let batEnergy = 0
		let storedEnergy = 0
		switch (wbdata.graphMode) {
			case 'live':
				this.plotdata = Object.values(wbdata.sourceSummary)
					.filter(row => this.plotfilter(row))
					.concat(wbdata.usageDetails
						.filter(row => this.plotfilter(row)));
				if (wbdata.smartHomeSummary && wbdata.usageSummary.devices.energy > 0) {
					this.plotdata.push(wbdata.usageSummary.devices)
				}
				importedEnergy = wbdata.sourceSummary.evuIn.energy
				exportedEnergy = wbdata.usageSummary.evuOut.energy
				generatedEnergy = wbdata.sourceSummary.pv.energy
				batEnergy = wbdata.sourceSummary.batOut.energy
				storedEnergy = wbdata.usageSummary.batIn.energy
				break;
			case 'day':
				if (wbdata.showTodayGraph) {
					this.plotdata = Object.values(wbdata.sourceSummary)
						.filter(row => this.plotfilter(row));

					this.plotdata = this.plotdata.concat(wbdata.usageDetails
						.filter(row => this.plotfilter(row)));
					if (wbdata.smartHomeSummary && wbdata.usageSummary.devices.energy > 0) {
						this.plotdata.push(wbdata.usageSummary.devices)
					}
					importedEnergy = wbdata.sourceSummary.evuIn.energy
					exportedEnergy = wbdata.usageSummary.evuOut.energy
					generatedEnergy = wbdata.sourceSummary.pv.energy
					batEnergy = wbdata.sourceSummary.batOut.energy
					storedEnergy = wbdata.usageSummary.batIn.energy
				} else {
					this.plotdata = Object.values(wbdata.historicSummary)
						.filter(row => row.energy > 0 && row.name != "Geräte");
					if (wbdata.smartHomeSummary && wbdata.historicSummary.devices.energy > 0) {
						this.plotdata.push(wbdata.historicSummary.devices)
					}
					importedEnergy = wbdata.historicSummary.evuIn.energy
					exportedEnergy = wbdata.historicSummary.evuOut.energy
					generatedEnergy = wbdata.historicSummary.pv.energy
					batEnergy = wbdata.historicSummary.batOut.energy
					storedEnergy = wbdata.historicSummary.batIn.energy
				}
				break;
			case 'month':
			case 'year':
				this.plotdata = Object.values(wbdata.historicSummary)
					.filter(row => this.plotfilter(row));
				if (wbdata.smartHomeSummary && wbdata.historicSummary.devices.energy > 0) {
					this.plotdata.push(wbdata.historicSummary.devices)
				}
				importedEnergy = wbdata.historicSummary.evuIn.energy
				exportedEnergy = wbdata.historicSummary.evuOut.energy
				generatedEnergy = wbdata.historicSummary.pv.energy
				batEnergy = wbdata.historicSummary.batOut.energy
				storedEnergy = wbdata.historicSummary.batIn.energy

				break;
			default: break;
		}
		this.selfUsePercentage = Math.round((generatedEnergy - exportedEnergy) / generatedEnergy * 100)
		this.autarchyPercentage = Math.round((generatedEnergy + batEnergy - exportedEnergy - storedEnergy) / (generatedEnergy + batEnergy + importedEnergy - exportedEnergy - storedEnergy) * 100)
		this.adjustLabelSize()
		const svg = this.createOrUpdateSvg();
		this.drawChart(svg);
		this.updateHeading();
	};

	plotfilter(row) {
		if (row instanceof ChargePoint && !wbdata.showCpEnergyDetails) {
			return false
		} else {
			if (row.energy > 0) {
				switch (row.name) {
					case "Geräte": return (wbdata.smartHomeSummary)
					case "Laden": return (wbdata.showCpEnergySummary)
					default: return true
				}
			}
		}
	}
	createOrUpdateSvg() {
		this.svg.selectAll("*").remove();
		const g = this.svg.append("g")
			.attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
		this.xScale = d3.scaleBand()
			.range([0, this.width - this.margin.left - this.margin.right])
			.padding(0.4);
		this.yScale = d3.scaleLinear()
			.range([this.height - this.margin.bottom - this.margin.top, 10]);
		return g;
	}

	drawChart(svg) {
		let chargedata = this.plotdata.filter(d => d.name == "Laden")
		const ymax = d3.max(this.plotdata, (d) => d.energy);
		this.xScale.domain(this.plotdata.map((d) => d.name));
		this.yScale.domain([0, Math.ceil(ymax)]);
		// Draw the bars
		const bargroups = svg
			.selectAll(".bar")
			.data(this.plotdata)
			.enter()
			.append("g");
		bargroups
			.append("rect")
			.attr("class", "bar")
			.attr("x", (d) => this.xScale(d.name))
			.attr("y", (d) => this.yScale(d.energy))
			.attr("width", this.xScale.bandwidth())
			.attr("height", (d) => (this.height - this.yScale(d.energy) - this.margin.top - this.margin.bottom))
			.attr("fill", (d) => d.color);
		if (wbdata.graphMode != 'live') {
			// Display the PV Charging inner bar
			bargroups
				.append("rect")
				.attr("class", "bar")
				.attr("x", (d) => this.xScale(d.name) + this.xScale.bandwidth() / 6)
				.attr("y", (d) => this.yScale(d.energyPv))
				.attr("width", this.xScale.bandwidth() * 2 / 3)
				.attr("height", (d) => (this.height - this.yScale(d.energyPv) - this.margin.top - this.margin.bottom))
				.attr("fill", this.pvColor)
				.attr("fill-opacity", "66%");
			// Display the Bat Charging inner bar
			bargroups.append("rect")
				.attr("class", "bar")
				.attr("x", (d) => this.xScale(d.name) + this.xScale.bandwidth() / 6)
				.attr("y", (d) => this.yScale(d.energyBat + d.energyPv))
				.attr("width", this.xScale.bandwidth() * 2 / 3)
				.attr("height", (d) => (this.height - this.yScale(d.energyBat) - this.margin.top - this.margin.bottom))
				.attr("fill", this.batColor)
				.attr("fill-opacity", "66%");
		}
		const yAxisGenerator = d3.axisLeft(this.yScale)
			.tickFormat((d, i) => {
				if (wbdata.graphMode == 'year' || wbdata.graphMode == 'month') {
					return ((d == 0) ? "" : (Math.round(d / 100) / 10))
				} else {
					return ((d == 0) ? "" : d)
				}
			})
			.ticks(8)
			.tickSizeInner(-this.width);

		const yAxis = svg.append("g")
			.attr("class", "axis")
			.attr("transform", "translate(0," + 0 + ")")
			.call(yAxisGenerator);

		yAxis.append("text")
			.attr("y", 6)
			.attr("dy", "0.71em")
			.attr("text-anchor", "end")
			.text("energy");

		yAxis.selectAll(".tick").attr("font-size", this.axisFontSize);
		if (wbdata.showGrid) {
			yAxis.selectAll(".tick line")
				.attr("stroke", this.gridColor)
				.attr("stroke-width", "0.5");
		} else {
			yAxis.selectAll(".tick line").attr("stroke", this.bgColor);
		}
		yAxis.select(".domain")
			.attr("stroke", this.bgcolor);

		svg.append("text")
			.attr("x", -this.margin.left)
			.attr("y", -15)
			.style("fill", this.axisColor)
			.attr("font-size", this.axisFontSize)
			.text((wbdata.graphMode == 'month' || wbdata.graphMode == 'year') ? "MWh" : "kWh")
			;

		// add value labels to the bars
		const labels = svg.selectAll(".label")
			.data(this.plotdata)
			.enter()
			.append("g");
		labels
			.append("text")
			.attr("x", (d) => this.xScale(d.name) + this.xScale.bandwidth() / 2)
			.attr("y", (d) => {
				if (wbdata.graphMode != 'live' && ((d.pvPercentage > 0) || (d.name == 'Netz') || (d.name == 'PV'))) {
					return this.yScale(d.energy) - 25
				} else {
					return this.yScale(d.energy) - 10
				}
			})
			.attr("font-size", this.labelfontsize)
			.attr("text-anchor", "middle")
			.attr("fill", (d) => d.color)
			.text((d) => (formatWattH(d.energy * 1000)));
		if (wbdata.graphMode != 'live') {
			// add a PV percentage tag to the charging bar
			labels.append("text")
				.attr("x", (d) => this.xScale(d.name) + this.xScale.bandwidth() / 2)
				.attr("y", (d) => this.yScale(d.energy) - 10)
				.attr("font-size", this.labelfontsize - 2)
				.attr("text-anchor", "middle")
				.attr("fill", (d) => this.subColor(d))
				.text((d) => this.subString(d));
		}
		// Add category labels
		labels
			.append("text")
			.attr("x", (d) => this.xScale(d.name) + this.xScale.bandwidth() / 2)
			.attr("y", this.height - this.margin.bottom - 5)
			.attr("font-size", (d) => (d.icon.length <= 2) ? this.labelfontsize + 3 : this.labelfontsize)
			.attr("text-anchor", "middle")
			.attr("fill", (d) => d.color)
			.text((d) => (this.truncateCategory(d.icon)))
			.classed("fas", (d) => d.icon.length <= 2);
	}

	subString(item) {
		if (item.pvPercentage > 0) {
			return ("Aut: " + item.pvPercentage.toLocaleString(undefined) + " %");
		} else if (item.name == 'Netz') {
			return ("Aut: " + this.autarchyPercentage.toLocaleString(undefined) + " %");

		} else if (item.name == 'PV') {
			return ("Eigen: " + this.selfUsePercentage.toLocaleString(undefined) + " %")
		} else {
			return "";
		}
	}
	subColor(item) {
		if (item.name == 'Netz' || item.name == 'PV') {
			return (this.axisColor)
		} else {
			return (this.pvColor)
		}
	}
	updateHeading() {
		var heading = "Energie ";

		switch (wbdata.graphMode) {
			case 'live':
				heading = heading + " heute";
				break;
			case 'day':
				if (wbdata.showTodayGraph) {
					heading = heading + " heute";
				} else {
					heading = heading + wbdata.graphDate.getDate() + "." + (wbdata.graphDate.getMonth() + 1) + ".";
				}
				break;
			case 'month':
				heading = heading + formatMonth(wbdata.graphMonth.month, wbdata.graphMonth.year);
				break;
			case 'year':
				heading = heading + " " + wbdata.graphYear;
			default: break;
		}
		d3.select("h3#energyheading").text(heading);
	}

	adjustLabelSize() {
		let xCount = this.plotdata.length
		if (xCount <= 5) {
			this.maxTextLength = 12;
			this.labelfontsize = 16
		} else if (xCount == 6) {
			this.maxTextLength = 11;
			this.labelfontsize = 14
		} else if (xCount > 6 && xCount <= 8) {
			this.maxTextLength = 8;
			this.labelfontsize = 13
		} else if (xCount == 9) {
			this.maxTextLength = 8;
			this.labelfontsize = 11;
		} else if (xCount == 10) {
			this.maxTextLength = 7;
			this.labelfontsize = 10;
		}
		else {
			this.maxTextLength = 6;
			this.labelfontsize = 9
		}
	}

	truncateCategory(name) {
		if (name.length > this.maxTextLength) {
			return name.substr(0, this.maxTextLength) + "."
		} else {
			return name
		}
	}
}



var yieldMeter = new YieldMeter();

