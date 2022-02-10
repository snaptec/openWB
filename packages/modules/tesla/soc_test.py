from unittest.mock import Mock

import pytest

from helpermodules import compatibility
from modules.common import store
from modules.common.component_context import SingleComponentUpdateContext
from modules.tesla import api
from modules.tesla.soc import Soc, TeslaConfiguration


def create_tesla_configuration_dict() -> dict:
    return {"tesla_ev_num": 0, "id": 42}


class TestTeslaConfiguration:
    def test_from_dict_initializes_correctly(self):
        # execution
        actual = TeslaConfiguration.from_dict({"tesla_ev_num": 0, "id": 42})

        # evaluation
        assert actual.id == 42
        assert actual.tesla_ev_num == 0

    @pytest.mark.parametrize("property", ["id", "tesla_ev_num"])
    def test_from_dict_throws_if_missing_property(self, property: str):
        # setup
        dict = create_tesla_configuration_dict()
        del dict[property]

        # execution & evaluation
        with pytest.raises(Exception, match="^Illegal configuration"):
            TeslaConfiguration.from_dict(dict)


class TestTesla:
    @pytest.fixture(autouse=True)
    def set_up(self, monkeypatch):
        self.mock_context_exit = Mock(return_value=True)
        self.mock_get_token_file = Mock(
            name="get_token_file", return_value="/var/www/html/openWB/packages/modules/tesla/tokens.ev0")
        self.mock_is_ramdisk_in_use = Mock(name="is_ramdisk_in_use", return_value=False)
        self.mock_post_wake_up_command = Mock(name="post_wake_up_command", return_value="online")
        self.mock_request_soc = Mock(name="request_soc", return_value=42.5)
        self.mock_value_store = Mock(name="value_store")
        monkeypatch.setattr(Soc, "get_token_file", self.mock_get_token_file)
        monkeypatch.setattr(compatibility, "is_ramdisk_in_use", self.mock_is_ramdisk_in_use)
        monkeypatch.setattr(api, "post_wake_up_command", self.mock_post_wake_up_command)
        monkeypatch.setattr(api, "request_soc", self.mock_request_soc)
        monkeypatch.setattr(store, "get_car_value_store", Mock(return_value=self.mock_value_store))
        monkeypatch.setattr(SingleComponentUpdateContext, '__exit__', self.mock_context_exit)

    def test_update_updates_value_store_no_chargepoint(self, monkeypatch):
        # execution
        Soc(TeslaConfiguration(0, 0)).update(chargepoint_state=None)

        # evaluation
        self.assert_context_manager_called_with(None)
        self.mock_request_soc.assert_called_once_with(
            vehicle=0, token_file="/var/www/html/openWB/packages/modules/tesla/tokens.ev0")
        assert self.mock_value_store.set.call_count == 1
        assert self.mock_value_store.set.call_args[0][0].soc == 42.5

    def test_update_updates_value_store_not_charging(self, monkeypatch):
        # execution
        chargepoint_state = {"get": {"charge_state": False}}
        Soc(TeslaConfiguration(0, 0)).update(chargepoint_state=chargepoint_state)

        # evaluation
        self.assert_context_manager_called_with(None)
        self.mock_request_soc.assert_called_once_with(
            vehicle=0, token_file="/var/www/html/openWB/packages/modules/tesla/tokens.ev0")
        assert self.mock_value_store.set.call_count == 1
        assert self.mock_value_store.set.call_args[0][0].soc == 42.5

    def test_update_passes_errors_to_context(self, monkeypatch):
        # setup
        dummy_error = Exception()
        self.mock_request_soc.side_effect = dummy_error

        # execution
        Soc(TeslaConfiguration(0, 0)).update(chargepoint_state=None)

        # evaluation
        self.assert_context_manager_called_with(dummy_error)

    def assert_context_manager_called_with(self, error):
        assert self.mock_context_exit.call_count == 1
        assert self.mock_context_exit.call_args[0][1] is error
