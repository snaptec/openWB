/**
 * Functions to provide services for MQTT
 * topic set with array var topicsToSubscribe has to be loaded before
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

//Connect Options
var isSSL = location.protocol == 'https:'
var options = {
	timeout: 5,
	useSSL: isSSL,
	//Gets Called if the connection has sucessfully been established
	onSuccess: function () {
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
});

//Gets  called if the websocket/mqtt connection gets disconnected for any reason
client.onConnectionLost = function (responseObject) {
	client.connect(options);
};

//Gets called whenever you receive a message
client.onMessageArrived = function (message) {
    // func processMessages defined in respective processAllMqttMsg_
	processMessages(message.destinationName, message.payloadString);
};

client.onDeliveryComplete = function (token) {
    // func processMessages defined in respective processAllMqttMsg_
	console.log("token");
};

//Creates a new Messaging.Message Object and sends it
function publish(payload, topic) {
	var message = new Messaging.Message(payload);
	message.destinationName = topic;
	message.qos = 2;
	message.retained = true;
	client.send(message);
}
