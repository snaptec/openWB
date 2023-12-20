#!/usr/bin/env python3
from enum import Enum
import logging
import os
import re
import sys
import threading
import time
from typing import List, Optional
import RPi.GPIO as GPIO

from helpermodules.pub import pub_single
from modules.common.store import ramdisk_read, ramdisk_write
from modules.common.store._util import get_rounding_function_by_digits
from modules.common.fault_state import FaultState
from modules.common.component_state import ChargepointState
from modules.internal_chargepoint_handler import chargepoint_module
from modules.internal_chargepoint_handler.clients import client_factory, ClientHandler
from modules.internal_chargepoint_handler.socket import Socket

basePath = "/var/www/html/openWB"
ramdiskPath = basePath + "/ramdisk"
logFilename = ramdiskPath + "/isss.log"
MAP_LOG_LEVEL = [logging.ERROR, logging.WARNING, logging.DEBUG]


class IsssMode(Enum):
    SOCKET = "socket"
    DUO = "duo"
    DAEMON = "daemon"


logging.basicConfig(filename=ramdiskPath+'/isss.log',
                    format='%(asctime)s - {%(name)s:%(lineno)s} - %(levelname)s - %(message)s',
                    level=MAP_LOG_LEVEL[int(os.environ.get('debug'))])
log = logging.getLogger()
log.error("Loglevel: "+str(int(os.environ.get('debug'))))

pymodbus_logger = logging.getLogger("pymodbus")
pymodbus_logger.setLevel(logging.WARNING)


class UpdateValues:
    MAP_KEY_TO_OLD_TOPIC = {
        "imported": "kWhCounter",
        "exported": None,
        "power": "W",
        "voltages": ["VPhase1", "VPhase2", "VPhase3"],
        "currents": ["APhase1", "APhase2", "APhase3"],
        "power_factors": None,
        "phases_in_use": "countPhasesInUse",
        "charge_state": "boolChargeStat",
        "plug_state": "boolPlugStat",
        "rfid": "LastScannedRfidTag",
    }

    def __init__(self, local_charge_point_num: int) -> None:
        self.local_charge_point_num = local_charge_point_num
        self.old_counter_state = None

    def update_values(self, counter_state: ChargepointState) -> None:
        self.parent_wb = Isss.get_parent_wb()
        self.cp_num_str = str(Isss.get_cp_num(self.local_charge_point_num))
        if self.old_counter_state:
            # iterate over counter_state
            vars_old_counter_state = vars(self.old_counter_state)
            for key, value in vars(counter_state).items():
                # Zählerstatus immer veröffentlichen für Lade-Log-Einträge
                if value != vars_old_counter_state[key] or key == "imported":
                    self._pub_values_to_1_9(key, value)
                    self._pub_values_to_2(key, value)
            self.old_counter_state = counter_state
        else:
            # Bei Neustart alles veröffentlichen
            for key, value in vars(counter_state).items():
                self._pub_values_to_1_9(key, value)
                self._pub_values_to_2(key, value)
            self.old_counter_state = counter_state
        for topic, value in [
                    ("fault_state", 0),
                    ("fault_str", "Keine Fehler.")
                ]:
            self._pub_values_to_2(topic, value)

    def _pub_values_to_1_9(self, key: str, value) -> None:
        def pub_value(topic: str, value):
            pub_single("openWB/lp/"+str(self.local_charge_point_num+1) +
                       "/"+topic, payload=str(value), no_json=True)
            if self.parent_wb != "localhost":
                pub_single("openWB/lp/"+self.cp_num_str+"/"+topic,
                           payload=str(value), hostname=self.parent_wb, no_json=True)
        topic = self.MAP_KEY_TO_OLD_TOPIC.get(key)
        rounding = get_rounding_function_by_digits(2)
        if topic is not None:
            if isinstance(topic, List):
                for i in range(0, 3):
                    pub_value(topic[i], rounding(value[i]))
            else:
                if "power" == key:
                    value = int(value)
                elif "imported" == key:
                    value = value / 1000
                if "rfid" == key:
                    pub_value(self.MAP_KEY_TO_OLD_TOPIC[key], value)
                else:
                    pub_value(self.MAP_KEY_TO_OLD_TOPIC[key], rounding(value))

    def _pub_values_to_2(self, topic: str, value) -> None:
        rounding = get_rounding_function_by_digits(2)
        # fix rfid default value
        if topic == "rfid" and value == "0":
            value = None
        if isinstance(value, (str, bool, type(None))):
            pub_single("openWB/set/chargepoint/" + self.cp_num_str +
                       "/get/"+topic, payload=value, hostname=self.parent_wb)
        else:
            if isinstance(value, list):
                pub_single("openWB/set/chargepoint/" + self.cp_num_str+"/get/"+topic,
                           payload=[rounding(v) for v in value], hostname=self.parent_wb)
            else:
                pub_single("openWB/set/chargepoint/" + self.cp_num_str+"/get/"+topic,
                           payload=rounding(value), hostname=self.parent_wb)


