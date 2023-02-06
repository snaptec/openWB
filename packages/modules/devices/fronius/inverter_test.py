from unittest.mock import Mock

import pytest
import requests_mock

from helpermodules import compatibility
from modules.common.store._api import LoggingValueStore
from modules.devices.fronius import inverter
from modules.devices.fronius.config import FroniusConfiguration, FroniusInverterSetup
from test_utils.mock_ramdisk import MockRamdisk

SAMPLE_IP = "1.1.1.1"


@pytest.fixture
def mock_ramdisk(monkeypatch):
    monkeypatch.setattr(compatibility, "is_ramdisk_in_use", lambda: True)
    return MockRamdisk(monkeypatch)


def test_update(monkeypatch, requests_mock: requests_mock.Mocker, mock_ramdisk, mock_simcount):
    wr = inverter.FroniusInverter(0, FroniusInverterSetup(), FroniusConfiguration(ip_address=SAMPLE_IP))

    mock = Mock(return_value=None)
    monkeypatch.setattr(LoggingValueStore, "set", mock)
    mock_simcount.return_value = 0, 0
    requests_mock.get(
        "http://" + SAMPLE_IP + "/solar_api/v1/GetPowerFlowRealtimeData.fcgi",
        json=json_wr1)

    wr.update()

    # mock.assert_called_once()
    inverter_state = mock.call_args[0][0]
    assert inverter_state.exported == 0
    assert inverter_state.currents == [0, 0, 0]
    assert inverter_state.power == -196.08712768554688


json_wr1 = {
    "Body": {
        "Data": {
            "Inverters": {
                "1": {
                    "Battery_Mode": "normal",
                    "DT": 1,
                    "E_Day": None,
                    "E_Total": 9824871.8336111102,
                    "E_Year": None,
                    "P": 1263.8095703125,
                    "SOC": 41.100000000000001
                }
            },
            "Site": {
                "BackupMode": "false",
                "BatteryStandby": "true",
                "E_Day": None,
                "E_Total": 9824871.8336111102,
                "E_Year": None,
                "Meter_Location": "grid",
                "Mode": "bidirectional",
                "P_Akku": 1126.365966796875,
                "P_Grid": -107.8,
                "P_Load": -1143.5296386718751,
                "P_PV": 196.08712768554688,
                "rel_Autonomy": 100.0,
                "rel_SelfConsumption": 91.385163695601761
            },
            "Smartloads": {
                "Ohmpilots": {}
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
        "Timestamp": "2022-01-04T09:45:59+00:00"
    }
}

json_wr2 = {
    "Body": {
        "Data": {
            "Inverters": {
                "1": {
                    "DT": 232,
                    "E_Day": 172.69999694824219,
                    "E_Total": 3372.76953125,
                    "E_Year": 10754989,
                    "P": 108
                }
            },
            "Site": {
                "E_Day": 172.69999694824219,
                "E_Total": 3372.7694444444446,
                "E_Year": 10754989,
                "Meter_Location": "unknown",
                "Mode": "produce-only",
                "P_Akku": None,
                "P_Grid": None,
                "P_Load": None,
                "P_PV": 108,
                "rel_Autonomy": None,
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
        "Timestamp": "2021-12-30T10:37:02+01:00"
    }
}
