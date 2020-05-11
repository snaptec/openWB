/**
 * set of topics that has to be subscribed for the sofort-charging settings
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

// line[0] = topic
// line[1] = load counter (if needed)

var topicsToSubscribe = [
	["openWB/config/get/global/minEVSECurrentAllowed", 0],

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
	["openWB/config/get/sofort/lp/2/socToChargeTo", 0]
];
