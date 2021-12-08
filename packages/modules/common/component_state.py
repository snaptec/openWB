from typing import List


class BatState:
    def __init__(self, imported: float, exported: float, power: float, soc: int = 0):
        self.imported = imported
        self.exported = exported
        self.power = power
        self.soc = soc


class CounterState:
    def __init__(self,
                 imported: float = 0,
                 exported: float = 0,
                 power_all: float = 0,
                 voltages: List[float] = None,
                 currents: List[float] = None,
                 powers: List[float] = None,
                 power_factors: List[float] = None,
                 frequency: float = 50):
        if voltages is None:
            voltages = [0]*3
        self.voltages = voltages
        if currents is None:
            currents = [0]*3
        self.currents = currents
        if powers is None:
            powers = [0]*3
        self.powers = powers
        if power_factors is None:
            power_factors = [0]*3
        self.power_factors = power_factors
        self.imported = imported
        self.exported = exported
        self.power_all = power_all
        self.frequency = frequency


class InverterState:
    def __init__(
        self,
        counter: float,
        power: float,
        currents: List[float] = None,
    ):
        if currents is None:
            currents = [0]*3
        self.currents = currents
        self.power = power
        self.counter = counter


class CarState:
    def __init__(self, soc: float):
        self.soc = soc
