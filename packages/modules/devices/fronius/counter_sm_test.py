from unittest.mock import Mock

import pytest
import requests_mock

from dataclass_utils import dataclass_from_dict
from helpermodules import compatibility
from modules.common.store._api import LoggingValueStore
from modules.devices.fronius import counter_sm
from modules.devices.fronius.config import FroniusConfiguration, FroniusSmCounterSetup
from test_utils.mock_ramdisk import MockRamdisk

SAMPLE_IP = "1.1.1.1"


@pytest.fixture
def mock_ramdisk(monkeypatch):
    monkeypatch.setattr(compatibility, "is_ramdisk_in_use", lambda: True)
    return MockRamdisk(monkeypatch)


def test_update_grid(monkeypatch, requests_mock: requests_mock.Mocker, mock_ramdisk, mock_simcount):
    component_config = FroniusSmCounterSetup()
    assert component_config.configuration.variant == 0
    device_config = FroniusConfiguration()
    device_config.ip_address = SAMPLE_IP
    assert component_config.configuration.meter_id == 0
    counter = counter_sm.FroniusSmCounter(0, component_config, dataclass_from_dict(FroniusConfiguration, device_config))

    mock = Mock(return_value=None)
    monkeypatch.setattr(LoggingValueStore, "set", mock)
    mock_simcount.return_value = 0, 0
    requests_mock.get(
        "http://" + SAMPLE_IP + "/solar_api/v1/GetMeterRealtimeData.cgi",
        json=json_grid)

    counter.update()

    # mock.assert_called_once()
    counter_state = mock.call_args[0][0]
    assert counter_state.exported == 0
    assert counter_state.imported == 0
    assert counter_state.currents == [0.4339647008179079, 1.3994802944997833, 0.5339012669287898]
    assert counter_state.frequency == 50
    assert counter_state.power == 546.16
    assert counter_state.powers == [100.81, 323.14, 122.21]
    assert counter_state.power_factors == [0.57, 0.74, 0.47]
    assert counter_state.voltages == [232.3, 230.9, 228.9]
    assert counter_state.power == sum(counter_state.powers)


def test_update_grid_var2(monkeypatch, requests_mock: requests_mock.Mocker, mock_ramdisk, mock_simcount):
    component_config = FroniusSmCounterSetup()
    component_config.configuration.variant = 2
    device_config = FroniusConfiguration()
    device_config.ip_address = SAMPLE_IP
    assert component_config.configuration.meter_id == 0
    counter = counter_sm.FroniusSmCounter(0, component_config, dataclass_from_dict(FroniusConfiguration, device_config))

    mock = Mock(return_value=None)
    monkeypatch.setattr(LoggingValueStore, "set", mock)
    mock_simcount.return_value = 0, 0
    requests_mock.get(
        "http://" + SAMPLE_IP + "/solar_api/v1/GetMeterRealtimeData.cgi",
        json=json_grid_var2)

    counter.update()

    # mock.assert_called_once()
    counter_state = mock.call_args[0][0]
    assert counter_state.exported == 0
    assert counter_state.imported == 0
    assert counter_state.currents == [-2.777267315214871, -6.06216401684521, -5.903017198144055]
    assert counter_state.frequency == 50
    assert counter_state.power == -4496.6
    assert counter_state.powers == [-645.1591973244145, -1403.390969899666, -1377.7642140468224]
    assert counter_state.power_factors == [-0.998, -0.998, -0.999]
    assert counter_state.voltages == [232.3, 231.5, 233.4]


def test_update_external_var2(monkeypatch, requests_mock: requests_mock.Mocker, mock_ramdisk, mock_simcount):
    component_config = FroniusSmCounterSetup()
    component_config.configuration.variant = 2
    device_config = FroniusConfiguration()
    device_config.ip_address = SAMPLE_IP
    component_config.configuration.meter_id = 1
    counter = counter_sm.FroniusSmCounter(0, component_config, dataclass_from_dict(FroniusConfiguration, device_config))

    mock = Mock(return_value=None)
    monkeypatch.setattr(LoggingValueStore, "set", mock)
    mock_simcount.return_value = 0, 0
    requests_mock.get(
        "http://" + SAMPLE_IP + "/solar_api/v1/GetMeterRealtimeData.cgi",
        json=json_ext_var2)

    counter.update()

    # mock.assert_called_once()
    counter_state = mock.call_args[0][0]
    assert counter_state.exported == 0
    assert counter_state.imported == 0
    assert counter_state.currents == [-5.373121093182142, -5.664436188811191, -5.585225225225224]
    assert counter_state.frequency == 49.9
    assert counter_state.power == 3809.4
    assert counter_state.powers == [-1232.0566666666653, -1296.0230000000006, -1281.2506666666663]
    assert counter_state.power_factors == [0.643, 0.68, 0.667]
    assert counter_state.voltages == [229.3, 228.8, 229.4]


