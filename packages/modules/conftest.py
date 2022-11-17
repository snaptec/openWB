import sys
from unittest.mock import Mock

import pytest

from modules.common import simcount

sys.modules['pymodbus'] = type(sys)('pymodbus')
sys.modules['aiohttp'] = type(sys)('aiohttp')
sys.modules['lxml'] = type(sys)('lxml')
sys.modules['lxml.html'] = type(sys)('lxml.html')

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


@pytest.fixture(autouse=True)
def mock_simcount(monkeypatch) -> Mock:
    mock = Mock(return_value=(100, 200))
    monkeypatch.setattr(simcount.SimCounter, 'sim_count', mock)
    return mock
