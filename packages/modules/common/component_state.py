from typing import List


class BatState:
    def __init__(self, power: float, soc: int, imported: float, exported: float):
        self.power = power
        self.soc = soc
        self.imported = imported
        self.exported = exported


class CounterState:
    def __init__(self,
                 voltages: List[float],
                 currents: List[float],
                 powers: List[float],
                 power_factors: List[float],
                 imported: float,
                 exported: float,
                 power_all: float,
                 frequency: float):
        self.voltages = voltages
        self.currents = currents
        self.powers = powers
        self.power_factors = power_factors
        self.imported = imported
        self.exported = exported
        self.power_all = power_all
        self.frequency = frequency


class InverterState:
    def __init__(self, power: float, counter: float, currents: List[float]):
        self.power = power
        self.counter = counter
        self.currents = currents
