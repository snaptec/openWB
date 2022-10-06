import logging
from abc import abstractmethod
from queue import Queue, Empty
from typing import Optional

from paho.mqtt.client import Client as MqttClient, MQTTMessage

from helpermodules import pub, compatibility
from modules.common.fault_state import FaultState
from modules.common.simcount._simcounter_state import SimCounterState
from modules.common.store import ramdisk_write, ramdisk_read_float

log = logging.getLogger(__name__)


def get_topic(prefix: str) -> str:
    """ ermittelt das zum Präfix gehörende Topic."""
    if prefix == "bezug":
        topic = "evu"
    elif prefix == "pv" or prefix == "pv2":
        topic = prefix
    elif prefix == "speicher":
        topic = "housebattery"
    else:
        raise FaultState.error("Fehler im Modul simcount: Unbekannter Präfix: " + prefix)
    return topic


def get_existing_imports_exports(file: str) -> float:
    try:
        result = ramdisk_read_float(file)
        log.info("Found counter reading <%g Wh> in file <%s>", result, file)
        return result
    except FileNotFoundError:
        return 0


def get_serial():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line[0:6] == 'Serial':
                    return line[10:26]
    except Exception:
        log.exception("Could not read serial from cpuinfo")

    return "0000000000000000"


def read_mqtt_topic(topic: str) -> Optional[str]:
    """Reads and returns the first message received for the specified topic.

    Returns None if no value is received before timeout"""

    def on_message(_client, _userdata, message: MQTTMessage):
        queue.put(message.payload.decode("utf-8"))

    def on_connect(*_args):
        client.subscribe(topic)

    queue = Queue(1)  # type: Queue[str]
    client = MqttClient("openWB-simcounter-" + get_serial())
    try:
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect("localhost", 1883)
        client.loop_start()
        return queue.get(block=True, timeout=.5)
    except Empty:
        return None
    finally:
        client.disconnect()


def restore_value(name: str, prefix: str) -> float:
    """Returns value in Watt-seconds for historic reasons"""
    topic = "openWB/" + get_topic(prefix) + ("/WHImported_temp" if name == "watt0pos" else "/WHExport_temp")
    mqtt_value = read_mqtt_topic(topic)
    log.info("read from broker: %s=%s", topic, mqtt_value)
    if mqtt_value is None:
        result = None
    else:
        try:
            result = float(mqtt_value)
        except ValueError:
            log.warning("Value <%s> from topic <%s> is not a valid number", mqtt_value, topic)
            result = None

    if result is None:
        if prefix == "bezug":
            file = "bezugkwh" if name == "watt0pos" else "einspeisungkwh"
        elif prefix == "pv2":
            file = "pv2kwh"
        elif prefix == "pv":
            file = "pvkwh"
        else:
            file = "speicherikwh" if name == "watt0pos" else "speicherekwh"
        result = get_existing_imports_exports(file) * 3600

    ramdisk_write(prefix + name, result)
    return result


class SimCounterStore:
    @abstractmethod
    def load(self, prefix: str, topic: str) -> Optional[SimCounterState]:
        pass

    @abstractmethod
    def save(self, prefix: str, topic: str, state: SimCounterState):
        pass

    @abstractmethod
    def initialize(self, prefix: str, topic: str, power: float, timestamp: float) -> SimCounterState:
        pass


class SimCounterStoreRamdisk(SimCounterStore):
    def initialize(self, prefix: str, topic: str, power: float, timestamp: float) -> SimCounterState:
        if prefix == "bezug":
            imported = get_existing_imports_exports("bezugkwh")
            exported = get_existing_imports_exports("einspeisungkwh")
        elif prefix == "pv" or prefix == "pv2":
            imported = 0
            exported = get_existing_imports_exports(prefix + "kwh")
        else:
            imported = get_existing_imports_exports("speicherikwh")
            exported = get_existing_imports_exports("speicherekwh")
        result = SimCounterState(timestamp, power, imported, exported)
        self.save(prefix, topic, result)
        return result

    def load(self, prefix: str, topic: str) -> Optional[SimCounterState]:
        try:
            timestamp = ramdisk_read_float(prefix + "sec0")
        except FileNotFoundError:
            return None

        def read_or_restore(name: str) -> float:
            # For historic reasons, the SimCount stored state uses Watt-seconds instead of Watt-hours -> / 3600:
            try:
                return ramdisk_read_float(prefix + name) / 3600
            except Exception:
                return restore_value(name, prefix) / 3600

        return SimCounterState(
            timestamp=timestamp,
            power=ramdisk_read_float(prefix + "wh0"),
            imported=read_or_restore("watt0pos"),
            # abs() weil runs/simcount.py speichert das Zwischenergebnis des Exports negativ ab:
            exported=abs(read_or_restore("watt0neg")),
        )

    def save(self, prefix: str, topic: str, state: SimCounterState):
        topic = get_topic(prefix)
        ramdisk_write(prefix + "sec0", state.timestamp)
        ramdisk_write(prefix + "wh0", state.power)

        # For historic reasons, the SimCount stored state uses Watt-seconds instead of Watt-hours -> * 3600:
        ramdisk_write(prefix + "watt0pos", state.imported * 3600)
        ramdisk_write(prefix + "watt0neg", state.exported * 3600)
        pub.pub_single("openWB/" + topic + "/WHImported_temp", state.imported * 3600, no_json=True)
        pub.pub_single("openWB/" + topic + "/WHExport_temp", state.exported * 3600, no_json=True)


class SimCounterStoreBroker(SimCounterStore):
    def initialize(self, prefix: str, topic: str, power: float, timestamp: float) -> SimCounterState:
        state = SimCounterState(timestamp, power, imported=0, exported=0)
        self.save(prefix, topic, state)
        return state

    def load(self, prefix: str, topic: str) -> Optional[SimCounterState]:
        return None

    def save(self, prefix: str, topic: str, state: SimCounterState):
        pub.Pub().pub(topic + "simulation", vars(state))


def get_sim_counter_store() -> SimCounterStore:
    return SimCounterStoreRamdisk() if compatibility.is_ramdisk_in_use() else SimCounterStoreBroker()
