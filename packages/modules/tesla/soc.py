#!/usr/bin/env python3
import json
import time
from pathlib import Path
from typing import List, Union

from modules.common import store
from modules.common.abstract_soc import AbstractSoc
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_state import CarState
from modules.common.fault_state import ComponentInfo, FaultState
from modules.tesla import tesla_lib


from helpermodules import log
from helpermodules.cli import run_using_positional_cli_args


def get_default_config():
    return {
        "name": "Tesla SoC-Modul",
        "type": "tesla",
        "id": 0,
        "username": "user",
        "token_file": str(Path(__file__).resolve().parents[0])+"tokens.ev"+str(id),
        "tesla_ev_num": 0
    }


class TeslaConfiguration:
    def __init__(self, id: int, username: str, token_file: str, tesla_ev_num: int):
        self.id = id
        self.username = username
        self.token_file = token_file
        self.tesla_ev_num = tesla_ev_num

    @staticmethod
    def from_dict(device_config: dict):
        keys = ["id", "username", "token_file", "tesla_ev_num"]
        try:
            values = [device_config[key] for key in keys]
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return TeslaConfiguration(*values)


class Soc(AbstractSoc):
    def __init__(self, device_config: Union[dict, TeslaConfiguration]):
        self.config = device_config \
            if isinstance(device_config, TeslaConfiguration) \
            else TeslaConfiguration.from_dict(device_config)
        self.value_store = store.get_car_value_store(self.config.id)
        self.component_info = ComponentInfo(self.config.id, "Tesla", "vehicle")

    def update(self, chargepoint_state=None) -> None:
        if chargepoint_state is None:
            # Wenn das Ev keinem LP zugeordnet ist, kann es auch nicht laden.
            charge_state = False
        else:
            charge_state = chargepoint_state["get"]["charge_state"]
        with SingleComponentUpdateContext(self.component_info):
            if Path(self.config.token_file).is_file():
                if charge_state is False:
                    self.__wake_up_car()
                soc = self.__get_soc()
                self.value_store.set(CarState(soc))
            else:
                raise FaultState.error("Keine Zugangsdaten eingetragen.")

    def __wake_up_car(self):
        log.MainLogger().debug("Tesla"+str(self.config.id)+": Waking up car.")
        counter = 0
        state = "offline"
        while counter <= 12:
            response = tesla_lib.lib(email=self.config.username, vehicle=self.config.tesla_ev_num,
                                     tokensfile=self.config.token_file, command="vehicles/#/wake_up")
            if response != "":
                response = json.loads(response)
                state = response["response"]["state"]
                if state == "online":
                    break
                counter = counter+1
                time.sleep(5)
                log.MainLogger().debug("Tesla "+str(self.config.id)+": Loop: "+str(counter)+", State: "+str(state))
            else:
                raise FaultState.error("EV"+str(self.config.id)+" konnte nicht gewecket werden.")
        log.MainLogger().info("Tesla "+str(self.config.id)+": Status nach Aufwecken: "+str(state))
        if state != "online":
            raise FaultState.error("EV"+str(self.config.id)+" konnte nicht geweckt werden.")

    def __get_soc(self):
        response = tesla_lib.lib(email=self.config.username, vehicle=self.config.tesla_ev_num,
                                 tokensfile=self.config.token_file, data="vehicles/#/vehicle_data")
        response = json.loads(response)
        log.MainLogger().debug("Tesla "+str(self.config.id)+": State: "+str(response))
        soc = response["response"]["charge_state"]["battery_level"]
        return float(soc)


def read_legacy(id: int,
                username: str,
                tokenfile: str,
                tesla_ev_num: int,
                charge_state: bool):

    log.MainLogger().debug('SoC-Module tesla num: ' + str(id))
    log.MainLogger().debug('SoC-Module tesla username: ' + str(username))
    log.MainLogger().debug('SoC-Module tesla tokenfile: ' + str(tokenfile))
    log.MainLogger().debug('SoC-Module tesla tesla_ev_num: ' + str(tesla_ev_num))
    log.MainLogger().debug('SoC-Module tesla charge_state: ' + str(charge_state))

    config = TeslaConfiguration(id, username, tokenfile, tesla_ev_num)
    soc = Soc(config)
    chargepoint_state = {"get": {"charge_state": charge_state}}
    soc.update(chargepoint_state)


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
