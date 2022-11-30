from typing import List, NamedTuple, Type
from unittest.mock import Mock

import pytest

from modules.devices.solaredge import device
from modules.devices.solaredge.bat import SolaredgeBat
from modules.devices.solaredge.counter import SolaredgeCounter
from modules.devices.solaredge.external_inverter import SolaredgeExternalInverter
from modules.devices.solaredge.inverter import SolaredgeInverter


Params = NamedTuple("Params", [("configured_meter_ids", List[int]), ("effective_meter_ids", List[int])])


@pytest.mark.parametrize(["params"], [
    pytest.param(
        Params(configured_meter_ids=[1, 2], effective_meter_ids=[1, 2]),
        id="ids unchanged if meter_ids are continuous starting from 1"
    ),
    pytest.param(
        Params(configured_meter_ids=[2, 3], effective_meter_ids=[1, 2]),
        id="ids move forward if not starting at 1"
    ),
    pytest.param(
        Params(configured_meter_ids=[1, 3], effective_meter_ids=[1, 2]),
        id="gaps in ids are closed"
    )
])
def test_set_component_registers_assigns_effective_meter_ids(monkeypatch, params: Params):
    # setup
    monkeypatch.setattr(
        device, "SolaredgeMeterRegisters", Mock(side_effect=lambda internal_meter_id, _: internal_meter_id)
    )
    components_list = [
        Mock(spec=SolaredgeCounter, component_config=Mock(configuration=Mock(meter_id=meter_id)))
        for meter_id in params.configured_meter_ids
    ]

    # execution
    device.Device.set_component_registers(components_list, synergy_units=1)

    # evaluation
    assert [component.registers for component in components_list] == params.effective_meter_ids


@pytest.mark.parametrize("type,should_use", [
    (SolaredgeCounter, True),
    (SolaredgeExternalInverter, True),
    (SolaredgeBat, False),
    (SolaredgeInverter, False),
])
def test_set_component_registers_ignores_wrong_types(monkeypatch, type: Type, should_use: bool):
    # setup
    monkeypatch.setattr(
        device, "SolaredgeMeterRegisters", Mock(side_effect=lambda *args: True)
    )
    components = [Mock(spec=type, component_config=Mock(configuration=Mock(meter_id=1)))
                  ]
    # execution
    device.Device.set_component_registers(components, synergy_units=1)

    # evaluation
    assert hasattr(components[0], "registers") == should_use