class UpdateState:
    def __init__(self, cp_module: chargepoint_module.ChargepointModule) -> None:
        self.old_phases_to_use = 0
        self.old_set_current = 0
        self.phase_switch_thread = None  # type: Optional[threading.Thread]
        self.cp_interruption_thread = None  # type: Optional[threading.Thread]
        self.cp_module = cp_module
        self.__set_current_error = 0

    def update_state(self) -> None:
        if self.cp_module.local_charge_point_num == 0:
            suffix = ""
        else:
            suffix = "s1"
        try:
            heartbeat = int(ramdisk_read("heartbeat"))
        except (FileNotFoundError, ValueError):
            log.error("Error reading heartbeat. Setting to default 0.")
            heartbeat = 0
        if heartbeat > 80:
            set_current = 0
            log.error("Heartbeat Fehler seit " + str(heartbeat) + "Sekunden keine Verbindung, Stoppe Ladung.")
        else:
            try:
                set_current = int(float(ramdisk_read("llsoll"+suffix)))
                self.__set_current_error = 0
            except (FileNotFoundError, ValueError) as e:
                if isinstance(e, FileNotFoundError):
                    log.error("Didn't find llsoll"+suffix+".")
                else:
                    log.error("Couldn't convert "+str(ramdisk_read("llsoll"+suffix))+" in llsoll"+suffix+" to number.")
                self.__set_current_error += 1
                if self.__set_current_error > 3:
                    log.error("Error reading llsoll. Error counter exceed, setting to default 0.")
                    set_current = 0
                else:
                    log.error("Error reading llsoll. Error counter not exceed, leaving set current unchanged.")
                    return
        try:
            cp_interruption_duration = int(float(ramdisk_read("extcpulp1")))
        except (FileNotFoundError, ValueError):
            log.error("Error reading extcpulp1. Setting to default 3.")
            cp_interruption_duration = 3
        try:
            phases_to_use = int(float(ramdisk_read("u1p3pstat")))
        except (FileNotFoundError, ValueError):
            log.error("Error reading u1p3pstat. Setting to default 3.")
            phases_to_use = 3
        log.debug("Values from ramdisk: set_current" + str(set_current) + " heartbeat " + str(heartbeat) +
                  " phases_to_use " + str(phases_to_use) + "cp_interruption_duration" + str(cp_interruption_duration))

        if self.phase_switch_thread:
            if self.phase_switch_thread.is_alive():
                log.debug("Thread zur Phasenumschaltung an LP"+str(self.cp_module.local_charge_point_num) +
                          " noch aktiv. Es muss erst gewartet werden, bis die Phasenumschaltung abgeschlossen ist.")
                return
        if self.cp_interruption_thread:
            if self.cp_interruption_thread.is_alive():
                log.debug("Thread zur CP-Unterbrechung an LP"+str(self.cp_module.local_charge_point_num) +
                          " noch aktiv. Es muss erst gewartet werden, bis die CP-Unterbrechung abgeschlossen ist.")
                return
        self.cp_module.set_current(set_current)
        if self.old_phases_to_use != phases_to_use and phases_to_use != 0:
            log.debug("Switch Phases from "+str(self.old_phases_to_use) + " to " + str(phases_to_use))
            self.__thread_phase_switch(phases_to_use)
            self.old_phases_to_use = phases_to_use

        if cp_interruption_duration > 0:
            self.__thread_cp_interruption(cp_interruption_duration)

    def __thread_phase_switch(self, phases_to_use: int) -> None:
        self.phase_switch_thread = threading.Thread(
            target=self.cp_module.perform_phase_switch, args=(phases_to_use, 5))
        self.phase_switch_thread.start()
        log.debug("Thread zur Phasenumschaltung an LP"+str(self.cp_module.local_charge_point_num)+" gestartet.")

    def __thread_cp_interruption(self, duration: int) -> None:
        self.cp_interruption_thread = threading.Thread(
            target=self.cp_module.perform_cp_interruption, args=(duration,))
        self.cp_interruption_thread.start()
        log.debug("Thread zur CP-Unterbrechung an LP"+str(self.cp_module.local_charge_point_num)+" gestartet.")
        ramdisk_write("extcpulp1", "0")


