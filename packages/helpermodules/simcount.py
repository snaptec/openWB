""" Sim Count
Berechnet die importierte und exportierte Leistung, wenn der Zähler / PV-Modul / Speicher diese nicht liefert.
"""
import os
import sys
import time

try:
    from . import log
    from . import pub
except:
    # for 1.9 compability
    from pathlib import Path
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from helpermodules import pub

def sim_count(present_power_all, topic="", data={}, ramdisk = False, pref = ""):
    """ emulate import export

    Parameters
    ----------
    present_power_all: float
        aktuelle Leistung
    topic: str "openWB/set/counter/0/"
        Topic, an das gepublished werden soll
    data:  data.data.counter_data[item].data["set"]
        Daten aus dem data-Modul auf die lesen zugegriffen wird.
    Return
    ------
    imported: importierte Energie
    exported: exportierte Energie
    """
    try:
        sim_timestamp = time.time()
        watt1 = 0
        seconds1 = 0.0
        start_new = True
        if ramdisk == True:
            if os.path.isfile('/var/www/html/openWB/ramdisk/'+pref+'sec0'): 
                f = open('/var/www/html/openWB/ramdisk/'+pref+'sec0', 'r')
                seconds1=float(f.read())
                f.close()
                f = open('/var/www/html/openWB/ramdisk/'+pref+'wh0', 'r')
                watt1=int(float(f.read()))
                f.close()
                f = open('/var/www/html/openWB/ramdisk/'+pref+'watt0pos', 'r')
                wattposh=int(float(f.read()))
                f.close()
                f = open('/var/www/html/openWB/ramdisk/'+pref+'watt0neg', 'r')
                wattnegh=int(f.read())
                f.close()
                f = open('/var/www/html/openWB/ramdisk/'+pref+'sec0', 'w')
                value1 = "%22.6f" % sim_timestamp
                f.write(str(value1))
                f.close()
                f = open('/var/www/html/openWB/ramdisk/'+pref+'wh0', 'w')
                f.write(str(present_power_all))
                f.close()
                start_new = False
        else:
            if "sim_timestamp" in data:
                seconds1 = float(data["sim_timestamp"])
                watt1 = int(data["present_power_all"])
                if "present_imported" in data:
                    wattposh = int(data["present_imported"])
                else:
                    wattposh = 0
                if "present_exported" in data:
                    wattnegh = int(data["present_exported"])
                else:
                    wattnegh = 0
                value1 = "%22.6f" % sim_timestamp
                pub.pub(topic+"module/simulation/sim_timestamp", value1)
                pub.pub(topic+"module/simulation/present_power_all", present_power_all)
                start_new = False
            
        if start_new == False:
            seconds1 = seconds1+1
            deltasec = sim_timestamp - seconds1
            deltasectrun = int(deltasec * 1000) / 1000
            stepsize = int((present_power_all-watt1)/deltasec)
            while seconds1 <= sim_timestamp:
                if watt1 < 0:
                    wattnegh = wattnegh + watt1
                else:
                    wattposh = wattposh + watt1
                watt1 = watt1 + stepsize
                if stepsize < 0:
                    watt1 = max(watt1, present_power_all)
                else:
                    watt1 = min(watt1, present_power_all)
                seconds1 = seconds1 + 1
            rest = deltasec - deltasectrun
            seconds1 = seconds1 - 1 + rest
            if rest > 0:
                watt1 = int(watt1 * rest)
                if watt1 < 0:
                    wattnegh = wattnegh + watt1
                else:
                    wattposh = wattposh + watt1
            wattposkh = wattposh/3600
            wattnegkh = (wattnegh*-1)/3600
            if ramdisk == True:
                f = open('/var/www/html/openWB/ramdisk/'+pref+'watt0pos', 'w')
                f.write(str(wattposh))
                f.close()
                f = open('/var/www/html/openWB/ramdisk/'+pref+'watt0neg', 'w')
                f.write(str(wattnegh))
                f.close()
            else:
                pub.pub(topic+"module/simulation/present_imported", wattposh)
                pub.pub(topic+"module/simulation/present_exported", wattnegh)
            return wattposkh, wattnegkh
        else:
            value1 = "%22.6f" % sim_timestamp
            if ramdisk == True:
                f = open('/var/www/html/openWB/ramdisk/'+pref+'sec0', 'w')
                f.write(str(value1))
                f.close()
                f = open('/var/www/html/openWB/ramdisk/'+pref+'wh0', 'w')
                f.write(str(watt2))
                f.close()
            else:
                pub.pub(topic+"module/simulation/sim_timestamp", value1)
                pub.pub(topic+"module/simulation/present_power_all", present_power_all)
            return 0, 0
    except Exception as e:
        log.log_exception_comp(e, ramdisk)

if __name__ == "__main__":
    try:
        watt2 = int(sys.argv[1])
        pref = str(sys.argv[2])
        sim_count(watt2, ramdisk=True, pref=pref)
    except Exception as e:
        log.log_exception_comp(e, True)