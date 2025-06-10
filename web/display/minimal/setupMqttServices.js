/**
 * Functions to provide services for MQTT
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

// these topics will be subscribed
// index 1 represents flag if value was received, needed for preloader progress bar
// if flags are preset with 1 they are not counted on reload and page will show even if topic was not received
var topicsToSubscribe = [
	// system topics
	["openWB/system/reloadDisplay", 1],
	["openWB/lp/1/W", 1],
	["openWB/lp/1/%Soc", 1],
	["openWB/lp/1/boolSocConfigured"],
	["openWB/lp/1/boolPlugStat", 1],
	["openWB/lp/1/boolChargeStat", 1],
	["openWB/lp/1/ChargePointEnabled", 1],
];

if (lastmanagementold == 1) {
	topicsToSubscribe.push(
		["openWB/lp/2/W", 1],
		["openWB/lp/2/%Soc", 1],
		["openWB/lp/2/boolSocConfigured"],
		["openWB/lp/2/boolPlugStat", 1],
		["openWB/lp/2/ChargePointEnabled", 1],
		["openWB/lp/2/boolChargeStat", 1],
	);
}

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
		client.connect(options);
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