def test_update_load(monkeypatch, requests_mock: requests_mock.Mocker, mock_ramdisk, mock_simcount):
    component_config = FroniusSmCounterSetup()
    assert component_config.configuration.variant == 0
    device_config = FroniusConfiguration()
    device_config.ip_address = SAMPLE_IP
    component_config.configuration.meter_id = 2
    counter = counter_sm.FroniusSmCounter(0, component_config, dataclass_from_dict(FroniusConfiguration, device_config))

    mock = Mock(return_value=None)
    monkeypatch.setattr(LoggingValueStore, "set", mock)
    mock_simcount.return_value = 0, 0
    requests_mock.get(
        "http://" + SAMPLE_IP + "/solar_api/v1/GetMeterRealtimeData.cgi",
        json=json_load_meter)

    requests_mock.get(
        "http://" + SAMPLE_IP + "/solar_api/v1/GetPowerFlowRealtimeData.fcgi",
        json=json_load_power)

    counter.update()

    # mock.assert_called_once()
    counter_state = mock.call_args[0][0]
    assert counter_state.exported == 0
    assert counter_state.imported == 0
    assert counter_state.currents == [-1.3272330233868694, -1.8569568294409058, -1.2909967389763222]
    assert counter_state.frequency == 50
    assert counter_state.power == -1059.03
    assert counter_state.powers == [-314.0233333333333, -437.31333333333333, -303.5133333333333]
    assert counter_state.power_factors == [0.79, 0.42, 0.84]
    assert counter_state.voltages == [236.6, 235.5, 235.1]
    assert abs(counter_state.power - sum(counter_state.powers)) < 5


json_grid = {
    "Body": {
        "Data": {
            "Current_AC_Phase_1": 0.81299999999999994,
            "Current_AC_Phase_2": 2.0649999999999999,
            "Current_AC_Phase_3": 1.3009999999999999,
            "Details": {
                "Manufacturer": "Fronius",
                "Model": "Smart Meter 63A",
                "Serial": "12345678"
            },
            "Enable": 1,
            "EnergyReactive_VArAC_Sum_Consumed": 1241750,
            "EnergyReactive_VArAC_Sum_Produced": 77981830,
            "EnergyReal_WAC_Minus_Absolute": 31189707,
            "EnergyReal_WAC_Plus_Absolute": 5084426,
            "EnergyReal_WAC_Sum_Consumed": 5084426,
            "EnergyReal_WAC_Sum_Produced": 31189707,
            "Frequency_Phase_Average": 50,
            "Meter_Location_Current": 0,
            "PowerApparent_S_Phase_1": 188.85990000000001,
            "PowerApparent_S_Phase_2": 476.80849999999998,
            "PowerApparent_S_Phase_3": 297.7989,
            "PowerApparent_S_Sum": 854,
            "PowerFactor_Phase_1": 0.56999999999999995,
            "PowerFactor_Phase_2": 0.73999999999999999,
            "PowerFactor_Phase_3": 0.46999999999999997,
            "PowerFactor_Sum": 0.63,
            "PowerReactive_Q_Phase_1": -142.34,
            "PowerReactive_Q_Phase_2": -286.5,
            "PowerReactive_Q_Phase_3": -228.88999999999999,
            "PowerReactive_Q_Sum": -657.73000000000002,
            "PowerReal_P_Phase_1": 100.81,
            "PowerReal_P_Phase_2": 323.13999999999999,
            "PowerReal_P_Phase_3": 122.20999999999999,
            "PowerReal_P_Sum": 546.15999999999997,
            "TimeStamp": 1641661311,
            "Visible": 1,
            "Voltage_AC_PhaseToPhase_12": 401.10000000000002,
            "Voltage_AC_PhaseToPhase_23": 398.19999999999999,
            "Voltage_AC_PhaseToPhase_31": 399.39999999999998,
            "Voltage_AC_Phase_1": 232.30000000000001,
            "Voltage_AC_Phase_2": 230.90000000000001,
            "Voltage_AC_Phase_3": 228.90000000000001
        }
    },
    "Head": {
        "RequestArguments": {
            "DeviceClass": "Meter",
            "DeviceId": "0",
            "Scope": "Device"
        },
        "Status": {
            "Code": 0,
            "Reason": "",
            "UserMessage": ""
        },
        "Timestamp": "2022-01-08T18:01:52+01:00"
    }
}

