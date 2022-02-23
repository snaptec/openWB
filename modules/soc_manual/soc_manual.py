import logging
from typing import List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.store import ramdisk_write, ramdisk_read_float
from modules.common.store.ramdisk import files

log = logging.getLogger("SoC Manual")


def run(charge_point: int, battery_size: float, efficiency: float):
    """
    :param charge_point: charge point number >= 1
    :param battery_size: battery size in kWh
    :param efficiency: efficiency as fraction (usually between 0 and 1)
    :return:
    """
    file_soc_start = "manual_soc_lp{}".format(charge_point)
    file_meter_start = "manual_soc_meter_lp{}".format(charge_point)
    charge_point_files = files.charge_points[charge_point - 1]

    meter_now = charge_point_files.energy.read()
    try:
        meter_start = ramdisk_read_float(file_meter_start)
        soc_start = ramdisk_read_float(file_soc_start) / 100
    except FileNotFoundError:
        soc_now = charge_point_files.soc.read() / 100
        log.warning("Not initialized. Begin with meter=%g kWh, soc=%g%%", meter_now, soc_now * 100)
        ramdisk_write(file_meter_start, meter_now)
        ramdisk_write(file_soc_start, soc_now * 100, 1)
        return

    energy_counted = meter_now - meter_start
    energy_battery_gain = energy_counted * efficiency
    battery_soc_gain = energy_battery_gain / battery_size
    soc_new = soc_start + battery_soc_gain
    log.debug("Charged: %g kWh -> %g kWh = %g kWh", meter_start, meter_now, energy_counted)
    log.debug(
        "SoC-Gain: Charged (%g kWh) * efficiency (%g%%) / battery-size (%g kWh) = %.1f%%",
        energy_counted, efficiency * 100, battery_size, battery_soc_gain * 100
    )
    log.info("%g%% + %g kWh = %g%%", soc_start * 100, energy_battery_gain, soc_new * 100)
    if soc_new > 1:
        log.warning("Calculated SoC of %g%% exceeds maximum and is limited to 100%%! Check your settings!", soc_new * 100)
        soc_new = 1
    charge_point_files.soc.write(soc_new * 100)


def run_command_line(charge_point: int, efficiency: float, battery_size: float):
    run(charge_point, battery_size, efficiency / 100)


def main(argv: List[str]):
    run_using_positional_cli_args(run_command_line, argv)
