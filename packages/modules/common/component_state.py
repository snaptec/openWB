from typing import Dict, List, Optional

from helpermodules.auto_str import auto_str


@auto_str
class BatState:
    def __init__(
        self,
        imported: float = 0,
        exported: float = 0,
        power: float = 0,
        soc: float = 0,
    ):
        """Args:
            imported: total imported energy in Wh
            exported: total exported energy in Wh
            power: actual power in W
            soc: actual state of charge in percent
        """
        self.imported = imported
        self.exported = exported
        self.power = power
        self.soc = soc


@auto_str
class CounterState:
    def __init__(
        self,
        imported: float = 0,
        exported: float = 0,
        power: float = 0,
        voltages: Optional[List[float]] = None,
        currents: Optional[List[float]] = None,
        powers: Optional[List[float]] = None,
        power_factors: Optional[List[float]] = None,
        frequency: float = 50,
    ):
        """Args:
            imported: total imported energy in Wh
            exported: total exported energy in Wh
            power: actual power in W
            voltages: actual voltages for 3 phases in V
            currents: actual currents for 3 phases in A
            powers: actual powers for 3 phases in W
            power_factors: actual power factors for 3 phases
            frequency: actual grid frequency in Hz
        """
        if voltages is None:
            voltages = [230.0]*3
        self.voltages = voltages
        if powers is None:
            if currents is None:
                powers = [0.0]*3
            else:
                powers = [currents[i]*voltages[i] for i in range(0, 3)]
        self.powers = powers
        if currents is None and powers:
            currents = [powers[i]/voltages[i] for i in range(0, 3)]
        if currents and powers:
            currents = [currents[i]*-1 if powers[i] < 0 and currents[i] > 0 else currents[i] for i in range(0, 3)]
        self.currents = currents
        if power_factors is None:
            power_factors = [0.0]*3
        self.power_factors = power_factors
        self.imported = imported
        self.exported = exported
        self.power = power
        self.frequency = frequency


@auto_str
class InverterState:
    def __init__(
        self,
        counter: float,
        power: float,
        currents: Optional[List[float]] = None,
    ):
        """Args:
            counter: total energy in Wh
            power: actual power in W
            currents: actual currents for 3 phases in A
        """
        if currents is None:
            currents = [0.0]*3
        self.currents = currents
        self.power = power
        self.counter = counter


@auto_str
class CarState:
    def __init__(self, soc: float, range: Optional[float] = None, soc_timestamp: str = ""):
        """Args:
            soc: actual state of charge in percent
            range: actual range in km
            soc_timestamp: timestamp of last request in %m/%d/%Y, %H:%M:%S
        """
        self.soc = soc
        self.range = range
        self.soc_timestamp = soc_timestamp


class ChargepointState:
    def __init__(self,
                 imported: float = 0,
                 exported: float = 0,
                 power: float = 0,
                 voltages: Optional[List[float]] = None,
                 currents: Optional[List[float]] = None,
                 power_factors: Optional[List[float]] = None,
                 phases_in_use: int = 1,
                 charge_state: bool = False,
                 plug_state: bool = False,
                 read_tag: Optional[Dict[str, str]] = None):
        if voltages is None:
            voltages = [0.0]*3
        self.voltages = voltages
        if currents is None:
            currents = [0.0]*3
        self.currents = currents
        if power_factors is None:
            power_factors = [0.0]*3
        self.power_factors = power_factors
        self.imported = imported
        self.exported = exported
        self.power = power
        self.phases_in_use = phases_in_use
        self.charge_state = charge_state
        self.plug_state = plug_state
        self.read_tag = read_tag
