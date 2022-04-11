/* powerData.js
 * data definitions and shared data for the power graphs
 *
 * Author: Claus Hagen
 *
 */

class WbData {

	constructor(date) {
		this.date = date;
		this.pvwatt = 0;
		this.pvDailyYield = 0;
		this.powerEvuIn = 0;
		this.powerEvuOut = 0;
		this.evuiDailyYield = 0;
		this.evueDailyYield = 0;
		this.chargePower = 0;
		this.chargeSum = 0;
		this.housePower = 0;
		this.smartHomePower = 0;
		this.houseEnergy = 0;
		this.batteryEnergyExport = 0;
		this.batteryEnergyImport = 0;
		this.batteryPowerExport = 0;
		this.batteryPowerImport = 0;
		this.graphDate = new Date();
		this.graphMonth = {
			"month": this.graphDate.getMonth(),
			"year": this.graphDate.getFullYear()
		}
		this.etPrice = 0;
		this.etMaxPrice = 0;
		this.etPriceList = "";
		this.isEtEnabled = false;
		this.rfidConfigured = false;
		this.consumer = [new Consumer(), new Consumer()];
		this.chargePoint = Array.from({ length: 9 }, (v, i) => new ChargePoint(i));
		this.shDevice = Array.from({ length: 9 }, (v, i) => new SHDevice(i));

		this.sourceSummary = {
			"evuIn": { name: "Netz", power: 0, energy: 0, color: "white" },
			"pv": { name: "PV", power: 0, energy: 0, color: "white" },
			"batOut": { name: "Bat >", power: 0, energy: 0, color: "white" }
		};

		this.usageSummary = {
			"evuOut": { name: "Export", power: 0, energy: 0, color: "white" },
			"charging": { name: "Laden", power: 0, energy: 0, color: "white" },
			"devices": { name: "Geräte", power: 0, energy: 0, color: "white" },
			"batIn": { name: "> Bat", power: 0, energy: 0, color: "white" },
			"house": { name: "Haus", power: 0, energy: 0, color: "white" }
		};

		this.historicSummary = {
			"evuIn": { name: "Netz", power: 0, energy: 0, color: "white" },
			"pv": { name: "PV", power: 0, energy: 0, color: "white" },
			"batOut": { name: "Bat >", power: 0, energy: 0, color: "white" },
			"evuOut": { name: "Export", power: 0, energy: 0, color: "white" },
			"charging": { name: "Laden", power: 0, energy: 0, color: "white" },
			"devices": { name: "Geräte", power: 0, energy: 0, color: "white" },
			"batIn": { name: "> Bat", power: 0, energy: 0, color: "white" },
			"house": { name: "Haus", power: 0, energy: 0, color: "white" }
		};

		this.usageDetails = [this.usageSummary.evuOut];
		this.graphPreference = "live";
		this.graphMode = "live";
		this.showTodayGraph = true;
		this.showGrid = false;
		this.displayMode = "gray";
		this.usageStackOrder = 0;
		this.prefs = {};
		this.chargePointToConfig = 0;
		this.minCurrent = 6;
	};

