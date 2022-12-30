import pytest

from modules.devices.fronius.config import MeterLocation


def test_meter_enum():
    assert MeterLocation.get(0) == MeterLocation.grid
    assert MeterLocation.get(1) == MeterLocation.load
    assert MeterLocation.get(3) == MeterLocation.external
    assert MeterLocation.get(257) == MeterLocation.subload

    assert MeterLocation.get(0.0) == MeterLocation.grid
    assert MeterLocation.get(1.0) == MeterLocation.load
    assert MeterLocation.get(3.0) == MeterLocation.external
    assert MeterLocation.get(257.0) == MeterLocation.subload

    with pytest.raises(Exception):
        assert MeterLocation.get(2)
    with pytest.raises(Exception):
        assert MeterLocation.get(4.0)

    with pytest.raises(Exception):
        assert MeterLocation.get("0")
    with pytest.raises(Exception):
        assert MeterLocation.get("1")

    with pytest.raises(Exception):
        assert MeterLocation.get("0.0")
    with pytest.raises(Exception):
        assert MeterLocation.get("1.0")
