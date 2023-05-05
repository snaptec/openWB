import logging
from abc import abstractmethod
from enum import Enum
from queue import Queue, Empty
from typing import Optional

from paho.mqtt.client import Client as MqttClient, MQTTMessage

from helpermodules import pub, compatibility
from modules.common.simcount.simcounter_state import SimCounterState
from modules.common.store import ramdisk_write, ramdisk_read_float
from modules.common.store.ramdisk.io import RamdiskReadError

POSTFIX_EXPORT = "watt0neg"
POSTFIX_IMPORT = "watt0pos"

log = logging.getLogger(__name__)


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


class SimCountPrefix(Enum):
    PV = ("pv", None, "pvkwh")
    PV2 = ("pv2", None, "pvkwh2")
    BEZUG = ("evu", "bezugkwh", "einspeisungkwh")
    SPEICHER = ("housebattery", "speicherikwh", "speicherekwh")

    def __init__(self, topic: str, import_file: Optional[str], export_file: str):
        self.topic = topic
        self.import_file = import_file
        self.export_file = export_file

    def read_import(self) -> float:
        return self.__read_file(self.import_file)

    def read_export(self) -> float:
        return self.__read_file(self.export_file)

    @staticmethod
    def __read_file(file: str) -> float:
        if file is None:
            return 0.0
        try:
            result = ramdisk_read_float(file)
            log.info("Found counter reading <%g Wh> in file <%s>", result, file)
            return result
        except FileNotFoundError:
            return 0.0


def restore_value(prefix_str: str, postfix: str) -> float:
    prefix = SimCountPrefix[prefix_str.upper()]
    #  topic = "openWB/" + prefix.topic + ("/WHImported_temp" if postfix == POSTFIX_IMPORT else "/WHExport_temp")
    if prefix.topic == "pv2":
        topic = "openWB/pv" + ("/WH2Imported_temp" if postfix == POSTFIX_IMPORT else "/WH2Export_temp")
    else:
        topic = "openWB/" + prefix.topic + ("/WHImported_temp" if postfix == POSTFIX_IMPORT else "/WHExport_temp")
    mqtt_value = read_mqtt_topic(topic)
    log.info("read from broker: %s=%s", topic, mqtt_value)
    if mqtt_value is None:
        result = None
    else:
        try:
            # MQTT-Value is in Watt-seconds for historic reasons -> / 3600
            result = float(mqtt_value) / 3600
        except ValueError:
            log.warning("Value <%s> from topic <%s> is not a valid number", mqtt_value, topic)
            result = None

    if result is None:
        result = (prefix.read_import if postfix == POSTFIX_IMPORT else prefix.read_export)()

    ramdisk_write(prefix_str + postfix, result)
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
        result = SimCounterState(
            timestamp, power, restore_value(prefix, POSTFIX_IMPORT), restore_value(prefix, POSTFIX_EXPORT)
        )
        self.save(prefix, topic, result)
        return result

    def load(self, prefix: str, topic: str) -> Optional[SimCounterState]:
        try:
            timestamp = ramdisk_read_float(prefix + "sec0")
        except FileNotFoundError:
            return None

        def read_or_restore(postfix: str) -> float:
            try:
                # ramdisk value is in watt-seconds for historic reasons -> / 3600
                return ramdisk_read_float(prefix + postfix) / 3600
            except (FileNotFoundError, RamdiskReadError) as e:
                log.warning("Read from ramdisk failed: %s. Attempting restore from broker", e)
            return restore_value(prefix, postfix)

        return SimCounterState(
            timestamp=timestamp,
            power=ramdisk_read_float(prefix + "wh0"),
            imported=read_or_restore(POSTFIX_IMPORT),
            # abs() weil runs/simcount.py speichert das Zwischenergebnis des Exports negativ ab:
            exported=abs(read_or_restore(POSTFIX_EXPORT)),
        )

    def save(self, prefix: str, topic: str, state: SimCounterState):
        topic = SimCountPrefix[prefix.upper()].topic
        ramdisk_write(prefix + "sec0", state.timestamp)
        ramdisk_write(prefix + "wh0", state.power)

        # For historic reasons, the SimCount stored state uses Watt-seconds instead of Watt-hours -> * 3600:
        ramdisk_write(prefix + POSTFIX_IMPORT, state.imported * 3600)
        ramdisk_write(prefix + POSTFIX_EXPORT, state.exported * 3600)
        if topic == "pv2":
            pub.pub_single("openWB/pv/WH2Imported_temp", state.imported * 3600, no_json=True)
            pub.pub_single("openWB/pv/WH2Export_temp", state.exported * 3600, no_json=True)
        else:
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
