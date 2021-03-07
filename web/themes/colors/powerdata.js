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
		this.houseEnergy = 0;
		this.batteryEnergyExport = 0;
		this.batteryEnergyImport = 0;
		this.batteryPowerExport = 0;
		this.batteryPowerImport = 0;
		this.graphDate = new Date();

		this.consumer = [new Consumer(), new Consumer()];
		this.chargePoint = Array.from({ length: 9 }, (v, i) => new ChargePoint(i));

		this.shDevice = Array.from({ length: 9 }, (v, i) => new SHDevice(i));

		this.sourceSummary = {
			"pv": { name: "PV", power: 0, energy: 0, color: "white" },
			"evuIn": { name: "Netz", power: 0, energy: 0, color: "white" },
			"batOut": { name: "Speicher out", power: 0, energy: 0, color: "white" }

		};
		this.usageSummary = [
			{ name: "Export", power: 0, energy: 0, color: "white" },
			{ name: "Laden", power: 0, energy: 0, color: "white" },
			{ name: "Geräte", power: 0, energy: 0, color: "white" },
			{ name: "Speicher in", power: 0, energy: 0, color: "white" },
			{ name: "Haus", power: 0, energy: 0, color: "white" }
		];
		this.historicSummary = {
			"pv": { name: "PV", power: 0, energy: 0, color: "white" },
			"evuIn": { name: "Netz", power: 0, energy: 0, color: "white" },
			"batOut": { name: "Speicher out", power: 0, energy: 0, color: "white" },
			"evuOut": { name: "Export", power: 0, energy: 0, color: "white" },
			"charging": { name: "Laden", power: 0, energy: 0, color: "white" },
			"devices": { name: "Geräte", power: 0, energy: 0, color: "white" },
			"batIn": { name: "Speicher in", power: 0, energy: 0, color: "white" },
			"house": { name: "Haus", power: 0, energy: 0, color: "white" }

		}
		this.usageDetails = [this.usageSummary[0]];
		this.showLiveGraph = true;
		this.showTodayGraph = false;
		this.displayMode = "dark";
		this.usageStackOrder = 0;
		this.prefs = {};
	};

	init() {
		var style = getComputedStyle(document.body);
		this.sourceSummary.pv.color = 'var(--color-pv)';
		this.sourceSummary.evuIn.color = 'var(--color-evu)';
		this.sourceSummary.batOut.color = 'var(--color-battery)';
		this.usageSummary[0].color = 'var(--color-export)';
		this.usageSummary[1].color = 'var(--color-charging)';
		this.usageSummary[2].color = 'var(--color-devices)';
		this.usageSummary[3].color = 'var(--color-battery)';
		this.usageSummary[4].color = 'var(--color-house)';
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

		

		this.readGraphPreferences();

		if (this.showLiveGraph) {
			powerGraph.deactivateDay();
			powerGraph.activateLive();
		} else {
			powerGraph.deactivateLive();
			powerGraph.activateDay();
		}
		// set display mode
		const doc = d3.select("html");
		doc.classed("theme-dark", (this.displayMode == "dark"));
		doc.classed("theme-light", (this.displayMode == "light"));
		doc.classed("theme-gray", (this.displayMode == "gray"));
	}

	updateEvu(field, value) {
		this[field] = value;
		switch (field) {
			case 'powerEvuIn':
			case 'powerEvuOut':
				this.updateSourceSummary("evuIn", "power", this.powerEvuIn);
				this.updateUsageSummary(0, "power", this.powerEvuOut);
				break;
			case 'evuiDailyYield':
				this.updateSourceSummary("evuIn", "energy", this.evuiDailyYield);

				break;
			case 'evueDailyYield':
				this.updateUsageSummary(0, "energy", this.evueDailyYield);
				break;
			default:
				break;
		}
	}

	updateGlobal(field, value) {
		this[field] = value;
		switch (field) {
			case 'housePower':
				this.updateUsageSummary(4, "power", value);
				break;
			case 'chargePower':
				this.updateUsageSummary(1, "power", value);
				break;
			case 'chargeEnergy':
				this.updateUsageSummary(1, "energy", value)
				break;
			case 'houseEnergy':
				console.log("Update House Energy: " + value);
				this.updateUsageSummary(4, "energy", value);
				break;
			case 'currentPowerPrice':
				chargePointList.update();
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
				console.log("Update PV Energy: " + value);
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
				this.persistGraphPreferences();
				this.updateUsageDetails();
				yieldMeter.update();
				break;
			default:
				break;
		}
		smartHomeList.update();
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
				powerMeter.update();
				break;
			default:
				break;
		}
		chargePointList.update();
	}

	updateBat(field, value) {
		this[field] = value;
		switch (field) {
			case 'batteryPowerImport':
				this.usageSummary[3].power = value;
				powerMeter.update();
				break;
			case 'batteryPowerExport':
				this.updateSourceSummary("batOut", "power", value);
				powerMeter.update();
				break;
			case 'batteryEnergyImport':
				this.usageSummary[3].energy = value;
				yieldMeter.update();
				break;
			case 'batteryEnergyExport':
				this.updateSourceSummary("batOut", "energy", value);
				yieldMeter.update();
				break;

			default:
				break;
		}
		batteryList.update();
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

	updateUsageSummary(index, field, value) {
		this.usageSummary[index][field] = value;

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
		this.usageDetails = [this.usageSummary[0],
		this.usageSummary[1]]
			.concat(this.shDevice.filter(row => (row.configured && row.showInGraph)))
			.concat(this.consumer.filter(row => (row.configured)))
			.concat([this.usageSummary[3], this.usageSummary[4]]);
	}

	updateConsumerSummary(cat) {
		this.updateUsageSummary(2, cat, this.shDevice.filter(dev => dev.configured).reduce((sum, consumer) => sum + consumer[cat], 0)
			+ this.consumer.filter(dev => dev.configured).reduce((sum, consumer) => sum + consumer[cat], 0));
	}

	//update cookie
	persistGraphPreferences() {
		this.prefs.hideSH = this.shDevice.filter(device => !device.showInGraph).map(device => device.id);
		this.prefs.showLG = this.showLiveGraph;
		this.prefs.displayM = this.displayMode;
		this.prefs.stackO = this.usageStackOrder;
		document.cookie = "openWBColorTheme=" + JSON.stringify(this.prefs) + "; max-age=16000000";
	}
	// read cookies and update settings
	readGraphPreferences() {
		const wbCookies = document.cookie.split(';');
		const myCookie = wbCookies.filter(entry => entry.split('=')[0] === "openWBColorTheme");
		if (myCookie.length > 0) {
			this.prefs = JSON.parse(myCookie[0].split('=')[1]);
			if ('hideSH' in this.prefs) {
				this.prefs.hideSH.map(i => this.shDevice[i].showInGraph = false)
			}
			if ('showLG' in this.prefs) {
				this.showLiveGraph = this.prefs.showLG;
				this.showTodayGraph = !this.prefs.showLG;
			}
			if ('maxPow' in this.prefs) {
				powerMeter.maxPower = +this.prefs.maxPow;
			}
			if ('relPM' in this.prefs) {
				powerMeter.showRelativeArcs = this.prefs.relPM;
			}
			if ('displayM' in this.prefs) {
				this.displayMode = this.prefs.displayM;
			}
			if ('stackO' in this.prefs) {
				this.usageStackOrder = this.prefs.stackO;
			}
		}
	}
	dayGraphUpdated() {
		yieldMeter.update();
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
	}
};