json_grid_var2 = {
    "Body": {
        "Data": {
            "0": {
                "ACBRIDGE_CURRENT_ACTIVE_MEAN_01_F32": -6.1150000000000002,
                "ACBRIDGE_CURRENT_ACTIVE_MEAN_02_F32": -6.7789999999999999,
                "ACBRIDGE_CURRENT_ACTIVE_MEAN_03_F32": -6.8259999999999996,
                "ACBRIDGE_CURRENT_AC_SUM_NOW_F64": -19.719999999999999,
                "ACBRIDGE_VOLTAGE_MEAN_12_F32": 403.60000000000002,
                "ACBRIDGE_VOLTAGE_MEAN_23_F32": 400.5,
                "ACBRIDGE_VOLTAGE_MEAN_31_F32": 403.30000000000001,
                "COMPONENTS_MODE_ENABLE_U16": 1.0,
                "COMPONENTS_MODE_VISIBLE_U16": 1.0,
                "COMPONENTS_TIME_STAMP_U64": 1628662724.0,
                "Details": {
                    "Manufacturer": "Fronius",
                    "Model": "Smart Meter TS 65A-3",
                    "Serial": "12345678"
                },
                "GRID_FREQUENCY_MEAN_F32": 50.0,
                "SMARTMETER_ENERGYACTIVE_ABSOLUT_MINUS_F64": 331624.0,
                "SMARTMETER_ENERGYACTIVE_ABSOLUT_PLUS_F64": 624751.0,
                "SMARTMETER_ENERGYACTIVE_CONSUMED_SUM_F64": 624751.0,
                "SMARTMETER_ENERGYACTIVE_PRODUCED_SUM_F64": 331624.0,
                "SMARTMETER_ENERGYREACTIVE_CONSUMED_SUM_F64": 19260.0,
                "SMARTMETER_ENERGYREACTIVE_PRODUCED_SUM_F64": 155945.0,
                "SMARTMETER_FACTOR_POWER_01_F64": -0.998,
                "SMARTMETER_FACTOR_POWER_02_F64": -0.998,
                "SMARTMETER_FACTOR_POWER_03_F64": -0.999,
                "SMARTMETER_FACTOR_POWER_SUM_F64": -0.998,
                "SMARTMETER_POWERACTIVE_01_F64": -1382.3,
                "SMARTMETER_POWERACTIVE_02_F64": -1541.4000000000001,
                "SMARTMETER_POWERACTIVE_03_F64": -1572.8,
                "SMARTMETER_POWERACTIVE_MEAN_01_F64": -645.15919732441455,
                "SMARTMETER_POWERACTIVE_MEAN_02_F64": -1403.3909698996661,
                "SMARTMETER_POWERACTIVE_MEAN_03_F64": -1377.7642140468224,
                "SMARTMETER_POWERACTIVE_MEAN_SUM_F64": -4496.6000000000004,
                "SMARTMETER_POWERAPPARENT_01_F64": 1385.2,
                "SMARTMETER_POWERAPPARENT_02_F64": 1544.2,
                "SMARTMETER_POWERAPPARENT_03_F64": 1575.0999999999999,
                "SMARTMETER_POWERAPPARENT_MEAN_01_F64": 803.26989966555163,
                "SMARTMETER_POWERAPPARENT_MEAN_02_F64": 1406.3418060200672,
                "SMARTMETER_POWERAPPARENT_MEAN_03_F64": 1378.3571906354512,
                "SMARTMETER_POWERAPPARENT_MEAN_SUM_F64": 4504.6000000000004,
                "SMARTMETER_POWERREACTIVE_01_F64": -90.200000000000003,
                "SMARTMETER_POWERREACTIVE_02_F64": -92.900000000000006,
                "SMARTMETER_POWERREACTIVE_03_F64": -84.200000000000003,
                "SMARTMETER_POWERREACTIVE_MEAN_SUM_F64": -267.39999999999998,
                "SMARTMETER_VALUE_LOCATION_U16": 0.0,
                "SMARTMETER_VOLTAGE_01_F64": 232.30000000000001,
                "SMARTMETER_VOLTAGE_02_F64": 231.5,
                "SMARTMETER_VOLTAGE_03_F64": 233.40000000000001,
                "SMARTMETER_VOLTAGE_MEAN_01_F64": 231.16622073578603,
                "SMARTMETER_VOLTAGE_MEAN_02_F64": 231.5230769230773,
                "SMARTMETER_VOLTAGE_MEAN_03_F64": 233.76622073578602
            }
        }
    },
    "Head": {
        "RequestArguments": {
            "DeviceClass": "Meter",
            "Scope": "System"
        },
        "Status": {
            "Code": 0,
            "Reason": "",
            "UserMessage": ""
        },
        "Timestamp": "2021-08-11T06:18:45+00:00"
    }
}

