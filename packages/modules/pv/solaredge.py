#!/usr/bin/env python3
import sys
import struct
from pymodbus.client.sync import ModbusTcpClient

if __name__ == "__main__":
    from pathlib import Path
    import os
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from helpermodules import pub
    from helpermodules import simcount
    import set_values
else:
    from ...helpermodules import log
    from ...helpermodules import pub
    from ...helpermodules import simcount
    from . import set_values


class module(set_values.set_values):
    def __init__(self, pv_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.pv_num = pv_num

    def read(self):
        try:
            if self.data["config"]["ip_address2"] == None:
                self._read_all()
            else:
                self._read_2_inverter()
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))

    def _read_all(self):
        try:
            storage2power = 0

            client = ModbusTcpClient(self.data["config"]["ip_address1"], port=502)

            # batterie auslesen und pv leistung korrigieren
            storagepower = 0
            storage2power = 0
            if self.data["config"]["ip_address1"] == self.data["config"]["bat_ip"]:
                rr = client.read_holding_registers(62852, 2, unit=self.data["config"]["slave_id1"])
                raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
                soc = int(struct.unpack('>f', raw)[0])
                try:
                    if self.data["config"]["second_bat"] == 1:
                        rr = client.read_holding_registers(62852, 2, unit=self.data["config"]["slave_id2"])
                        raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
                        soc2 = int(struct.unpack('>f', raw)[0])
                        fsoc=(soc+soc2)/2
                    else:
                        fsoc=soc
                except:
                    fsoc=soc
                    if self.ramdisk == True:
                        f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
                        f.write(str(fsoc))
                        f.close()
                    else:
                        pub.pub("openWB/set/bat/1/get/soc", fsoc)
                rr = client.read_holding_registers(62836, 2, unit=self.data["config"]["slave_id1"])
                raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
                storagepower = int(struct.unpack('>f', raw)[0])
                try:
                    if self.data["config"]["second_bat"] == 1:
                        rr = client.read_holding_registers(62836, 2, unit=self.data["config"]["slave_id2"])
                        raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
                        storage2power = int(struct.unpack('>f', raw)[0])
                except:
                    storage2power = 0
                final=storagepower+storage2power
                if self.ramdisk == True:
                    f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
                    f.write(str(final))
                    f.close()
                else:
                    pub.pub("openWB/set/bat/1/get/power", fsoc)
            if self.ramdisk == True:
                imported, exported = simcount.sim_count(final, ramdisk=True, pref="speicher")
                with open("/var/www/html/openWB/ramdisk/speicherikwh", "w") as f:
                    f.write(str(round(imported, 2)))
                with open("/var/www/html/openWB/ramdisk/speicherekwh", "w") as f:
                    f.write(str(round(exported, 2)))
            else:
                imported, exported = simcount.sim_count(final, topic="openWB/set/bat/"+str(self.bat_num)+"/", data=self.data["simulation"])
                pub.pub("openWB/set/bat/1/get/imported", round(imported, 2))
                pub.pub("openWB/set/bat/1/get/exported", round(exported, 2))

            power = 0
            counter = 0

            slave_ids = [self.data["config"]["slave_id1"], self.data["config"]["slave_id2"], 
                    self.data["config"]["slave_id3"], self.data["config"]["slave_id4"]]
            for i in slave_ids:
                try:
                    if slave_ids[i] != 0:
                        try:
                            resp= client.read_holding_registers(40083,2,unit=slave_ids[i])
                            # read watt
                            watt=format(resp.registers[0], '04x')
                            wr2watt=int(struct.unpack('>h', watt.decode('hex'))[0]) * -1
                            # read multiplier
                            multiplier=format(resp.registers[1], '04x')
                            fmultiplier=int(struct.unpack('>h', multiplier.decode('hex'))[0])
                            if fmultiplier == 2:
                                power_slave = wr2watt * 100
                            if fmultiplier == 1:
                                power_slave = wr2watt * 10
                            if fmultiplier == 0:
                                power_slave = wr2watt
                            if fmultiplier == -1:
                                power_slave = wr2watt / 10
                            if fmultiplier == -2:
                                power_slave = wr2watt / 100
                            if fmultiplier == -3:
                                power_slave = wr2watt / 1000
                            if fmultiplier == -4:
                                power_slave = wr2watt / 10000
                            if fmultiplier == -5:
                                power_slave = wr2watt / 10000
                            resp= client.read_holding_registers(40093,2,unit=slave_ids[i])
                            value1 = resp.registers[0]
                            value2 = resp.registers[1]
                            all = format(value1, '04x') + format(value2, '04x')
                            counter = counter + int(struct.unpack('>i', all.decode('hex'))[0])
                        except:
                            power_slave=0
                        power = power + power_slave
                except:
                    pass

            if self.data["config"]["ext_prod"] == 1:
                try:
                    resp= client.read_holding_registers(40380,1,unit=self.data["config"]["slave_id1"])
                    value1 = resp.registers[0]
                    all = format(value1, '04x')
                    extprod = int(struct.unpack('>h', all.decode('hex'))[0]) * -1
                except:
                    extprod = 0
            else:
                extprod = 0
            if self.data["config"]["subtract_bat"] == 1:
                if storagepower > 0:
                    storagepower=0
                if storage2power > 0:
                    storage2power=0
                power=power-storagepower-storage2power+extprod
            else:
                power=power-storagepower-storage2power+extprod
            if power > 0:
                power=0

            values = [power,
                      counter,
                      [0, 0, 0]]
            self.set(self.pv_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))

    def _read_2_inverter(self):
        try:
            client = ModbusTcpClient(self.data["config"]["ip_address1"], port=502)
            # batterie auslesen und pv leistung korrigieren
            storagepower = 0
            if self.data["config"]["ip_address"] == self.data["config"]["bat_ip"]:
                rr = client.read_holding_registers(62836, 2, unit=1)
                raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
                storagepower = int(struct.unpack('>f', raw)[0])
            power1, counter1 = self._get_power_counter(client) - storagepower

            client = ModbusTcpClient(self.data["config"]["ip_address2"], port=502)
            power2, counter2 = self._get_power_counter(client)

            if self.data["config"]["ext_prod"] == 1:
                resp= client.read_holding_registers(40380,1,unit=self.data["config"]["slave_id1"])
                value1 = resp.registers[0]
                all = format(value1, '04x')
                extprod = int(struct.unpack('>h', all.decode('hex'))[0]) * -1
            else:
                extprod = 0
            power = extprod + power1 + power2    
            counter = counter1 + counter2

            values = [power,
                      counter,
                      [0, 0, 0]]
            self.set(self.pv_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))

    def _get_power_counter(self, client):
        try:
            resp= client.read_holding_registers(40084,2,unit=self.data["config"]["slave_id1"])
            multipli = resp.registers[0]
            multiplint = format(multipli, '04x')
            fmultiplint = int(struct.unpack('>h', multiplint.decode('hex'))[0])

            respw= client.read_holding_registers(40083,2,unit=self.data["config"]["slave_id1"])
            value1w = respw.registers[0]
            allw = format(value1w, '04x')
            power = int(struct.unpack('>h', allw.decode('hex'))[0]) * -1
            resp= client.read_holding_registers(40084,2,unit=self.data["config"]["slave_id1"])
            mult2ipli = resp.registers[0]
            mult2iplint = format(mult2ipli, '04x')
            fmult2iplint = int(struct.unpack('>h', mult2iplint.decode('hex'))[0])

            if fmultiplint == fmult2iplint:
                if fmultiplint == 0:
                    power = power
                if fmultiplint == -1:
                    power = power / 10 
                if fmultiplint == -2:
                    power = power / 100
                if fmultiplint == -3:
                    power = power / 1000
                if fmultiplint == -4:
                    power = power / 10000
                if fmultiplint == -5:
                    power = power / 100000

            resp= client.read_holding_registers(40093,2,unit=self.data["config"]["slave_id1"])
            value1 = resp.registers[0]
            value2 = resp.registers[1]
            all = format(value1, '04x') + format(value2, '04x')
            counter = int(struct.unpack('>i', all.decode('hex'))[0])
            return power, counter
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
            return 0


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        ip_address1 = str(sys.argv[1])
        mod.data["config"]["ip_address1"] = ip_address1
        try:
            slave_id1 = int(sys.argv[2])
        except:
            slave_id1=0
        mod.data["config"]["slave_id1"] = slave_id1
        try:
            slave_id2 = int(sys.argv[3])
        except:
            slave_id2=0
        mod.data["config"]["slave_id2"] = slave_id2
        try:
            slave_id3 = int(sys.argv[4])
        except:
            slave_id3=0
        mod.data["config"]["slave_id3"] = slave_id3
        try:
            slave_id4 = int(sys.argv[5])
        except:
            slave_id4=0
        mod.data["config"]["slave_id4"] = slave_id4
        ext_prod = int(sys.argv[6])
        mod.data["config"]["ext_prod"] = ext_prod
        bat_ip = str(sys.argv[7])
        mod.data["config"]["bat_ip"] = bat_ip
        second_bat = int(sys.argv[8])
        mod.data["config"]["second_bat"] = second_bat
        subtract_bat = int(sys.argv[9])
        mod.data["config"]["subtract_bat"] = subtract_bat
        ip_address2 = str(sys.argv[10])
        mod.data["config"]["ip_address2"] = ip_address2

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)