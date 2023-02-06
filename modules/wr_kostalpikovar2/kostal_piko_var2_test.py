from pathlib import Path

import pytest

from kostal_piko_var2 import parse_kostal_piko_var2_html
from test_utils.mock_ramdisk import MockRamdisk


@pytest.fixture
def mock_ramdisk(monkeypatch):
    return MockRamdisk(monkeypatch)


def test_parse_html(mock_ramdisk: MockRamdisk):
    # setup
    sample_html = (Path(__file__).parent / "kostal_piko_var2_test_sample.html").read_text()

    # execution
    actual = parse_kostal_piko_var2_html(sample_html)

    # evaluation
    assert actual.power == -50
    assert actual.exported == 73288000


def test_parse_html_off(mock_ramdisk: MockRamdisk):
    # setup
    sample_html = (Path(__file__).parent / "kostal_piko_var2_test_sample_off.html").read_text()

    # execution
    actual = parse_kostal_piko_var2_html(sample_html)

    # evaluation
    assert actual.power == 0
    assert actual.exported == 42906000
