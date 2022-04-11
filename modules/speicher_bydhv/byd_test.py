from pathlib import Path

import byd


def test_byd_rundata():
    # execution
    state = byd.BydParser.parse((Path(__file__).parent / "byd_test_sample_rundata.html").read_text())

    # evaluation
    assert state.soc == 95.9
    assert state.power == -1355


def test_byd_home():
    # execution
    state = byd.BydParser.parse((Path(__file__).parent / "byd_test_sample_home.html").read_text())

    # evaluation
    assert state.soc == 34.5
    assert state.power == 4158
