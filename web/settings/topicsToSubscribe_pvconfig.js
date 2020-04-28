/**
 * set of topics that has to be subscribed for the graph settings
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

// line[0] = topic
// line[1] = load counter (if needed)

var topicsToSubscribe = [
	["openWB/config/get/pv/chargeSubmode", 0],
	["openWB/config/get/pv/regulationPoint", 0],
	["openWB/config/get/pv/minFeedinPowerBeforeStart", 0],
	["openWB/config/get/pv/startDelay", 0],
	["openWB/config/get/pv/maxPowerConsumptionBeforeStop", 0],
	["openWB/config/get/pv/stopDelay", 0],
	["openWB/config/get/pv/lp/1/minCurrent", 0],
	["openWB/config/get/pv/lp/2/minCurrent", 0],
	["openWB/config/get/pv/boolAdaptiveCharging", 0],
	["openWB/config/get/pv/adaptiveChargingFactor", 0],
	["openWB/config/get/pv/nurpv70dynact", 0],
	["openWB/config/get/pv/nurpv70dynw", 0],
	["openWB/config/get/pv/lp/1/minSocAlwaysToChargeTo", 0],
	["openWB/config/get/pv/lp/1/minSocAlwaysToChargeToCurrent", 0],
	["openWB/config/get/pv/lp/1/maxSocToChargeTo", 0],
	["openWB/config/get/pv/priorityModeEVBattery", 0],
	["openWB/config/get/pv/boolShowPriorityIconInTheme", 0],
	["openWB/config/get/pv/minBatteryChargePowerAtEvPriority", 0],
	["openWB/config/get/pv/minBatteryDischargeSocAtBattPriority", 0],
	["openWB/config/get/pv/batteryDischargePowerAtBattPriority", 0],

	["openWB/config/get/pv/minCurrentMinPv", 0],
	["openWB/config/get/pv/socStartChargeAtMinPv", 0],
	["openWB/config/get/pv/socStopChargeAtMinPv", 0]
];
