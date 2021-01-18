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
		this.houseSum = 0;

		this.cpName = "Wallbox 1";
		this.soc = 0;
		this.consumer = [new Consumer(), new Consumer()];
		this.chargePoint = Array.from({ length: 9 }, (v, i) => new ChargePoint(i));

		this.shDevice = Array.from({ length: 9 }, (v, i) => new SHDevice(i));

		// this.chargeColors = d3.schemeGreens[9];
		this.sourceSummary = [
			{ name: "PV", power: 0, energy: 0, color: "white" },
			{ name: "Netz", power: 0, energy: 0, color: "white" },
			{ name: "Export", power: 0, energy: 0, color: "white" },
		];
		this.usageSummary = [
			{ name: "Haus", power: 0, energy: 0, color: "white" },
			{ name: "Geräte", power: 0, energy: 0, color: "white" },
			{ name: "Laden", power: 0, energy: 0, color: "white" }
		]
		this.usageDetails = [this.usageSummary[0]];
	};

	init() {
		var style = getComputedStyle(document.body);
		this.sourceSummary[0].color = style.getPropertyValue('--color-pv');
		this.sourceSummary[1].color = style.getPropertyValue('--color-evu');
		this.sourceSummary[2].color = style.getPropertyValue('--color-export');
		this.usageSummary[0].color = style.getPropertyValue('--color-house');
		this.usageSummary[1].color = style.getPropertyValue('--color-devices');
		this.usageSummary[2].color = style.getPropertyValue('--color-charging');
		var i;
		for (i = 0; i < 8; i++) {
			this.chargePoint[i].color = style.getPropertyValue('--color-lp' + (i + 1));
		}
		for (i = 0; i < 9; i++) {
			this.shDevice[i].color = style.getPropertyValue('--color-sh' + (i + 1));
		}
	}

	updateEvu(field, value) {

		this[field] = value;
		switch (field) {
			case 'powerEvuIn':
			case 'powerEvuOut':
				this.updateSourceSummary(1, "power", this.powerEvuIn);
				this.updateSourceSummary(2, "power", this.powerEvuOut);
				break;
			case 'evuiDailyYield':
				this.updateSourceSummary(1, "energy", this.evuiDailyYield);

				break;
			case 'evueDailyYield':
				this.updateSourceSummary(2, "energy", this.evueDailyYield);
				break;
			default:
				break;
		}
	}

	updateGlobal(field, value) {

		this[field] = value;
		switch (field) {
			case 'housePower':
				this.updateUsageSummary(0, "power", value);
				break;
			case 'chargePower':
				this.updateUsageSummary(2, "power", value);
				break;
			case 'chargeEnergy':
				this.updateUsageSummary(2, "energy", value)
				break;
			case 'houseEnergy':
				this.updateUsageSummary(0, "energy", value);
				break;
			default:
				break;
		}
	}

	updatePv(field, value) {

		this[field] = value;
		switch (field) {
			case 'pvwatt':
				this.updateSourceSummary(0, "power", this.pvwatt);

				break;
			case 'pvDailyYield':
				this.updateSourceSummary(0, "energy", this.pvDailyYield);

				break;

			default:
				break;
		}
		// powerTable.update();

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
				this.updateUsageSummary(1, "power", this.shDevice.filter(dev => dev.configured).reduce((sum, consumer) => sum + consumer.power, 0));

				break;
			case 'energy':
				this.updateUsageSummary(1, "energy", this.shDevice.filter(dev => dev.configured).reduce((sum, consumer) => sum + consumer.energy, 0));

				break;
			default:
				break;
		}
		smartHomeList.update();
	}

	updateCP(index, field, value) {
		this.chargePoint[index - 1][field] = value;
		chargePointList.update();
		switch (field) {
			case 'power':
				powerMeter.update();
				break;
			case 'energy':
				yieldMeter.update();
				break;
			case 'isPluggedIn':
				chargePointList.update();
				break;
			case 'soc':
				chargePointList.update();
			default:
				break;
		}
	}

	updateSourceSummary(index, field, value) {
		this.sourceSummary[index][field] = value;
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
		this.usageDetails = [this.usageDetails[0]]
			.concat(this.chargePoint.filter(row => (row.configured)))
			.concat(this.shDevice.filter(row => (row.configured)))
			.concat(this.consumer.filter(row => (row.configured)));
	}

	updateConsumerSummary(cat) {
		this.updateUsageSummary(1, cat, this.shDevice.filter(dev => dev.configured).reduce((sum, consumer) => sum + consumer[cat], 0)
			+ this.consumer.filter(dev => dev.configured).reduce((sum, consumer) => sum + consumer[cat], 0));
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
	constructor(index, name = "", power = 0, dailyYield = 0, configured = false) {
		this.name = name;
		this.power = power;
		this.energy = dailyYield;
		this.configured = configured;


	}
};

class SHDevice {
	constructor(index, name = "", power = 0, dailyYield = 0, configured = false) {
		this.name = name;
		this.power = power;
		this.energy = dailyYield;
		this.configured = configured;
		//	this.color = d3.interpolateBlues (index / 10 + 0.3);
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

