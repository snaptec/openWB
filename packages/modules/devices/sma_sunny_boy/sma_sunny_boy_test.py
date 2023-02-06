from unittest.mock import Mock
import pytest

from modules.common.component_state import BatState, InverterState
from modules.common.modbus import ModbusClient
from modules.devices.sma_sunny_boy import device
from modules.devices.sma_sunny_boy.bat import SunnyBoyBat
from modules.devices.sma_sunny_boy.inverter import SmaSunnyBoyInverter


@pytest.fixture(autouse=True)
def mock_modbus_client(monkeypatch):
    monkeypatch.setattr(ModbusClient, '__enter__',  Mock())
    monkeypatch.setattr(ModbusClient, '__exit__',  Mock())


class Params:
    def __init__(self, name: str,
                 expected_inverter_power: float,
                 ip2: str = "none",
                 ip3: str = "none",
                 ip4: str = "none",
                 hybrid: int = 0) -> None:
        self.name = name
        self.expected_inverter_power = expected_inverter_power
        self.ip2 = ip2
        self.ip3 = ip3
        self.ip4 = ip4
        self.hybrid = hybrid


SAMPLE_IP = "1.1.1.1"

cases = [
    Params("no hybrid, one inverter", -5786, "none", "none", "none", 0),
    Params("no hybrid, four inverter", -23144, SAMPLE_IP, SAMPLE_IP, SAMPLE_IP, 0),
    Params("hybrid, one inverter", -6009, "none", "none", "none", 1),
    Params("hybrid, four inverter", -23367, SAMPLE_IP, SAMPLE_IP, SAMPLE_IP, 1),
]


@pytest.mark.parametrize("params", cases, ids=[c.name for c in cases])
def test_sma_modbus_hybrid(monkeypatch, params: Params):
    # setup
    mock_inverter_value_store = Mock()
    monkeypatch.setattr(device, "get_inverter_value_store", Mock(return_value=mock_inverter_value_store))
    monkeypatch.setattr(SmaSunnyBoyInverter, "read", Mock(return_value=SAMPLE_INVERTER_STATE))
    monkeypatch.setattr(SunnyBoyBat, "read", Mock(return_value=SAMPLE_BAT_STATE))

    # execution
    device.read_legacy("inverter", SAMPLE_IP, 0, params.ip2, params.ip3,
                       params.ip4, 0, params.hybrid, 0, 0)
    # evaluation
    assert mock_inverter_value_store.set.call_args[0][0].power == params.expected_inverter_power


SAMPLE_BAT_STATE = BatState(
    exported=200,
    imported=100,
    power=223,
    soc=100,
)

SAMPLE_INVERTER_STATE = InverterState(
    power=-5786,
    exported=200,
    dc_power=-1
)
