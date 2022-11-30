from unittest.mock import Mock

import pytest

from modules.common.component_state import CounterState
from modules.common.component_state import InverterState
from modules.devices.discovergy import counter, inverter, utils
from modules.devices.discovergy.device import read_legacy

SAMPLE_COUNTER_STATE = CounterState(
    imported=1,
    exported=2,
    power=3,
    voltages=[4, 5, 6],
    currents=[7, 8, 9],
    powers=[10, 11, 12],
)
SAMPLE_INVERTER_STATE = InverterState(
    exported=2,
    power=3,
    currents=[-7, -8, -9],
)
SAMPLE_USER = "some username"
SAMPLE_PASSWORD = "some password"
SAMPLE_COUNTER_METER_ID = "some counter meter id"
SAMPLE_INVERTER_METER_ID = "some inverter meter id"


class TestDiscovergyDevice:
    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch):
        self.mock_counter_value_store = Mock()
        self.mock_inverter_value_store = Mock()
        self.mock_get_last_reading = Mock(return_value=SAMPLE_COUNTER_STATE)
        monkeypatch.setattr(counter, 'get_counter_value_store', Mock(return_value=self.mock_counter_value_store))
        monkeypatch.setattr(inverter, 'get_inverter_value_store', Mock(return_value=self.mock_inverter_value_store))
        monkeypatch.setattr(utils, 'get_last_reading', self.mock_get_last_reading)

    def test_read_legacy_reads_counter(self, monkeypatch):
        # execution
        read_legacy(SAMPLE_USER, SAMPLE_PASSWORD, SAMPLE_COUNTER_METER_ID, "")

        # evaluation
        self.assert_get_last_reading_called(SAMPLE_COUNTER_METER_ID)
        self.assert_counter_state_set()

    def test_read_legacy_reads_inverter(self):
        # execution
        read_legacy(SAMPLE_USER, SAMPLE_PASSWORD, "", SAMPLE_INVERTER_METER_ID)

        # evaluation
        self.assert_get_last_reading_called(SAMPLE_INVERTER_METER_ID)
        self.assert_inverter_state_set()

    def test_read_legacy_reads_counter_and_inverter(self):
        # execution
        read_legacy(SAMPLE_USER, SAMPLE_PASSWORD, SAMPLE_COUNTER_METER_ID, SAMPLE_INVERTER_METER_ID)

        # evaluation
        self.assert_get_last_reading_called(SAMPLE_COUNTER_METER_ID, SAMPLE_INVERTER_METER_ID)
        self.assert_inverter_state_set()
        self.assert_counter_state_set()

    def assert_get_last_reading_called(self, *meter_ids):
        assert self.mock_get_last_reading.call_count == len(meter_ids)
        # Check that one call was made for each meter_id, ignoring order:
        assert sorted(call_args[0][1] for call_args in self.mock_get_last_reading.call_args_list) == sorted(meter_ids)
        # Check that credentials were passed along each call:
        for call_args in self.mock_get_last_reading.call_args_list:
            assert call_args[0][0].auth == (SAMPLE_USER, SAMPLE_PASSWORD)

    def assert_counter_state_set(self):
        assert self.mock_counter_value_store.set.call_count == 1
        assert self.mock_counter_value_store.set.call_args[0][0] is SAMPLE_COUNTER_STATE

    def assert_inverter_state_set(self):
        assert self.mock_inverter_value_store.set.call_count == 1
        inverter_state = self.mock_inverter_value_store.set.call_args[0][0]  # type: InverterState
        assert inverter_state.power == SAMPLE_INVERTER_STATE.power
        assert inverter_state.currents == SAMPLE_INVERTER_STATE.currents
        assert inverter_state.exported == SAMPLE_INVERTER_STATE.exported
