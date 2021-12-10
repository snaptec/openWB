import pytest

import soc_manual
from test_utils.mock_ramdisk import MockRamdisk


@pytest.fixture(scope='function')
def mock_ramdisk(monkeypatch):
    return MockRamdisk(monkeypatch)


def test_charge_point_1(mock_ramdisk):
    # setup
    mock_ramdisk["manual_soc_lp1"] = "12.6"
    mock_ramdisk["manual_soc_meter_lp1"] = "42.123"
    mock_ramdisk["soc"] = "42"
    mock_ramdisk["llkwh"] = "52.123"

    # execution
    soc_manual.run(charge_point=1, battery_size=100, efficiency=.9)

    # evaluation
    assert mock_ramdisk["soc"] == "21"


def test_charge_point_2(mock_ramdisk):
    # setup
    mock_ramdisk["manual_soc_lp2"] = "12.6"
    mock_ramdisk["manual_soc_meter_lp2"] = "42.123"
    mock_ramdisk["soc1"] = "42"
    mock_ramdisk["llkwhs1"] = "52.123"

    # execution
    soc_manual.run(charge_point=2, battery_size=100, efficiency=.9)

    # evaluation
    assert mock_ramdisk["soc1"] == "21"


@pytest.mark.parametrize(
    "manual_files",
    [
        {"manual_soc_meter_lp2": "42.123"},
        {"manual_soc_lp2": "15"},
        {}
    ]
)
def test_reinitializes_if_state_is_missing(mock_ramdisk, manual_files: dict):
    # setup
    mock_ramdisk["soc1"] = "42"
    mock_ramdisk["llkwhs1"] = "52.123"
    mock_ramdisk.files.update(manual_files)

    # execution
    soc_manual.run(charge_point=2, battery_size=100, efficiency=.9)

    # evaluation
    assert mock_ramdisk["soc1"] == "42"  # Expect value to be unchanged
    assert mock_ramdisk["manual_soc_lp2"] == "42.0"
    assert mock_ramdisk["manual_soc_meter_lp2"] == "52.123"