json_load_meter = {
    "Body": {
        "Data": {
            "Current_AC_Phase_1": 0.98699999999999999,
            "Current_AC_Phase_2": 0.17899999999999999,
            "Current_AC_Phase_3": 0.98399999999999999,
            "Details": {
                "Manufacturer": "Fronius",
                "Model": "Smart Meter 63A",
                "Serial": "12345678"
            },
            "Enable": 1,
            "EnergyReactive_VArAC_Sum_Consumed": 5330470,
            "EnergyReactive_VArAC_Sum_Produced": 65844530,
            "EnergyReal_WAC_Minus_Absolute": 14987911,
            "EnergyReal_WAC_Plus_Absolute": 0,
            "EnergyReal_WAC_Sum_Consumed": 14987911,
            "EnergyReal_WAC_Sum_Produced": 0,
            "Frequency_Phase_Average": 50,
            "Meter_Location_Current": 1,
            "PowerApparent_S_Phase_1": 233.52419999999998,
            "PowerApparent_S_Phase_2": 42.154499999999999,
            "PowerApparent_S_Phase_3": 231.33839999999998,
            "PowerApparent_S_Sum": 376,
            "PowerFactor_Phase_1": 0.79000000000000004,
            "PowerFactor_Phase_2": 0.41999999999999998,
            "PowerFactor_Phase_3": 0.83999999999999997,
            "PowerFactor_Sum": 0.79000000000000004,
            "PowerReactive_Q_Phase_1": -106.41,
            "PowerReactive_Q_Phase_2": -29.899999999999999,
            "PowerReactive_Q_Phase_3": -92.180000000000007,
            "PowerReactive_Q_Sum": -228.49000000000001,
            "PowerReal_P_Phase_1": -137.31,
            "PowerReal_P_Phase_2": -14.02,
            "PowerReal_P_Phase_3": -147.81999999999999,
            "PowerReal_P_Sum": -299.14999999999998,
            "TimeStamp": 1647704960,
            "Visible": 1,
            "Voltage_AC_PhaseToPhase_12": 408.89999999999998,
            "Voltage_AC_PhaseToPhase_23": 407.60000000000002,
            "Voltage_AC_PhaseToPhase_31": 408.5,
            "Voltage_AC_Phase_1": 236.59999999999999,
            "Voltage_AC_Phase_2": 235.5,
            "Voltage_AC_Phase_3": 235.09999999999999
        }
    },
    "Head": {
        "RequestArguments": {
            "DeviceClass": "Meter",
            "DeviceId": "2",
            "Scope": "Device"
        },
        "Status": {
            "Code": 0,
            "Reason": "",
            "UserMessage": ""
        },
        "Timestamp": "2022-03-19T16:49:20+01:00"
    }
}

