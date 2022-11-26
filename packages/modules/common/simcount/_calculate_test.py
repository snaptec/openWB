from typing import Tuple

import pytest as pytest

from modules.common.simcount._calculate import Number, calculate_import_export


class Params:
    def __init__(self,
                 name: str,
                 seconds: int,
                 power_previous: int,
                 power_present: int,
                 expected_energy: Tuple[Number, Number]):
        self.name = name
        self.seconds = seconds
        self.power_previous = power_previous
        self.power_present = power_present
        self.expected_energy = expected_energy

    def invert(self):
        return Params(
            "inverse: " + self.name, self.seconds, self.power_present, self.power_previous, self.expected_energy
        )


cases = [
    Params(name="Ascending from zero:",
           seconds=1, power_previous=0, power_present=10, expected_energy=(5, 0)),
    Params(name="Ascending from more than zero:",
           seconds=1, power_previous=10, power_present=11, expected_energy=(10.5, 0)),
    Params(name="Ascending to zero:",
           seconds=1, power_previous=-1, power_present=0, expected_energy=(0, .5)),
    Params(name="Ascending to less than zero:",
           seconds=1, power_previous=-11, power_present=-10, expected_energy=(0, 10.5)),
    Params(name="Ascending from negative to positive",
           seconds=2, power_previous=-1, power_present=1, expected_energy=(.5, .5)),
    Params(name="Ascending from negative to positive with asymmetric intersection",
           seconds=10, power_previous=-9, power_present=1, expected_energy=(.5, 40.5)),
    Params(name="Nothing changed positive",
           seconds=1, power_previous=1, power_present=1, expected_energy=(1, 0)),
    Params(name="Nothing changed zero",
           seconds=1, power_previous=0, power_present=0, expected_energy=(0, 0)),
    Params(name="Nothing changed negative",
           seconds=1, power_previous=-1, power_present=-1, expected_energy=(0, 1)),
]
cases.extend(map(lambda case: case.invert(), cases[:]))


@pytest.mark.parametrize("params", cases, ids=[c.name for c in cases])
def test_energy_calculation(params: Params):
    # execution
    actual = calculate_import_export(params.seconds, params.power_previous, params.power_present)

    # evaluation
    assert actual == params.expected_energy
