from builtins import property
from typing import Generic, TypeVar, Callable, Sequence, List, Iterable, Union

from modules.common.store.ramdisk.io import ramdisk_write, ramdisk_read

_T = TypeVar("_T")


class _Coder(Generic[_T]):
    def __init__(self, decoder: Callable[[str], _T], encoder: Callable[[_T], str] = str):
        self.encoder = encoder
        self.decoder = decoder


def _encode_int(value: Union[int, float]):
    return str(int(value))


_int_coder = _Coder(int, _encode_int)
_float_coder = _Coder(float)
_bool_coder = _Coder(lambda value: value == "1", lambda value: "1" if value else "0")


class _RamdiskFile(Generic[_T]):
    def __init__(self, filename: str, coder: _Coder[_T]):
        self.filename = filename
        self.coder = coder

    def read(self) -> _T:
        return self.coder.decoder(ramdisk_read(self.filename))

    def write(self, value: _T):
        ramdisk_write(self.filename, self.coder.encoder(value))

    def get_filename(self):
        return self.filename


class _RamdiskIndexFile(Generic[_T]):
    def __init__(self, filename_formatter: Callable[[int], str], coder: _Coder[_T]):
        self.filename_formatter = filename_formatter
        self.coder = coder

    @staticmethod
    def for_prefix(prefix: str, coder: _Coder[_T]):
        return _RamdiskIndexFile(lambda index: prefix + str(index + 1), coder)

    def __getitem__(self, index: int) -> _RamdiskFile[_T]:
        return _RamdiskFile(self.filename_formatter(index), self.coder)

    def read(self, range: Sequence) -> List[_T]:
        return [self[index].read() for index in range]

    def write(self, values: Iterable[_T]):
        for index, value in enumerate(values):
            self[index].write(value)


def _build_filename_charge_point_phase(prefix: str, charge_point_index: int):
    def result(phase_index: int):
        if charge_point_index == 0:
            return prefix + str(phase_index + 1)
        if charge_point_index <= 2:
            return "{}s{}{}".format(prefix, charge_point_index, phase_index + 1)
        return "{}{}lp{}".format(prefix, phase_index + 1, charge_point_index + 1)

    return result


def _build_filename_charge_point(prefix: str, charge_point_index: int, s_limit=2):
    if charge_point_index == 0:
        return prefix
    if charge_point_index <= s_limit:
        return "{}s{}".format(prefix, charge_point_index)
    return "{}lp{}".format(prefix, charge_point_index + 1)


class _ChargePoint:
    def __init__(self, charge_point_index: int):
        self.charge_point_index = charge_point_index

    @property
    def is_charging(self):
        return self.__create_ramdisk_file("chargestat", _bool_coder, s_limit=1)

    @property
    def voltages(self):
        return self.__create_ramdisk_phase_file("llv", _float_coder)

    @property
    def currents(self):
        return self.__create_ramdisk_phase_file("lla", _float_coder)

    @property
    def current_target(self):
        return self.__create_ramdisk_file("llsoll", _int_coder)

    @property
    def energy(self):
        """Total energy charged in Wh"""
        return self.__create_ramdisk_file("llkwh", _float_coder)

    @property
    def is_plugged(self):
        filename = "plugstat"
        if self.charge_point_index == 1:
            filename += "s1"
        elif self.charge_point_index > 1:
            filename += "lp" + str(self.charge_point_index + 1)
        return _RamdiskFile(filename, _bool_coder)

    @property
    def power(self):
        return self.__create_ramdisk_file("llaktuell", _float_coder)

    @property
    def frequency(self):
        return self.__create_ramdisk_file("llhz", _float_coder)

    @property
    def power_factors(self):
        return self.__create_ramdisk_phase_file("llpf", _float_coder)

    @property
    def soc(self):
        return _RamdiskFile("soc" if self.charge_point_index == 0 else "soc" + str(self.charge_point_index), _int_coder)

    def __create_ramdisk_file(self, prefix: str, coder: _Coder, s_limit=2):
        return _RamdiskFile(_build_filename_charge_point(prefix, self.charge_point_index, s_limit), coder)

    def __create_ramdisk_phase_file(self, prefix: str, coder: _Coder):
        return _RamdiskIndexFile(_build_filename_charge_point_phase(prefix, self.charge_point_index), coder)


class _PV:
    def __init__(self, index: int):
        self.prefix = "pv" if index == 0 else "pv" + str(index + 1)

    @property
    def currents(self):
        return _RamdiskIndexFile.for_prefix(self.prefix + "a", _float_coder)

    @property
    def power(self):
        return _RamdiskFile(self.prefix + "watt", _int_coder)

    @property
    def energy(self):
        """Total energy produced in Wh"""
        return _RamdiskFile(self.prefix + "kwh", _float_coder)

    @property
    def energy_k(self):
        """Total energy produced in kWh"""
        return _RamdiskFile(self.prefix + "kwhk", _float_coder)


class _Battery:
    @property
    def power(self):
        return _RamdiskFile("speicherleistung", _int_coder)

    @property
    def soc(self):
        """battery state of charge. 0=empty, 100=full"""
        return _RamdiskFile("speichersoc", _int_coder)

    @property
    def energy_imported(self):
        """total energy imported in Wh"""
        return _RamdiskFile("speicherikwh", _float_coder)

    @property
    def energy_exported(self):
        """total energy exported in Wh"""
        return _RamdiskFile("speicherekwh", _float_coder)


class _Counter:
    @property
    def voltages(self):
        return _RamdiskIndexFile.for_prefix("evuv", _float_coder)

    @property
    def currents(self):
        return _RamdiskIndexFile.for_prefix("bezuga", _float_coder)

    @property
    def powers_import(self):
        return _RamdiskIndexFile.for_prefix("bezugw", _int_coder)

    @property
    def power_factors(self):
        return _RamdiskIndexFile.for_prefix("evupf", _float_coder)

    @property
    def energy_import(self):
        """Total energy imported in Wh"""
        return _RamdiskFile("bezugkwh", _float_coder)

    @property
    def energy_export(self):
        """Total energy exported in Wh"""
        return _RamdiskFile("einspeisungkwh", _float_coder)

    @property
    def power_import(self):
        return _RamdiskFile("wattbezug", _int_coder)

    @property
    def frequency(self):
        return _RamdiskFile("evuhz", _float_coder)


class _RootIndex(Generic[_T]):
    def __init__(self, factory: Callable[[int], _T]):
        self.factory = factory

    def __getitem__(self, item):
        return self.factory(item)


class _ChargePoints:
    def __getitem__(self, charge_point_index: int):
        return _ChargePoint(charge_point_index)


charge_points = _RootIndex(_ChargePoint)
pv = _RootIndex(_PV)
battery = _Battery()
evu = _Counter()
