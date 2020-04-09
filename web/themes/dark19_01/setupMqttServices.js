/**
 * Functions to provide services for MQTT
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

// these topics will always be subscribed
// topics for the charge points are subscribed only for configured
// # (hash character) – multi level wildcard
// + (plus character) -single level wildcard
var topicsToSubscribe = [
	"openWB/global/#",
	"openWB/evu/W",
	"openWB/pv/W",
	"openWB/pv/DailyYieldKwh",
	"openWB/housebattery/#",
	"openWB/system/Timestamp",

	"openWB/graph/lastlivevalues",
	"openWB/graph/1alllivevalues",
	"openWB/graph/2alllivevalues",
	"openWB/graph/3alllivevalues",
	"openWB/graph/4alllivevalues",
	"openWB/graph/5alllivevalues",
	"openWB/graph/6alllivevalues",
	"openWB/graph/7alllivevalues",
	"openWB/graph/8alllivevalues",
	"openWB/graph/boolDisplayHouseConsumption",
	"openWB/graph/boolDisplayLoad1",
	"openWB/graph/boolDisplayLoad2",
	"openWB/graph/boolDisplayLp1Soc",
	"openWB/graph/boolDisplayLp2Soc",
	"openWB/graph/boolDisplayLp1",
	"openWB/graph/boolDisplayLp2",
	"openWB/graph/boolDisplayLp3",
	"openWB/graph/boolDisplayLp4",
	"openWB/graph/boolDisplayLp5",
	"openWB/graph/boolDisplayLp6",
	"openWB/graph/boolDisplayLp7",
	"openWB/graph/boolDisplayLp8",
	"openWB/graph/boolDisplayLpAll",
	"openWB/graph/boolDisplaySpeicherSoc",
	"openWB/graph/boolDisplaySpeicher",
	"openWB/graph/boolDisplayEvu",
	"openWB/graph/boolDisplayLegend",
	"openWB/graph/boolDisplayLiveGraph",
	"openWB/graph/boolDisplayPv"
];

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
			client.subscribe(topic, {qos: 0});
		});
		// check which lp is configured and subscribe to topics
		// configured lp all have class lpEnableSpan
		$(".lpEnableSpan").each(function() {
			var lp = $(this).attr('lp');
			var topic = "openWB/lp/" + lp + "/#";
			client.subscribe(topic, {qos: 0});
		});
	},
	//Gets Called if the connection could not be established
	onFailure: function (message) {
		client.connect(options);
	}
};

var clientuid = Math.random().toString(36).replace(/[^a-z]+/g, "").substr(0, 5);
var client = new Messaging.Client(location.host, 9001, clientuid);

$(document).ready(function(){
	client.connect(options);
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
}
