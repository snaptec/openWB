from unittest.mock import Mock

import pytest

from modules.common import store
from modules.common.component_context import SingleComponentUpdateContext
from modules.vehicles.evnotify import api
from modules.vehicles.evnotify.soc import EVNotify, EVNotifyConfiguration, Soc


class TestEVNotify:
    @pytest.fixture(autouse=True)
    def set_up(self, monkeypatch):
        self.mock_context_exit = Mock(return_value=True)
        self.mock_fetch_soc = Mock(name="fetch_soc", return_value=42.5)
        self.mock_value_store = Mock(name="value_store")
        monkeypatch.setattr(api, "fetch_soc", self.mock_fetch_soc)
        monkeypatch.setattr(store, "get_car_value_store", Mock(return_value=self.mock_value_store))
        monkeypatch.setattr(SingleComponentUpdateContext, '__exit__', self.mock_context_exit)

    def test_update_updates_value_store(self, monkeypatch):
        # execution
        Soc(EVNotify(configuration=EVNotifyConfiguration(1, "someKey", "someToken")), 0).update()

        # evaluation
        self.assert_context_manager_called_with(None)
        self.mock_fetch_soc.assert_called_once_with("someKey", "someToken")
        assert self.mock_value_store.set.call_count == 1
        assert self.mock_value_store.set.call_args[0][0].soc == 42.5

    def test_update_passes_errors_to_context(self, monkeypatch):
        # setup
        dummy_error = Exception()
        self.mock_fetch_soc.side_effect = dummy_error

        # execution
        Soc(EVNotify(configuration=EVNotifyConfiguration(1, "someKey", "someToken")), 0).update()

        # evaluation
        self.assert_context_manager_called_with(dummy_error)

    def assert_context_manager_called_with(self, error):
        assert self.mock_context_exit.call_count == 1
        assert self.mock_context_exit.call_args[0][1] is error
