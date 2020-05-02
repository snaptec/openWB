/**
 * set of topics that has to be subscribed for the graph settings
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
	["openWB/config/get/sofort/lp/8/current", 0]
];
