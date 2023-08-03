from modules.devices.kostal_steca.config import KostalStecaInverterSetup
from modules.devices.kostal_steca.inverter import KostalStecaInverter

SAMPLE_IP = "1.1.1.1"


def test_get_values(requests_mock):
    # setup
    inverter = KostalStecaInverter(KostalStecaInverterSetup(), SAMPLE_IP)

    with open("packages/modules/devices/kostal_steca/measurements.xml", "r") as f:
        measurements_sample = f.read()
    requests_mock.get("http://" + SAMPLE_IP + "/measurements.xml", text=measurements_sample)

    with open("packages/modules/devices/kostal_steca/yields.xml", "r") as f:
        yields_sample = f.read()
    requests_mock.get("http://" + SAMPLE_IP + "/yields.xml", text=yields_sample)

    # execution
    power, exported = inverter.get_values()

    # evaluation
    assert power == -132.8
    assert exported == 12306056