	init() {
		var style = getComputedStyle(document.body);
		this.sourceSummary.pv.color = 'var(--color-pv)';
		this.sourceSummary.evuIn.color = 'var(--color-evu)';
		this.sourceSummary.batOut.color = 'var(--color-battery)';
		this.usageSummary.evuOut.color = 'var(--color-export)';
		this.usageSummary.charging.color = 'var(--color-charging)';
		this.usageSummary.devices.color = 'var(--color-devices)';
		this.usageSummary.batIn.color = 'var(--color-battery)';
		this.usageSummary.house.color = 'var(--color-house)';
		var i;
		for (i = 0; i < 8; i++) {
			this.chargePoint[i].color = 'var(--color-lp' + (i + 1) + ')';
		}
		for (i = 0; i < 9; i++) {
			this.shDevice[i].color = 'var(--color-sh' + (i + 1) + ')';
		}
		this.consumer[0].color = 'var(--color-co1)';
		this.consumer[1].color = 'var(--color-co2)';

		this.historicSummary.pv.color = 'var(--color-pv)';
		this.historicSummary.evuIn.color = 'var(--color-evu)';
		this.historicSummary.batOut.color = 'var(--color-battery)';
		this.historicSummary.evuOut.color = 'var(--color-export)';
		this.historicSummary.charging.color = 'var(--color-charging)';
		this.historicSummary.devices.color = 'var(--color-devices)';
		this.historicSummary.batIn.color = 'var(--color-battery)';
		this.historicSummary.house.color = 'var(--color-house)';
		evuCol = style.getPropertyValue('--evuCol');
		xgridCol = style.getPropertyValue('--xgridCol');
		tickCol = style.getPropertyValue('--tickCol');
		fontCol = style.getPropertyValue('--fontCol');
		gridCol = style.getPropertyValue('--gridCol');
		evuCol = style.getPropertyValue('--evuCol');

		this.graphMode = 'live';

		// set display mode
		const doc = d3.select("html");
		doc.classed("theme-dark", (this.displayMode == "dark"));
		doc.classed("theme-light", (this.displayMode == "light"));
		doc.classed("theme-gray", (this.displayMode == "gray"));
		doc.classed("shcolors-normal", true);

		d3.select("button#powerSelectButton")
			.on("click", switchToPowerView);
		d3.select("button#timeSelectButton")
			.on("click", switchToTimeView);
		d3.select("button#energySelectButton")
			.on("click", switchToEnergyView);
		d3.select("button#statusButton")
			.on("click", showStatus);
		d3.select("button#codeButton")
			.on("click", showCode);
			
		d3.select(".minpvRangeInput")
			.on("input", function () { updateMinpvRangeInput(this.value) });
		d3.select(".sofortRangeInput")
			.on("input", function () { updateSofortRangeInput(this.value) });
		d3.select(".socRangeInput")
			.on("input", function () { updateSocRangeInput(this.value) });
		d3.select(".energyRangeInput")
			.on("input", function () { updateEnergyRangeInput(this.value) });
		d3.select(".maxPriceInput")
			.on("input", function () { updateMaxPriceInput(this.value) });
		d3.select("#codeButton").classed ("hide", !this.rfidConfigured)
		powerMeter.init()
		powerGraph.init()
		yieldMeter.init()
		chargePointList.init()
		priceChart.init()
	}

	updateEvu(field, value) {
		this[field] = value;
		switch (field) {
			case 'powerEvuIn':
			case 'powerEvuOut':
				this.updateSourceSummary("evuIn", "power", this.powerEvuIn);
				this.updateUsageSummary("evuOut", "power", this.powerEvuOut);
				break;
			case 'evuiDailyYield':
				this.updateSourceSummary("evuIn", "energy", this.evuiDailyYield);

				break;
			case 'evueDailyYield':
				this.updateUsageSummary("evuOut", "energy", this.evueDailyYield);
				break;
			default:
				break;
		}
	}

	updateGlobal(field, value) {
		this[field] = value;
		switch (field) {
			case 'housePower':
				this.updateUsageSummary("house", "power", value);
				break;
			case 'chargePower':
				this.updateUsageSummary("charging", "power", value);
				break;
			case 'chargeEnergy':
				this.updateUsageSummary("charging", "energy", value)
				break;
			case 'houseEnergy':
				this.updateUsageSummary("house", "energy", value);
				break;
			case 'smarthomePower':
				this.updateConsumerSummary();
				powerMeter.update();
				break;
			case 'currentPowerPrice':
				chargePointList.updateValues();
				break;
			case 'chargeMode':
				chargePointList.updateValues();
				break;
			case 'rfidConfigured':
				d3.select('#codeButton').classed ("hide", (!value))
				break
			default:
				break;
		}
	}

	updatePv(field, value) {
		this[field] = value;
		switch (field) {
			case 'pvwatt':
				this.updateSourceSummary("pv", "power", this.pvwatt);
				break;
			case 'pvDailyYield':
				this.updateSourceSummary("pv", "energy", this.pvDailyYield);
				break;
			case 'isBatteryConfigured':
			case 'hasEVPriority':
			case 'minCurrent':
				chargePointList.updateValues()
				break;
			default:
				break;
		}
	}

	updateConsumer(index, field, value) {
		this.consumer[index - 1][field] = value;
		switch (field) {
			case 'power':
				this.updateConsumerSummary('power');
				break;
			case 'energy':
				this.updateConsumerSummary('energy');
				break;
			default:
				break;
		}
		smartHomeList.update();
	}

	updateSH(index, field, value) {
		this.shDevice[index - 1][field] = value;
		switch (field) {
			case 'power':
				this.updateConsumerSummary("power");
				break;
			case 'energy':
				this.updateConsumerSummary("energy");
				break;
			case 'showInGraph':
				this.updateUsageDetails();
				yieldMeter.update();
				break;
			case 'countAsHouse':
				break;
			default:
				break;
		}
	}

