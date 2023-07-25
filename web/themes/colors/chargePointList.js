/** 
 * List the configured chargepoints and their key data
 * 
 */

class ChargePointList {
	tbody;
	footer;

	constructor() {
		this.chargepoints = [];
		this.phaseSymbols = ['/', '\u2460', '\u2461', '\u2462']
		this.headers = ["Ladepunkt", "Parameter", "geladen", "Stand"];
		this.manualSoc = 0;
	};

	// initialize after document is created
	init() {
		const div = d3.select("div#chargePointTable")
		const table = div.append("table")
			.attr("class", "table table-borderless p-0 m-0");

		table.append("thead")
			.append("tr")
			.selectAll("headers")
			.data(this.headers).enter()
			.append("th")
			.attr("class", "tablecell")
			// .style("color", "white")
			.style("text-align", (data, i) => (i == 0) ? "left" : "center")
			//.classed ("tablecell", true)
			//.classed ("px-1", true)
			.text((data) => data)
			;

		this.tbody = table.append("tbody");
		this.footer = div.append("div");
		this.fgColor = "var(--color-fg)";
	}

	// update if data has changed
	update() {
		this.updateValues();
		this.tbody.selectAll("*").remove();
		this.footer.selectAll("*").remove();

		const chargePoint = this.tbody
			.selectAll("rows")
			.data(this.chargepoints).enter()
			;
		const rows = chargePoint.append("tr")
			.style("color", "var(--color-fg)")
			.style("text-align", "center")
			.style("vertical-align", "middle");

		rows.append((row) => this.cpNameButtonCell(row));
		rows.append((row) => this.cpChargeParamCell(row));
		rows.append((row) => this.cpChargeDataCell(row));
		rows.append((row) => this.cpSocButtonCell(row));

		if (wbdata.isEtEnabled) {
			this.footer.append('p')
				.attr("class", "pt-3 pb-0 m-0")
				.style("text-align", "center")
				.text("Aktueller Strompreis: " + wbdata.etPrice + " ct/kWh");
		}

		d3.select("div#chargePointConfigWidget").classed("hide", (wbdata.chargeMode != "0" && wbdata.chargeMode != "1"))
	}

	updateValues() {
		this.chargepoints = wbdata.chargePoint.filter(cp => cp.configured);
	}

	cpNameButtonCell(row) {
		const cell = d3.create("td")
			.attr("class", "tablecell px-1 py-1")
			.style("color", row.color)
			.style("vertical-align", "middle")
			.style("text-align", "left")
			.attr("onClick", "lpButtonClicked(" + row.id + ")");

		if (row.isEnabled) {
			cell.append("span")
				.attr("class", "fa fa-toggle-on text-green px-0")
		} else {
			cell.append("span")
				.attr("class", "fa fa-toggle-off text-red px-0")
		}

		cell
			.append("span").text(row.name)
			.attr("class", "px-2");

		if (row.isPluggedIn) {
			const span =
				cell.append("span")
					.attr("class", "fa fa-xs fa-plug")
				;
			span.classed("text-orange", (!row.isCharging))
			span.classed("text-green", row.isCharging)
		}
		if (row.willFinishAtTime) {
			cell.append("span")
				.attr("class", "fa fa-xs fa-flag-checkered pl-1")
				.style("color", this.fgColor);
		}
		if (row.chargeAtNight) {
			cell.append("span")
				.attr("class", "fa fa-xs fa-moon pl-1")
				.style("color", this.fgColor)
		}
		return cell.node();
	}

