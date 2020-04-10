/**
 * Functions to provide services for MQTT
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

// these topics will be subscribed
// index 1 represents flag if value was received, needed for preloaderbar progress
var topicsToSubscribe = [
	// graph topcis
	["openWB/global/awattar/MaxPriceForCharging", 0],
	["openWB/global/awattar/pricelist", 0],
	["openWB/graph/lastlivevalues", 0],
	["openWB/graph/1alllivevalues", 0],
	["openWB/graph/2alllivevalues", 0],
	["openWB/graph/3alllivevalues", 0],
	["openWB/graph/4alllivevalues", 0],
	["openWB/graph/5alllivevalues", 0],
	["openWB/graph/6alllivevalues", 0],
	["openWB/graph/7alllivevalues", 0],
	["openWB/graph/8alllivevalues", 0],
	["openWB/graph/boolDisplayHouseConsumption", 0],
	["openWB/graph/boolDisplayLoad1", 0],
	["openWB/graph/boolDisplayLoad2", 0],
	["openWB/graph/boolDisplayLp1Soc", 0],
	["openWB/graph/boolDisplayLp2Soc", 0],
	["openWB/graph/boolDisplayLp1", 0],
	["openWB/graph/boolDisplayLp2", 0],
	["openWB/graph/boolDisplayLp3", 0],
	["openWB/graph/boolDisplayLp4", 0],
	["openWB/graph/boolDisplayLp5", 0],
	["openWB/graph/boolDisplayLp6", 0],
	["openWB/graph/boolDisplayLp7", 0],
	["openWB/graph/boolDisplayLp8", 0],
	["openWB/graph/boolDisplayLpAll", 0],
	["openWB/graph/boolDisplaySpeicherSoc", 0],
	["openWB/graph/boolDisplaySpeicher", 0],
	["openWB/graph/boolDisplayEvu", 0],
	["openWB/graph/boolDisplayLegend", 0],
	["openWB/graph/boolDisplayLiveGraph", 0],
	["openWB/graph/boolDisplayPv", 0],
	// global topics
	["openWB/global/WHouseConsumption", 0],
	["openWB/global/ChargeMode", 0],
	["openWB/global/WAllChargePoints", 0],
	["openWB/global/strLastmanagementActive", 0],
	// system topics
	["openWB/system/Timestamp", 0],
	// pv topics
	["openWB/pv/W", 0],
	["openWB/pv/DailyYieldKwh", 0],
	// evu topics
	["openWB/evu/W", 0],
	// lp topics
		["openWB/lp/1/%Soc", 0],
		["openWB/lp/2/%Soc", 0],
		// geladene kWh seit anstecken des EV
		["openWB/lp/1/kWhChargedSincePlugged", 0],
		["openWB/lp/2/kWhChargedSincePlugged", 0],
		["openWB/lp/3/kWhChargedSincePlugged", 0],
		["openWB/lp/4/kWhChargedSincePlugged", 0],
		["openWB/lp/5/kWhChargedSincePlugged", 0],
		["openWB/lp/6/kWhChargedSincePlugged", 0],
		["openWB/lp/7/kWhChargedSincePlugged", 0],
		["openWB/lp/8/kWhChargedSincePlugged", 0],
		// Durchschnittsverbrauch
		["openWB/lp/1/energyConsumptionPer100km", 0],
		["openWB/lp/2/energyConsumptionPer100km", 0],
		["openWB/lp/3/energyConsumptionPer100km", 0],
		// Ladeleistung am LP
		["openWB/lp/1/W", 0],
		["openWB/lp/2/W", 0],
		["openWB/lp/3/W", 0],
		["openWB/lp/4/W", 0],
		["openWB/lp/5/W", 0],
		["openWB/lp/6/W", 0],
		["openWB/lp/7/W", 0],
		["openWB/lp/8/W", 0],
		// Status Stecker
		["openWB/lp/1/boolPlugStat", 0],
		["openWB/lp/2/boolPlugStat", 0],
		["openWB/lp/3/boolPlugStat", 0],
		["openWB/lp/4/boolPlugStat", 0],
		["openWB/lp/5/boolPlugStat", 0],
		["openWB/lp/6/boolPlugStat", 0],
		["openWB/lp/7/boolPlugStat", 0],
		["openWB/lp/8/boolPlugStat", 0],
		// Status Laden
		["openWB/lp/1/boolChargeStat", 0],
		["openWB/lp/2/boolChargeStat", 0],
		["openWB/lp/3/boolChargeStat", 0],
		["openWB/lp/4/boolChargeStat", 0],
		["openWB/lp/5/boolChargeStat", 0],
		["openWB/lp/6/boolChargeStat", 0],
		["openWB/lp/7/boolChargeStat", 0],
		["openWB/lp/8/boolChargeStat", 0],
		// Status Konfiguration SoC
		["openWB/lp/1/boolSocConfigured", 0],
		["openWB/lp/2/boolSocConfigured", 0],
		// eingestellter Ladestrom
		["openWB/lp/1/AConfigured", 0],
		["openWB/lp/2/AConfigured", 0],
		["openWB/lp/3/AConfigured", 0],
		["openWB/lp/8/AConfigured", 0],
		["openWB/lp/4/AConfigured", 0],
		["openWB/lp/5/AConfigured", 0],
		["openWB/lp/6/AConfigured", 0],
		["openWB/lp/7/AConfigured", 0],
		// Restzeit
		["openWB/lp/1/TimeRemaining", 0],
		["openWB/lp/2/TimeRemaining", 0],
		["openWB/lp/3/TimeRemaining", 0],

		["openWB/lp/1/ChargeStatus", 0],
		["openWB/lp/2/ChargeStatus", 0],
		["openWB/lp/3/ChargeStatus", 0],
		["openWB/lp/4/ChargeStatus", 0],
		["openWB/lp/5/ChargeStatus", 0],
		["openWB/lp/6/ChargeStatus", 0],
		["openWB/lp/7/ChargeStatus", 0],
		["openWB/lp/8/ChargeStatus", 0],
		// Status Konfiguration Ladepunkt
		["openWB/lp/1/boolChargePointConfigured", 0],
		["openWB/lp/2/boolChargePointConfigured", 0],
		["openWB/lp/3/boolChargePointConfigured", 0],
		["openWB/lp/4/boolChargePointConfigured", 0],
		["openWB/lp/5/boolChargePointConfigured", 0],
		["openWB/lp/6/boolChargePointConfigured", 0],
		["openWB/lp/7/boolChargePointConfigured", 0],
		["openWB/lp/8/boolChargePointConfigured", 0],

		["openWB/lp/1/boolDirectChargeMode_none_kwh_soc", 0],
		["openWB/lp/2/boolDirectChargeMode_none_kwh_soc", 0],
		["openWB/lp/3/boolDirectChargeMode_none_kwh_soc", 0],
		["openWB/lp/4/boolDirectChargeMode_none_kwh_soc", 0],
		["openWB/lp/5/boolDirectChargeMode_none_kwh_soc", 0],
		["openWB/lp/6/boolDirectChargeMode_none_kwh_soc", 0],
		["openWB/lp/7/boolDirectChargeMode_none_kwh_soc", 0],
		["openWB/lp/8/boolDirectChargeMode_none_kwh_soc", 0],
		//
		["openWB/lp/1/ChargePointEnabled", 0],
		["openWB/lp/2/ChargePointEnabled", 0],
		["openWB/lp/3/ChargePointEnabled", 0],
		["openWB/lp/4/ChargePointEnabled", 0],
		["openWB/lp/5/ChargePointEnabled", 0],
		["openWB/lp/6/ChargePointEnabled", 0],
		["openWB/lp/7/ChargePointEnabled", 0],
		["openWB/lp/8/ChargePointEnabled", 0],
		// Name LP
		["openWB/lp/1/strChargePointName", 0],
		["openWB/lp/2/strChargePointName", 0],
		["openWB/lp/3/strChargePointName", 0],
		["openWB/lp/4/strChargePointName", 0],
		["openWB/lp/5/strChargePointName", 0],
		["openWB/lp/6/strChargePointName", 0],
		["openWB/lp/7/strChargePointName", 0],
		["openWB/lp/8/strChargePointName", 0],
		// Status Autolock konfiguriert
		["openWB/lp/1/AutolockConfigured", 0],
		["openWB/lp/2/AutolockConfigured", 0],
		["openWB/lp/3/AutolockConfigured", 0],
		["openWB/lp/4/AutolockConfigured", 0],
		["openWB/lp/5/AutolockConfigured", 0],
		["openWB/lp/6/AutolockConfigured", 0],
		["openWB/lp/7/AutolockConfigured", 0],
		["openWB/lp/8/AutolockConfigured", 0],
		// Status Autolock
		["openWB/lp/1/AutolockStatus", 0],
		["openWB/lp/2/AutolockStatus", 0],
		["openWB/lp/3/AutolockStatus", 0],
		["openWB/lp/4/AutolockStatus", 0],
		["openWB/lp/5/AutolockStatus", 0],
		["openWB/lp/6/AutolockStatus", 0],
		["openWB/lp/7/AutolockStatus", 0],
		["openWB/lp/8/AutolockStatus", 0],

		["openWB/lp/1/ADirectModeAmps", 0],
		["openWB/lp/2/ADirectModeAmps", 0],
		["openWB/lp/3/ADirectModeAmps", 0],
		["openWB/lp/4/ADirectModeAmps", 0],
		["openWB/lp/5/ADirectModeAmps", 0],
		["openWB/lp/6/ADirectModeAmps", 0],
		["openWB/lp/7/ADirectModeAmps", 0],
		["openWB/lp/8/ADirectModeAmps", 0],
	// housebattery topics
	["openWB/housebattery/boolHouseBatteryConfigured", 0],
	["openWB/housebattery/W", 0],
	["openWB/housebattery/%Soc", 0],
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
			client.subscribe(topic[0], {qos: 0});
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
}