class Isss:
    def __init__(self, mode: IsssMode, socket_max_current: int) -> None:
        log.debug("Init isss")
        self.cp0_client_handler = client_factory(0)
        self.cp0 = IsssChargepoint(self.cp0_client_handler, 0, mode, socket_max_current)
        if mode == IsssMode.DUO:
            log.debug("Zweiter Ladepunkt für Duo konfiguriert.")
            self.cp1_client_handler = client_factory(1, self.cp0_client_handler)
            self.cp1 = IsssChargepoint(self.cp1_client_handler, 1, mode, socket_max_current)
        else:
            self.cp1 = None
            self.cp1_client_handler = None
        self.init_gpio()

    def init_gpio(self) -> None:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(37, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)
        GPIO.setup(29, GPIO.OUT)
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(15, GPIO.OUT)
        # GPIOs for socket
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def loop(self) -> None:
        def _loop():
            while True:
                log.setLevel(MAP_LOG_LEVEL[int(os.environ.get('debug'))])
                log.debug("***Start***")
                self.cp0.update()
                if self.cp1:
                    self.cp1.update()
                time.sleep(1.1)
        if self.cp1_client_handler is None:
            with self.cp0_client_handler.serial_client:
                _loop()
        elif self.cp0_client_handler.serial_client == self.cp1_client_handler.serial_client:
            with self.cp0_client_handler.serial_client:
                _loop()
        else:
            with self.cp0_client_handler:
                with self.cp1_client_handler.serial_client:
                    _loop()

    @staticmethod
    def get_cp_num(local_charge_point_num: int) -> int:
        try:
            if local_charge_point_num == 0:
                return int(re.sub(r'\D', '', ramdisk_read("parentCPlp1")))
            else:
                return int(re.sub(r'\D', '', ramdisk_read("parentCPlp2")))
        except Exception:
            FaultState.warning("Es konnte keine Ladepunkt-Nummer ermittelt werden. Auf Default-Wert 0 gesetzt.")
            return 0

    @staticmethod
    def get_parent_wb() -> str:
        # check for parent openWB
        try:
            return ramdisk_read("parentWB").replace('\\n', '').replace('\"', '')
        except Exception:
            FaultState.warning("Für den Betrieb im Nur-Ladepunkt-Modus ist zwingend eine Master-openWB erforderlich.")
            return "localhost"


class IsssChargepoint:
    def __init__(self, client_handler: ClientHandler, local_charge_point_num: int, mode: IsssMode,
                 socket_max_current: int) -> None:
        self.local_charge_point_num = local_charge_point_num
        if local_charge_point_num == 0:
            if mode == IsssMode.SOCKET:
                self.module = Socket(socket_max_current,  local_charge_point_num, client_handler, "localhost")
            else:
                self.module = chargepoint_module.ChargepointModule(local_charge_point_num, client_handler, "localhost")
        else:
            self.module = chargepoint_module.ChargepointModule(local_charge_point_num, client_handler, "localhost")
        self.update_values = UpdateValues(local_charge_point_num)
        self.update_state = UpdateState(self.module)
        self.old_plug_state = False

    def update(self) -> None:
        def __thread_active(thread: Optional[threading.Thread]) -> bool:
            if thread:
                return thread.is_alive()
            else:
                return False
        try:
            if self.local_charge_point_num == 1:
                time.sleep(0.1)
            phase_switch_cp_active = __thread_active(self.update_state.cp_interruption_thread) or __thread_active(
                self.update_state.phase_switch_thread)
            state, _ = self.module.get_values(phase_switch_cp_active)
            log.debug("Published plug state "+str(state.plug_state))
            self.update_values.update_values(state)
            self.update_state.update_state()
        except Exception:
            log.exception("Fehler bei Ladepunkt "+str(self.local_charge_point_num))


Isss(IsssMode(sys.argv[1]), int(sys.argv[2])).loop()