	cpChargeParamCell(row) {
		const cell = d3.create("td")
			.attr("class", "tablecell px-1 py-1")
			.style("vertical-align", "middle")
			.style("text-align", "center");

		cell.append("span").text(
			formatWatt(row.power) + " " + this.phaseSymbols[row.phasesInUse] + " " + row.targetCurrent + " A"
		)
		return cell.node()
	}
	cpChargeDataCell(row) {
		const cell = d3.create("td")
			.attr("class", "tablecell px-1 py-1 d-flex align-items-center justify-content-center flex-wrap")
			.style("vertical-align", "middle")
			.style("text-align", "center");
		cell.append("span").text(
			formatWattH(row.energySincePlugged * 1000))
		cell.append("span")
			.classed("px-1", true).text("/")
		cell.append("span").text(" " + Math.round(row.energySincePlugged / row.energyPer100km * 100) + " km")
		return cell.node()
	}
	cpSocButtonCell(row) {
		const cell = d3.create("td")
			.attr("class", "tablecell px-1 py-1")
			.attr("onClick", ("socButtonClicked(" + row.id + ")"))
			.style("text-align", "center")
			.style("vertical-align", "middle");
		if (row.isSocConfigured) {
			cell.append("span").text(row.soc + " %")
				.attr("class", "px-2");
			if (row.isSocManual) {
				cell.append("i")
					.attr("class", "small fas fa-edit")
					.style("color", "var(--color-fg");
			} else {
				cell.append("i")
					.attr("class", "small fas fa-redo-alt")
					.attr("id", "soclabel-" + row.id)
					.style("color", "var(--color-fg)");
			}
		}
		return cell.node();
	}

	editManualSoc(i) {
		this.manualSoc = wbdata.chargePoint[i].soc;
		const div = d3.select("div#socSelector");
		div.selectAll("*").remove();

		const col = div.append("div")
			.style("background-color", "steelblue")
			.attr("class", "px-2 py-1");

		col.append("div")
			.attr("class", "row justify-content-center")
			.append("p")
			.attr("class", "largeTextSize popup-header")
			.style("text-align", "center")
			.text("Manuelle SoC-Eingabe - Ladepunkt " + (i + 1));

		const row2 = col.append("div")
			.attr("class", "row justify-content-center")
		row2.append("div")
			.attr("class", "col-2 px-1 py-1")
			.append("button")
			.attr("class", "btn btn-block btn-sm btn-secondary")
			.text("-")
			.on("click", () => {
				if (this.manualSoc > 0) {
					this.manualSoc--;
				}
				box.node().value = this.manualSoc;
			});
		const col22 = row2.append("div").attr("class", "col-5 py-1")
			.append("div").attr("class", "input-group");
		const box = col22.append("input")
			.attr("type", "text")
			.attr("value", this.manualSoc)
			.attr("class", "form-control text-right")
			.on("input", () => {
				const v = box.node().value;
				if (v >= 0 && v <= 100) {
					this.manualSoc = box.node().value;
				}
			});
		col22.append("div").attr("class", "input-group-append")
			.append("div").attr("class", "input-group-text")
			.text("%");
		row2.append("div").attr("class", "col-2 px-1 py-1")
			.append("button")
			.attr("class", "btn btn-block btn-sm btn-secondary")
			.text("+")
			.on("click", () => {
				if (this.manualSoc < 100) {
					this.manualSoc++;
				}
				box.node().value = this.manualSoc;
			});

		const row3 = col.append("div").attr("class", "row justify-content-center");
		const button1 = row3.append("button")
			.attr("type", "submit")
			.attr("class", "btn btn-sm  btn-secondary")
			.text("Abbrechen")
			.on("click", () => {
				div.selectAll("*").remove();
			})
		const button2 = row3.append("button")
			.attr("id", "socSubmitButton")
			.attr("class", "btn btn-sm btn-primary")
			.text("Übernehmen")
			.on("click", () => {
				publish("" + this.manualSoc, "openWB/set/lp/" + (i + 1) + "/manualSoc");
				div.selectAll("*").remove();
			})
	}
}

function lpButtonClicked(i) {
	if (wbdata.chargePoint[i].isEnabled) {
		publish("0", "openWB/set/lp/" + (+i + 1) + "/ChargePointEnabled");
	} else {
		publish("1", "openWB/set/lp/" + (+i + 1) + "/ChargePointEnabled");
	}
	d3.select("button#lpbutton-" + i)
		.classed("disabled", true);
}

function socButtonClicked(i) {
	if (wbdata.chargePoint[i].isSocManual) {
		chargePointList.editManualSoc(i);
	} else {
		publish("1", "openWB/set/lp/" + (+i + 1) + "/ForceSoCUpdate");
		d3.select("i#soclabel-" + i)
			.classed("fa-spin", true)
	}
}

var chargePointList = new ChargePointList();
