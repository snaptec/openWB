import sys
from unittest.mock import Mock

import pytest

from modules.common import simcount

sys.modules['jq'] = type(sys)('jq')
sys.modules['pymodbus'] = type(sys)('pymodbus')

module = type(sys)('pymodbus.client.sync')
module.ModbusSerialClient = Mock()
module.ModbusTcpClient = Mock()
sys.modules['pymodbus.client.sync'] = module

module = type(sys)('pymodbus.constants')
module.Endian = Mock()
sys.modules['pymodbus.constants'] = module

module = type(sys)('pymodbus.payload')
module.BinaryPayloadDecoder = Mock()
sys.modules['pymodbus.payload'] = module


class MockSimCount:
    def __init__(self):
        self.sim_count = Mock(return_value=(100, 200))


@pytest.fixture(autouse=True)
def mock_simcount(monkeypatch) -> MockSimCount:
    mock = MockSimCount()
    monkeypatch.setattr(simcount.SimCountFactory, 'get_sim_counter', Mock(return_value=lambda: mock))
    return mock
