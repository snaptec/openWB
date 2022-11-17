from functools import partial

import pytest
import requests

from modules.devices.discovergy.api import get_last_reading

SAMPLE_JSON_1 = """{
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

# Es gibt verschiedene Antworten vom Discovergy-Modul.
SAMPLE_JSON_2 = """{
    "time": 1641374253118,
    "values": {
        "phase2Power": 241970,
        "energyOut": 7690248872000,
        "energy2": 28550717775000,
        "energy1": 2258421000,
        "phase1Power": 81310,
        "power": 485890,
        "phase3Power": 162600,
        "phase1Voltage": 225500,
        "energy": 28552976196000,
        "phase2Voltage": 226400,
        "phase3Voltage": 226800
    }
}"""

SAMPLE_JSON_3 = """{
    "time": 1641807548104,
    "values": {
        "power": 460000,
        "power3": -230000,
        "energyOut": 294243456924000,
        "power1": -345000,
        "energy": 43083460817000,
        "power2": 575000
    }
}"""

SAMPLE_JSON_4 = """{
    "time":1642590304850,
    "values":{
        "energyOut":75910110000000,
        "energy2":0,
        "energy1":73284260000000,
        "energyOut1":75910110000000,
        "power":6131200,
        "energyOut2":0,
        "energy":73284260000000
    }
}"""


@pytest.fixture
def mock_discovery_response(requests_mock):
    def do_mock(json_str: str):
        requests_mock.get("https://api.discovergy.com/public/v1/last_reading?meterId=someMeterId", text=json_str)

    return do_mock


def test_sample_json_1(mock_discovery_response):
    # setup
    mock_discovery_response(SAMPLE_JSON_1)

    # execution
    actual = get_last_reading(requests.Session(), "someMeterId")

    # evaluation
    assert actual.currents == [5.0, 11.3, -1.15]
    assert actual.imported == 1259576.1479
    assert actual.powers == [1167.0, 2650.98, -230.0]
    assert actual.exported == 2554564.9812
    assert actual.voltages == [233.4, 234.6, 200.0]
    assert actual.power == 1234.567


def test_sample_json_2(mock_discovery_response):
    # setup
    mock_discovery_response(SAMPLE_JSON_2)

    # execution
    actual = get_last_reading(requests.Session(), "someMeterId")

    # evaluation
    assert actual.imported == 2855297.6196
    assert actual.powers == [81.31, 241.97, 162.6]
    assert actual.exported == 769024.8872
    assert actual.voltages == [225.5, 226.4, 226.8]
    assert actual.power == 485.89
    assert list(map(partial(round, ndigits=2), actual.currents)) == [0.36, 1.07, 0.72]


def test_sample_json_3(mock_discovery_response):
    # setup
    mock_discovery_response(SAMPLE_JSON_3)

    # execution
    actual = get_last_reading(requests.Session(), "someMeterId")

    # evaluation
    assert actual.imported == 4308346.0817
    assert actual.powers == [-345, 575, -230]
    assert actual.exported == 29424345.6924
    assert actual.power == 460
    assert actual.currents == [-1.5, 2.5, -1.0]


def test_sample_json_4(mock_discovery_response):
    # setup
    mock_discovery_response(SAMPLE_JSON_4)

    # execution
    actual = get_last_reading(requests.Session(), "someMeterId")

    # evaluation
    assert actual.imported == 7328426.0000
    assert actual.exported == 7591011.0000
    assert actual.power == 6131.2
