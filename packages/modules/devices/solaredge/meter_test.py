from typing import NamedTuple
import pytest

from modules.devices.solaredge.meter import SolaredgeMeterRegisters


Params = NamedTuple("Params", [("meter_id", int),
                               ("synergy_units", int),
                               ("expected_power_register", int)])

cases = [Params(meter_id=1, synergy_units=1, expected_power_register=40206),
         Params(meter_id=2, synergy_units=1, expected_power_register=40380),
         Params(meter_id=3, synergy_units=1, expected_power_register=40554),
         Params(meter_id=1, synergy_units=2, expected_power_register=40256),
         Params(meter_id=1, synergy_units=3, expected_power_register=40276),
         Params(meter_id=2, synergy_units=2, expected_power_register=40430),
         ]


@pytest.mark.parametrize("params", cases, ids=str)
def test_meter(params: Params):
    # setup and execution
    registers = SolaredgeMeterRegisters(params.meter_id, params.synergy_units)

    # assert
    assert registers.powers == params.expected_power_register
