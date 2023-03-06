#!/usr/bin/env python3
import logging
from typing import Optional
from modules.common import req
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.common.simcount._simcounter import SimCounter
from modules.devices.shelly.config import ShellyInverterSetup

log = logging.getLogger(__name__)


class ShellyInverter:

    def __init__(self,
                 device_id: int,
                 component_config: ShellyInverterSetup,
                 address: str,
                 generation: Optional[int]) -> None:
        self.component_config = component_config
        self.sim_counter = SimCounter(device_id, self.component_config.id, prefix="pv")
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)
        self.address = address
        self.generation = generation

    def totalPowerFromShellyJson(self, answer) -> int:
        if 'meters' in answer:
            meters = answer['meters']  # shelly
        else:
            meters = answer['emeters']  # shellyEM & shelly3EM
        total = 0
        # shellyEM has one meter, shelly3EM has three meters:
        for meter in meters:
            total = total + meter['power']
        return int(total)

    def update(self) -> None:
        if self.generation == 1:
            url = "http://" + self.address + "/status"
        else:
            url = "http://" + self.address + "/rpc/Shelly.GetStatus"
        answer = req.get_http_session().get(url, timeout=3).json()
        # Versuche Werte aus der Antwort zu extrahieren.
        try:
            if self.generation == 1:
                pv = self.totalPowerFromShellyJson(answer) * -1
            else:
                pv = int(answer['switch:0']['apower']) * -1
        except Exception:
            pv = 0
        _, pv_exported = self.sim_counter.sim_count(pv)
        inverter_state = InverterState(
            power=pv,
            exported=pv_exported
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=ShellyInverterSetup)
