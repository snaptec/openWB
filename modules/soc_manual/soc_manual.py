import argparse
import logging

from helpermodules.cli import run_using_positional_cli_args
from helpermodules.log import setup_logging_stdout
from modules.common.store import ramdisk_write, ramdisk_read_float

setup_logging_stdout()
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
    # SoC-file contains float with SoC 0..100:
    file_soc = "soc{}".format(charge_point - 1)
    # meter file contains float with total energy ever charged at this charge point in kWh:
    file_meter = "llkwhs{}".format(charge_point - 1)
    if charge_point == 1:
        # For historic reasons some file names for charge point one do not fit the usual pattern:
        file_soc = "soc"
        file_meter = "llkwh"

    meter_now = ramdisk_read_float(file_meter)
    try:
        meter_start = ramdisk_read_float(file_meter_start)
        soc_start = ramdisk_read_float(file_soc_start) / 100
    except FileNotFoundError:
        soc_now = ramdisk_read_float(file_soc) / 100
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
    ramdisk_write(file_soc, soc_new * 100, digits=0)


def run_command_line(charge_point: int, efficiency: float, battery_size: float):
    run(charge_point, battery_size, efficiency / 100)


if __name__ == '__main__':
    run_using_positional_cli_args(run_command_line)
