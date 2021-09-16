"""Modul, das die publish-Verbindung zum Broker bereit stellt.
"""

import json
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from . import log

client = None


def setup_connection():
    """ öffnet die Verbindugn zum Broker. Bei Verbindungsabbruch wird automatisch versucht, eine erneute Verbindung herzustellen.
    """
    try:
        global client
        client = mqtt.Client("openWB-python-bulkpublisher-" + str(os.getpid()))
        client.connect("localhost", 1883)
        client.loop_start()
    except Exception as e:
        log.exception_logging(e)

def pub(topic, payload):
    """ published das übergebene Payload als json-Objekt an das übergebene Topic.

    Parameter
    ---------
    topic : str
        Topic, an das gepusht werden soll

    payload : int, str, list, float
        Payload, der gepusht werden soll
    """
    try:
        if payload == "":
            client.publish(topic, payload, qos=0, retain=True)
        else:
            client.publish(topic, payload=json.dumps(payload), qos=0, retain=True)
    except Exception as e:
        log.exception_logging(e)

def delete_connection():
    """ schließt die Verbindung zum Broker.
    """
    try:
        client.loop_stop()
        client.disconnect
    except Exception as e:
        log.exception_logging(e)

def pub_single(topic, payload, hostname):
    """ published eine einzelne Nachricht an einen Host, der nicht der localhost ist.

        Parameter
    ---------
    topic : str
        Topic, an das gepusht werden soll
    payload : int, str, list, float
        Payload, der gepusht werden soll. Nicht als json, da ISSS kein json-Payload verwendet.
    hostname: str
        IP des Hosts
    """
    try:
        publish.single(topic, json.dumps(payload), hostname=hostname)
    except Exception as e:
        log.exception_logging(e)