function formatWatt(watt) {
	if (watt >= 1000) {
		return ((Math.round(watt / 100) / 10) + " kW");
	} else {
		return (watt + " W");
	}
}

function formatWattH(watt) {
	if (watt >= 1000) {
		return ((Math.round(watt / 100) / 10) + " kWh");
	} else {
		return (Math.round(watt) + " Wh");
	}
}
function formatTime(seconds) {
	const hours = (seconds / 3600).toFixed(0);
	const minutes = ((seconds % 3600) / 60).toFixed(0);
	if (hours > 0) {
		return (hours + "h " + minutes + " min");
	} else {
		return (minutes + " min");
	}
}

function shiftLeft() {
  if (wbdata.showLiveGraph) {
    wbdata.showLiveGraph = false;
    wbdata.showTodayGraph = true;
    powerGraph.deactivateLive();
    powerGraph.activateDay();
    wbdata.prefs.showLG = false;
    wbdata.persistGraphPreferences();
    d3.select("button#graphRightButton").classed("disabled", false)
  } else { 
    if (wbdata.showTodayGraph) {
      wbdata.showTodayGraph = false;
    }
    wbdata.graphDate.setTime(wbdata.graphDate.getTime() - 86400000);
    powerGraph.activateDay();
  }
}
function shiftRight() {
  today = new Date();
  const d = wbdata.graphDate;
  if (d.getDate() == today.getDate() && d.getMonth() == today.getMonth() && d.getFullYear() == today.getFullYear()) {
    if (!wbdata.showLiveGraph) {
      wbdata.showLiveGraph = true;
      powerGraph.deactivateDay();
      powerGraph.activateLive();
      wbdata.prefs.showLG = true;
      wbdata.persistGraphPreferences();
      d3.select("button#graphLeftButton").classed("disabled", false)
      d3.select("button#graphRightButton").classed("disabled", true)
    }
  } else {
    wbdata.graphDate.setTime(wbdata.graphDate.getTime() + 86400000);
    const nd = wbdata.graphDate;
    if (nd.getDate() == today.getDate() && nd.getMonth() == today.getMonth() && nd.getFullYear() == today.getFullYear()) {
      wbdata.showTodayGraph = true;
    }
    powerGraph.activateDay();
  }
}
// required for pricechart to work
var evuCol;
var xgridCol;
var gridCol;
var tickCol;
var fontCol;

var wbdata = new WbData(new Date(Date.now()));

