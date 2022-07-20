#!/usr/bin/env python3
import csv
import argparse
from glob import glob
import os
from pathlib import Path
from typing import Iterable

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--price", type=float, default=0.3, help="price per kWh, defaults to 0.30")
parser.add_argument("-v", "--verbose", action="store_true", help="verbose debug output")
args = parser.parse_args()


def debugPrint(text: str):
    if(args.verbose):
        print(text)


CHARGE_LOG_PATH = Path(__file__).resolve().parents[1] / "web" / "logging" / "data" / "ladelog"

print("upgrading charge logs with a price of " + str(args.price) + "€/kWh")

csv_files = glob(str(CHARGE_LOG_PATH) + '/*.csv')
print(csv_files)

for current_filename in csv_files:
    print("checking file \"" + current_filename + "\"")
    current_file = (CHARGE_LOG_PATH / current_filename)
    new_file = (CHARGE_LOG_PATH / (current_filename + '.new'))
    data_modified = False
    with current_file.open("r") as log_file:
        data = list(csv.reader(log_file, delimiter=","))
        for row in data:
            if len(row) == 10:
                debugPrint("file already upgraded")
                break
            if len(row) == 9:
                costs = round(float(row[3]) * args.price, 2)
                debugPrint("costs missing! adding calculated costs: " + str(costs))
                row.append(costs)
                debugPrint(row)
                data_modified = True
            else:
                print("unexpected row format")
                print(row)
        if data_modified:
            debugPrint("file was modified")
            with new_file.open("w") as new_log_file:
                writer = csv.writer(new_log_file, delimiter=",", lineterminator="\n")
                writer.writerows(data)
            os.remove(str(current_file))
            os.rename(str(new_file), str(current_file))
print("upgrading charge logs done")
