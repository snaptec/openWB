import pytest

from modules.solaredge.meter import SolaredgeMeterRegisters


class Params:
    def __init__(self,
                 name: str,
                 meter_id: int,
                 synergy_units: int,
                 expected_power_register: int):
        self.name = name
        self.meter_id = meter_id
        self.synergy_units = synergy_units
        self.expected_power_register = expected_power_register


cases = [Params("meter id 1, synergy units 1", meter_id=1, synergy_units=1, expected_power_register=40206),
         Params("meter id 2, synergy units 1", meter_id=2, synergy_units=1, expected_power_register=40380),
         Params("meter id 3, synergy units 1", meter_id=3, synergy_units=1, expected_power_register=40554),
         Params("meter id 1, synergy units 2", meter_id=1, synergy_units=2, expected_power_register=40256),
         Params("meter id 1, synergy units 3", meter_id=1, synergy_units=3, expected_power_register=40276),
         Params("meter id 2, synergy units 2", meter_id=2, synergy_units=2, expected_power_register=40430),
         ]


@pytest.mark.parametrize("params", cases, ids=[c.name for c in cases])
def test_meter(params: Params):
    # setup and execution
    registers = SolaredgeMeterRegisters(params.meter_id, params.synergy_units)

    # assert
    assert registers.powers == params.expected_power_register
