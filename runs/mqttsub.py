#!/usr/bin/env python3
import fileinput
import logging
import re
import subprocess
import sys
import threading
import time
from json import loads as json_loads
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Callable, Any, Union, Iterable, Pattern

import paho.mqtt.client as mqtt

from modules.common.store.ramdisk import files

inaction = 0
openwb_conf_file = "/var/www/html/openWB/openwb.conf"
numberOfSupportedDevices = 9  # limit number of smarthome devices
lock = threading.Lock()
RAMDISK_PATH = Path(__file__).resolve().parents[1] / "ramdisk"

logging.basicConfig(filename=str(RAMDISK_PATH / "mqtt.log"), level=logging.DEBUG, format='%(asctime)s: %(message)s')
log = logging.getLogger("MQTT")


def replace_all(change_val, new_val):
    global inaction
    if (inaction == 0):
        inaction = 1
        for line in fileinput.input(openwb_conf_file, inplace=1):
            if line.startswith(change_val):
                line = change_val + new_val + "\n"
            sys.stdout.write(line)
        time.sleep(0.1)
        inaction = 0


def get_config_value(key):
    with fileinput.input(openwb_conf_file) as file:
        for line in file:
            if line.startswith(str(key+"=")):
                return line.split("=", 1)[1]
        return


def get_serial():
    # Extract serial from cpuinfo file
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line[0:6] == 'Serial':
                return line[10:26]
        return "0000000000000000"


mqtt_broker_ip = "localhost"
client = mqtt.Client("openWB-mqttsub-" + get_serial())
ip_allowed = r'^[0-9.]+$'
name_allowed = r'^[a-zA-Z ]+$'
name_number_allowed = r'^[0-9a-zA-Z ]+$'
email_allowed = r'^([\w\.]+)([\w]+)@(\w{2,})\.(\w{2,})$'


Validator = Callable[[str], Any]


def int_range_validator(min: int, max: int) -> Validator:
    def validator(message: str):
        if not min <= int(message) <= max:
            raise ValueError("Expected value between %d and %d, got %s" % (min, max, message))
    return validator


def regex_match_validator(regex: Union[str, Pattern]) -> Validator:
    def validator(message: str):
        if re.match(regex, message) is None:
            raise ValueError("Expected value to match %s, got %s" % (regex, message))
    return validator


def equals_one_of_validator(*options: str) -> Validator:
    def validator(message: str):
        if message not in options:
            raise ValueError("Expected one of %s, got %s" % (options, message))
    return validator


def min_length_validator(min_length: int) -> Validator:
    def validator(message: str):
        if len(message) < min_length:
            raise ValueError("Expected string with length >= %d, got %s" % (min_length, message))
    return validator


def multi_validator(*validators: Validator) -> Validator:
    def validator(message: str):
        for sub_validator in validators:
            sub_validator(message)
    return validator


ip_address_validator = multi_validator(min_length_validator(7), regex_match_validator(ip_allowed))


TopicHandler = Callable[[str, int, str], None]


