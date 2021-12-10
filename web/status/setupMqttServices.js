/**
 * Functions to provide services for MQTT
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

// these topics will be subscribed
// index 1 represents flag if value was received, needed for preloaderbar progress
// if flags are preset with 1 they are not counted on reload and page will show even if topic was not received
var topicsToSubscribe = [
	["openWB/global/WAllChargePoints", 1],
	["openWB/global/kWhCounterAllChargePoints", 1],
	["openWB/evu/ASchieflast", 1],
	["openWB/evu/APhase1", 1],
	["openWB/evu/APhase2", 1],
	["openWB/evu/APhase3", 1],
	["openWB/evu/WPhase1", 1],
	["openWB/evu/WPhase2", 1],
	["openWB/evu/WPhase3", 1],
	["openWB/evu/VPhase1", 1],
	["openWB/evu/VPhase2", 1],
	["openWB/evu/VPhase3", 1],
	["openWB/evu/PfPhase1", 1],
	["openWB/evu/PfPhase2", 1],
	["openWB/evu/PfPhase3", 1],
	["openWB/evu/WhImported", 1],
	["openWB/evu/WhExported", 1],
	["openWB/evu/Hz", 1],
	["openWB/evu/W", 1],
	["openWB/evu/faultState", 1],
	["openWB/evu/faultStr", 1],

	["openWB/lp/1/boolChargePointConfigured", 0],
	["openWB/lp/1/AConfigured", 1], 
	["openWB/lp/1/APhase1", 1],
	["openWB/lp/1/APhase2", 1],
	["openWB/lp/1/APhase3", 1],
	["openWB/lp/1/kWhCounter", 1],
	["openWB/lp/1/VPhase1", 1],
	["openWB/lp/1/VPhase2", 1],
	["openWB/lp/1/VPhase3", 1],
	["openWB/lp/1/PfPhase1", 1],
	["openWB/lp/1/PfPhase2", 1],
	["openWB/lp/1/PfPhase3", 1],
	["openWB/lp/1/W", 1],
	["openWB/lp/1/boolSocConfigured", 1],
	["openWB/lp/1/%Soc", 1],
	["openWB/lp/1/faultState", 1],
	["openWB/lp/1/faultStr", 1],
	["openWB/lp/1/socFaultState", 1],
	["openWB/lp/1/socFaultStr", 1],

	["openWB/lp/2/boolChargePointConfigured", 0],
	["openWB/lp/2/AConfigured", 1], 
	["openWB/lp/2/APhase1", 1],
	["openWB/lp/2/APhase2", 1],
	["openWB/lp/2/APhase3", 1],
	["openWB/lp/2/kWhCounter", 1],
	["openWB/lp/2/VPhase1", 1],
	["openWB/lp/2/VPhase2", 1],
	["openWB/lp/2/VPhase3", 1],
	["openWB/lp/2/W", 1],
	["openWB/lp/2/boolSocConfigured", 1],
	["openWB/lp/2/%Soc", 1],
	["openWB/lp/2/faultState", 1],
	["openWB/lp/2/faultStr", 1],
	["openWB/lp/2/socFaultState", 1],
	["openWB/lp/2/socFaultStr", 1],

	["openWB/lp/3/boolChargePointConfigured", 0],
	["openWB/lp/3/AConfigured", 1], 
	["openWB/lp/3/APhase1", 1],
	["openWB/lp/3/APhase2", 1],
	["openWB/lp/3/APhase3", 1],
	["openWB/lp/3/kWhCounter", 1],
	["openWB/lp/3/VPhase1", 1],
	["openWB/lp/3/VPhase2", 1],
	["openWB/lp/3/VPhase3", 1],
	["openWB/lp/3/W", 1],
	["openWB/lp/3/boolSocConfigured", 1],
	["openWB/lp/3/%Soc", 1],
	["openWB/lp/3/faultState", 1],
	["openWB/lp/3/faultStr", 1],
	["openWB/lp/3/socFaultState", 1],
	["openWB/lp/3/socFaultStr", 1],

	["openWB/lp/4/boolChargePointConfigured", 0],
	["openWB/lp/4/AConfigured", 1], 
	["openWB/lp/4/APhase1", 1],
	["openWB/lp/4/APhase2", 1],
	["openWB/lp/4/APhase3", 1],
	["openWB/lp/4/kWhCounter", 1],
	["openWB/lp/4/VPhase1", 1],
	["openWB/lp/4/VPhase2", 1],
	["openWB/lp/4/VPhase3", 1],
	["openWB/lp/4/W", 1],
	["openWB/lp/4/boolSocConfigured", 1],
	["openWB/lp/4/%Soc", 1],
	["openWB/lp/4/faultState", 1],
	["openWB/lp/4/faultStr", 1],
	["openWB/lp/4/socFaultState", 1],
	["openWB/lp/4/socFaultStr", 1],

	["openWB/lp/5/boolChargePointConfigured", 0],
	["openWB/lp/5/AConfigured", 1], 
	["openWB/lp/5/APhase1", 1],
	["openWB/lp/5/APhase2", 1],
	["openWB/lp/5/APhase3", 1],
	["openWB/lp/5/kWhCounter", 1],
	["openWB/lp/5/VPhase1", 1],
	["openWB/lp/5/VPhase2", 1],
	["openWB/lp/5/VPhase3", 1],
	["openWB/lp/5/W", 1],
	["openWB/lp/5/boolSocConfigured", 1],
	["openWB/lp/5/%Soc", 1],
	["openWB/lp/5/faultState", 1],
	["openWB/lp/5/faultStr", 1],
	["openWB/lp/5/socFaultState", 1],
	["openWB/lp/5/socFaultStr", 1],

	["openWB/lp/6/boolChargePointConfigured", 0],
	["openWB/lp/6/AConfigured", 1], 
	["openWB/lp/6/APhase1", 1],
	["openWB/lp/6/APhase2", 1],
	["openWB/lp/6/APhase3", 1],
	["openWB/lp/6/kWhCounter", 1],
	["openWB/lp/6/VPhase1", 1],
	["openWB/lp/6/VPhase2", 1],
	["openWB/lp/6/VPhase3", 1],
	["openWB/lp/6/W", 1],
	["openWB/lp/6/boolSocConfigured", 1],
	["openWB/lp/6/%Soc", 1],
	["openWB/lp/6/faultState", 1],
	["openWB/lp/6/faultStr", 1],
	["openWB/lp/6/socFaultState", 1],
	["openWB/lp/6/socFaultStr", 1],

	["openWB/lp/7/boolChargePointConfigured", 0],
	["openWB/lp/7/AConfigured", 1], 
	["openWB/lp/7/APhase1", 1],
	["openWB/lp/7/APhase2", 1],
	["openWB/lp/7/APhase3", 1],
	["openWB/lp/7/kWhCounter", 1],
	["openWB/lp/7/VPhase1", 1],
	["openWB/lp/7/VPhase2", 1],
	["openWB/lp/7/VPhase3", 1],
	["openWB/lp/7/W", 1],
	["openWB/lp/7/boolSocConfigured", 1],
	["openWB/lp/7/%Soc", 1],
	["openWB/lp/7/faultState", 1],
	["openWB/lp/7/faultStr", 1],
	["openWB/lp/7/socFaultState", 1],
	["openWB/lp/7/socFaultStr", 1],

	["openWB/lp/8/boolChargePointConfigured", 0],
	["openWB/lp/8/AConfigured", 1], 
	["openWB/lp/8/APhase1", 1],
	["openWB/lp/8/APhase2", 1],
	["openWB/lp/8/APhase3", 1],
	["openWB/lp/8/kWhCounter", 1],
	["openWB/lp/8/VPhase1", 1],
	["openWB/lp/8/VPhase2", 1],
	["openWB/lp/8/VPhase3", 1],
	["openWB/lp/8/W", 1],
	["openWB/lp/8/boolSocConfigured", 1],
	["openWB/lp/8/%Soc", 1],
	["openWB/lp/8/faultState", 1],
	["openWB/lp/8/faultStr", 1],
	["openWB/lp/8/socFaultState", 1],
	["openWB/lp/8/socFaultStr", 1],

	["openWB/pv/CounterTillStartPvCharging", 1],
	["openWB/pv/W", 1],
	["openWB/pv/WhCounter", 1],
	["openWB/pv/DailyYieldKwh", 1],
	["openWB/pv/MonthlyYieldKwh", 1],
	["openWB/pv/YearlyYieldKwh", 1],
	["openWB/pv/1/boolPVConfigured", 0],
	["openWB/pv/1/W", 1],
	["openWB/pv/1/WhCounter", 1],
	// no data in openWB 1.x
	// ["openWB/pv/1/DailyYieldKwh", 1],
	// ["openWB/pv/1/MonthlyYieldKwh", 1],
	// ["openWB/pv/1/YearlyYieldKwh", 1],
	["openWB/pv/1/faultState", 1],
	["openWB/pv/1/faultStr", 1],
	["openWB/pv/2/boolPVConfigured", 0],
	["openWB/pv/2/W", 1],
	["openWB/pv/2/WhCounter", 1],
	// no data in openWB 1.x
	// ["openWB/pv/2/DailyYieldKwh", 1],
	// ["openWB/pv/2/MonthlyYieldKwh", 1],
	// ["openWB/pv/2/YearlyYieldKwh", 1],
	["openWB/pv/2/faultState", 1],
	["openWB/pv/2/faultStr", 1],


	["openWB/housebattery/boolHouseBatteryConfigured", 0],
	["openWB/housebattery/WhImported", 1],
	["openWB/housebattery/WhExported", 1],
	["openWB/housebattery/W", 1],
	["openWB/housebattery/%Soc", 1],
	["openWB/housebattery/faultState", 1],
	["openWB/housebattery/faultStr", 1],

	["openWB/SmartHome/Status/maxspeicherladung", 1],
	["openWB/SmartHome/Status/wattschalt", 1],
	["openWB/SmartHome/Status/wattnichtschalt", 1],
	["openWB/SmartHome/Status/uberschuss", 1],
	["openWB/SmartHome/Status/uberschussoffset", 1],

	["openWB/Verbraucher/1/Configured", 1],
	["openWB/Verbraucher/1/Watt", 1],
	["openWB/Verbraucher/1/WhImported", 1],
	["openWB/Verbraucher/1/WhExported", 1],
	["openWB/Verbraucher/2/Configured", 1],
	["openWB/Verbraucher/2/Watt", 1],
	["openWB/Verbraucher/2/WhImported", 1],
	["openWB/Verbraucher/2/WhExported", 1],
];

// holds number of topics flagged 1 initially
var countTopicsNotForPreloader = topicsToSubscribe.filter(row => row[1] === 1).length;

var retries = 0;

//Connect Options
var isSSL = location.protocol == 'https:'
var options = {
	timeout: 5,
	useSSL: isSSL,
	//Gets Called if the connection has been established
	onSuccess: function () {
		retries = 0;
		topicsToSubscribe.forEach((topic) => {
			client.subscribe(topic[0], {qos: 0});
		});
	},
	//Gets Called if the connection could not be established
	onFailure: function (message) {
		setTimeout(function() { client.connect(options); }, 5000);
	}
};

var clientuid = Math.random().toString(36).replace(/[^a-z]+/g, "").substr(0, 5);
var client = new Messaging.Client(location.hostname, 9001, clientuid);

$(document).ready(function(){
	client.connect(options);
	timeOfLastMqttMessage = Date.now();
});

//Gets  called if the websocket/mqtt connection gets disconnected for any reason
client.onConnectionLost = function (responseObject) {
	client.connect(options);
};
//Gets called whenever you receive a message
client.onMessageArrived = function (message) {
	handlevar(message.destinationName, message.payloadString);
};

//Creates a new Messaging.Message Object and sends it
function publish(payload, topic) {
	var message = new Messaging.Message(payload);
	message.destinationName = topic;
	message.qos = 2;
	message.retained = true;
	client.send(message);
	var message = new Messaging.Message("local client uid: " + clientuid + " sent: " + topic);
	message.destinationName = "openWB/set/system/topicSender";
	message.qos = 2;
	message.retained = true;
	client.send(message);
}