json_load_power = {
    "Body": {
        "Data": {
            "Inverters": {
                "1": {
                    "DT": 123,
                    "E_Day": 37080,
                    "E_Total": 45367100,
                    "E_Year": 1195098.375,
                    "P": 1354
                }
            },
            "Site": {
                "E_Day": 37080,
                "E_Total": 45367100,
                "E_Year": 1195098.375,
                "Meter_Location": "load",
                "Mode": "meter",
                "P_Akku": None,
                "P_Grid": -1059.03,
                "P_Load": -294.97000000000003,
                "P_PV": 1354,
                "rel_Autonomy": 100,
                "rel_SelfConsumption": 21.785081240768097
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
        "Timestamp": "2022-03-19T16:53:38+01:00"
    }
}

json_ext_var2 = {
    "Body": {
        "Data": {
            "1": {
                "ACBRIDGE_CURRENT_ACTIVE_MEAN_01_F32": -8.4849999999999994,
                "ACBRIDGE_CURRENT_ACTIVE_MEAN_02_F32": -8.5009999999999994,
                "ACBRIDGE_CURRENT_ACTIVE_MEAN_03_F32": -8.5350000000000001,
                "ACBRIDGE_CURRENT_AC_SUM_NOW_F64": -25.520999999999997,
                "ACBRIDGE_VOLTAGE_MEAN_12_F32": 396.69999999999999,
                "ACBRIDGE_VOLTAGE_MEAN_23_F32": 396.80000000000001,
                "ACBRIDGE_VOLTAGE_MEAN_31_F32": 397.19999999999999,
                "COMPONENTS_MODE_ENABLE_U16": 1.0,
                "COMPONENTS_MODE_VISIBLE_U16": 1.0,
                "COMPONENTS_TIME_STAMP_U64": 1611650230.0,
                "Details": {
                    "Manufacturer": "Fronius",
                    "Model": "Smart Meter TS 65A-3",
                    "Serial": "1234567890"
                },
                "GRID_FREQUENCY_MEAN_F32": 49.899999999999999,
                "SMARTMETER_ENERGYACTIVE_ABSOLUT_MINUS_F64": 28233.0,
                "SMARTMETER_ENERGYACTIVE_ABSOLUT_PLUS_F64": 5094426.0,
                "SMARTMETER_ENERGYACTIVE_CONSUMED_SUM_F64": 28233.0,
                "SMARTMETER_ENERGYACTIVE_PRODUCED_SUM_F64": 5094426.0,
                "SMARTMETER_ENERGYREACTIVE_CONSUMED_SUM_F64": 5905771.0,
                "SMARTMETER_ENERGYREACTIVE_PRODUCED_SUM_F64": 31815.0,
                "SMARTMETER_FACTOR_POWER_01_F64": 0.64300000000000002,
                "SMARTMETER_FACTOR_POWER_02_F64": 0.68000000000000005,
                "SMARTMETER_FACTOR_POWER_03_F64": 0.66700000000000004,
                "SMARTMETER_FACTOR_POWER_SUM_F64": 0.66300000000000003,
                "SMARTMETER_POWERACTIVE_01_F64": 1229.7,
                "SMARTMETER_POWERACTIVE_02_F64": 1298.0999999999999,
                "SMARTMETER_POWERACTIVE_03_F64": 1281.5,
                "SMARTMETER_POWERACTIVE_MEAN_01_F64": -1232.0566666666653,
                "SMARTMETER_POWERACTIVE_MEAN_02_F64": -1296.0230000000006,
                "SMARTMETER_POWERACTIVE_MEAN_03_F64": -1281.2506666666663,
                "SMARTMETER_POWERACTIVE_MEAN_SUM_F64": 3809.4000000000001,
                "SMARTMETER_POWERAPPARENT_01_F64": 1911.8,
                "SMARTMETER_POWERAPPARENT_02_F64": 1910.0999999999999,
                "SMARTMETER_POWERAPPARENT_03_F64": 1922.3,
                "SMARTMETER_POWERAPPARENT_MEAN_01_F64": 1910.7656666666664,
                "SMARTMETER_POWERAPPARENT_MEAN_02_F64": 1904.090666666666,
                "SMARTMETER_POWERAPPARENT_MEAN_03_F64": 1923.9343333333331,
                "SMARTMETER_POWERAPPARENT_MEAN_SUM_F64": 5744.3000000000002,
                "SMARTMETER_POWERREACTIVE_01_F64": 1463.8,
                "SMARTMETER_POWERREACTIVE_02_F64": 1401.0999999999999,
                "SMARTMETER_POWERREACTIVE_03_F64": 1432.8,
                "SMARTMETER_POWERREACTIVE_MEAN_SUM_F64": 4297.8999999999996,
                "SMARTMETER_VALUE_LOCATION_U16": 3.0,
                "SMARTMETER_VOLTAGE_01_F64": 229.30000000000001,
                "SMARTMETER_VOLTAGE_02_F64": 228.80000000000001,
                "SMARTMETER_VOLTAGE_03_F64": 229.40000000000001,
                "SMARTMETER_VOLTAGE_MEAN_01_F64": 228.8716666666669,
                "SMARTMETER_VOLTAGE_MEAN_02_F64": 228.90133333333321,
                "SMARTMETER_VOLTAGE_MEAN_03_F64": 229.3593333333333
            }
        }
    },
    "Head": {
        "RequestArguments": {
            "DeviceClass": "Meter",
            "Scope": "System"
        },
        "Status": {
            "Code": 0,
            "Reason": "",
            "UserMessage": ""
        },
        "Timestamp": "2021-01-26T08:37:11+00:00"
    }
}
