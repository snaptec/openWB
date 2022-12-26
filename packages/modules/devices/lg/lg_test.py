import pytest
from requests import HTTPError
from unittest.mock import Mock

from modules.common.component_state import BatState, CounterState, InverterState
from modules.devices.lg import bat, counter, device, inverter
from modules.devices.lg.config import LG, LgConfiguration
from test_utils.mock_ramdisk import MockRamdisk


@pytest.fixture
def mock_ramdisk(monkeypatch):
    return MockRamdisk(monkeypatch)


@pytest.fixture
def dev() -> device.Device:
    dev = device.Device(LG(configuration=LgConfiguration(ip_address=API_URL, password="some password")))
    dev.session_key = "67567d76-0c83-11ea-8a59-d84fb802005a"
    return dev


def assert_battery_state_correct(state: BatState):
    assert state.soc == 14.58333
    assert state.power == -372
    assert state.imported == 100
    assert state.exported == 200


def assert_counter_state_correct(state: CounterState):
    assert state.power == 11
    assert state.imported == 100
    assert state.exported == 200


def assert_inverter_state_correct(state: InverterState):
    assert state.power == 0
    assert state.exported == 200


def test_valid_login(monkeypatch, dev: device.Device):
    # setup
    mock_bat_value_store = Mock()
    monkeypatch.setattr(bat, "get_bat_value_store", Mock(return_value=mock_bat_value_store))
    mock_counter_value_store = Mock()
    monkeypatch.setattr(counter, "get_counter_value_store", Mock(return_value=mock_counter_value_store))
    mock_inverter_value_store = Mock()
    monkeypatch.setattr(inverter, "get_inverter_value_store", Mock(return_value=mock_inverter_value_store))
    monkeypatch.setattr(device.Device, "_request_data", Mock(return_value=sample_auth_key_valid))
    component_config = bat.component_descriptor.configuration_factory()
    component_config.id = None
    dev.add_component(component_config)
    component_config = counter.component_descriptor.configuration_factory()
    component_config.id = 1
    dev.add_component(component_config)
    component_config = inverter.component_descriptor.configuration_factory()
    component_config.id = 2
    dev.add_component(component_config)

    # execution
    dev.update()

    # evaluation
    assert_battery_state_correct(mock_bat_value_store.set.call_args[0][0])
    assert_counter_state_correct(mock_counter_value_store.set.call_args[0][0])
    assert_inverter_state_correct(mock_inverter_value_store.set.call_args[0][0])


def test_update_session_key(monkeypatch, dev: device.Device):
    # setup
    mock_bat_value_store = Mock()
    monkeypatch.setattr(bat, "get_bat_value_store", Mock(return_value=mock_bat_value_store))
    mock_counter_value_store = Mock()
    monkeypatch.setattr(counter, "get_counter_value_store", Mock(return_value=mock_counter_value_store))
    mock_inverter_value_store = Mock()
    monkeypatch.setattr(inverter, "get_inverter_value_store", Mock(return_value=mock_inverter_value_store))
    monkeypatch.setattr(device.Device, "_update_session_key", Mock())
    monkeypatch.setattr(device.Device, "_request_data", Mock(
        side_effect=[HTTPError, sample_auth_key_valid]))
    component_config = bat.component_descriptor.configuration_factory()
    component_config.id = None
    dev.add_component(component_config)
    component_config = counter.component_descriptor.configuration_factory()
    component_config.id = 1
    dev.add_component(component_config)
    component_config = inverter.component_descriptor.configuration_factory()
    component_config.id = 2
    dev.add_component(component_config)

    # execution
    dev.update()

    # evaluation
    assert_battery_state_correct(mock_bat_value_store.set.call_args[0][0])
    assert_counter_state_correct(mock_counter_value_store.set.call_args[0][0])
    assert_inverter_state_correct(mock_inverter_value_store.set.call_args[0][0])


API_URL = "https://sample-address"

sample_session_key = {
    "status": "success",
    "auth_key": "67567d76-0c83-11ea-8a59-d84fb802005a",
    "regnum": "XXXXXXXXXXXX",
    "role": "installer"
}

sample_auth_key_invalid = {
    "auth": "auth_key failed"
}

sample_auth_key_valid = {
    "statistics":
    {
        "pcs_pv_total_power": "0",
        "batconv_power": "372",
        "bat_use": "1",
        "bat_status": "2",
        "bat_user_soc": "14.58333",
        "load_power": "361",
        "load_today": "0.0",
        "grid_power": "11",
        "current_day_self_consumption": "94.8",
        "current_pv_generation_sum": "7415",
        "current_grid_feed_in_energy": "385"
    },
    "direction":
    {
        "is_direct_consuming_": "0",
        "is_battery_charging_": "0",
        "is_battery_discharging_": "1",
        "is_grid_selling_": "0",
        "is_grid_buying_": "0",
        "is_charging_from_grid_": "0"
    },
    "operation":
    {
        "status": "start",
        "mode": "1"
    },
    "wintermode":
    {
        "winter_status": "on"
    },
    "pcs_fault":
    {
        "pcs_status": "pcs_ok"
    }
}
