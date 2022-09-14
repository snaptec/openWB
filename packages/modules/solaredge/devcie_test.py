from typing import Tuple
from unittest.mock import Mock

import pytest

from modules.solaredge import device
from modules.solaredge.config import (SolaredgeCounterConfiguration, SolaredgeCounterSetup,
                                      SolaredgeExternalInverterConfiguration, SolaredgeExternalInverterSetup)
from modules.solaredge.counter import SolaredgeCounter
from modules.solaredge.external_inverter import SolaredgeExternalInverter


class Params:
    def __init__(self,
                 name: str,
                 meter_id_counter: int,
                 meter_id_inverter: int,
                 synergy_units: int,
                 expected_counter_register: Tuple[int, int],
                 expected_inverter_register: Tuple[int, int]):
        self.name = name
        self.meter_id_counter = meter_id_counter
        self.meter_id_inverter = meter_id_inverter
        self.synergy_units = synergy_units
        self.expected_counter_register = expected_counter_register
        self.expected_inverter_register = expected_inverter_register


cases = [Params("counter id 1, inverter id 2, synergy units 1", 1, 2, 1, (1, 1), (2, 1)),
         Params("counter id 1, inverter id 3, synergy units 2", 1, 3, 2, (1, 2), (2, 2)),
         Params("counter id 2, inverter id 1, synergy units 3", 2, 1, 3, (2, 3), (1, 3)),
         Params("counter id 3, inverter id 1, synergy units 1", 3, 1, 1, (2, 1), (1, 1))
         ]


@pytest.mark.parametrize("params", cases, ids=[c.name for c in cases])
def test_set_component_registers(monkeypatch, params: Params):
    # setup
    client = Mock()
    monkeypatch.setattr(device, "SolaredgeMeterRegisters", Mock(side_effect=lambda *args: args))
    counter = SolaredgeCounter(2, SolaredgeCounterSetup(
        configuration=SolaredgeCounterConfiguration(meter_id=params.meter_id_counter)), client)
    external_inverter = SolaredgeExternalInverter(2, SolaredgeExternalInverterSetup(
        configuration=SolaredgeExternalInverterConfiguration(meter_id=params.meter_id_inverter)), client)
    components = {"component1": counter, "component2": external_inverter}

    # execution
    device.Device.set_component_registers(components, synergy_units=params.synergy_units)

    # evaluation
    assert external_inverter.registers == params.expected_inverter_register
    assert counter.registers == params.expected_counter_register
