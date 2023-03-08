#!/usr/bin/env python3
import logging
import re
from subprocess import Popen
from pathlib import Path
import paho.mqtt.client as mqtt

BASE_PATH = Path(__file__).resolve().parents[2]
RAMDISK_PATH = BASE_PATH / "ramdisk"
REMOTE_SUPPORT_TOPIC = "openWB/set/system/RemoteSupportTest"
ssh_tunnel = None  # type: Popen

logging.basicConfig(
    filename=str(RAMDISK_PATH / "remote_support.log"),
    level=logging.INFO, format='%(asctime)s: %(message)s'
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
    client.subscribe(REMOTE_SUPPORT_TOPIC, 2)


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    """handle incoming messages"""
    global ssh_tunnel
    payload = msg.payload.decode("utf-8")
    if msg.topic == REMOTE_SUPPORT_TOPIC and len(payload) >= 1:
        log.debug("Topic: %s, Message: %s", msg.topic, payload)

        if payload == 'stop':
            if ssh_tunnel is None:
                log.error("received stop tunnel message but ssh tunnel is not running")
            else:
                log.info("stop remote support")
                ssh_tunnel.terminate()
                ssh_tunnel.wait(timeout=3)
                ssh_tunnel = None
        elif re.match(r'^[A-Za-z0-9]+(;[1-9][0-9]+(;[a-zA-Z0-9]+)?)?$', payload):
            if ssh_tunnel is not None:
                log.error("received start tunnel message but ssh tunnel is already running")
            else:
                splitted = payload.split(";")
                token = splitted[0]
                port = splitted[1] if len(splitted) > 1 else "2223"
                user = splitted[2] if len(splitted) > 2 else "getsupport"
                log.info("start remote support")
                ssh_tunnel = Popen(["sshpass", "-p", token, "ssh", "-tt", "-o", "StrictHostKeyChecking=no",
                                               "-o", "ServerAliveInterval 60", "-R", port + ":localhost:22",
                                               user + "@remotesupport.openwb.de"])
                log.info("ssh tunnel running with pid " + ssh_tunnel.pid)
        else:
            log.info("unknown message: " + payload)
        # clear topic
        client.publish(msg.topic, "", qos=2, retain=True)


mqtt_broker_host = "localhost"
client = mqtt.Client("openWB-remote-support-" + get_serial())
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_host, 1883)
client.loop_forever()
client.disconnect()