def create_smart_home_device_config_handler() -> TopicHandler:
    def republish_action(message: str, device_number: int, option: str):
        client.publish(
            "openWB/config/get/SmartHome/Devices/%d/%s" % (device_number, option),
            message,
            qos=0,
            retain=True
        )

    def write_ramdisk_action(prefix: str):
        def action(message: str, device_number: int, _: str):
            RAMDISK_PATH.joinpath("%s_%d" % (prefix, device_number)).write_text(message)
        return action

    def create_topic_handler(validators: Union[Iterable[Validator], Validator] = (),
                             actions: Union[Iterable[TopicHandler], TopicHandler] = (republish_action),
                             map_message: Callable[[str], str] = None) -> TopicHandler:
        validators_iterable = validators if isinstance(validators, Iterable) else (validators,)
        actions_iterable = actions if isinstance(actions, Iterable) else (actions,)

        def run(message: str, device_number: int, option: str) -> None:
            for validator in validators_iterable:
                validator(message)
            for action in actions_iterable:
                action(message, device_number, option)

        def map_run(message: str, device_number: int, option: str):
            run(map_message(message), device_number, option)

        return run if map_message is None else map_run

    smart_home_device_config_topics = {
        "device_configured": create_topic_handler(int_range_validator(0, 1)),
        "device_canSwitch": create_topic_handler(int_range_validator(0, 1)),
        "device_differentMeasurement": create_topic_handler(int_range_validator(0, 1)),
        "device_shauth": create_topic_handler(int_range_validator(0, 1)),
        "device_measureshauth": create_topic_handler(int_range_validator(0, 1)),
        "device_chan": create_topic_handler(int_range_validator(0, 6)),
        "device_nxdacxxtype": create_topic_handler(int_range_validator(0, 3)),
        "device_measchan": create_topic_handler(int_range_validator(0, 6)),
        "device_ip": create_topic_handler(ip_address_validator),
        "device_pbip": create_topic_handler(ip_address_validator),
        "device_pbtype": create_topic_handler(equals_one_of_validator("none", "shellypb")),
        "device_measureip": create_topic_handler(ip_address_validator),
        "device_name": create_topic_handler((min_length_validator(4), regex_match_validator(name_allowed))),
        "device_type": create_topic_handler(
            equals_one_of_validator("none", "shelly", "tasmota", "acthor", "lambda", "elwa", "askoheat", "idm", "vampair",
                                    "stiebel", "http", "avm", "mystrom", "viessmann", "mqtt", "NXDACXX", "ratiotherm"
                                    )),
        "device_measureType": create_topic_handler(
            equals_one_of_validator("shelly", "tasmota", "http", "mystrom", "sdm630", "lovato", "we514", "fronius", "b23",
                                    "json", "avm", "mqtt", "sdm120", "smaem")),
        "device_temperatur_configured": create_topic_handler(int_range_validator(0, 3)),
        "device_einschaltschwelle": create_topic_handler(int_range_validator(-100000, 100000)),
        "device_deactivateper": create_topic_handler(int_range_validator(0, 100)),
        "device_deactivateWhileEvCharging": create_topic_handler(int_range_validator(0, 2)),
        "device_ausschaltschwelle": create_topic_handler(int_range_validator(-100000, 100000)),
        "device_ausschaltverzoegerung": create_topic_handler(int_range_validator(0, 10000)),
        "device_einschaltverzoegerung": create_topic_handler(int_range_validator(0, 100000)),
        "device_updatesec": create_topic_handler(int_range_validator(0, 180)),
        "device_measureid": create_topic_handler(int_range_validator(1, 255)),
        "device_speichersocbeforestart": create_topic_handler(int_range_validator(0, 100)),
        "device_speichersocbeforestop": create_topic_handler(int_range_validator(0, 100)),
        "device_maxeinschaltdauer": create_topic_handler(int_range_validator(0, 100000)),
        "device_mineinschaltdauer": create_topic_handler(int_range_validator(0, 100000)),
        "device_mindayeinschaltdauer": create_topic_handler(int_range_validator(0, 100000)),
        "device_manual_control": create_topic_handler(int_range_validator(0, 1), (
            write_ramdisk_action("smarthome_device_manual_control"), republish_action)),
        "mode": create_topic_handler(int_range_validator(0, 1),
                                     (write_ramdisk_action("smarthome_device_manual"), republish_action)),
        "device_einschalturl": create_topic_handler(),
        "device_ausschalturl": create_topic_handler(),
        "device_leistungurl": create_topic_handler(),
        "device_stateurl": create_topic_handler(),
        "device_measureurlc": create_topic_handler(map_message=lambda message: "" if message == "none" else message),
        "device_measureurl": create_topic_handler(),
        "device_measurejsonurl": create_topic_handler(),
        "device_measurejsonpower": create_topic_handler(),
        "device_measurejsoncounter": create_topic_handler(),
        "device_username": create_topic_handler(),
        "device_password": create_topic_handler(),
        "device_shusername": create_topic_handler(),
        "device_shpassword": create_topic_handler(),
        "device_manwatt": create_topic_handler(int_range_validator(0, 30000)),
        "device_maxueb": create_topic_handler(int_range_validator(0, 30000)),
        "device_measureshusername": create_topic_handler(),
        "device_measureshpassword": create_topic_handler(),
        "device_actor": create_topic_handler(),
        "device_measureavmusername": create_topic_handler(),
        "device_measureavmpassword": create_topic_handler(),
        "device_measureavmactor": create_topic_handler(),
        "device_acthortype": create_topic_handler(equals_one_of_validator("M1", "M3", "9s", "9s18", "9s27", "9s45", "E2M1", "E2M3")),
        "device_lambdaueb": create_topic_handler(equals_one_of_validator("UP", "UN", "UZ")),
        "device_idmueb": create_topic_handler(equals_one_of_validator("UP", "UZ")),
        "device_acthorpower": create_topic_handler(int_range_validator(0, 50000)),
        "device_finishTime": create_topic_handler(regex_match_validator(r"^([01]{0,1}\d|2[0-3]):[0-5]\d$")),
        "device_onTime": create_topic_handler(regex_match_validator(r"^([01]{0,1}\d|2[0-3]):[0-5]\d$")),
        "device_offTime": create_topic_handler(regex_match_validator(r"^([01]{0,1}\d|2[0-3]):[0-5]\d$")),
        "device_onuntilTime": create_topic_handler(regex_match_validator(r"^([01]{0,1}\d|2[0-3]):[0-5]\d$")),
        "device_startTime": create_topic_handler(regex_match_validator(r"^([01]{0,1}\d|2[0-3]):[0-5]\d$")),
        "device_endTime": create_topic_handler(regex_match_validator(r"^([01]{0,1}\d|2[0-3]):[0-5]\d$")),
        "device_homeConsumtion": create_topic_handler(int_range_validator(0, 1)),
        "device_setauto": create_topic_handler(int_range_validator(0, 1)),
        "device_measurePortSdm": create_topic_handler(int_range_validator(0, 9999)),
        "device_dacport": create_topic_handler(int_range_validator(0, 9999)),
        "device_startupDetection": create_topic_handler(int_range_validator(0, 1)),
        "device_standbyPower": create_topic_handler(int_range_validator(0, 1000)),
        "device_nonewatt": create_topic_handler(int_range_validator(0, 10000)),
        "device_idmnav": create_topic_handler(int_range_validator(1, 2)),
        "device_nxdacxxueb": create_topic_handler(int_range_validator(0, 32000)),
        "device_standbyDuration": create_topic_handler(int_range_validator(0, 86400)),
        "device_startupMulDetection": create_topic_handler(int_range_validator(0, 1)),
        "device_measuresmaage": create_topic_handler(int_range_validator(0, 1000)),
        "device_measuresmaser": create_topic_handler(),
    }

    def root_handler(message: str, device_number: int, option: str):
        if not 1 <= device_number <= numberOfSupportedDevices:
            log.error(
                "Unsupported device number %d while setting smart home device configuration %s",
                device_number,
                option
            )
            return
        try:
            handler = smart_home_device_config_topics[option]
        except KeyError:
            log.warning("Ignoring message to unknown config option <%s>", option)
            return
        try:
            handler(message, device_number, option)
            RAMDISK_PATH.joinpath("rereadsmarthomedevices").write_text("1")
        except Exception:
            log.exception("Error setting smart home option <%s> for device <%d>", option, device_number)

    return root_handler


smart_home_device_config_handler = create_smart_home_device_config_handler()


# connect to broker and subscribe to set topics
def on_connect(client: mqtt.Client, userdata, flags: dict, rc: int):
    log.info("Connected")
    client.subscribe("openWB/set/#", 2)
    client.subscribe("openWB/config/set/#", 2)


