import json
from unittest.mock import Mock

import pytest

import discovergy
from test_utils.mock_ramdisk import MockRamdisk

SAMPLE_JSON = """{
    "time":1622132613773,
    "values":{
        "energyOut":25545649812000,
        "energy2":12593551340000,
        "energy1":2210138000,
        "voltage1":233400,
        "voltage2":234600,
        "voltage3":200000,
        "energyOut1":0,
        "energyOut2":0,
        "power":1234567,
        "power1":1167000,
        "power2":2650980,
        "power3":-230000,
        "energy":12595761479000
    }
}"""


@pytest.fixture(scope='function')
def mock_ramdisk(monkeypatch):
    return MockRamdisk(monkeypatch)


def test_update(mock_ramdisk: MockRamdisk, monkeypatch):
    # setup
    mock_get_last_reading = Mock(return_value=json.loads(SAMPLE_JSON))
    monkeypatch.setattr(discovergy, 'get_last_reading', mock_get_last_reading)

    # exeuction
    discovergy.update("someUser", "somePassword", "someMeterId")

    # evaluation
    mock_get_last_reading.assert_called_once_with("someUser", "somePassword", "someMeterId")
    assert mock_ramdisk["bezuga1"] == "5.0"
    assert mock_ramdisk["bezuga2"] == "11.3"
    assert mock_ramdisk["bezuga3"] == "-1.15"
    assert mock_ramdisk["bezugkwh"] == "1259576.1479"
    assert mock_ramdisk["bezugw1"] == "1167"
    assert mock_ramdisk["bezugw2"] == "2650"
    assert mock_ramdisk["bezugw3"] == "-230"
    assert mock_ramdisk["einspeisungkwh"] == "2554564.9812"
    assert mock_ramdisk["evuv1"] == "233.4"
    assert mock_ramdisk["evuv2"] == "234.6"
    assert mock_ramdisk["evuv3"] == "200.0"
    assert mock_ramdisk["wattbezug"] == "1234"

