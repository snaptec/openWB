from unittest.mock import Mock

import requests_mock


from modules.common.component_state import CounterState
from modules.devices.fems import counter, device
from modules.devices.fems.config import Fems, FemsConfiguration, FemsCounterSetup


def test_fems_bat(monkeypatch, requests_mock: requests_mock.mock):
    # setup
    mock_counter_value_store = Mock()
    monkeypatch.setattr(counter, 'get_counter_value_store', Mock(return_value=mock_counter_value_store))
    requests_mock.get('http://1.1.1.1:8084/rest/channel/meter0/(ActivePower.*|VoltageL.|Frequency)',
                      json=SAMPLE_RESPONSE)
    requests_mock.get('http://1.1.1.1:8084/rest/channel/_sum/Grid.+ActiveEnergy',
                      json=SAMPLE_RESPONSE_ENERGY)

    dev = device.create_device(Fems(configuration=FemsConfiguration(ip_address="1.1.1.1", password="abc")))
    dev.add_component(FemsCounterSetup())

    # execution
    dev.update()

    # evaluation
    assert mock_counter_value_store.set.call_count == 1
    assert vars(mock_counter_value_store.set.call_args[0][0]) == vars(SAMPLE_STATE)


# example FEMS response on rest/channel/meter0/(ActivePower.*|VoltageL.|Frequency)
SAMPLE_RESPONSE = [
    {
        "address": "meter0/ActivePowerL3",
        "type": "INTEGER",
        "accessMode": "RO",
        "text": "Negative values for Consumption; positive for Production",
        "unit": "W",
        "value": -547
    },
    {
        "address": "meter0/ActivePower",
        "type": "INTEGER",
        "accessMode": "RO",
        "text": "",
        "unit": "W",
        "value": -44
    },
    {
        "address": "meter0/ActivePowerL1",
        "type": "INTEGER",
        "accessMode": "RO",
        "text": "Negative values for Consumption; positive for Production",
        "unit": "W",
        "value": 0
    },
    {
        "address": "meter0/ActivePowerL2",
        "type": "INTEGER",
        "accessMode": "RO",
        "text": "Negative values for Consumption; positive for Production",
        "unit": "W",
        "value": 503
    },
    {
        "address": "meter0/VoltageL1",
        "type": "INTEGER",
        "accessMode": "RO",
        "text": "",
        "unit": "mV",
        "value": 229800
    },
    {
        "address": "meter0/VoltageL2",
        "type": "INTEGER",
        "accessMode": "RO",
        "text": "",
        "unit": "mV",
        "value": 230400
    },
    {
        "address": "meter0/VoltageL3",
        "type": "INTEGER",
        "accessMode": "RO",
        "text": "",
        "unit": "mV",
        "value": 232900
    },
    {
        "address": "meter0/Frequency",
        "type": "INTEGER",
        "accessMode": "RO",
        "text": "",
        "unit": "mHz",
        "value": 50000
    }
]

# example FEMS response on channel/_sum/Grid.+ActiveEnergy
SAMPLE_RESPONSE_ENERGY = [
    {
        "address": "_sum/GridSellActiveEnergy",
        "type": "LONG",
        "accessMode": "RO",
        "text": "",
        "unit": "Wh",
        "value": 179771
    },
    {
        "address": "_sum/GridBuyActiveEnergy",
        "type": "LONG",
        "accessMode": "RO",
        "text": "",
        "unit": "Wh",
        "value": 2183647
    }
]

SAMPLE_STATE = CounterState(
    currents=[0.0, 2.1831597222222223, -2.3486474881923574],
    exported=179771,
    frequency=50.0,
    imported=2183647,
    power=-44,
    power_factors=[0.0, 0.0, 0.0],
    powers=[0, 503, -547],
    voltages=[229.8, 230.4, 232.9]
)
