from unittest.mock import Mock

import requests_mock


from modules.common.component_state import BatState, CounterState, InverterState
from modules.devices.batterx import bat, counter, inverter
from modules.devices.batterx.config import (BatterX, BatterXBatSetup, BatterXConfiguration, BatterXCounterSetup,
                                            BatterXInverterSetup)
from modules.devices.batterx.device import create_device


def test_batterx(monkeypatch, requests_mock: requests_mock.mock):
    # setup
    mock_bat_value_store = Mock()
    mock_counter_value_store = Mock()
    mock_inverter_value_store = Mock()
    monkeypatch.setattr(bat, 'get_bat_value_store', Mock(return_value=mock_bat_value_store))
    monkeypatch.setattr(counter, 'get_counter_value_store', Mock(return_value=mock_counter_value_store))
    monkeypatch.setattr(inverter, 'get_inverter_value_store', Mock(return_value=mock_inverter_value_store))
    requests_mock.get("http://1.1.1.1/api.php?get=currentstate", json=SAMPLE)

    dev = create_device(BatterX(configuration=BatterXConfiguration(ip_address="1.1.1.1")))
    dev.add_component(BatterXBatSetup(id=2))
    dev.add_component(BatterXCounterSetup(id=0))
    dev.add_component(BatterXInverterSetup(id=1))

    # execution
    dev.update()

    # evaluation
    assert mock_counter_value_store.set.call_count == 1
    assert vars(mock_bat_value_store.set.call_args[0][0]) == vars(SAMPLE_BAT_STATE)
    assert vars(mock_counter_value_store.set.call_args[0][0]) == vars(SAMPLE_COUNTER_STATE)
    assert vars(mock_inverter_value_store.set.call_args[0][0]) == vars(SAMPLE_INVERTER_STATE)


SAMPLE_BAT_STATE = BatState(
    exported=200,
    imported=100,
    power=223,
    soc=100,
)
SAMPLE_COUNTER_STATE = CounterState(
    currents=[-6.11, -7.38, -7.52],
    exported=200,
    frequency=49.92,
    imported=100,
    power=-5001,
    powers=[-1452.0, -1763.0, -1784.0],
    voltages=[237.56, 239.09, 237.25]
)
SAMPLE_INVERTER_STATE = InverterState(
    power=-5786,
    exported=200
)

SAMPLE = {'1042': {'1': 5320},
          '1058': {'1': 420},
          '1074': {'1': 100},
          '1121': {'1': 223},
          '1297': {'1': 23760},
          '1298': {'1': 23970},
          '1299': {'1': 23780},
          '1329': {'1': 0},
          '1330': {'1': 0},
          '1331': {'1': 0},
          '1361': {'1': 0},
          '1362': {'1': 0},
          '1363': {'1': 0},
          '1377': {'1': 0},
          '1378': {'1': 4998},
          '1553': {'1': 48940},
          '1554': {'1': 45450},
          '1569': {'1': 662},
          '1570': {'1': 573},
          '1617': {'1': 3210},
          '1618': {'1': 2576},
          '1634': {'0': 5786},
          '2321': {'1': 0, '2': 0, '3': 0, '4': 0},
          '2337': {'1': 0, '2': 10, '3': 11, '4': 0},
          '24582': {'1': 1728000},
          '2465': {'1': 1, '2': 11, '3': 10, '4': 1, '5': 0},
          '273': {'1': 23860},
          '274': {'1': 24040},
          '275': {'1': 23840},
          '2833': {'0': 23756},
          '2834': {'0': 23909},
          '2835': {'0': 23725},
          '2865': {'0': -611},
          '2866': {'0': -738},
          '2867': {'0': -752},
          '2897': {'0': -1452, '2': 410},
          '2898': {'0': -1763, '2': 85},
          '2899': {'0': -1784, '2': 105},
          '2913': {'0': -5001, '2': 600},
          '2914': {'0': 4992},
          '305': {'1': -780},
          '306': {'1': -769},
          '307': {'1': -792},
          '3090': {'1': 5310},
          '3106': {'1': 0},
          '3122': {'1': 100},
          '3169': {'1': 0},
          '3313': {'1': 1110},
          '3314': {'1': 11100},
          '337': {'1': -1863},
          '338': {'1': -1849},
          '339': {'1': -1890},
          '353': {'1': -5602},
          '354': {'1': 4999},
          '369': {'1': 33},
          '370': {'1': 52},
          '371': {'1': 0},
          'logtime': '2022-05-04 11:00:51'}
