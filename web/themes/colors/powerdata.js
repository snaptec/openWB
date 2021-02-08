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
		this.usageDetails = [this.usageSummary[0]];
		this.showLiveGraph = true;
		this.prefs = {};
	};

	init() {
		var style = getComputedStyle(document.body);
		this.sourceSummary.pv.color = style.getPropertyValue('--color-pv');
		this.sourceSummary.evuIn.color = style.getPropertyValue('--color-evu');
		this.sourceSummary.batOut.color = style.getPropertyValue('--color-battery');
		this.usageSummary[0].color = style.getPropertyValue('--color-export');
		this.usageSummary[1].color = style.getPropertyValue('--color-charging');
		this.usageSummary[2].color = style.getPropertyValue('--color-devices');
		this.usageSummary[3].color = style.getPropertyValue('--color-battery');
		this.usageSummary[4].color = style.getPropertyValue('--color-house');
		var i;
		for (i = 0; i < 8; i++) {
			this.chargePoint[i].color = style.getPropertyValue('--color-lp' + (i + 1));
		}
		for (i = 0; i < 9; i++) {
			this.shDevice[i].color = style.getPropertyValue('--color-sh' + (i + 1));
		}
		// read preferences stored in cookie
		const wbCookies = document.cookie.split(';');
		const myCookie = wbCookies.filter(entry => entry.split('=')[0] === "openWBColorTheme");
		if (myCookie.length > 0) {
			this.prefs = JSON.parse(myCookie[0].split('=')[1]);
			if ('hideSH' in this.prefs) {
				this.prefs.hideSH.map(i => this.shDevice[i].showInGraph = false)
			}
			if ('showLG' in this.prefs) {
				this.showLiveGraph = this.prefs.showLG;
			}
		}
		if (this.showLiveGraph) {
			dayGraph.deactivate();
			powerGraph.activate();
			} else {
				powerGraph.deactivate();
				dayGraph.activate();
			}
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
				this.updateUsageSummary(2, "power", this.shDevice.filter(dev => dev.configured).reduce((sum, consumer) => sum + consumer.power, 0));
				break;
			case 'energy':
				this.updateUsageSummary(2, "energy", this.shDevice.filter(dev => dev.configured).reduce((sum, consumer) => sum + consumer.energy, 0));
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
		this.updateUsageSummary(3, cat, this.shDevice.filter(dev => dev.configured).reduce((sum, consumer) => sum + consumer[cat], 0)
			+ this.consumer.filter(dev => dev.configured).reduce((sum, consumer) => sum + consumer[cat], 0));
	}

	//update cookie
	persistGraphPreferences() {
		this.prefs.hideSH = this.shDevice.filter(device => !device.showInGraph).map(device=>device.id);
		this.prefs.showLG = this.showLiveGraph;
		document.cookie = "openWBColorTheme=" + JSON.stringify(this.prefs);
	}
}

class Consumer {
	constructor(name = "", power = 0, dailyYield = 0, configured = false) {
		this.name = name;
		this.power = power;
		this.dailyYield = dailyYield;
		this.configured = configured;
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
	constructor(index, name = "", power = 0, dailyYield = 0, configured = false, color = "") {
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
		return (watt + " Wh");
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

var wbdata = new WbData(new Date(Date.now()));

