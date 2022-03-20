import pytest

from modules.fronius.meter import MeterLocation


def test_meter_enum():
    assert MeterLocation(0) == MeterLocation.grid
    assert MeterLocation(1) == MeterLocation.load
    assert MeterLocation(3) == MeterLocation.external

    assert MeterLocation(0.0) == MeterLocation.grid
    assert MeterLocation(1.0) == MeterLocation.load
    assert MeterLocation(3.0) == MeterLocation.external

    with pytest.raises(Exception):
        assert MeterLocation(2)
    with pytest.raises(Exception):
        assert MeterLocation(4.0)

    with pytest.raises(Exception):
        assert MeterLocation("0")
    with pytest.raises(Exception):
        assert MeterLocation("1")

    with pytest.raises(Exception):
        assert MeterLocation("0.0")
    with pytest.raises(Exception):
        assert MeterLocation("1.0")