# handle each set topic
def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    if (len(msg.payload.decode("utf-8")) >= 1):
        lock.acquire()
        try:
            setTopicCleared = False
            # log all messages before any error forces this process to die
            log.debug("Topic: %s, Message: %s", msg.topic, msg.payload.decode("utf-8"))

            if (("openWB/set/lp" in msg.topic) and ("ChargePointEnabled" in msg.topic)):
                devicenumb = re.sub(r'\D', '', msg.topic)
                if (1 <= int(devicenumb) <= 8 and 0 <= int(msg.payload) <= 1):
                    f = open('/var/www/html/openWB/ramdisk/lp'+str(devicenumb)+'enabled', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/lp/"+str(devicenumb)+"/ChargePointEnabled",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (("openWB/set/lp" in msg.topic) and ("ForceSoCUpdate" in msg.topic)):
                devicenumb = re.sub(r'\D', '', msg.topic)
                if (1 <= int(devicenumb) <= 2 and int(msg.payload) == 1):
                    if (int(devicenumb) == 1):
                        soctimerfile = '/var/www/html/openWB/ramdisk/soctimer'
                    elif (int(devicenumb) == 2):
                        soctimerfile = '/var/www/html/openWB/ramdisk/soctimer1'
                    f = open(soctimerfile, 'w')
                    f.write("20005")
                    f.close()

            match = re.match(r"^openWB/config/set/SmartHome/Devices/(\d+)/([^/]+)$", msg.topic)
            if match is not None:
                smart_home_device_config_handler(msg.payload.decode("utf-8"), int(match.group(1)), match.group(2))

            if (msg.topic == "openWB/config/set/SmartHome/maxBatteryPower"):
                if (0 <= int(msg.payload) <= 30000):
                    f = open('/var/www/html/openWB/ramdisk/smarthomehandlermaxbatterypower', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/config/get/SmartHome/maxBatteryPower",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
                    RAMDISK_PATH.joinpath("rereadsmarthomedevices").write_text("1")
            if (msg.topic == "openWB/config/set/SmartHome/logLevel"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    f = open('/var/www/html/openWB/ramdisk/smarthomehandlerloglevel', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/config/get/SmartHome/logLevel",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (("openWB/config/set/lp" in msg.topic) and ("stopchargeafterdisc" in msg.topic)):
                devicenumb = re.sub(r'\D', '', msg.topic)
                if (1 <= int(devicenumb) <= 8 and 0 <= int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "stopchargeafterdisclp" + str(devicenumb) + "=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/lp/" + str(devicenumb) + "/stopchargeafterdisc",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (("openWB/config/set/sofort/lp" in msg.topic) and ("current" in msg.topic)):
                devicenumb = re.sub(r'\D', '', msg.topic)
                if (1 <= int(devicenumb) <= 8 and 6 <= int(msg.payload) <= 32):
                    client.publish("openWB/config/get/sofort/lp/"+str(devicenumb)+"/current",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
                    f = open('/var/www/html/openWB/ramdisk/lp'+str(devicenumb)+'sofortll', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (("openWB/set/lp" in msg.topic) and ("manualSoc" in msg.topic)):
                devicenumb = re.sub(r'\D', '', msg.topic)
                devicenumb_int = int(devicenumb)
                soc = int(msg.payload)
                if 1 <= devicenumb_int <= 2 and 0 <= soc <= 100:
                    if devicenumb_int == 1:
                        soc_suffix = ""
                        counter_suffix = ""
                    else:
                        soc_suffix = str(devicenumb_int - 1)
                        counter_suffix = "s" + soc_suffix
                    for soc_file in ["manual_soc_lp" + devicenumb, "soc" + soc_suffix]:
                        (RAMDISK_PATH / soc_file).write_text(str(soc))
                    RAMDISK_PATH.joinpath("manual_soc_meter_lp" + devicenumb).write_text(
                        RAMDISK_PATH.joinpath("llkwh" + counter_suffix).read_text()
                    )
                    for topic_suffix in ["manualSoc", "%Soc"]:
                        client.publish("openWB/lp/"+devicenumb+"/"+topic_suffix, soc, qos=0, retain=True)
            if (("openWB/config/set/sofort/lp" in msg.topic) and ("energyToCharge" in msg.topic)):
                devicenumb = re.sub(r'\D', '', msg.topic)
                if (1 <= int(devicenumb) <= 8 and 0 <= int(msg.payload) <= 100):
                    if (int(devicenumb) == 1):
                        sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                       "lademkwh=", msg.payload.decode("utf-8")]
                        subprocess.run(sendcommand)
                    if (int(devicenumb) == 2):
                        sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                       "lademkwhs1=", msg.payload.decode("utf-8")]
                        subprocess.run(sendcommand)
                    if (int(devicenumb) == 3):
                        sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                       "lademkwhs2=", msg.payload.decode("utf-8")]
                        subprocess.run(sendcommand)
                    if (int(devicenumb) >= 4):
                        sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                       "lademkwhlp"+str(devicenumb)+"=", msg.payload.decode("utf-8")]
                        subprocess.run(sendcommand)
                    client.publish("openWB/config/get/sofort/lp/"+str(devicenumb)+"/energyToCharge",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (("openWB/config/set/sofort/lp" in msg.topic) and ("resetEnergyToCharge" in msg.topic)):
                devicenumb = re.sub(r'\D', '', msg.topic)
                if (1 <= int(devicenumb) <= 8 and int(msg.payload) == 1):
                    if (int(devicenumb) == 1):
                        f = open('/var/www/html/openWB/ramdisk/aktgeladen', 'w')
                        f.write("0")
                        f.close()
                        f = open('/var/www/html/openWB/ramdisk/gelrlp1', 'w')
                        f.write("0")
                        f.close()
                    if (int(devicenumb) == 2):
                        f = open('/var/www/html/openWB/ramdisk/aktgeladens1', 'w')
                        f.write("0")
                        f.close()
                        f = open('/var/www/html/openWB/ramdisk/gelrlp2', 'w')
                        f.write("0")
                        f.close()
                    if (int(devicenumb) == 3):
                        f = open('/var/www/html/openWB/ramdisk/aktgeladens2', 'w')
                        f.write("0")
                        f.close()
                        f = open('/var/www/html/openWB/ramdisk/gelrlp3', 'w')
                        f.write("0")
                        f.close()
                    if (int(devicenumb) >= 4):
                        f = open('/var/www/html/openWB/ramdisk/aktgeladenlp'+str(devicenumb), 'w')
                        f.write("0")
                        f.close()
                        f = open('/var/www/html/openWB/ramdisk/gelrlp'+str(devicenumb), 'w')
                        f.write("0")
                        f.close()
            if (("openWB/config/set/sofort/lp" in msg.topic) and ("socToChargeTo" in msg.topic)):
                devicenumb = re.sub(r'\D', '', msg.topic)
                if (1 <= int(devicenumb) <= 2 and 0 <= int(msg.payload) <= 100):
                    client.publish("openWB/config/get/sofort/lp/"+str(devicenumb)+"/socToChargeTo",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "sofortsoclp"+str(devicenumb)+"=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
            if (("openWB/config/set/sofort/lp" in msg.topic) and ("etBasedCharging" in msg.topic)):
                devicenumb = re.sub(r'\D', '', msg.topic)
                if (1 <= int(devicenumb) <= 8 and 0 <= int(msg.payload) <= 1):
                    client.publish("openWB/config/get/sofort/lp/"+str(devicenumb)+"/etBasedCharging",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "lp" +
                                   str(devicenumb)+"etbasedcharging=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
            if (("openWB/config/set/sofort/lp" in msg.topic) and ("chargeLimitation" in msg.topic)):
                devicenumb = re.sub(r'\D', '', msg.topic)
                if (3 <= int(devicenumb) <= 8 and 0 <= int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "msmoduslp"+str(devicenumb)+"=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    time.sleep(0.4)
                    if (int(msg.payload) == 1):
                        sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                       "lademstatlp"+str(devicenumb)+"=", "1"]
                        subprocess.run(sendcommand)
                        client.publish("openWB/lp/"+str(devicenumb)+"/boolDirectModeChargekWh",
                                       msg.payload.decode("utf-8"), qos=0, retain=True)
                    else:
                        sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                       "lademstatlp"+str(devicenumb)+"=", "0"]
                        subprocess.run(sendcommand)
                        client.publish("openWB/lp/"+str(devicenumb)+"/boolDirectModeChargekWh", "0", qos=0, retain=True)
                    client.publish("openWB/config/get/sofort/lp/"+str(devicenumb)+"/chargeLimitation",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/minFeedinPowerBeforeStart"):
                if (int(msg.payload) >= -100000 and int(msg.payload) <= 100000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "mindestuberschuss=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/minFeedinPowerBeforeStart",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/maxPowerConsumptionBeforeStop"):
                if (int(msg.payload) >= -100000 and int(msg.payload) <= 100000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "abschaltuberschuss=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/maxPowerConsumptionBeforeStop",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/stopDelay"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 10000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "abschaltverzoegerung=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/stopDelay", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/startDelay"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 100000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "einschaltverzoegerung=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/startDelay", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/minCurrentMinPv"):
                if (int(msg.payload) >= 6 and int(msg.payload) <= 16):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "minimalampv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/minCurrentMinPv",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/1/maxSoc"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 100):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "stopchargepvpercentagelp1=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/1/maxSoc", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/2/maxSoc"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 100):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "stopchargepvpercentagelp2=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/2/maxSoc", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/1/socLimitation"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "stopchargepvatpercentlp1=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/1/socLimitation",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/2/socLimitation"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "stopchargepvatpercentlp2=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/2/socLimitation",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/1/minCurrent"):
                if (int(msg.payload) >= 6 and int(msg.payload) <= 16):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "minimalapv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/1/minCurrent",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/2/minCurrent"):
                if (int(msg.payload) >= 6 and int(msg.payload) <= 16):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "minimalalp2pv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/2/minCurrent",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (("openWB/set/pv" in msg.topic) and ("faultState" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ((1 <= devicenumb <= 2) and (0 <= int(msg.payload) <= 2)):
                    client.publish("openWB/pv/"+str(devicenumb)+"/faultState",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (("openWB/set/pv" in msg.topic) and ("faultStr" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if (1 <= devicenumb <= 2):
                    client.publish("openWB/pv/"+str(devicenumb)+"/faultStr",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/u1p3p/standbyPhases"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 3):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "u1p3pstandby=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/u1p3p/standbyPhases",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/u1p3p/sofortPhases"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 3):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "u1p3psofort=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/u1p3p/sofortPhases",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/u1p3p/nachtPhases"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 3):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "u1p3pnl=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/u1p3p/nachtPhases",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/u1p3p/minundpvPhases"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 4):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "u1p3pminundpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/u1p3p/minundpvPhases",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/u1p3p/nurpvPhases"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 4):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "u1p3pnurpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/u1p3p/nurpvPhases",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/u1p3p/isConfigured"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "u1p3paktiv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/u1p3p/isConfigured",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/global/minEVSECurrentAllowed"):
                if (int(msg.payload) >= 6 and int(msg.payload) <= 32):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "minimalstromstaerke=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/global/minEVSECurrentAllowed",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/global/maxEVSECurrentAllowed"):
                if (int(msg.payload) >= 6 and int(msg.payload) <= 32):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "maximalstromstaerke=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/global/maxEVSECurrentAllowed",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/global/dataProtectionAcknoledged"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "datenschutzack=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/global/dataProtectionAcknoledged",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/1/minSocAlwaysToChargeTo"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 80):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "minnurpvsoclp1=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/1/minSocAlwaysToChargeTo",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/1/maxSocToChargeTo"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 101):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "maxnurpvsoclp1=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/1/maxSocToChargeTo",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/lp/1/minSocAlwaysToChargeToCurrent"):
                if (int(msg.payload) >= 6 and int(msg.payload) <= 32):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "minnurpvsocll=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/lp/1/minSocAlwaysToChargeToCurrent",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/chargeSubmode"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "pvbezugeinspeisung=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/chargeSubmode",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/regulationPoint"):
                if (int(msg.payload) >= -300000 and int(msg.payload) <= 300000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "offsetpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/regulationPoint",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/boolShowPriorityIconInTheme"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "speicherpvui=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/boolShowPriorityIconInTheme",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/minBatteryChargePowerAtEvPriority"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 90000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "speichermaxwatt=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/minBatteryChargePowerAtEvPriority",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/minBatteryDischargeSocAtBattPriority"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 101):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "speichersocnurpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/minBatteryDischargeSocAtBattPriority",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/batteryDischargePowerAtBattPriority"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 90000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "speicherwattnurpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/batteryDischargePowerAtBattPriority",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/socStartChargeAtMinPv"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 101):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "speichersocminpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/socStartChargeAtMinPv",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/socStopChargeAtMinPv"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 101):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "speichersochystminpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/socStopChargeAtMinPv",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/boolAdaptiveCharging"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "adaptpv=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/boolAdaptiveCharging",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/adaptiveChargingFactor"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 100):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "adaptfaktor=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/adaptiveChargingFactor",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/nurpv70dynact"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "nurpv70dynact=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/nurpv70dynact",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/nurpv70dynw"):
                if (int(msg.payload) >= 2000 and int(msg.payload) <= 50000):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "nurpv70dynw=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/nurpv70dynw", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/system/GetRemoteSupport"):
                if (5 <= len(msg.payload.decode("utf-8")) <= 50):
                    f = open('/var/www/html/openWB/ramdisk/remotetoken', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    getsupport = ["/var/www/html/openWB/runs/initremote.sh"]
                    subprocess.run(getsupport)
            if (msg.topic == "openWB/set/hook/HookControl"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 30):
                    hookmsg = msg.payload.decode("utf-8")
                    hooknmb = hookmsg[1:2]
                    hookact = hookmsg[0:1]
                    sendhook = ["/var/www/html/openWB/runs/hookcontrol.sh", hookmsg]
                    subprocess.run(sendhook)
                    client.publish("openWB/hook/"+hooknmb+"/BoolHookStatus", hookact, qos=0, retain=True)
            if (msg.topic == "openWB/config/set/display/displaysleep"):
                if (int(msg.payload) >= 10 and int(msg.payload) <= 1800):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "displaysleep=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/display/displaysleep",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/display/displaypincode"):
                if (int(msg.payload) >= 1000 and int(msg.payload) <= 99999999):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "displaypincode=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    # ! intentionally not publishing PIN code via MQTT !
            if (msg.topic == "openWB/config/set/slave/MinimumAdjustmentInterval"):
                if (int(msg.payload) >= 10 and int(msg.payload) <= 300):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "slaveModeMinimumAdjustmentInterval=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/slave/MinimumAdjustmentInterval",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/slave/SlowRamping"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "slaveModeSlowRamping=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/slave/SlowRamping",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/slave/StandardSocketInstalled"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    standardSocketInstalled = msg.payload.decode("utf-8")
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "standardSocketInstalled=", standardSocketInstalled]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/slave/StandardSocketInstalled",
                                   standardSocketInstalled, qos=0, retain=True)
            if (msg.topic == "openWB/config/set/slave/UseLastChargingPhase"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "slaveModeUseLastChargingPhase=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/slave/UseLastChargingPhase",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (("openWB/config/set/slave/lp" in msg.topic) and ("EnergyLimit" in msg.topic)):
                devicenumb = re.sub(r'\D', '', msg.topic)
                if (1 <= int(devicenumb) <= 8 and -1 <= int(msg.payload) <= 99999999):
                    f = open('/var/www/html/openWB/ramdisk/energyLimitLp'+str(devicenumb), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/config/get/slave/lp/" + str(devicenumb) +
                                   "/EnergyLimit", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/configure/AllowedTotalCurrentPerPhase"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 200):
                    f = open('/var/www/html/openWB/ramdisk/AllowedTotalCurrentPerPhase', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/config/set/slave/SocketApproved"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    f = open('/var/www/html/openWB/ramdisk/socketApproved', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/config/get/slave/SocketApproved",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/configure/AllowedPeakPower"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 300000):
                    f = open('/var/www/html/openWB/ramdisk/AllowedPeakPower', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/FixedChargeCurrentCp1"):
                if (int(msg.payload) >= -1 and int(msg.payload) <= 32):
                    f = open('/var/www/html/openWB/ramdisk/FixedChargeCurrentCp1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/FixedChargeCurrentCp2"):
                if (int(msg.payload) >= -1 and int(msg.payload) <= 32):
                    f = open('/var/www/html/openWB/ramdisk/FixedChargeCurrentCp2', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/SlaveModeAllowedLoadImbalance"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 200):
                    f = open('/var/www/html/openWB/ramdisk/SlaveModeAllowedLoadImbalance', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/AllowedRfidsForSocket"):
                f = open('/var/www/html/openWB/ramdisk/AllowedRfidsForSocket', 'w')
                f.write(msg.payload.decode("utf-8"))
                f.close()
                setTopicCleared = True
            if (msg.topic == "openWB/set/configure/AllowedRfidsForLp1"):
                f = open('/var/www/html/openWB/ramdisk/AllowedRfidsForLp1', 'w')
                f.write(msg.payload.decode("utf-8"))
                f.close()
                setTopicCleared = True
            if (msg.topic == "openWB/set/configure/AllowedRfidsForLp2"):
                f = open('/var/www/html/openWB/ramdisk/AllowedRfidsForLp2', 'w')
                f.write(msg.payload.decode("utf-8"))
                f.close()
                setTopicCleared = True
            if (msg.topic == "openWB/set/configure/LastControllerPublish"):
                f = open('/var/www/html/openWB/ramdisk/LastControllerPublish', 'w')
                f.write(msg.payload.decode("utf-8"))
                f.close()
                setTopicCleared = True
            if (msg.topic == "openWB/set/configure/TotalPower"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 999999):
                    f = open('/var/www/html/openWB/ramdisk/TotalPower', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/TotalCurrentConsumptionOnL1"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 2000):
                    f = open('/var/www/html/openWB/ramdisk/TotalCurrentConsumptionOnL1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/TotalCurrentConsumptionOnL2"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 2000):
                    f = open('/var/www/html/openWB/ramdisk/TotalCurrentConsumptionOnL2', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/TotalCurrentConsumptionOnL3"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 2000):
                    f = open('/var/www/html/openWB/ramdisk/TotalCurrentConsumptionOnL3', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/ImbalanceCurrentConsumptionOnL1"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 2000):
                    f = open('/var/www/html/openWB/ramdisk/ImbalanceCurrentConsumptionOnL1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/ImbalanceCurrentConsumptionOnL2"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 2000):
                    f = open('/var/www/html/openWB/ramdisk/ImbalanceCurrentConsumptionOnL2', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/ImbalanceCurrentConsumptionOnL3"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 2000):
                    f = open('/var/www/html/openWB/ramdisk/ImbalanceCurrentConsumptionOnL3', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/ChargingVehiclesOnL1"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 200):
                    f = open('/var/www/html/openWB/ramdisk/ChargingVehiclesOnL1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/ChargingVehiclesOnL2"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 200):
                    f = open('/var/www/html/openWB/ramdisk/ChargingVehiclesOnL2', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/set/configure/ChargingVehiclesOnL3"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 200):
                    f = open('/var/www/html/openWB/ramdisk/ChargingVehiclesOnL3', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    setTopicCleared = True
            if (msg.topic == "openWB/config/set/global/rfidConfigured"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    rfidMode = msg.payload.decode("utf-8")
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "rfidakt=", rfidMode]
                    subprocess.run(sendcommand)
                    client.publish("openWB/global/rfidConfigured", rfidMode, qos=0, retain=True)
            if (msg.topic == "openWB/config/set/global/slaveMode"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    slaveMode = msg.payload.decode("utf-8")
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "slavemode=", slaveMode]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/global/slaveMode", slaveMode, qos=0, retain=True)
            if (msg.topic == "openWB/config/set/global/lp/1/cpInterrupt"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    einbeziehen = msg.payload.decode("utf-8")
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "cpunterbrechunglp1=", einbeziehen]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/global/lp/1/cpInterrupt", einbeziehen, qos=0, retain=True)
            if (msg.topic == "openWB/config/set/global/lp/2/cpInterrupt"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    einbeziehen = msg.payload.decode("utf-8")
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "cpunterbrechunglp2=", einbeziehen]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/global/lp/2/cpInterrupt", einbeziehen, qos=0, retain=True)
            if (msg.topic == "openWB/config/set/pv/priorityModeEVBattery"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    einbeziehen = msg.payload.decode("utf-8")
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "speicherpveinbeziehen=", einbeziehen]
                    subprocess.run(sendcommand)
                    client.publish("openWB/config/get/pv/priorityModeEVBattery", einbeziehen, qos=0, retain=True)
            if (msg.topic == "openWB/set/graph/LiveGraphDuration"):
                if (int(msg.payload) >= 20 and int(msg.payload) <= 120):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "livegraph=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
            if (msg.topic == "openWB/set/system/SimulateRFID"):
                if (
                    len(str(msg.payload.decode("utf-8"))) >= 1 and
                    bool(re.match(name_number_allowed, msg.payload.decode("utf-8")))
                ):
                    f = open('/var/www/html/openWB/ramdisk/readtag', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/system/PerformUpdate"):
                if (int(msg.payload) == 1):
                    client.publish("openWB/set/system/PerformUpdate", "0", qos=0, retain=True)
                    setTopicCleared = True
                    subprocess.run("/var/www/html/openWB/runs/update.sh")
            if (msg.topic == "openWB/set/system/SendDebug"):
                payload = msg.payload.decode("utf-8")
                if (20 <= len(payload) <= 1000):
                    try:
                        json_payload = json_loads(str(payload))
                    except JSONDecodeError:
                        file = open('/var/www/html/openWB/ramdisk/mqtt.log', 'a')
                        file.write("payload is not valid JSON, fallback to simple text\n")
                        file.close()
                        payload = payload.rpartition('email: ')
                        json_payload = {"message": payload[0], "email": payload[2]}
                    finally:
                        if (re.match(email_allowed, json_payload["email"])):
                            f = open('/var/www/html/openWB/ramdisk/debuguser', 'w')
                            f.write("%s\n%s\n" % (json_payload["message"], json_payload["email"]))
                            f.close()
                            f = open('/var/www/html/openWB/ramdisk/debugemail', 'w')
                            f.write(json_payload["email"] + "\n")
                            f.close()
                        else:
                            file = open('/var/www/html/openWB/ramdisk/mqtt.log', 'a')
                            file.write("payload does not contain a valid email: '%s'\n" % (str(json_payload["email"])))
                            file.close()
                        client.publish("openWB/set/system/SendDebug", "0", qos=0, retain=True)
                        setTopicCleared = True
                        subprocess.run("/var/www/html/openWB/runs/senddebuginit.sh")
            if (msg.topic == "openWB/set/system/reloadDisplay"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    client.publish("openWB/system/reloadDisplay", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/system/releaseTrain"):
                releaseTrain = msg.payload.decode("utf-8")
                if (
                    releaseTrain == "stable17" or releaseTrain == "master" or releaseTrain == "beta" or
                    releaseTrain.startswith("yc/")
                ):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh", "releasetrain=", releaseTrain]
                    subprocess.run(sendcommand)
                    client.publish("openWB/system/releaseTrain", releaseTrain, qos=0, retain=True)
            if (msg.topic == "openWB/set/graph/RequestLiveGraph"):
                if (int(msg.payload) == 1):
                    subprocess.run("/var/www/html/openWB/runs/sendlivegraphdata.sh")
                else:
                    client.publish("openWB/system/LiveGraphData", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestLLiveGraph"):
                if (int(msg.payload) == 1):
                    subprocess.run("/var/www/html/openWB/runs/sendllivegraphdata.sh")
                else:
                    client.publish("openWB/system/1alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/2alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/3alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/4alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/5alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/6alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/7alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/8alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/9alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/10alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/11alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/12alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/13alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/14alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/15alllivevalues", "empty", qos=0, retain=True)
                    client.publish("openWB/system/16alllivevalues", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestDayGraph"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 20501231):
                    sendcommand = ["/var/www/html/openWB/runs/senddaygraphdata.sh", msg.payload]
                    subprocess.run(sendcommand)
                else:
                    client.publish("openWB/system/DayGraphData1", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData2", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData3", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData4", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData5", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData6", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData7", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData8", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData9", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData10", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData11", "empty", qos=0, retain=True)
                    client.publish("openWB/system/DayGraphData12", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestMonthGraph"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 205012):
                    sendcommand = ["/var/www/html/openWB/runs/sendmonthgraphdata.sh", msg.payload]
                    subprocess.run(sendcommand)
                else:
                    client.publish("openWB/system/MonthGraphData1", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData2", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData3", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData4", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData5", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData6", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData7", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData8", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData9", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData10", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData11", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphData12", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestMonthGraphv1"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 205012):
                    sendcommand = ["/var/www/html/openWB/runs/sendmonthgraphdatav1.sh", msg.payload]
                    subprocess.run(sendcommand)
                else:
                    client.publish("openWB/system/MonthGraphDatan1", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan2", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan3", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan4", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan5", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan6", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan7", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan8", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan9", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan10", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan11", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthGraphDatan12", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestYearGraph"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 2050):
                    sendcommand = ["/var/www/html/openWB/runs/sendyeargraphdata.sh", msg.payload]
                    subprocess.run(sendcommand)
                else:
                    client.publish("openWB/system/YearGraphData1", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData2", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData3", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData4", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData5", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData6", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData7", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData8", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData9", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData10", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData11", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphData12", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestYearGraphv1"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 2050):
                    sendcommand = ["/var/www/html/openWB/runs/sendyeargraphdatav1.sh", msg.payload]
                    subprocess.run(sendcommand)
                else:
                    client.publish("openWB/system/YearGraphDatan1", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan2", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan3", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan4", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan5", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan6", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan7", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan8", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan9", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan10", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan11", "empty", qos=0, retain=True)
                    client.publish("openWB/system/YearGraphDatan12", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/system/debug/RequestDebugInfo"):
                if (int(msg.payload) == 1):
                    sendcommand = ["/var/www/html/openWB/runs/sendmqttdebug.sh"]
                    subprocess.run(sendcommand)
                setTopicCleared = True
            if (msg.topic == "openWB/set/graph/RequestMonthLadelog"):
                if (int(msg.payload) >= 1 and int(msg.payload) <= 205012):
                    sendcommand = ["/var/www/html/openWB/runs/sendladelog.sh", msg.payload]
                    subprocess.run(sendcommand)
                else:
                    client.publish("openWB/system/MonthLadelogData1", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData2", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData3", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData4", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData5", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData6", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData7", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData8", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData9", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData10", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData11", "empty", qos=0, retain=True)
                    client.publish("openWB/system/MonthLadelogData12", "empty", qos=0, retain=True)
                setTopicCleared = True
            if (msg.topic == "openWB/set/pv/NurPV70Status"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 1):
                    client.publish("openWB/pv/bool70PVDynStatus", msg.payload.decode("utf-8"), qos=0, retain=True)
                    f = open('/var/www/html/openWB/ramdisk/nurpv70dynstatus', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/RenewMQTT"):
                if (int(msg.payload) == 1):
                    client.publish("openWB/set/RenewMQTT", "0", qos=0, retain=True)
                    setTopicCleared = True
                    f = open('/var/www/html/openWB/ramdisk/renewmqtt', 'w')
                    f.write("1")
                    f.close()
            if (msg.topic == "openWB/set/ChargeMode"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 4):
                    f = open('/var/www/html/openWB/ramdisk/lademodus', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/global/ChargeMode", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/sofort/lp/1/chargeLimitation"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "msmoduslp1=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    if (int(msg.payload) == 1):
                        client.publish("openWB/lp/1/boolDirectModeChargekWh",
                                       msg.payload.decode("utf-8"), qos=0, retain=True)
                    else:
                        client.publish("openWB/lp/1/boolDirectModeChargekWh", "0", qos=0, retain=True)
                    if (int(msg.payload) == 2):
                        client.publish("openWB/lp/1/boolDirectChargeModeSoc", "1", qos=0, retain=True)
                    else:
                        client.publish("openWB/lp/1/boolDirectChargeModeSoc", "0", qos=0, retain=True)
                    client.publish("openWB/config/get/sofort/lp/1/chargeLimitation",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/config/set/sofort/lp/2/chargeLimitation"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    sendcommand = ["/var/www/html/openWB/runs/replaceinconfig.sh",
                                   "msmoduslp2=", msg.payload.decode("utf-8")]
                    subprocess.run(sendcommand)
                    if (int(msg.payload) == 1):
                        client.publish("openWB/lp/2/boolDirectModeChargekWh",
                                       msg.payload.decode("utf-8"), qos=0, retain=True)
                    else:
                        client.publish("openWB/lp/2/boolDirectModeChargekWh", "0", qos=0, retain=True)
                    if (int(msg.payload) == 2):
                        client.publish("openWB/lp/2/boolDirectChargeModeSoc", "1", qos=0, retain=True)
                    else:
                        client.publish("openWB/lp/2/boolDirectChargeModeSoc", "0", qos=0, retain=True)
                    client.publish("openWB/config/get/sofort/lp/2/chargeLimitation",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/lp/1/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replace_all("lademstat=", msg.payload.decode("utf-8"))
                    replace_all("sofortsocstatlp1=", msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replace_all("lademstat=", msg.payload.decode("utf-8"))
                    replace_all("sofortsocstatlp1=", "0")
                if (int(msg.payload) == 2):
                    replace_all("lademstat=", "0")
                    replace_all("sofortsocstatlp1=", "1")
            if (msg.topic == "openWB/set/lp/2/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replace_all("lademstats1=", msg.payload.decode("utf-8"))
                    replace_all("sofortsocstatlp2=", msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replace_all("lademstats1=", msg.payload.decode("utf-8"))
                    replace_all("sofortsocstatlp2=", "0")
                if (int(msg.payload) == 2):
                    replace_all("lademstats1=", "0")
                    replace_all("sofortsocstatlp2=", "1")
            if (msg.topic == "openWB/set/lp/3/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replace_all("lademstats2=", msg.payload.decode("utf-8"))
                    # replace_all("sofortsocstatlp2=",msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replace_all("lademstats2=", msg.payload.decode("utf-8"))
                    # replace_all("sofortsocstatlp2=","0")
                # if (int(msg.payload) == 2):
                #    replace_all("lademstats1=","0")
                #    replace_all("sofortsocstatlp2=","1")
            if (msg.topic == "openWB/set/lp/4/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replace_all("lademstatlp4=", msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replace_all("lademstatlp4=", msg.payload.decode("utf-8"))
            if (msg.topic == "openWB/set/lp/5/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replace_all("lademstatlp5=", msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replace_all("lademstatlp5=", msg.payload.decode("utf-8"))
            if (msg.topic == "openWB/set/lp/6/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replace_all("lademstatlp6=", msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replace_all("lademstatlp6=", msg.payload.decode("utf-8"))
            if (msg.topic == "openWB/set/lp/7/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replace_all("lademstatlp7=", msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replace_all("lademstatlp7=", msg.payload.decode("utf-8"))
            if (msg.topic == "openWB/set/lp/8/DirectChargeSubMode"):
                if (int(msg.payload) == 0):
                    replace_all("lademstatlp8=", msg.payload.decode("utf-8"))
                if (int(msg.payload) == 1):
                    replace_all("lademstatlp8=", msg.payload.decode("utf-8"))
            if (msg.topic == "openWB/set/isss/ClearRfid"):
                if (int(msg.payload) > 0 and int(msg.payload) <= 1):
                    f = open('/var/www/html/openWB/ramdisk/readtag', 'w')
                    f.write("0")
                    f.close()
            if (msg.topic == "openWB/set/isss/Current") and int(get_config_value("isss")) == 1:
                if (float(msg.payload) >= 0 and float(msg.payload) <= 32):
                    f = open('/var/www/html/openWB/ramdisk/llsoll', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/isss/Lp2Current") and int(get_config_value("isss")) == 1:
                if (float(msg.payload) >= 0 and float(msg.payload) <= 32):
                    f = open('/var/www/html/openWB/ramdisk/llsolls1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/isss/U1p3p") and int(get_config_value("isss")) == 1:
                if (int(msg.payload) >= 0 and int(msg.payload) <= 5):
                    f = open('/var/www/html/openWB/ramdisk/u1p3pstat', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/isss/U1p3pLp2") and int(get_config_value("isss")) == 1:
                if (int(msg.payload) >= 0 and int(msg.payload) <= 5):
                    f = open('/var/www/html/openWB/ramdisk/u1p3plp2stat', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/isss/Cpulp1") and int(get_config_value("isss")) == 1:
                if (int(msg.payload) >= 0 and int(msg.payload) <= 5):
                    f = open('/var/www/html/openWB/ramdisk/extcpulp1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/isss/heartbeat") and int(get_config_value("isss")) == 1:
                if (int(msg.payload) >= -1 and int(msg.payload) <= 5):
                    f = open('/var/www/html/openWB/ramdisk/heartbeat', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/isss/parentWB"):
                if int(get_config_value("isss")) == 1:
                    f = open('/var/www/html/openWB/ramdisk/parentWB', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/system/parentWB", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/isss/parentCPlp1"):
                client.publish("openWB/system/parentCPlp1", msg.payload.decode("utf-8"), qos=0, retain=True)
                f = open('/var/www/html/openWB/ramdisk/parentCPlp1', 'w')
                f.write(msg.payload.decode("utf-8"))
                f.close()
            if (msg.topic == "openWB/set/isss/parentCPlp2"):
                client.publish("openWB/system/parentCPlp2", msg.payload.decode("utf-8"), qos=0, retain=True)
                f = open('/var/www/html/openWB/ramdisk/parentCPlp2', 'w')
                f.write(msg.payload.decode("utf-8"))
                f.close()
            if (msg.topic == "openWB/set/awattar/MaxPriceForCharging"):
                if (float(msg.payload) >= -50 and float(msg.payload) <= 95):
                    f = open('/var/www/html/openWB/ramdisk/etprovidermaxprice', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/houseBattery/W"):
                if (float(msg.payload) >= -30000 and float(msg.payload) <= 30000):
                    f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/houseBattery/WhImported"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 9000000):
                    f = open('/var/www/html/openWB/ramdisk/speicherikwh', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/houseBattery/WhExported"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 9000000):
                    f = open('/var/www/html/openWB/ramdisk/speicherekwh', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/houseBattery/%Soc"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 100):
                    f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/houseBattery/faultState"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    client.publish("openWB/housebattery/faultState", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/houseBattery/faultStr"):
                client.publish("openWB/housebattery/faultStr", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/evu/W"):
                if (float(msg.payload) >= -100000 and float(msg.payload) <= 100000):
                    f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/APhase1"):
                if (float(msg.payload) >= -1000 and float(msg.payload) <= 1000):
                    f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/APhase2"):
                if (float(msg.payload) >= -1000 and float(msg.payload) <= 1000):
                    f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/APhase3"):
                if (float(msg.payload) >= -1000 and float(msg.payload) <= 1000):
                    f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/VPhase1"):
                if (float(msg.payload) >= -1000 and float(msg.payload) <= 1000):
                    f = open('/var/www/html/openWB/ramdisk/evuv1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/VPhase2"):
                if (float(msg.payload) >= -1000 and float(msg.payload) <= 1000):
                    f = open('/var/www/html/openWB/ramdisk/evuv2', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/VPhase3"):
                if (float(msg.payload) >= -1000 and float(msg.payload) <= 1000):
                    f = open('/var/www/html/openWB/ramdisk/evuv3', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if msg.topic == "openWB/set/evu/HzFrequenz" or msg.topic == "openWB/set/evu/Hz":
                if (float(msg.payload) >= 0 and float(msg.payload) <= 80):
                    f = open('/var/www/html/openWB/ramdisk/evuhz', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            wphase_match = re.match("openWB/set/evu/WPhase([123])$", msg.topic)
            if wphase_match is not None:
                files.evu.powers_import[int(wphase_match.group(1)) - 1].write(float(msg.payload.decode("utf-8")))
            pfphase_match = re.match("openWB/set/evu/PfPhase([123])$", msg.topic)
            if pfphase_match is not None:
                files.evu.power_factors[int(pfphase_match.group(1)) - 1].write(float(msg.payload.decode("utf-8")))
            if (msg.topic == "openWB/set/evu/WhImported"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 10000000000):
                    f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/WhExported"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 10000000000):
                    f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/evu/faultState"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 2):
                    client.publish("openWB/evu/faultState", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/evu/faultStr"):
                client.publish("openWB/evu/faultStr", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/lp/1/%Soc"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 100):
                    f = open('/var/www/html/openWB/ramdisk/soc', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/2/%Soc"):
                if (float(msg.payload) >= 0 and float(msg.payload) <= 100):
                    f = open('/var/www/html/openWB/ramdisk/soc1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            set_pv_match = re.match(r"^openWB/set/pv/([12])/(.*)$", msg.topic)
            if set_pv_match is not None:
                pv = files.pv[int(set_pv_match.group(1)) - 1]
                subtopic = set_pv_match.group(2)
                if subtopic == "kWhCounter":
                    value = float(msg.payload)
                    if 0 <= value <= 10000000000:
                        pv.energy.write(float(msg.payload) * 1000)
                elif subtopic == "WhCounter":
                    value = float(msg.payload)
                    if 0 <= value <= 10000000000:
                        pv.energy.write(float(msg.payload))
                elif subtopic == "W":
                    value = abs(float(msg.payload))
                    if value <= 100000000:
                        pv.power.write(-float(value))
            if (msg.topic == "openWB/set/lp/1/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp1', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
                    client.publish("openWB/lp/1/AutolockStatus", msg.payload.decode("utf-8"), qos=0, retain=True)
            if (msg.topic == "openWB/set/lp/2/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp2', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/3/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp3', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/4/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp4', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/5/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp5', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/6/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp6', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/7/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp7', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (msg.topic == "openWB/set/lp/8/AutolockStatus"):
                if (int(msg.payload) >= 0 and int(msg.payload) <= 3):
                    f = open('/var/www/html/openWB/ramdisk/autolockstatuslp8', 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (("openWB/set/lp" in msg.topic) and ("faultState" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ((1 <= devicenumb <= 8) and (0 <= int(msg.payload) <= 2)):
                    client.publish("openWB/lp/"+str(devicenumb)+"/faultState",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (("openWB/set/lp" in msg.topic) and ("faultStr" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if (1 <= devicenumb <= 8):
                    client.publish("openWB/lp/"+str(devicenumb)+"/faultStr",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (("openWB/set/lp" in msg.topic) and ("socFaultState" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ((1 <= devicenumb <= 2) and (0 <= int(msg.payload) <= 2)):
                    client.publish("openWB/lp/"+str(devicenumb)+"/socFaultState",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)
            if (("openWB/set/lp" in msg.topic) and ("socFaultStr" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if (1 <= devicenumb <= 2):
                    client.publish("openWB/lp/"+str(devicenumb)+"/socFaultStr",
                                   msg.payload.decode("utf-8"), qos=0, retain=True)

            # Topics for Mqtt-EVSE module
            # ToDo: check if Mqtt-EVSE module is selected!
            # llmodule = get_config_value("evsecon")
            if (("openWB/set/lp" in msg.topic) and ("plugStat" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ((1 <= devicenumb <= 3) and (0 <= int(msg.payload) <= 1)):
                    plugstat = int(msg.payload.decode("utf-8"))
                    if (devicenumb == 1):
                        filename = "plugstat"
                    elif (devicenumb == 2):
                        filename = "plugstats1"
                    elif (devicenumb == 3):
                        filename = "plugstatlp3"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(str(plugstat))
                    f.close()
            if (("openWB/set/lp" in msg.topic) and ("chargeStat" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ((1 <= devicenumb <= 3) and (0 <= int(msg.payload) <= 1)):
                    chargestat = int(msg.payload.decode("utf-8"))
                    if (devicenumb == 1):
                        filename = "chargestat"
                    elif (devicenumb == 2):
                        filename = "chargestats1"
                    elif (devicenumb == 3):
                        filename = "chargestatlp3"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(str(chargestat))
                    f.close()

            # Topics for Mqtt-LL module
            # ToDo: check if Mqtt-LL module is selected!
            # llmodule = get_config_value("ladeleistungsmodul")
            if (("openWB/set/lp" in msg.topic) and ("/W" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ((1 <= devicenumb <= 3) and (0 <= int(msg.payload) <= 100000)):
                    llaktuell = int(msg.payload.decode("utf-8"))
                    if (devicenumb == 1):
                        filename = "llaktuell"
                    elif (devicenumb == 2):
                        filename = "llaktuells1"
                    elif (devicenumb == 3):
                        filename = "llaktuells2"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(str(llaktuell))
                    f.close()
            if (("openWB/set/lp" in msg.topic) and ("kWhCounter" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ((1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 10000000000)):
                    if (devicenumb == 1):
                        filename = "llkwh"
                    elif (devicenumb == 2):
                        filename = "llkwhs1"
                    elif (devicenumb == 3):
                        filename = "llkwhs2"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (("openWB/set/lp" in msg.topic) and ("VPhase1" in msg.topic)):
                devicenumb = int(re.sub(r'\D.', '', msg.topic))
                if ((1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 300)):
                    if (devicenumb == 1):
                        filename = "llv1"
                    elif (devicenumb == 2):
                        filename = "llvs11"
                    elif (devicenumb == 3):
                        filename = "llvs21"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (("openWB/set/lp" in msg.topic) and ("VPhase2" in msg.topic)):
                devicenumb = int(re.sub(r'\D.', '', msg.topic))
                if ((1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 300)):
                    if (devicenumb == 1):
                        filename = "llv2"
                    elif (devicenumb == 2):
                        filename = "llvs12"
                    elif (devicenumb == 3):
                        filename = "llvs22"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (("openWB/set/lp" in msg.topic) and ("VPhase3" in msg.topic)):
                devicenumb = int(re.sub(r'\D.', '', msg.topic))
                if ((1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 300)):
                    if (devicenumb == 1):
                        filename = "llv3"
                    elif (devicenumb == 2):
                        filename = "llvs13"
                    elif (devicenumb == 3):
                        filename = "llvs23"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (("openWB/set/lp" in msg.topic) and ("APhase1" in msg.topic)):
                devicenumb = int(re.sub(r'\D.', '', msg.topic))
                if ((1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 3000)):
                    if (devicenumb == 1):
                        filename = "lla1"
                    elif (devicenumb == 2):
                        filename = "llas11"
                    elif (devicenumb == 3):
                        filename = "llas21"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (("openWB/set/lp" in msg.topic) and ("APhase2" in msg.topic)):
                devicenumb = int(re.sub(r'\D.', '', msg.topic))
                if ((1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 3000)):
                    if (devicenumb == 1):
                        filename = "lla2"
                    elif (devicenumb == 2):
                        filename = "llas12"
                    elif (devicenumb == 3):
                        filename = "llas22"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (("openWB/set/lp" in msg.topic) and ("APhase3" in msg.topic)):
                devicenumb = int(re.sub(r'\D.', '', msg.topic))
                if ((1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 3000)):
                    if (devicenumb == 1):
                        filename = "lla3"
                    elif (devicenumb == 2):
                        filename = "llas13"
                    elif (devicenumb == 3):
                        filename = "llas23"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()
            if (("openWB/set/lp" in msg.topic) and ("HzFrequenz" in msg.topic)):
                devicenumb = int(re.sub(r'\D', '', msg.topic))
                if ((1 <= devicenumb <= 3) and (0 <= float(msg.payload) <= 80)):
                    if (devicenumb == 1):
                        filename = "llhz"
                    elif (devicenumb == 2):
                        filename = "llhzs1"
                    elif (devicenumb == 3):
                        filename = "llhzs2"
                    f = open('/var/www/html/openWB/ramdisk/'+str(filename), 'w')
                    f.write(msg.payload.decode("utf-8"))
                    f.close()

            # clear all set topics if not already done
            if not setTopicCleared:
                client.publish(msg.topic, "", qos=2, retain=True)
        except Exception:
            log.exception("Error handling MQTT-Message")
        finally:
            lock.release()


client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()
