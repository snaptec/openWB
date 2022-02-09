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
		this.chargeMode="0"
		this.graphDate = new Date();
		this.graphMonth = {
			"month": this.graphDate.getMonth(),
			"year": this.graphDate.getFullYear()
		}
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
		this.decimalPlaces = 1;
		this.smartHomeColors = "normal";
		this.prefs = {};
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

		this.readGraphPreferences();
		this.graphMode = this.graphPreference;
		switch (this.graphMode) {
			case 'live':
				powerGraph.deactivateDay();
				powerGraph.activateLive();
				break;
			case 'day':
				powerGraph.deactivateLive();
				powerGraph.activateDay();
				break;
			default:
				powerGraph.deactivateDay();
				powerGraph.activateLive();
		}
		// set display mode
		const doc = d3.select("html");
		doc.classed("theme-dark", (this.displayMode == "dark"));
		doc.classed("theme-light", (this.displayMode == "light"));
		doc.classed("theme-gray", (this.displayMode == "gray"));
		switch (this.smartHomeColors) {
			case 'standard':
				doc.classed("shcolors-standard", true);
				break;
			case 'advanced':
				doc.classed("shcolors-advanced", true);
				break;
			case 'normal':
				doc.classed("shcolors-normal", true);
				break;
			default:
				doc.classed("shcolors-normal", true);
				this.smartHomeColors = 'normal';
				this.persistGraphPreferences();
				break;
		}
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
				case 'chargeMode':
				priceChart.update();
				chargePointList.update();
				break
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
			case 'countAsHouse':
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
				this.updateUsageSummary ("batIn", "power", value);
				powerMeter.update();
				break;
			case 'batteryPowerExport':
				this.updateSourceSummary("batOut", "power", value);
				powerMeter.update();
				break;
			case 'batteryEnergyImport':
				this.updateUsageSummary ("batIn", "energy", value);
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
			.concat(this.shDevice.filter(row => (row.configured && row.showInGraph)))
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

	//update cookie
	persistGraphPreferences() {
		this.prefs.hideSH = this.shDevice.filter(device => !device.showInGraph).map(device => device.id);
		this.prefs.showLG = (this.graphPreference == 'live');
		this.prefs.displayM = this.displayMode;
		this.prefs.stackO = this.usageStackOrder;
		this.prefs.showGr = this.showGrid;
		this.prefs.decimalP = this.decimalPlaces;
		this.prefs.smartHomeC = this.smartHomeColors;
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
				this.graphPreference = (this.prefs.showLG) ? "live" : "day";
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
			if ('showGr' in this.prefs) {
				this.showGrid = this.prefs.showGr;
			}
			if ('decimalP' in this.prefs) {
				this.decimalPlaces = this.prefs.decimalP;
			}
			if ('smartHomeC' in this.prefs) {
				this.smartHomeColors = this.prefs.smartHomeC;
			}
		}
	}
	dayGraphUpdated() {
		yieldMeter.update();
	}
	monthGraphUpdated() {
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
		this.countAsHouse = false;
	}
};

function formatWatt(watt) {
	let wattResult;
	if (watt >= 1000) {
		switch (wbdata.decimalPlaces) {
			case 0:
				wattResult = Math.round(watt / 1000);
				break;
			case 1:
				wattResult = (Math.round(watt / 100) / 10).toFixed(1);
				break;
			case 2:
				wattResult = (Math.round(watt / 10) / 100).toFixed(2);
				break;
			case 3:
				wattResult = (Math.round(watt) / 1000).toFixed(3);
				break;
			default: 
				wattResult = Math.round(watt / 100) / 10;
				break;
		}
		return (wattResult + " kW");
	} else {
		return (watt + " W");
	}
}

