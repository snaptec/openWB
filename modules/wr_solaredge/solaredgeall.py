#!/usr/bin/env python3
import math
import sys
from statistics import mean

from modules.common.component_state import InverterState, BatState
from modules.common.modbus import ModbusClient, ModbusDataType
from modules.common.store import get_inverter_value_store, get_bat_value_store

# Sunspec (API) documentation: https://www.solaredge.com/sites/default/files/sunspec-implementation-technical-note.pdf

ipaddress = str(sys.argv[1])
slave_ids = list(map(int, filter(lambda id: id.isnumeric(), sys.argv[2:6])))
batwrsame = int(sys.argv[6])
extprodakt = int(sys.argv[7])
zweiterspeicher = int(sys.argv[8])
subbat = int(sys.argv[9])

client = ModbusClient(ipaddress)

storage_slave_ids = slave_ids[0: 1 + zweiterspeicher]
storage_powers = []
if batwrsame == 1:
    soc = mean(
        client.read_holding_registers(62852, ModbusDataType.FLOAT_32, unit=slave_id) for slave_id in storage_slave_ids
    )
    storage_powers = [
        client.read_holding_registers(62836, ModbusDataType.FLOAT_32, unit=slave_id) for slave_id in storage_slave_ids
    ]
    get_bat_value_store(1).set(BatState(power=sum(storage_powers), soc=soc))

total_energy = 0
total_power = 0

for slave_id in slave_ids:
    # 40083 = AC Power value (Watt), 40084 = AC Power scale factor
    power_base, power_scale = client.read_holding_registers(40083, [ModbusDataType.INT_16] * 2, unit=slave_id)
    total_power -= power_base * math.pow(10, power_scale)
    # 40093 = AC Lifetime Energy production (Watt hours)
    total_energy += client.read_holding_registers(40093, ModbusDataType.INT_32, unit=slave_id)

if extprodakt == 1:
    # 40380 = "Meter 2/Total Real Power (sum of active phases)" (Watt)
    total_power -= client.read_holding_registers(40380, ModbusDataType.INT_16, unit=slave_ids[0])
if subbat == 1:
    total_power -= sum(min(p, 0) for p in storage_powers)
else:
    total_power -= sum(storage_powers)

get_inverter_value_store(1).set(InverterState(counter=total_energy, power=total_power))
