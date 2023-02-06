from unittest.mock import Mock

import pytest
import requests_mock

from dataclass_utils import dataclass_from_dict
from helpermodules import compatibility
from modules.common.store._api import LoggingValueStore
from modules.devices.fronius import counter_s0
from modules.devices.fronius.config import FroniusConfiguration, FroniusS0CounterSetup
from test_utils.mock_ramdisk import MockRamdisk

SAMPLE_IP = "1.1.1.1"


@pytest.fixture
def mock_ramdisk(monkeypatch):
    monkeypatch.setattr(compatibility, "is_ramdisk_in_use", lambda: True)
    return MockRamdisk(monkeypatch)


def test_update(monkeypatch, requests_mock: requests_mock.Mocker, mock_ramdisk, mock_simcount):
    component_config = FroniusS0CounterSetup()
    device_config = FroniusConfiguration()
    device_config.ip_address = SAMPLE_IP
    counter = counter_s0.FroniusS0Counter(
        0, component_config,  dataclass_from_dict(FroniusConfiguration, device_config))

    mock = Mock(return_value=None)
    monkeypatch.setattr(LoggingValueStore, "set", mock)
    mock_simcount.return_value = 0, 0
    requests_mock.get(
        "http://" + SAMPLE_IP + "/solar_api/v1/GetPowerFlowRealtimeData.fcgi",
        json=json)

    counter.update()

    # mock.assert_called_once()
    counter_state = mock.call_args[0][0]
    assert counter_state.exported == 0
    assert counter_state.imported == 0
    assert counter_state.currents == [0.0, 0.0, 0.0]
    assert counter_state.frequency == 50
    assert counter_state.power == 330.7664210983294
    assert counter_state.powers == [0, 0, 0]
    assert counter_state.power_factors == [0, 0, 0]
    assert counter_state.voltages == [230, 230, 230]


json = {
    "Body": {
        "Data": {
            "Inverters": {
                "1": {
                    "DT": 105,
                    "E_Day": 9668,
                    "E_Total": 45503300,
                    "E_Year": 7010823.5,
                    "P": 0
                },
                "2": {
                    "DT": 115,
                    "E_Day": 16189,
                    "E_Total": 16581639,
                    "E_Year": 11989318,
                    "P": 0
                }
            },
            "Site": {
                "E_Day": 25857,
                "E_Total": 62084939,
                "E_Year": 19000141.5,
                "Meter_Location": "load",
                "Mode": "vague-meter",
                "P_Akku": None,
                "P_Grid": 330.7664210983294,
                "P_Load": -330.7664210983294,
                "P_PV": None,
                "rel_Autonomy": 0,
                "rel_SelfConsumption": None
            },
            "Version": "12"
        }
    },
    "Head": {
        "RequestArguments": {},
        "Status": {
            "Code": 0,
            "Reason": "",
            "UserMessage": ""
        },
        "Timestamp": "2021-08-11T06:27:35+00:00"
    }
}
