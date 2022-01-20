import json
from unittest.mock import Mock

import pytest
import requests
import requests_mock

import powerwall
from modules.common.component_state import BatState
from test_utils.mock_ramdisk import MockRamdisk

sample_soe_json = """{"percentage":69.16}"""

sample_aggregates_json = """
{
   "site":{
      "last_communication_time":"2018-04-02T16:11:41.885377469-07:00",
      "instant_power":-21.449996948242188,
      "instant_reactive_power":-138.8300018310547,
      "instant_apparent_power":140.47729986545957,
      "frequency":60.060001373291016,
      "energy_exported":1136916.6875,
      "energy_imported":3276432.6625,
      "instant_average_voltage":239.81999969482422,
      "instant_total_current":0,
      "i_a_current":0,
      "i_b_current":0,
      "i_c_current":0
   },
   "battery":{
      "last_communication_time":"2018-04-02T16:11:41.89022247-07:00",
      "instant_power":-2350,
      "instant_reactive_power":0,
      "instant_apparent_power":2350,
      "frequency":60.033,
      "energy_exported":1169030,
      "energy_imported":1638140,
      "instant_average_voltage":239.10000000000002,
      "instant_total_current":45.8,
      "i_a_current":0,
      "i_b_current":0,
      "i_c_current":0
   },
   "load":{
      "last_communication_time":"2018-04-02T16:11:41.885377469-07:00",
      "instant_power":1546.2712597712405,
      "instant_reactive_power":-71.43153973801415,
      "instant_apparent_power":1547.920305979569,
      "frequency":60.060001373291016,
      "energy_exported":0,
      "energy_imported":7191016.994444443,
      "instant_average_voltage":239.81999969482422,
      "instant_total_current":6.44763264839839,
      "i_a_current":0,
      "i_b_current":0,
      "i_c_current":0
   },
   "solar":{
      "last_communication_time":"2018-04-02T16:11:41.885541803-07:00",
      "instant_power":3906.1700439453125,
      "instant_reactive_power":53.26999855041504,
      "instant_apparent_power":3906.533259164868,
      "frequency":60.060001373291016,
      "energy_exported":5534272.949724403,
      "energy_imported":13661.930279959455,
      "instant_average_voltage":239.8699951171875,
      "instant_total_current":0,
      "i_a_current":0,
      "i_b_current":0,
      "i_c_current":0
   },
   "busway":{
      "last_communication_time":"0001-01-01T00:00:00Z",
      "instant_power":0,
      "instant_reactive_power":0,
      "instant_apparent_power":0,
      "frequency":0,
      "energy_exported":0,
      "energy_imported":0,
      "instant_average_voltage":0,
      "instant_total_current":0,
      "i_a_current":0,
      "i_b_current":0,
      "i_c_current":0
   },
   "frequency":{
      "last_communication_time":"0001-01-01T00:00:00Z",
      "instant_power":0,
      "instant_reactive_power":0,
      "instant_apparent_power":0,
      "frequency":0,
      "energy_exported":0,
      "energy_imported":0,
      "instant_average_voltage":0,
      "instant_total_current":0,
      "i_a_current":0,
      "i_b_current":0,
      "i_c_current":0
   },
   "generator":{
      "last_communication_time":"0001-01-01T00:00:00Z",
      "instant_power":0,
      "instant_reactive_power":0,
      "instant_apparent_power":0,
      "frequency":0,
      "energy_exported":0,
      "energy_imported":0,
      "instant_average_voltage":0,
      "instant_total_current":0,
      "i_a_current":0,
      "i_b_current":0,
      "i_c_current":0
   }
}"""


def match_cookie_ok(request: requests.PreparedRequest):
    return "AuthCookie=auth-cookie" in request.headers['Cookie']


def match_cookie_reject(request: requests.PreparedRequest):
    return not match_cookie_ok(request)


@pytest.fixture
def mock_ramdisk(monkeypatch):
    return MockRamdisk(monkeypatch)


API_URL = "https://sample-address/api"
COOKIE_FILE_NAME = "powerwall_cookie.txt"


def assert_battery_state_correct(state: BatState):
    assert state.soc == 69.16
    assert state.power == 2350
    assert state.imported == 1638140
    assert state.exported == 1169030


def test_powerwall_update_if_cookie_cached(monkeypatch, requests_mock: requests_mock.Mocker, mock_ramdisk: MockRamdisk):
    # setup
    mock_bat_value_store = Mock()
    monkeypatch.setattr(powerwall, "get_bat_value_store", Mock(return_value=mock_bat_value_store))
    requests_mock.get("https://sample-address/api/meters/aggregates", text=sample_aggregates_json,
                      additional_matcher=match_cookie_ok)
    requests_mock.get("https://sample-address/api/system_status/soe", text=sample_soe_json,
                      additional_matcher=match_cookie_ok)
    mock_ramdisk[COOKIE_FILE_NAME] = """{"AuthCookie": "auth-cookie", "UserRecord": "user-record"}"""

    # execution
    powerwall.update("sample-address", "sample@mail.com", "some password")

    # evaluation
    assert_battery_state_correct(mock_bat_value_store.set.call_args[0][0])


@pytest.mark.parametrize(
    "cookie_file", [
        pytest.param("""{"AuthCookie": "reject-me", "UserRecord": "user-record"}""", id="expired cookie"),
        pytest.param("""{this is not valid json}""", id="garbage file"),
        pytest.param(None, id="no cookie file")
    ]
)
def test_powerwall_update_retrieves_new_cookie_if_cookie_rejected(monkeypatch,
                                                                  requests_mock: requests_mock.Mocker,
                                                                  mock_ramdisk: MockRamdisk,
                                                                  cookie_file: str):
    # setup
    mock_bat_value_store = Mock()
    monkeypatch.setattr(powerwall, "get_bat_value_store", Mock(return_value=mock_bat_value_store))
    requests_mock.post(API_URL + "/login/Basic", cookies={"AuthCookie": "auth-cookie", "UserRecord": "user-record"})
    requests_mock.get(API_URL + "/meters/aggregates", status_code=401, additional_matcher=match_cookie_reject)
    requests_mock.get(API_URL + "/system_status/soe", status_code=401, additional_matcher=match_cookie_reject)
    requests_mock.get(API_URL + "/meters/aggregates", text=sample_aggregates_json, additional_matcher=match_cookie_ok)
    requests_mock.get(API_URL + "/system_status/soe", text=sample_soe_json, additional_matcher=match_cookie_ok)
    if cookie_file is not None:
        mock_ramdisk[COOKIE_FILE_NAME] = cookie_file

    # execution
    powerwall.update("sample-address", "sample@mail.com", "some password")

    # evaluation
    assert json.loads(mock_ramdisk[COOKIE_FILE_NAME]) == {"AuthCookie": "auth-cookie", "UserRecord": "user-record"}
    assert_battery_state_correct(mock_bat_value_store.set.call_args[0][0])
