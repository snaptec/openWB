/** 
 * List the configured chargepoints and their key data
 * 
 */

class SmartHomeList {

	div;

	constructor() {
		var consumers = [];
	};

	// initialize after document is created
	init() {
		this.div = d3.select("div#smartHomeTable");
		this.fgColor = "var(--color-fg)";
		this.switchColorRed = "var(--color-switchRed)";
		this.switchColorGreen = "var(--color-switchGreen)";
		this.switchColorBlue = "var(--color-switchBlue)";
		this.switchColorWhite = "var(--color-fg)";
	}

	// update if data has changed
	update() {
		this.updateValues();
		this.div.selectAll("*").remove();

		if (this.consumers.length > 0) {
			d3.select("div#smartHomeWidget").classed("hide", false);
			var table = this.div.append("table")
				.attr("class", "table table-borderless table-condensed p-0 m-0");

			const headers = ["Gerät", "Verbrauch", "Laufzeit", "Modus"];
			const thead = table.append("thead");
			thead
				.selectAll("headers")
				.data(headers).enter()
				.append("th")
				.attr("style", (data, i) => (i == 0) ? "text-align:left;"
					: "text-align:left;")
				.attr("class", "tablecell p-1 m-0")
				.text((data) => data)
				;
			thead.append("th")
				.attr("style", "text-align:right")
				.attr("class", "tablecell")
				.append("span")
				.attr("class", "fa fa-chart-area px-0");

			const rows = table.append("tbody").selectAll("rows")
				.data(this.consumers).enter()
				.append("tr")
				.attr("style", row => this.calcColor(row));
			rows.append((row, i) => this.formatName(row, i));
			// Power/energy
			let cell = rows.append("td")
				.attr("class", "tablecell py-1 px-1 d-flex align-items-center justify-content-center flex-wrap")
				.attr("style", "vertical-align: middle;color:var(--color-fg)")
			cell
				.append("span")
				.text(row => formatWatt(row.power));
			cell
				.append("span")
				.text(row => " (" + formatWattH(row.energy * 1000) + ")");
			// Running time
			rows.append("td")
				.attr("class", "tablecell py-1 px-1")
				.attr("style", "vertical-align: middle;color:var(--color-fg)")
				.text(row => formatTime(row.runningTime))
			// Automatic mode button
			rows.append("td")
				.attr("class", "tablecell py-1 px-1")
				.append("button")
				.attr("id", (row) => "shmodebutton-" + row.id)
				.attr("class", row => this.modeClass(row))
				.attr("style", "color:var(--color-fg); text-align:center;")
				.attr("onClick", (row) => "shModeClicked(" + row.id + ")")
				.classed("disabled", false)
				.text(row => row.isAutomatic ? "Auto" : "Manuell");
			// select graph display
			rows.append("td")
				.attr("class", "tablecell py-1 px-1")
				.append("div")
				.attr("class", "form-check")
				.style("text-align", "right")
				.append("input")
				.attr("type", "checkbox")
				.attr("name", "graphswitch")
				.attr("class", "form-check-input")
				.property("checked", row => row.showInGraph)
				.attr("id", (row) => row.id)
				;

			d3.selectAll("[name=graphswitch]")
				.on("change", function () {
					wbdata.updateSH(+this.id + 1, "showInGraph", this.checked);
				})
		}
		else {
			d3.select("div#smartHomeWidget").classed("hide", true);
		}
	}

	formatName(row, i) {
		const cell = d3.create("td")
			.attr("class", "tablecell py-1 px-1")
			.attr("onClick", "shDeviceClicked(" + row.id + ")")
			.attr("id", "shbutton-" + i)
			.attr("style", "text-align:left; vertical-align:middle;");
		// status indicator
		cell.append("span")
			.attr("id", "shbutton-" + row.id)
			.attr("class", row.status == 'off' ? "fa fa-toggle-off pr-2" : "fa fa-toggle-on pr-2")
			.style("color", (row.status == 'off') ? this.switchColorRed
				: (row.status == 'on') ? this.switchColorGreen
					: (row.status == 'on-by-detection') ? this.switchColorBlue
						: (row.status == 'on-by-timeout') ? this.switchColorWhite
							: this.switchColorRed);
		// name
		cell.append("span")
			.text(row.name);
		let temps = row.temp.filter(r => (r < 200.0))
		let tempString = "";
		if (temps.length > 0) {
			tempString += " (";
			temps.map((t, i) => {
				tempString += formatTemp(t);
				if (i + 1 < temps.length) {
					tempString += ', ';
				}
			})
			tempString += ") ";
		}
		cell.append("span")
			.text(tempString);
		if (row.countAsHouse) {
			cell.append("span")
				.attr("class", "fa fa-xs fa-home pl-1")
			// .style("color", this.fgColor);
		}
		return cell.node();
	}
	calcColor(row) {
		return ("color:" + row.color + "; text-align:center");
	}

	buttonClass = "btn btn-sm";

	deviceClass(row) {
		return (this.buttonClass + (row.isOn ? " btn-outline-success" : " btn-outline-danger"));
	}

	modeClass(row) {
		return (this.buttonClass + (row.isAutomatic ? " btn-outline-info" : " btn-outline-warning"));
	}

	updateValues() {
		this.consumers = wbdata.shDevice.filter((dv) => dv.configured);
	}
}

function shModeClicked(i) {
	// send mqtt set to enable/disable Device after click
	if (wbdata.shDevice[i].isAutomatic) {
		publish("1", "openWB/config/set/SmartHome/Devices/" + (+i + 1) + "/mode");
	} else {
		publish("0", "openWB/config/set/SmartHome/Devices/" + (+i + 1) + "/mode");
	}
	d3.select("button#shmodebutton-" + i)
		.classed("disabled", true);
};

function shDeviceClicked(i) {

	if (!wbdata.shDevice[i].isAutomatic) {
		if (wbdata.shDevice[i].isOn) {
			publish("0", "openWB/config/set/SmartHome/Devices/" + (+i + 1) + "/device_manual_control");
		} else {
			publish("1", "openWB/config/set/SmartHome/Devices/" + (+i + 1) + "/device_manual_control");
		}
		d3.select("span#shbutton-" + i)
			.attr("class", "fa fa-clock text-white pr-2")
			;
	}
}

function toggleGraphDisplay(i) {
	console.log("toggle graph display");
	const checkbox = d3.select("input#graphcheckbox-" + i)

}

var smartHomeList = new SmartHomeList();



