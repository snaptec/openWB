#!/usr/bin/env python3
import logging
import subprocess
from pathlib import Path
import paho.mqtt.client as mqtt

BASE_PATH = Path(__file__).resolve().parents[2]
RAMDISK_PATH = BASE_PATH / "ramdisk"

logging.basicConfig(
    filename=str(RAMDISK_PATH / "remote_support.log"),
    level=logging.DEBUG, format='%(asctime)s: %(message)s'
)
log = logging.getLogger("RemoteSupport")


def get_serial():
    """Extract serial from cpuinfo file"""
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line[0:6] == 'Serial':
                return line[10:26]
        return "0000000000000000"


def on_connect(client: mqtt.Client, userdata, flags: dict, rc: int):
    """connect to broker and subscribe to set topics"""
    log.info("Connected")
    client.subscribe("openWB/set/system/GetRemoteSupport", 2)


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    """handle incoming messages"""
    if (len(msg.payload.decode("utf-8")) >= 1):
        log.debug("Topic: %s, Message: %s", msg.topic, msg.payload.decode("utf-8"))

        if (msg.topic == "openWB/set/system/GetRemoteSupport"):
            if (5 <= len(msg.payload.decode("utf-8")) <= 50):
                log.debug("token file: " + str(RAMDISK_PATH / "remote_support_token"))
                with open(str(RAMDISK_PATH / "remote_support_token"), "w") as file:
                    file.write(msg.payload.decode("utf-8"))
                log.debug("init remote support: " + str(BASE_PATH / "runs" / "remoteSupport" / "initRemoteSupport.sh"))
                subprocess.run([str(BASE_PATH / "runs" / "remoteSupport" / "initRemoteSupport.sh")])
        # clear set topic
        client.publish(msg.topic, "", qos=2, retain=True)


mqtt_broker_ip = "localhost"
client = mqtt.Client("openWB-remote-support-" + get_serial())
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()
