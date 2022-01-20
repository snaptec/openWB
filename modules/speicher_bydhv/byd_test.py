from pathlib import Path

import byd


def test_byd():
    # execution
    state = byd.BydParser.parse((Path(__file__).parent / "byd_test_sample.html").read_text())

    # evaluation
    assert state.soc == 95.9
    assert state.power == -1355
