from pathlib import Path

from modules.devices.byd import bat


def test_byd_rundata():
    # execution
    power, soc = bat.BydParser.parse((Path(__file__).parent / "byd_test_sample_rundata.html").read_text())

    # evaluation
    assert soc == 95.9
    assert power == -1355


def test_byd_home():
    # execution
    power, soc = bat.BydParser.parse((Path(__file__).parent / "byd_test_sample_home.html").read_text())

    # evaluation
    assert soc == 34.5
    assert power == 4158
