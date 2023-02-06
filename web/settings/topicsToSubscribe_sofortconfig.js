/**
 * set of topics that has to be subscribed for the sofort-charging settings
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

// line[0] = topic
// line[1] = load counter (if needed)

var topicsToSubscribe = [
	["openWB/lp/1/boolChargePointConfigured", 0],
	["openWB/lp/2/boolChargePointConfigured", 0],
	["openWB/lp/3/boolChargePointConfigured", 0],
	["openWB/lp/4/boolChargePointConfigured", 0],
	["openWB/lp/5/boolChargePointConfigured", 0],
	["openWB/lp/6/boolChargePointConfigured", 0],
	["openWB/lp/7/boolChargePointConfigured", 0],
	["openWB/lp/8/boolChargePointConfigured", 0],

	["openWB/lp/1/boolSocConfigured", 0],
	["openWB/lp/2/boolSocConfigured", 0],

	["openWB/config/get/sofort/lp/1/current", 0],
	["openWB/config/get/sofort/lp/2/current", 0],
	["openWB/config/get/sofort/lp/3/current", 0],
	["openWB/config/get/sofort/lp/4/current", 0],
	["openWB/config/get/sofort/lp/5/current", 0],
	["openWB/config/get/sofort/lp/6/current", 0],
	["openWB/config/get/sofort/lp/7/current", 0],
	["openWB/config/get/sofort/lp/8/current", 0],

	["openWB/config/get/sofort/lp/1/chargeLimitation", 0],
	["openWB/config/get/sofort/lp/2/chargeLimitation", 0],
	["openWB/config/get/sofort/lp/3/chargeLimitation", 0],
	["openWB/config/get/sofort/lp/4/chargeLimitation", 0],
	["openWB/config/get/sofort/lp/5/chargeLimitation", 0],
	["openWB/config/get/sofort/lp/6/chargeLimitation", 0],
	["openWB/config/get/sofort/lp/7/chargeLimitation", 0],
	["openWB/config/get/sofort/lp/8/chargeLimitation", 0],

	["openWB/config/get/sofort/lp/1/energyToCharge", 0],
	["openWB/config/get/sofort/lp/2/energyToCharge", 0],
	["openWB/config/get/sofort/lp/3/energyToCharge", 0],
	["openWB/config/get/sofort/lp/4/energyToCharge", 0],
	["openWB/config/get/sofort/lp/5/energyToCharge", 0],
	["openWB/config/get/sofort/lp/6/energyToCharge", 0],
	["openWB/config/get/sofort/lp/7/energyToCharge", 0],
	["openWB/config/get/sofort/lp/8/energyToCharge", 0],

	["openWB/config/get/sofort/lp/1/socToChargeTo", 0],
	["openWB/config/get/sofort/lp/2/socToChargeTo", 0],

	["openWB/config/get/sofort/lp/1/etBasedCharging", 0],
	["openWB/config/get/sofort/lp/2/etBasedCharging", 0],
	["openWB/config/get/sofort/lp/3/etBasedCharging", 0],
	["openWB/config/get/sofort/lp/4/etBasedCharging", 0],
	["openWB/config/get/sofort/lp/5/etBasedCharging", 0],
	["openWB/config/get/sofort/lp/6/etBasedCharging", 0],
	["openWB/config/get/sofort/lp/7/etBasedCharging", 0],
	["openWB/config/get/sofort/lp/8/etBasedCharging", 0],

	["openWB/config/get/global/minEVSECurrentAllowed", 0],

	["openWB/global/awattar/boolAwattarEnabled", 0]
];
