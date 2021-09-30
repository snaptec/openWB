#!/usr/bin/python

import fnmatch

if __name__ == "__main__":
    from pathlib import Path
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from helpermodules import simcount
    import set_values
    import rct_lib
else:
    from ...helpermodules import log
    from ...helpermodules import simcount
    from . import set_values
    from . import rct_lib


class module(set_values.set_values):
    def __init__(self, counter_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.counter_num = counter_num

    def read(self):
        try:
            power_all = int(self.read_value(['/var/www/html/openWB/packages/modules/counter/rct.py', '--ip='+self.data["config"]["ip_address"], '--name=g_sync.p_ac_sc_sum']))
            current1 = int(self.read_value(['/var/www/html/openWB/packages/modules/counter/rct.py', '--ip='+self.data["config"]["ip_address"], '--id=0x27BE51D9']) / 230)
            current2 = int(self.read_value(['/var/www/html/openWB/packages/modules/counter/rct.py', '--ip='+self.data["config"]["ip_address"], '--id=0xF5584F90']) / 230)
            current3 = int(self.read_value(['/var/www/html/openWB/packages/modules/counter/rct.py', '--ip='+self.data["config"]["ip_address"], '--id=0xB221BCFA']) / 230)

            if self.ramdisk == True:
                imported, exported = simcount.sim_count(power_all, ramdisk=True, pref="bezug")
            else:
                imported, exported = simcount.sim_count(power_all, topic="openWB/set/counter/"+str(self.counter_num)+"/", data=self.data["simulation"])
            values = [[0, 0, 0],
                      [current1, current2, current3],
                      [0, 0, 0],
                      [0, 0, 0],
                      [imported, exported],
                      power_all,
                      50]
            self.set(self.counter_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))

    def read_value(self, argv):
        try:
            ret_val = None
            rct_lib.init(argv)

            clientsocket = rct_lib.connect_to_server()
            if clientsocket is not None:
                fmt = '#0x{:08X} {:'+str(rct_lib.param_len)+'}'  # {:'+str(rct_lib.desc_len)+'}:'
                for obj in rct_lib.id_tab:
                    if rct_lib.search_id > 0 and obj.id != rct_lib.search_id:
                        continue

                    if rct_lib.search_name is not None and fnmatch.fnmatch(obj.name, rct_lib.search_name) == False:
                        continue

                    value = rct_lib.read(clientsocket, obj.id)
                    if rct_lib.dbglog(fmt.format(obj.id, obj.name), value) == False:
                        ret_val = value
                rct_lib.close(clientsocket)
            if ret_val == None:
                raise ValueError('RCT konnte nicht abgefragt werden aufgrund falscher Konfiguration oder Gerät nicht erreichbar.')
            return ret_val
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
            return 0


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        ip_address = str(sys.argv[1])
        mod.data["config"]["ip_address"] = ip_address

        if int(os.environ.get('debug')) >= 2:
            log.log_1_9('Counter-Module rct ip_address: ' + str(ip_address))

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
