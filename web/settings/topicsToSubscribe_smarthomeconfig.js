/**
 * set of topics that has to be subscribed for the pv-charging settings
 *
 * @author Kevin Wieland
 * @author Michael Ortenstein
 */

// line[0] = topic
// line[1] = load counter (if needed)

var topicsToSubscribe = [
	// global settings
	["openWB/housebattery/boolHouseBatteryConfigured", 0],
	["openWB/config/get/SmartHome/logLevel", 0],
	["openWB/config/get/SmartHome/maxBatteryPower", 0],
	// SmartHome configuration
	["openWB/config/get/SmartHome/Devices/+/device_configured", 0],
	["openWB/config/get/SmartHome/Devices/+/device_canSwitch", 0],
	["openWB/config/get/SmartHome/Devices/+/device_ip", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measureip", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measureid", 0],
	["openWB/config/get/SmartHome/Devices/+/device_differentMeasurement", 0],
	["openWB/config/get/SmartHome/Devices/+/device_name", 0],
	["openWB/config/get/SmartHome/Devices/+/device_type", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measureType", 0],
	["openWB/config/get/SmartHome/Devices/+/device_einschaltschwelle", 0],
	["openWB/config/get/SmartHome/Devices/+/device_ausschaltschwelle", 0],
	["openWB/config/get/SmartHome/Devices/+/device_einschaltverzoegerung", 0],
	["openWB/config/get/SmartHome/Devices/+/device_maxeinschaltdauer", 0],
	["openWB/config/get/SmartHome/Devices/+/device_mineinschaltdauer", 0],
	["openWB/config/get/SmartHome/Devices/+/device_deactivateWhileEvCharging", 0],
	["openWB/config/get/SmartHome/Devices/+/device_speichersocbeforestop", 0],
	["openWB/config/get/SmartHome/Devices/+/device_speichersocbeforestart", 0],
	["openWB/config/get/SmartHome/Devices/+/device_temperatur_configured", 0],
	["openWB/config/get/SmartHome/Devices/+/device_ausschaltverzoegerung", 0],
	["openWB/config/get/SmartHome/Devices/+/device_einschalturl", 0],
	["openWB/config/get/SmartHome/Devices/+/device_ausschalturl", 0],
	["openWB/config/get/SmartHome/Devices/+/device_leistungurl", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measureurl", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measureurlc", 0],
	["openWB/config/get/SmartHome/Devices/+/device_username", 0],
	["openWB/config/get/SmartHome/Devices/+/device_password", 0],
	["openWB/config/get/SmartHome/Devices/+/device_actor", 0],
	["openWB/config/get/SmartHome/Devices/+/device_acthortype", 0],
	["openWB/config/get/SmartHome/Devices/+/device_acthorpower", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measurejsonurl", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measurejsonpower", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measurejsoncounter", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measureavmusername", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measureavmpassword", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measureavmactor", 0],
	["openWB/config/get/SmartHome/Devices/+/device_finishTime", 0],
	["openWB/config/get/SmartHome/Devices/+/device_startupDetection", 0],
	["openWB/config/get/SmartHome/Devices/+/device_standbyPower", 0],
	["openWB/config/get/SmartHome/Devices/+/device_standbyDuration", 0],
	["openWB/config/get/SmartHome/Devices/+/device_startupMulDetection", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measurePortSdm", 0],
	["openWB/config/get/SmartHome/Devices/+/device_startTime", 0],
	["openWB/config/get/SmartHome/Devices/+/device_endTime", 0],
	["openWB/config/get/SmartHome/Devices/+/device_homeConsumtion", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measuresmaser", 0],
	["openWB/config/get/SmartHome/Devices/+/device_onTime", 0],
	["openWB/config/get/SmartHome/Devices/+/device_onuntilTime", 0],
	["openWB/config/get/SmartHome/Devices/+/device_measuresmaage", 0]

];
