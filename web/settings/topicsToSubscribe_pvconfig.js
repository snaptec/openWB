/**
 * set of topics that has to be subscribed for the pv-charging settings
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
	["openWB/config/get/pv/lp/1/maxSoc", 0],
	["openWB/config/get/pv/lp/2/maxSoc", 0],
	["openWB/config/get/pv/lp/1/socLimitation", 0],
	["openWB/config/get/pv/lp/2/socLimitation", 0],
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
	["openWB/lp/2/boolSocConfigured", 0],
	["openWB/lp/1/boolSocConfigured", 0],
	["openWB/lp/1/boolChargePointConfigured", 0],
	["openWB/lp/2/boolChargePointConfigured", 0],
	["openWB/housebattery/boolHouseBatteryConfigured", 0],

	["openWB/config/get/pv/minCurrentMinPv", 0],
	["openWB/config/get/pv/socStartChargeAtMinPv", 0],
	["openWB/config/get/pv/socStopChargeAtMinPv", 0]
];
