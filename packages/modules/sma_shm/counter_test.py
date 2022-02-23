import base64

import pytest

from helpermodules import compatibility
from modules.sma_shm import counter, speedwiredecoder
from test_utils.mock_ramdisk import MockRamdisk

# This sample was collected from an SMA Energy Meter with Firmware 2.0.18.R on 2021-12-22:
SAMPLE_SMA_ENERGY_EM = """
U01BAAAEAqAAAAABAkQAEGBpAV1xVXzY4imVNQABBAAAAAAAAAEIAAAAAAZJYH0AAAIEAAAB03YAA
ggAAAAASKlcgTAAAwQAAAAOpgADCAAAAAABs7fAAAAEBAAAAAAAAAQIAAAAAAHA7tMwAAkEAAAAAA
AACQgAAAAABtNNHmAACgQAAAHTsgAKCAAAAABIyAd/4AANBAAAAAPoABUEAAAAAAAAFQgAAAAAAcc
tgCAAFgQAAACfQgAWCAAAAAAYndxeAAAXBAAAAAaQABcIAAAAAAB1R9JwABgEAAAAAAAAGAgAAAAA
AMHoL4AAHQQAAAAAAAAdCAAAAAACC2mY8AAeBAAAAJ9gAB4IAAAAABinDvUAAB8EAAAAQwgAIAQAA
AOjZgAhBAAAAAPnACkEAAAAAAAAKQgAAAAAAiAQN/AAKgQAAACfQgAqCAAAAAAYhLpHcAArBAAAAA
cIACsIAAAAAAFF1ESgACwEAAAAAAAALAgAAAAAADY1tcAAMQQAAAAAAAAxCAAAAAACUKu34AAyBAA
AAJ9+ADIIAAAAABibCGxQADMEAAAAQswANAQAAAOmwgA1BAAAAAPnAD0EAAAAAAAAPQgAAAAAAqNm
AhAAPgQAAACU8gA+CAAAAAAXyAkY4AA/BAAAAAEOAD8IAAAAAAB26GxwAEAEAAAAAAAAQAgAAAAAA
Ucd26AARQQAAAAAAABFCAAAAAADCmzGsABGBAAAAJTyAEYIAAAAABfUThagAEcEAAAAPpQASAQAAA
OkkgBJBAAAAAPokAAAAAIAElIAAAAA
"""


@pytest.fixture
def mock_ramdisk(monkeypatch):
    monkeypatch.setattr(compatibility, "is_ramdisk_in_use", lambda: True)
    return MockRamdisk(monkeypatch)


def test_process_datagram_energy_meter(mock_ramdisk):
    # setup
    data = base64.b64decode(SAMPLE_SMA_ENERGY_EM)
    sma_data = speedwiredecoder.decode_speedwire(data)
    sma_counter = counter.create_component(counter.get_default_config())

    # execution
    sma_counter.read_datagram(sma_data)

    # evaluation
    assert mock_ramdisk.files["wattbezug"] == "-11967"
    assert mock_ramdisk.files["einspeisungkwh"] == "86688627.0"
    assert mock_ramdisk.files["bezugkwh"] == "7500240.0"
    assert mock_ramdisk.files["bezugw1"] == "-4077"
    assert mock_ramdisk.files["bezugw2"] == "-4077"
    assert mock_ramdisk.files["bezugw3"] == "-3813"
    assert mock_ramdisk.files["bezuga1"] == "-17.16"
    assert mock_ramdisk.files["bezuga2"] == "-17.1"
    assert mock_ramdisk.files["bezuga3"] == "-16.02"
    assert mock_ramdisk.files["evuv1"] == "238.438"
    assert mock_ramdisk.files["evuv2"] == "239.298"
    assert mock_ramdisk.files["evuv3"] == "238.738"
    assert mock_ramdisk.files["evupf1"] == "0.999"
    assert mock_ramdisk.files["evupf2"] == "0.999"
    assert mock_ramdisk.files["evupf3"] == "1.0"
