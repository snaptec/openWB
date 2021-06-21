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
	// Status Konfiguration Ladepunkt
	["openWB/lp/1/boolChargePointConfigured", 0],
	["openWB/lp/2/boolChargePointConfigured", 0],
	["openWB/lp/3/boolChargePointConfigured", 0],
	["openWB/lp/4/boolChargePointConfigured", 0],
	["openWB/lp/5/boolChargePointConfigured", 0],
	["openWB/lp/6/boolChargePointConfigured", 0],
	["openWB/lp/7/boolChargePointConfigured", 0],
	["openWB/lp/8/boolChargePointConfigured", 0],
	// housebattery Konfiguration
	["openWB/housebattery/boolHouseBatteryConfigured", 0],
	// global topics
	["openWB/global/WHouseConsumption", 1],
	["openWB/global/ChargeMode", 1],
	["openWB/global/WAllChargePoints", 1],
	["openWB/global/strLastmanagementActive", 1],
	["openWB/global/rfidConfigured", 1],
	["openWB/config/get/pv/priorityModeEVBattery", 1],
	["openWB/config/get/pv/minCurrentMinPv", 1],
	// system topics
	["openWB/system/Timestamp", 1],
	["openWB/system/IpAddress", 1],
	["openWB/system/Uptime", 1],
	["openWB/system/Version", 1],
	["openWB/system/wizzardDone", 1],
	["openWB/system/reloadDisplay", 1],
	// pv topics
	["openWB/pv/W", 1],
	["openWB/pv/DailyYieldKwh", 1],
	["openWB/pv/1/boolPVConfigured", 1],
	["openWB/pv/2/boolPVConfigured", 1],
	// evu topics
	["openWB/evu/W", 1],
	// lp topics
	["openWB/lp/1/%Soc", 1],
	["openWB/lp/2/%Soc", 1],
	// geladene kWh seit anstecken des EV
	["openWB/lp/1/kWhChargedSincePlugged", 1],
	["openWB/lp/2/kWhChargedSincePlugged", 1],
	["openWB/lp/3/kWhChargedSincePlugged", 1],
	["openWB/lp/4/kWhChargedSincePlugged", 1],
	["openWB/lp/5/kWhChargedSincePlugged", 1],
	["openWB/lp/6/kWhChargedSincePlugged", 1],
	["openWB/lp/7/kWhChargedSincePlugged", 1],
	["openWB/lp/8/kWhChargedSincePlugged", 1],
	// geladene kWh seit Reset Lademengenbegrenzung
	["openWB/lp/1/kWhActualCharged", 1],
	["openWB/lp/2/kWhActualCharged", 1],
	["openWB/lp/3/kWhActualCharged", 1],
	["openWB/lp/4/kWhActualCharged", 1],
	["openWB/lp/5/kWhActualCharged", 1],
	["openWB/lp/6/kWhActualCharged", 1],
	["openWB/lp/7/kWhActualCharged", 1],
	["openWB/lp/8/kWhActualCharged", 1],
	// Durchschnittsverbrauch
	["openWB/lp/1/energyConsumptionPer100km", 1],
	["openWB/lp/2/energyConsumptionPer100km", 1],
	["openWB/lp/3/energyConsumptionPer100km", 1],
	// Ladeleistung am LP
	["openWB/lp/1/W", 1],
	["openWB/lp/2/W", 1],
	["openWB/lp/3/W", 1],
	["openWB/lp/4/W", 1],
	["openWB/lp/5/W", 1],
	["openWB/lp/6/W", 1],
	["openWB/lp/7/W", 1],
	["openWB/lp/8/W", 1],
	// Anzahl genutzter Phasen während Ladung am LP
	["openWB/lp/1/countPhasesInUse", 1],
	["openWB/lp/2/countPhasesInUse", 1],
	["openWB/lp/3/countPhasesInUse", 1],
	["openWB/lp/4/countPhasesInUse", 1],
	["openWB/lp/5/countPhasesInUse", 1],
	["openWB/lp/6/countPhasesInUse", 1],
	["openWB/lp/7/countPhasesInUse", 1],
	["openWB/lp/8/countPhasesInUse", 1],
	// Status Stecker
	["openWB/lp/1/boolPlugStat", 1],
	["openWB/lp/2/boolPlugStat", 1],
	["openWB/lp/3/boolPlugStat", 1],
	["openWB/lp/4/boolPlugStat", 1],
	["openWB/lp/5/boolPlugStat", 1],
	["openWB/lp/6/boolPlugStat", 1],
	["openWB/lp/7/boolPlugStat", 1],
	["openWB/lp/8/boolPlugStat", 1],
	// Status Laden
	["openWB/lp/1/boolChargeStat", 1],
	["openWB/lp/2/boolChargeStat", 1],
	["openWB/lp/3/boolChargeStat", 1],
	["openWB/lp/4/boolChargeStat", 1],
	["openWB/lp/5/boolChargeStat", 1],
	["openWB/lp/6/boolChargeStat", 1],
	["openWB/lp/7/boolChargeStat", 1],
	["openWB/lp/8/boolChargeStat", 1],
	// Status Konfiguration SoC
	["openWB/lp/1/boolSocConfigured", 1],
	["openWB/lp/2/boolSocConfigured", 1],
	// manual SoC
	["openWB/lp/1/boolSocManual", 1],
	["openWB/lp/2/boolSocManual", 1],
	// Status Nachtladen
	["openWB/lp/1/boolChargeAtNight", 1],
	["openWB/lp/2/boolChargeAtNight", 1],
	// eingestellter Ladestrom
	["openWB/lp/1/AConfigured", 1],
	["openWB/lp/2/AConfigured", 1],
	["openWB/lp/3/AConfigured", 1],
	["openWB/lp/8/AConfigured", 1],
	["openWB/lp/4/AConfigured", 1],
	["openWB/lp/5/AConfigured", 1],
	["openWB/lp/6/AConfigured", 1],
	["openWB/lp/7/AConfigured", 1],
	// Restzeit
	["openWB/lp/1/TimeRemaining", 1],
	["openWB/lp/2/TimeRemaining", 1],
	["openWB/lp/3/TimeRemaining", 1],
	["openWB/lp/4/TimeRemaining", 1],
	["openWB/lp/5/TimeRemaining", 1],
	["openWB/lp/6/TimeRemaining", 1],
	["openWB/lp/7/TimeRemaining", 1],
	["openWB/lp/8/TimeRemaining", 1],
	// Freigabe
	["openWB/lp/1/ChargePointEnabled", 1],
	["openWB/lp/2/ChargePointEnabled", 1],
	["openWB/lp/3/ChargePointEnabled", 1],
	["openWB/lp/4/ChargePointEnabled", 1],
	["openWB/lp/5/ChargePointEnabled", 1],
	["openWB/lp/6/ChargePointEnabled", 1],
	["openWB/lp/7/ChargePointEnabled", 1],
	["openWB/lp/8/ChargePointEnabled", 1],
	// Name LP
	["openWB/lp/1/strChargePointName", 1],
	["openWB/lp/2/strChargePointName", 1],
	["openWB/lp/3/strChargePointName", 1],
	["openWB/lp/4/strChargePointName", 1],
	["openWB/lp/5/strChargePointName", 1],
	["openWB/lp/6/strChargePointName", 1],
	["openWB/lp/7/strChargePointName", 1],
	["openWB/lp/8/strChargePointName", 1],
	// Status Autolock konfiguriert
	["openWB/lp/1/AutolockConfigured", 1],
	["openWB/lp/2/AutolockConfigured", 1],
	["openWB/lp/3/AutolockConfigured", 1],
	["openWB/lp/4/AutolockConfigured", 1],
	["openWB/lp/5/AutolockConfigured", 1],
	["openWB/lp/6/AutolockConfigured", 1],
	["openWB/lp/7/AutolockConfigured", 1],
	["openWB/lp/8/AutolockConfigured", 1],
	// Status Autolock
	["openWB/lp/1/AutolockStatus", 1],
	["openWB/lp/2/AutolockStatus", 1],
	["openWB/lp/3/AutolockStatus", 1],
	["openWB/lp/4/AutolockStatus", 1],
	["openWB/lp/5/AutolockStatus", 1],
	["openWB/lp/6/AutolockStatus", 1],
	["openWB/lp/7/AutolockStatus", 1],
	["openWB/lp/8/AutolockStatus", 1],
	// Sofortladen Stromstärke
	["openWB/lp/1/ADirectModeAmps", 1],
	["openWB/lp/2/ADirectModeAmps", 1],
	["openWB/lp/3/ADirectModeAmps", 1],
	["openWB/lp/4/ADirectModeAmps", 1],
	["openWB/lp/5/ADirectModeAmps", 1],
	["openWB/lp/6/ADirectModeAmps", 1],
	["openWB/lp/7/ADirectModeAmps", 1],
	["openWB/lp/8/ADirectModeAmps", 1],
	// Zielladen
	["openWB/lp/1/boolFinishAtTimeChargeActive", 1],
	// housebattery values
	["openWB/housebattery/W", 1],
	["openWB/housebattery/%Soc", 1],
	// Daily Yields
	["openWB/housebattery/DailyYieldImportKwh", 1],
	["openWB/housebattery/DailyYieldExportKwh", 1],
	["openWB/global/DailyYieldHausverbrauchKwh", 1],
	["openWB/global/DailyYieldAllChargePointsKwh", 1],
	["openWB/evu/DailyYieldImportKwh", 1],
	["openWB/evu/DailyYieldExportKwh", 1],
	// Config Vars Sofort current
	["openWB/config/get/sofort/lp/1/current", 1],
	["openWB/config/get/sofort/lp/2/current", 1],
	["openWB/config/get/sofort/lp/3/current", 1],
	["openWB/config/get/sofort/lp/4/current", 1],
	["openWB/config/get/sofort/lp/5/current", 1],
	["openWB/config/get/sofort/lp/6/current", 1],
	["openWB/config/get/sofort/lp/7/current", 1],
	["openWB/config/get/sofort/lp/8/current", 1],
	["openWB/config/get/sofort/lp/1/chargeLimitation", 1],
	["openWB/config/get/sofort/lp/2/chargeLimitation", 1],
	["openWB/config/get/sofort/lp/3/chargeLimitation", 1],
	["openWB/config/get/sofort/lp/4/chargeLimitation", 1],
	["openWB/config/get/sofort/lp/5/chargeLimitation", 1],
	["openWB/config/get/sofort/lp/6/chargeLimitation", 1],
	["openWB/config/get/sofort/lp/7/chargeLimitation", 1],
	["openWB/config/get/sofort/lp/8/chargeLimitation", 1],
	["openWB/config/get/sofort/lp/1/energyToCharge", 1],
	["openWB/config/get/sofort/lp/2/energyToCharge", 1],
	["openWB/config/get/sofort/lp/3/energyToCharge", 1],
	["openWB/config/get/sofort/lp/4/energyToCharge", 1],
	["openWB/config/get/sofort/lp/5/energyToCharge", 1],
	["openWB/config/get/sofort/lp/6/energyToCharge", 1],
	["openWB/config/get/sofort/lp/7/energyToCharge", 1],
	["openWB/config/get/sofort/lp/8/energyToCharge", 1],
	["openWB/config/get/sofort/lp/1/socToChargeTo", 1],
	["openWB/config/get/sofort/lp/2/socToChargeTo", 1],
	["openWB/pv/bool70PVDynStatus", 1],
	["openWB/config/get/pv/nurpv70dynact", 1],
	// Display configuration
	["openWB/config/get/display/chartEvuMinMax", 1],
	["openWB/config/get/display/chartBatteryMinMax", 1],
	["openWB/config/get/display/chartPvMax", 1],
	["openWB/config/get/display/showHouseConsumption", 1],
	["openWB/config/get/display/chartHouseConsumptionMax", 1],
	["openWB/config/get/display/chartLp/1/max", 1],
	["openWB/config/get/display/chartLp/2/max", 1],
	["openWB/config/get/display/chartLp/3/max", 1],
	["openWB/config/get/display/chartLp/4/max", 1],
	["openWB/config/get/display/chartLp/5/max", 1],
	["openWB/config/get/display/chartLp/6/max", 1],
	["openWB/config/get/display/chartLp/7/max", 1],
	["openWB/config/get/display/chartLp/8/max", 1]

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
		$('#backend .connectionState').text("verbunden");
		// $('#backend .reloadBtn').addClass('hide');
		$('#backend .counter').text(retries+1);
		console.log("connected, resetting counter");
		retries = 0;
		topicsToSubscribe.forEach((topic) => {
			client.subscribe(topic[0], {qos: 0});
		});
	},
	//Gets Called if the connection could not be established
	onFailure: function (message) {
		retries = retries + 1;
		console.log("connection failed, incrementing counter: " + retries);
		$('#backend .connectionState').text("getrennt");
		// $('#backend .reloadBtn').removeClass('hide');
		$('#backend .counter').text(retries+1);
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
	$('#backend .connectionState').text("getrennt");
	$('#backend .reloadBtn').removeClass('hide');
	$('#backend .counter').text(retries+1);
	setTimeout(function() { client.connect(options); }, 5000);
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
