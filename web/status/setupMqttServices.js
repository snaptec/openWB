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
 	["openWB/global/WAllChargePoints", 0],
	["openWB/global/kWhCounterAllChargePoints", 0],
	["openWB/evu/ASchieflast", 0],
	["openWB/evu/APhase1", 0],
	["openWB/evu/APhase2", 0],
	["openWB/evu/APhase3", 0],
	["openWB/evu/WPhase1", 0],
	["openWB/evu/WPhase2", 0],
	["openWB/evu/WPhase3", 0],
	["openWB/evu/VPhase1", 0],
	["openWB/evu/VPhase2", 0],
	["openWB/evu/VPhase3", 0],
	["openWB/evu/Hz", 0],
	["openWB/evu/PfPhase1", 0],
	["openWB/evu/PfPhase2", 0],
	["openWB/evu/PfPhase3", 0],
	["openWB/evu/WhImported", 0],
	["openWB/evu/WhExported", 0],
	["openWB/evu/Hz", 0],
	["openWB/evu/W", 0],

	["openWB/lp/1/boolChargePointConfigured", 0],
	["openWB/lp/1/AConfigured", 0], 
	["openWB/lp/1/APhase1", 0],
	["openWB/lp/1/APhase2", 0],
	["openWB/lp/1/APhase3", 0],
	["openWB/lp/1/kWhCounter", 0],
	["openWB/lp/1/VPhase1", 0],
	["openWB/lp/1/VPhase2", 0],
	["openWB/lp/1/VPhase3", 0],
	["openWB/lp/1/PfPhase1", 0],
	["openWB/lp/1/PfPhase2", 0],
	["openWB/lp/1/PfPhase3", 0],
	["openWB/lp/1/W", 0],
	["openWB/lp/1/%Soc", 0],

	["openWB/lp/2/boolChargePointConfigured", 0],
	["openWB/lp/2/AConfigured", 0], 
	["openWB/lp/2/APhase1", 0],
	["openWB/lp/2/APhase2", 0],
	["openWB/lp/2/APhase3", 0],
	["openWB/lp/2/kWhCounter", 0],
	["openWB/lp/2/VPhase1", 0],
	["openWB/lp/2/VPhase2", 0],
	["openWB/lp/2/VPhase3", 0],
	["openWB/lp/2/W", 0],

	["openWB/lp/3/boolChargePointConfigured", 0],
	["openWB/lp/3/AConfigured", 0], 
	["openWB/lp/3/APhase1", 0],
	["openWB/lp/3/APhase2", 0],
	["openWB/lp/3/APhase3", 0],
	["openWB/lp/3/kWhCounter", 0],
	["openWB/lp/3/VPhase1", 0],
	["openWB/lp/3/VPhase2", 0],
	["openWB/lp/3/VPhase3", 0],
	["openWB/lp/3/W", 0],

	["openWB/lp/4/boolChargePointConfigured", 0],
	["openWB/lp/4/AConfigured", 0], 
	["openWB/lp/4/APhase1", 0],
	["openWB/lp/4/APhase2", 0],
	["openWB/lp/4/APhase3", 0],
	["openWB/lp/4/kWhCounter", 0],
	["openWB/lp/4/VPhase1", 0],
	["openWB/lp/4/VPhase2", 0],
	["openWB/lp/4/VPhase3", 0],
	["openWB/lp/4/W", 0],

	["openWB/lp/5/boolChargePointConfigured", 0],
	["openWB/lp/5/AConfigured", 0], 
	["openWB/lp/5/APhase1", 0],
	["openWB/lp/5/APhase2", 0],
	["openWB/lp/5/APhase3", 0],
	["openWB/lp/5/kWhCounter", 0],
	["openWB/lp/5/VPhase1", 0],
	["openWB/lp/5/VPhase2", 0],
	["openWB/lp/5/VPhase3", 0],
	["openWB/lp/5/W", 0],

	["openWB/lp/6/boolChargePointConfigured", 0],
	["openWB/lp/6/AConfigured", 0], 
	["openWB/lp/6/APhase1", 0],
	["openWB/lp/6/APhase2", 0],
	["openWB/lp/6/APhase3", 0],
	["openWB/lp/6/kWhCounter", 0],
	["openWB/lp/6/VPhase1", 0],
	["openWB/lp/6/VPhase2", 0],
	["openWB/lp/6/VPhase3", 0],
	["openWB/lp/6/W", 0],

	["openWB/lp/7/boolChargePointConfigured", 0],
	["openWB/lp/7/AConfigured", 0], 
	["openWB/lp/7/APhase1", 0],
	["openWB/lp/7/APhase2", 0],
	["openWB/lp/7/APhase3", 0],
	["openWB/lp/7/kWhCounter", 0],
	["openWB/lp/7/VPhase1", 0],
	["openWB/lp/7/VPhase2", 0],
	["openWB/lp/7/VPhase3", 0],
	["openWB/lp/7/W", 0],

	["openWB/lp/8/boolChargePointConfigured", 0],
	["openWB/lp/8/AConfigured", 0], 
	["openWB/lp/8/APhase1", 0],
	["openWB/lp/8/APhase2", 0],
	["openWB/lp/8/APhase3", 0],
	["openWB/lp/8/kWhCounter", 0],
	["openWB/lp/8/VPhase1", 0],
	["openWB/lp/8/VPhase2", 0],
	["openWB/lp/8/VPhase3", 0],
	["openWB/lp/8/W", 0],

	["openWB/pv/boolPVConfigured", 0],
	["openWB/pv/CounterTillStartPvCharging", 0],
	["openWB/pv/W", 0],
	["openWB/pv/DailyYieldKwh", 0],
	["openWB/pv/MonthlyYieldKwh", 0],
	["openWB/pv/YearlyYieldKwh", 0],
	["openWB/pv/Modul1W", 0],
	["openWB/pv/Modul2W", 0],

	//pvkwhk1
	//daily_pvkwhk1
	//monthly_pvkwhk1
	//yearly_pvkwhk1
	//daily_pvkwhk2
	//monthly_pvkwhk2
	//yearly_pvkwhk2
	//wattbezug

	["openWB/housebattery/boolHouseBatteryConfigured", 0],
	["openWB/housebattery/WhImported", 0],
	["openWB/housebattery/WhExported", 0],
	["openWB/Verbraucher/1/Configured", 0],
	["openWB/Verbraucher/1/Watt", 0],
	["openWB/Verbraucher/1/WhImported", 0],
	["openWB/Verbraucher/1/WhExported", 0],
	["openWB/Verbraucher/2/Configured", 0],
	["openWB/Verbraucher/2/Watt", 0],
	["openWB/Verbraucher/2/WhImported", 0],
	["openWB/Verbraucher/2/WhExported", 0],
];

// holds number of topics flagged 1 initially
var countTopicsNotForPreloader = topicsToSubscribe.filter(row => row[1] === 1).length;

var retries = 0;

//Connect Options
var isSSL = location.protocol == 'https:'
var options = {
	timeout: 5,
	useSSL: isSSL,
	//Gets Called if the connection has sucessfully been established
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
var client = new Messaging.Client(location.host, 9001, clientuid);

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
