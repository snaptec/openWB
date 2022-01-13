#!/usr/bin/env python3

import logging
import requests

from helpermodules.cli import run_using_positional_cli_args
from helpermodules.log import setup_logging_stdout
from modules.common.component_state import BatState
from modules.common.store import get_bat_value_store
from modules.common.fault_state import FaultState

log = logging.getLogger("Sonnenbatterie")

def read_variant_0(address: str):
    response = requests.get('http://' + address + ':7979/rest/devices/battery', timeout=5)
    response.raise_for_status()
    return response.json()


def update_variant_0(address: str):
    # Auslesen einer Sonnenbatterie Eco 4 über die integrierte JSON-API des Batteriesystems
    battery_state = read_variant_0(address)
    battery_soc = int(battery_state["M05"])
    battery_export_power = int(battery_state["M34"])
    battery_import_power = int(battery_state["M35"])
    battery_power = battery_import_power - battery_export_power
    get_bat_value_store(1).set(BatState(
        power = battery_power,
        soc = battery_soc
    ))


def read_variant_1(address: str):
    response = requests.get("http://" + address + "/api/v1/status", timeout=5)
    response.raise_for_status()
    return response.json()


def update_variant_1(address: str):
    # Auslesen einer Sonnenbatterie Eco 8 über die integrierte JSON-API des Batteriesystems
    '''
    example data:
    {
        "Apparent_output": 225,
        "BackupBuffer": "0",
        "BatteryCharging": false,
        "BatteryDischarging": false,
        "Consumption_Avg": 2114,
        "Consumption_W": 2101,
        "Fac": 49.97200393676758,
        "FlowConsumptionBattery": false,
        "FlowConsumptionGrid": true,
        "FlowConsumptionProduction": false,
        "FlowGridBattery": false,
        "FlowProductionBattery": false,
        "FlowProductionGrid": false,
        "GridFeedIn_W": -2106,
        "IsSystemInstalled": 1,
        "OperatingMode": "2",
        "Pac_total_W": -5,
        "Production_W": 0,
        "RSOC": 6,
        "RemainingCapacity_Wh": 2377,
        "Sac1": 75,
        "Sac2": 75,
        "Sac3": 75,
        "SystemStatus": "OnGrid",
        "Timestamp": "2021-12-13 07:54:48",
        "USOC": 0,
        "Uac": 231,
        "Ubat": 48,
        "dischargeNotAllowed": true,
        "generator_autostart": false,
        "NVM_REINIT_STATUS": 0
    }
    '''
    battery_state = read_variant_1(address)

    battery_power = -battery_state["Pac_total_W"]
    log.debug('Speicher Leistung: ' + str(battery_power))
    battery_soc = battery_state["USOC"]
    log.debug('Speicher SoC: ' + str(battery_soc))
    # pv_power muss im Wechselrichter Modul gesetzt werden!
    pv_power = -battery_state["Production_W"]
    log.debug('Speicher PV Leistung (wird nicht verwendet, bitte als PV-Modul konfigurieren): ' + str(pv_power))
    get_bat_value_store(1).set(BatState(
        power = battery_power,
        soc = battery_soc
    ))


def read_variant_2_element(address: str, element: str):
    response = requests.get('http://' + address + ':7979/rest/devices/battery/' + element, timeout=5)
    response.raise_for_status()
    response.encoding = 'utf-8'
    return response.text.replace("\n", "")


def update_variant_2(address: str):
    # Auslesen einer Sonnenbatterie Eco 6 über die integrierte REST-API des Batteriesystems
    battery_soc = int(read_variant_2_element(address, "M05"))
    battery_export_power = int(read_variant_2_element(address, "M01"))
    battery_import_power = int(read_variant_2_element(address, "M02"))
    battery_power = battery_import_power - battery_export_power
    # pv_power muss im Wechselrichter Modul gesetzt werden!
    pv_power = -int(read_variant_2_element(address, "M03"))
    log.debug('Speicher PV Leistung (wird nicht verwendet, bitte als PV-Modul konfigurieren): ' + str(pv_power))
    get_bat_value_store(1).set(BatState(
        power = battery_power,
        soc = battery_soc
    ))


def update(address: str, variant: str):
    log.debug("Beginning update")
    if variant == "0":
        update_variant_0(address)
    elif variant == "1":
        update_variant_1(address)
    elif variant == "2":
        update_variant_2(address)
    else:
        raise FaultState.error("Unbekannte Variante: " + variant)
    log.debug("Update completed successfully")


if __name__ == '__main__':
    setup_logging_stdout()
    run_using_positional_cli_args(update)