	updateCP(index, field, value) {
		this.chargePoint[index - 1][field] = value;
		switch (field) {
			case 'power':
				powerMeter.update();
				break;
			case 'energy':
				yieldMeter.update();
				break;
			case 'soc':
				break;
			case 'configured':
				chargePointList.updateConfig()
			default:
				break;
		}
		chargePointList.updateValues();
	}

	updateBat(field, value) {
		this[field] = value;
		switch (field) {
			case 'batteryPowerImport':
				this.updateUsageSummary("batIn", "power", value);
				powerMeter.update();
				break;
			case 'batteryPowerExport':
				this.updateSourceSummary("batOut", "power", value);
				powerMeter.update();
				break;
			case 'batteryEnergyImport':
				this.updateUsageSummary("batIn", "energy", value);
				yieldMeter.update();
				break;
			case 'batteryEnergyExport':
				this.updateSourceSummary("batOut", "energy", value);
				yieldMeter.update();
				break;
			default:
				break;
		}
	}

	updateET(field,value) {
		this[field]=value;
		
		switch (field) {
			case 'etPrice':
			case 'isEtEnabled': chargePointList.updateValues();
			break;
			default:
				break;
		}
		priceChart.update()
	}

	updateSourceSummary(cat, field, value) {
		this.sourceSummary[cat][field] = value;
		if (field == "power") {
			this.updateUsageDetails();
			powerMeter.update();
		}

		if (field == "energy") {
			this.updateUsageDetails();
			yieldMeter.update();
		}
	}

	updateUsageSummary(cat, field, value) {
		this.usageSummary[cat][field] = value;

		if (field == "power") {
			this.updateUsageDetails();
			powerMeter.update();
		}
		if (field == "energy") {
			this.updateUsageDetails();
			yieldMeter.update();
		}
	}

	updateUsageDetails() {
		this.usageDetails = [this.usageSummary.evuOut,
		this.usageSummary.charging]
			.concat(this.shDevice.filter(row => (row.configured && row.showInGraph)).sort((a, b) => { return (b.power - a.power) }))
			.concat(this.consumer.filter(row => (row.configured)))
			.concat([this.usageSummary.batIn, this.usageSummary.house]);
	}

	updateConsumerSummary(cat) {
		if (cat == 'energy') {
			this.updateUsageSummary("devices", 'energy', this.shDevice.filter(dev => dev.configured).reduce((sum, consumer) => sum + consumer.energy, 0)
				+ this.consumer.filter(dev => dev.configured).reduce((sum, consumer) => sum + consumer.energy, 0));
		} else {
			this.updateUsageSummary("devices", 'power', this.smarthomePower
				+ this.consumer.filter(dev => dev.configured).reduce((sum, consumer) => sum + consumer.power, 0));
		}
	}

	setChargeLimitMode(limitMode) {
		d3.select(".socLimitSettings").classed("hide", (limitMode != "2"))
		d3.select(".energyLimitSettings").classed("hide", (limitMode != "1"))
		publish(limitMode, "openWB/config/set/sofort/lp/" + (this.chargePointToConfig + 1) + "/chargeLimitation")

	}
}


class Consumer {
	constructor(name = "", power = 0, dailyYield = 0, configured = false, color = "white") {
		this.name = name;
		this.power = power;
		this.dailyYield = dailyYield;
		this.configured = configured;
		this.color = color;
	}
};

class ChargePoint {
	constructor(index, name = "", power = 0, dailyYield = 0, configured = false, isSocConfigured = false, isSocManual = false) {
		this.name = name;
		this.power = power;
		this.energy = dailyYield;
		this.configured = configured;
		this.isSocConfigured = isSocConfigured;
		this.isSocManual = isSocManual;
	}
};

class SHDevice {
	constructor(index, name = "", power = 0, dailyYield = 0, configured = false, color = "white") {
		this.id = index;
		this.name = name;
		this.power = power;
		this.energy = dailyYield;
		this.configured = configured;
		this.showInGraph = true;
		this.color = color;
		this.countAsHouse = false;
	}
};

function formatWatt(watt) {
	if (watt >= 10000) {
		return (Math.round(watt / 1000) + " kW");
	} else if (watt >= 1000) {
		return ((Math.round(watt / 100) / 10) + " kW");
	} else {
		return (watt + " W");
	}
}

function formatWattH(watth) {
	if (watth >= 10000) {
		return (Math.round(watth / 1000) + " kWh");
	} else if (watth >= 1000) {
		return ((Math.round(watth / 100) / 10) + " kWh");
	} else {
		return (Math.round(watth) + " Wh");
	}
}
function formatTime(seconds) {
	const hours = Math.floor(seconds / 3600);
	const minutes = ((seconds % 3600) / 60).toFixed(0);
	if (hours > 0) {
		return (hours + "h " + minutes + " min");
	} else {
		return (minutes + " min");
	}
}