function formatWattH(watt) {
	if (watt >= 1000) {
		switch (wbdata.decimalPlaces) {
			case 0:
				wattResult = Math.round(watt / 1000);
				break;
			case 1:
				wattResult = (Math.round(watt / 100) / 10).toFixed(1);
				break;
			case 2:
				wattResult = (Math.round(watt / 10) / 100).toFixed(2);
				break;
			case 3:
				wattResult = (Math.round(watt) / 1000).toFixed(3);
				break;
			default: 
				wattResult = Math.round(watt / 100) / 10;
				break;
		}
		return (wattResult + " kWh");
	} else {
		return (Math.round(watt) + " Wh");
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

function formatMonth (month, year) {
	months = ['Jan', 'Feb', 'März', 'April', 'Mai', 'Juni', 'Juli', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'];
	return (months[month] + " "+ year);
}
function shiftLeft() {
	switch (wbdata.graphMode) {
		case 'live':
			wbdata.graphMode = 'day';
			wbdata.graphPreference = 'day';
    	wbdata.showTodayGraph = true;
    	powerGraph.deactivateLive();
    	powerGraph.activateDay();
    	wbdata.prefs.showLG = false;
    	wbdata.persistGraphPreferences();
    	d3.select("button#graphRightButton").classed("disabled", false)
			break;
		case 'day':
			wbdata.showTodayGraph = false;
			wbdata.graphDate.setTime(wbdata.graphDate.getTime() - 86400000);
    	powerGraph.activateDay();
			break;
		case 'month':
			wbdata.graphMonth.month = wbdata.graphMonth.month - 1;
			if (wbdata.graphMonth.month < 0) {
				wbdata.graphMonth.month = 11;
				wbdata.graphMonth.year = wbdata.graphMonth.year - 1;
			}
			powerGraph.activateMonth();
			break;
		default: break;		
	}
}

function shiftRight() {
  today = new Date();
  const d = wbdata.graphDate;
	switch (wbdata.graphMode) {
		case 'live':
			break;
		case 'day':
			if (d.getDate() == today.getDate() && d.getMonth() == today.getMonth() && d.getFullYear() == today.getFullYear()) { // date is today, switch to live graph
				wbdata.graphMode = 'live';
				powerGraph.deactivateDay();
				powerGraph.activateLive();
				wbdata.graphPreference = 'live';
				wbdata.prefs.showLG = true;
				wbdata.persistGraphPreferences();
				d3.select("button#graphLeftButton").classed("disabled", false)
				d3.select("button#graphRightButton").classed("disabled", true)
			} else { // currently looking at a previous day
				wbdata.graphDate.setTime(wbdata.graphDate.getTime() + 86400000);
				const nd = wbdata.graphDate;
				if (nd.getDate() == today.getDate() && nd.getMonth() == today.getMonth() && nd.getFullYear() == today.getFullYear()) {
					wbdata.showTodayGraph = true;
				}
				powerGraph.activateDay();
			}
			break;
		case 'month':
			if ((today.getMonth() != wbdata.graphMonth.month) || (today.getFullYear() != wbdata.graphMonth.year)) { // we are looking at a previous month
				wbdata.graphMonth.month = wbdata.graphMonth.month + 1;
				if (wbdata.graphMonth.month == 12) {
					wbdata.graphMonth.month = 0;
					wbdata.graphMonth.year = wbdata.graphMonth.year + 1;
				}
				powerGraph.activateMonth();
			} 
		}
	
}

function toggleGrid() {
	wbdata.showGrid = !wbdata.showGrid;
	powerGraph.updateGraph();
	yieldMeter.update();
	wbdata.persistGraphPreferences();
}

function switchDecimalPlaces() {
	if (wbdata.decimalPlaces  < 3) {
		wbdata.decimalPlaces = wbdata.decimalPlaces+1;
	} else {
		wbdata.decimalPlaces = 0;
	}
	wbdata.persistGraphPreferences();
	powerMeter.update();
	yieldMeter.update();
	smartHomeList.update();
}

function switchSmartHomeColors() {
	const doc = d3.select("html");
	switch (wbdata.smartHomeColors) {
		case 'normal':
			wbdata.smartHomeColors = 'standard';
			doc.classed("shcolors-normal", false);
			doc.classed("shcolors-standard", true);
			doc.classed("shcolors-advanced", false);
			break;
		case 'standard':
			wbdata.smartHomeColors = 'advanced';
			doc.classed("shcolors-normal", false);
			doc.classed("shcolors-standard", false);
			doc.classed("shcolors-advanced", true);
			break;
		case 'advanced':
			wbdata.smartHomeColors = 'normal';
			doc.classed("shcolors-normal", true);
			doc.classed("shcolors-standard", false);
			doc.classed("shcolors-advanced", false);
			break;
		default:
			wbdata.smartHomeColors = 'normal';
			doc.classed("shcolors-normal", true);
			doc.classed("shcolors-standard", false);
			doc.classed("shcolors-advanced", false);
			break;
	}
	wbdata.persistGraphPreferences();
}

function toggleMonthView() {
	if (wbdata.graphMode == 'month') {
		wbdata.graphMode = wbdata.graphPreference;
		if (wbdata.graphPreference == 'live') {
			powerGraph.activateLive();
			powerGraph.deactivateMonth();
		} else {
			powerGraph.activateDay();
			powerGraph.deactivateMonth();
		}
	} else {
		wbdata.graphMode = 'month';
		powerGraph.activateMonth();
		powerGraph.deactivateDay();
		powerGraph.deactivateLive();	
	}
	yieldMeter.update();
}
// required for price chart to work
var evuCol;
var xgridCol;
var gridCol;
var tickCol;
var fontCol;

var wbdata = new WbData(new Date(Date.now()));
