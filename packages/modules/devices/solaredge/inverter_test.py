from unittest.mock import Mock

from modules.common.component_state import InverterState
from modules.common.modbus import ModbusTcpClient_

from modules.devices.solaredge.config import SolaredgeInverterSetup
from modules.devices.solaredge.inverter import SolaredgeInverter


def test_read_state():
    # setup
    mock_read_holding_registers = Mock(side_effect=[
        [14152, -1],
        [8980404, 0],
        [616, 65535, 65535, -2],
        [14368, -1]
    ])
    inverter = SolaredgeInverter(0, SolaredgeInverterSetup(), Mock(
        spec=ModbusTcpClient_, read_holding_registers=mock_read_holding_registers))

    # execution
    inverter_state = inverter.read_state()

    # evaluation
    assert vars(inverter_state) == vars(InverterState(
        power=-1415.2,
        exported=8980404,
        currents=[6.16, 0, 0],
        dc_power=-1436.8000000000002
    )
    )
