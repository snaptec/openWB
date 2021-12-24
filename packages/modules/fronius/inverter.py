#!/usr/bin/env python3
from typing import Optional, Tuple
import paho.mqtt.client as mqtt
import time

import requests
from helpermodules import log
from helpermodules import pub
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from helpermodules import compatibility


def get_default_config() -> dict:
    return {
        "name": "Fronius Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration":
        {
            "ip_address2": "none",
            "gen24": False
        }
    }


class FroniusInverter:
    def __init__(self, device_id: int, component_config: dict, device_config: dict) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.device_config = device_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, bat: bool) -> float:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        gen24 = self.component_config["configuration"]["gen24"]

        # Rückgabewert ist die aktuelle Wirkleistung in [W].
        params = (
            ('Scope', 'System'),
        )
        response = requests.get(
            'http://' + self.device_config["ip_address"] + '/solar_api/v1/GetPowerFlowRealtimeData.fcgi', params=params,
            timeout=3)
        response.raise_for_status()
        try:
            power = float(response.json()["Body"]["Data"]["Site"]["P_PV"])
        except TypeError:
            # Ohne PV Produktion liefert der WR 'null', ersetze durch Zahl 0
            power = 0

        power2, counter2 = self.__get_wr2()
        power += power2
        power1 = power
        power *= -1
        topic = "openWB/set/system/device/" + str(self.__device_id)+"/component/" + str(self.component_config["id"])+"/"
        if gen24:
            _, counter = self.__sim_count.sim_count(power, topic=topic, data=self.__simulation, prefix="pv")
        else:
            counter = float(response.json()["Body"]["Data"]["Site"]["E_Total"])
            daily_yield = float(response.json()["Body"]["Data"]["Site"]["E_Day"])
            counter, counter_start, counter_offset = self.__calculate_offset(counter, daily_yield)
            counter = counter + counter2
            if counter > 0 and self.component_config["configuration"]["ip_address2"] == "none":
                counter = self.__add_and_save_offset(daily_yield, counter, counter_start, counter_offset)

        if bat is True:
            _, counter = self.__sim_count.sim_count(power, topic=topic, data=self.__simulation, prefix="pv")

        inverter_state = InverterState(
            power=power,
            counter=counter,
            currents=[0, 0, 0]
        )
        self.__store.set(inverter_state)
        # Rückgabe der Leistung des ersten WR ohne Vorzeichenumkehr
        return power1

    def __get_wr2(self) -> Tuple[float, float]:
        ip_address2 = self.component_config["configuration"]["ip_address2"]
        counter2 = 0
        if ip_address2 != "none":
            params = (('Scope', 'System'),)
            response = requests.get('http://'+ip_address2+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi',
                                    params=params, timeout=3)
            response.raise_for_status()
            try:
                power2 = float(response.json()["Body"]["Data"]["Site"]["P_PV"])
            except TypeError:
                # Ohne PV Produktion liefert der WR 'null', ersetze durch Zahl 0
                power2 = 0
            if not self.component_config["configuration"]["gen24"]:
                counter2 = float(response.json()["Body"]["Data"]["Site"]["E_Total"])
        else:
            power2 = 0
        return power2, counter2

    def __calculate_offset(self, counter: float, daily_yield: float) -> Tuple[float, float, float]:
        ramdisk = compatibility.is_ramdisk_in_use()
        if ramdisk:
            try:
                with open("/var/www/html/openWB/ramdisk/pvkwh_offset", "r") as f:
                    counter_offset = float(f.read())
            except FileNotFoundError as e:
                log.MainLogger().exception(str(e))
                counter_offset = 0
            try:
                with open("/var/www/html/openWB/ramdisk/pvkwh_start", "r") as f:
                    counter_start = float(f.read())
            except FileNotFoundError as e:
                log.MainLogger().exception(str(e))
                counter_start = counter - daily_yield
                with open("/var/www/html/openWB/ramdisk/pvkwh_start", "w") as f:
                    f.write(str(counter_start))
        else:
            topic = "openWB/system/device/" + str(self.__device_id)+"/component/" + \
                str(self.component_config["id"])+"/counter_offset"
            counter_offset = Offset().offset(topic)
            if counter_offset is None:
                counter_offset = 0
            topic = "openWB/system/device/" + str(self.__device_id)+"/component/" + \
                str(self.component_config["id"])+"/counter_start"
            counter_start = Offset().offset(topic)

        if counter_start is not None:
            counter_new = counter_start + daily_yield + counter_offset
            if counter_new > counter:
                if counter_new - counter >= 100:
                    # Korrigiere Abweichung
                    counter_diff = counter_new - counter - 99
                    counter_offset -= counter_diff
                    counter_new -= counter_diff
                counter = counter_new
            else:
                # Berechne Abweichung als Mittelwert von aktueller und bisheriger Abweichung
                counter_offset = round((counter_offset + counter - counter_start - daily_yield) / 2)
        else:
            counter_start = 0
        return counter, counter_start, counter_offset

    def __add_and_save_offset(
            self, daily_yield: float, counter: float, counter_start: float, counter_offset: float) -> float:
        ramdisk = compatibility.is_ramdisk_in_use()
        if daily_yield == 0 and counter > counter_start + counter_offset:
            if ramdisk:
                with open("/var/www/html/openWB/ramdisk/pvkwh_start", "w") as f:
                    f.write(str(counter))
                with open("/var/www/html/openWB/ramdisk/pvkwh", "r") as ff:
                    counter_old = float(ff.read())
            else:
                topic = "openWB/set/system/device/" + str(self.__device_id)+"/component/" + \
                    str(self.component_config["id"])+"/pvkwh_start"
                pub.pub_single(topic, counter)
                topic = "openWB/pv/" + str(self.component_config["id"])+"/counter"
                try:
                    counter_old = float(Offset().offset(topic))
                except ValueError:
                    counter_old = 0
            counter_offset = counter_old - counter
            counter += counter_offset
            if ramdisk:
                with open("/var/www/html/openWB/ramdisk/pvkwh_offset", "w") as f:
                    f.write(str(counter_offset))
            else:
                topic = "openWB/set/system/device/" + str(self.__device_id)+"/component/" + \
                    str(self.component_config["id"])+"/counter_offset"
                pub.pub_single(topic, counter_offset)
        else:
            if ramdisk:
                with open("/var/www/html/openWB/ramdisk/pvkwh_offset", "w") as f:
                    f.write(str(counter_offset))
            else:
                topic = "openWB/set/system/device/" + str(self.__device_id)+"/component/" + \
                    str(self.component_config["id"])+"/counter_offset"
                pub.pub_single(topic, counter_offset)
        return counter


class Offset():
    def offset(self, topic: str) -> Optional[float]:
        try:
            self.temp = None
            self.topic = topic
            client = mqtt.Client("openWB-fronius_offset-" + str(self.__getserial()))

            client.on_connect = self.__on_connect
            client.on_message = self.__on_message

            client.connect("localhost", 1883)
            client.loop_start()
            time.sleep(0.5)
            client.loop_stop()
        except Exception:
            log.MainLogger().exception("Fehler in der Restore-Klasse")
        finally:
            return self.temp

    def __on_connect(self, client, userdata, flags, rc):
        """ connect to broker and subscribe to set topics
        """
        try:
            client.subscribe(self.topic, 2)
        except Exception:
            log.MainLogger().exception("Fehler in der Restore-Klasse")

    def __on_message(self, client, userdata, msg):
        """ wartet auf eingehende Topics.
        """
        self.temp = float(msg.payload)

    def __getserial(self):
        """ Extract serial from cpuinfo file
        """
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line[0:6] == 'Serial':
                        return line[10:26]
                return "0000000000000000"
        except Exception:
            log.MainLogger().exception("Fehler in der Restore-Klasse")
