"""Modul, das die publish-Verbindung zum Broker bereit stellt.
"""

import json
import os
from typing import Optional

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from . import log

client = None  # type: Optional[mqtt.Client]


def setup_connection():
    """Öffnet die Verbindung zum Broker.

    Bei Verbindungsabbruch wird automatisch versucht, eine erneute Verbindung herzustellen.
    """
    try:
        global client
        client = mqtt.Client("openWB-python-bulkpublisher-" + str(os.getpid()))
        client.connect("localhost", 1886)
        client.loop_start()
    except Exception:
        log.MainLogger().exception("Fehler im pub-Modul")


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
    except Exception:
        log.MainLogger().exception("Fehler im pub-Modul")


def delete_connection():
    """ schließt die Verbindung zum Broker.
    """
    try:
        client.loop_stop()
        client.disconnect
    except Exception:
        log.MainLogger().exception("Fehler im pub-Modul")


def pub_single(topic, payload, hostname="localhost", no_json=False):
    """ published eine einzelne Nachricht an einen Host, der nicht der localhost ist.

        Parameter
    ---------
    topic : str
        Topic, an das gepusht werden soll
    payload : int, str, list, float
        Payload, der gepusht werden soll. Nicht als json, da ISSS kein json-Payload verwendet.
    hostname: str
        IP des Hosts
    no_json: bool
        Kompabilität mit isss, die ramdisk verwenden.
    """
    try:
        if no_json:
            publish.single(topic, payload, hostname=hostname, retain=True)
        else:
            publish.single(topic, json.dumps(payload), hostname=hostname, retain=True)
    except Exception:
        log.MainLogger().exception("Fehler im pub-Modul")
