#!/usr/bin/env python3
import csv
import argparse
import logging
from pathlib import Path
import sys

CHARGE_LOG_PATH = Path(__file__).resolve().parents[1] / "web" / "logging" / "data" / "ladelog"

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--price", type=float, default=0.3, help="price per kWh, defaults to 0.30")
parser.add_argument("-v", "--verbose", action="store_true", help="verbose debug output")
args = parser.parse_args()

log = logging.getLogger("upgradeChargeLogs")
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(
    logging.Formatter(u"%(asctime)s: PID: %(process)d: %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
)
log.addHandler(log_handler)

if(args.verbose):
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)

log.info("upgrading charge logs with a price of " + str(args.price) + " per kWh")
csv_files = CHARGE_LOG_PATH.glob("*.csv")

for current_file in csv_files:
    log.debug("checking file \"" + current_file.name + "\"")
    new_file = current_file.with_name(current_file.name + ".new")
    data_modified = False
    with current_file.open("r") as log_file:
        data = list(csv.reader(log_file, delimiter=","))
        for row in data:
            if len(row) == 10:
                log.debug("file \"" + current_file.name + "\" row already upgraded")
            if len(row) == 8:  # format until 2020/02 without rfid tag
                log.debug("rfid tag missing! adding \"0\" as default tag")
                row.append(0)
                data_modified = True
            if len(row) == 9:  # format until 2022/07 without costs
                costs = round(float(row[3]) * args.price, 2)
                log.debug("costs missing! adding calculated costs: " + str(costs))
                row.append(costs)
                log.debug(row)
                data_modified = True
            else:
                if len(row) not in [0, 10]:
                    log.error("file \"" + current_file.name + "\": unexpected row format: " + str(row))
        if data_modified:
            log.debug("file was modified")
            with new_file.open("w") as new_log_file:
                writer = csv.writer(new_log_file, delimiter=",", lineterminator="\n")
                writer.writerows(data)
            new_file.replace(current_file)
log.info("upgrading charge logs done")