function formatMonth(month, year) {
	months = ['Jan', 'Feb', 'März', 'April', 'Mai', 'Juni', 'Juli', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'];
	return (months[month] + " " + year);
}

// required for price chart to work
var evuCol;
var xgridCol;
var gridCol;
var tickCol;
var fontCol;

function switchToTimeView() {
	d3.select("figure#powermeter").classed("hide", true)
	d3.select("figure#powergraph").classed("hide", false)
	d3.select("figure#energymeter").classed("hide", true)
	d3.select("h3#widgetheading").html('&nbsp;')
	d3.select("button#powerSelectButton").classed("btn-secondary", false).classed("btn-outline-secondary", true)
	d3.select("button#timeSelectButton").classed("btn-secondary", true).classed("btn-outline-secondary", false)
	d3.select("button#energySelectButton").classed("btn-secondary", false).classed("btn-outline-secondary", true)
	powerGraph.activateLive();

}
function switchToPowerView() {
	d3.select("figure#powermeter").classed("hide", false)
	d3.select("figure#powergraph").classed("hide", true)
	d3.select("figure#energymeter").classed("hide", true)
	d3.select("h3#widgetheading").html('&nbsp;')
	d3.select("button#powerSelectButton").classed("btn-secondary", true).classed("btn-outline-secondary", false)
	d3.select("button#timeSelectButton").classed("btn-secondary", false).classed("btn-outline-secondary", true)
	d3.select("button#energySelectButton").classed("btn-secondary", false).classed("btn-outline-secondary", true)
	powerGraph.deactivateLive()
}
function switchToEnergyView() {
	d3.select("figure#powermeter").classed("hide", true)
	d3.select("figure#powergraph").classed("hide", true)
	d3.select("figure#energymeter").classed("hide", false)
	d3.select("h3#widgetheading").html('&nbsp;')
	d3.select("button#powerSelectButton").classed("btn-secondary", false).classed("btn-outline-secondary", true)
	d3.select("button#timeSelectButton").classed("btn-secondary", false).classed("btn-outline-secondary", true)
	d3.select("button#energySelectButton").classed("btn-secondary", true).classed("btn-outline-secondary", false)
	powerGraph.deactivateLive()
}
function showStatus() {
	$("#statusModal").modal("show");
}

function showCode() {
	$("#codeModal").modal("show");
	
}

function updateMinpvRangeInput(value) {
	const label = d3.select(".labelMinPv").text(value + " A");
	label.classed("text-danger", true)
	setTimeout(() => {
		label.classed("text-danger", false)
		publish(value, "openWB/config/set/pv/minCurrentMinPv")
	}, 2000)
}

function updateSofortRangeInput(value) {
	const label = d3.select(".labelSofortCurrent").text(value + " A");
	label.classed("text-danger", true)
	setTimeout(() => {
		label.classed("text-danger", false)
		publish(value, "openWB/config/set/sofort/lp/" + (wbdata.chargePointToConfig + 1) + "/current")
	}, 2000)
}

function updateSocRangeInput(value) {
	const label = d3.select(".labelSocLimit").text(value + " %");
	label.classed("text-danger", true)
	setTimeout(() => {
		label.classed("text-danger", false)
		publish(value, "openWB/config/set/sofort/lp/" + (wbdata.chargePointToConfig + 1) + "/socToChargeTo")
	}, 2000)
}

function updateEnergyRangeInput(value) {
	const label = d3.select(".labelEnergyLimit").text(value + " kWh");
	label.classed("text-danger", true)
	setTimeout(() => {
		label.classed("text-danger", false)
		publish(value, "openWB/config/set/sofort/lp/" + (wbdata.chargePointToConfig + 1) + "/energyToCharge")
	}, 2000)


}
function updateMaxPriceInput(value) {
	const label = d3.select(".labelMaxPrice").text(value + " Cent");
	label.classed("text-danger", true)

	wbdata.updateET ("etMaxPrice", value);
	if (wbdata.maxPriceDelayTimer) {
		clearTimeout(wbdata.maxPriceDelayTimer)
	}
	wbdata.maxPriceDelayTimer = setTimeout(() => {
		label.classed("text-danger", false)
		publish(value, "openWB/set/awattar/MaxPriceForCharging" )
		wbdata.maxPriceDelayTimer = null;
	}, 2000)


}



var wbdata = new WbData(new Date(Date.now()));


