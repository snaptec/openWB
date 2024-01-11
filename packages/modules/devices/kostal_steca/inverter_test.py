import pytest

from modules.devices.kostal_steca.config import KostalStecaInverterSetup
from modules.devices.kostal_steca.inverter import KostalStecaInverter

SAMPLE_IP = "1.1.1.1"


@pytest.mark.parametrize("measurements_file, expected_power",
                         [
                             pytest.param("measurements_production.xml", -132.8, id="WR produziert"),
                             pytest.param("measurements_no_production.xml", 0, id="WR produziert nicht"),
                         ])
def test_get_values(measurements_file, expected_power, requests_mock):
    # setup
    inverter = KostalStecaInverter(KostalStecaInverterSetup(), SAMPLE_IP)

    with open("packages/modules/devices/kostal_steca/"+measurements_file, "r") as f:
        measurements_sample = f.read()
    requests_mock.get("http://" + SAMPLE_IP + "/measurements.xml", text=measurements_sample)

    with open("packages/modules/devices/kostal_steca/yields.xml", "r") as f:
        yields_sample = f.read()
    requests_mock.get("http://" + SAMPLE_IP + "/yields.xml", text=yields_sample)

    # execution
    power, exported = inverter.get_values()

    # evaluation
    assert power == expected_power
    assert exported == 12306056
