
import logging


log = logging.getLogger(__name__)


class SolaredgeMeterRegisters:
    def __init__(self, internal_meter_id: int = 1, synergy_units: int = 1):
        # 40206: Total Real Power (sum of active phases)
        # 40207/40208/40209: Real Power by phase
        # 40210: AC Real Power Scale Factor
        self.powers = 40206
        # 40191/40192/40193: AC Current by phase
        # 40194: AC Current Scale Factor
        self.currents = 40191
        # 40196/40197/40198: Voltage per phase
        # 40203: AC Voltage Scale Factor
        self.voltages = 40196
        # 40204: AC Frequency
        # 40205: AC Frequency Scale Factor
        self.frequency = 40204
        # 40222/40223/40224: Power factor by phase (unit=%)
        # 40225: AC Power Factor Scale Factor
        self.power_factors = 40222
        # 40226: Total Exported Real Energy
        # 40228/40230/40232: Total Exported Real Energy Phase (not used)
        # 40234: Total Imported Real Energy
        # 40236/40238/40240: Total Imported Real Energy Phase (not used)
        # 40242: Real Energy Scale Factor
        self.imp_exp = 40226
        # 40155: C_Option Export + Import, Production, consumption,
        self.option = 40155
        self._update_offset_meter_id(internal_meter_id)
        self._update_offset_synergy_units(synergy_units)

    def _update_offset_meter_id(self, meter_id: int) -> None:
        OFFSET = [0, 174, 348]
        self._add_offset(OFFSET[meter_id-1])

    def _update_offset_synergy_units(self, synergy_units: int) -> None:
        """https://www.solaredge.com/sites/default/files/sunspec-implementation-technical-note.pdf:
        For 2-unit three phase inverters with Synergy technology, add 50 to the default addresses.
        For 3-unit three phase inverters with Synergy technology, add 70 to the default addresses.
        """
        OFFSET = [0, 50, 70]
        try:
            self._add_offset(OFFSET[synergy_units-1])
        except IndexError:
            log.debug("Undocumented synergy units value "+str(synergy_units)+". Use synergy_units 1.")
            self._add_offset(OFFSET[0])

    def _add_offset(self, offset: int) -> None:
        for name, value in self.__dict__.items():
            setattr(self, name, value+offset)
