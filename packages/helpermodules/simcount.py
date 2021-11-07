""" Sim Count
Berechnet die importierte und exportierte Leistung, wenn der Zähler / PV-Modul / Speicher diese nicht liefert.
"""
import os
import paho.mqtt.subscribe as subscribe
import re
import signal
import sys
import time
import typing
from pathlib import Path

try:
    from . import log
    from . import pub
except:
    # for 1.9 compability
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log


class SimCountFactory:
    def get_sim_counter(self):
        try:
            ramdisk = Path(str(Path(os.path.abspath(__file__)).parents[2])+"/ramdisk/bootinprogress").is_file()
            return SimCountLegacy if ramdisk else SimCount
        except:
           log.MainLogger().exception("Fehler im Modul simcount")


class SimCountLegacy:
    def sim_count(self, power_present: float, topic: str = "", data: dict = {}, prefix: str = "") -> typing.Tuple[float, float]:
        """ emulate import export

        Parameters
        ----------
        power_present: aktuelle Leistung
        topic: Topic, ungenutzt
        data:  ungenutzt
        prefix: prefix für die ramdisk-Datei
        Return
        ------
        imported: importierte Energie
        exported: exportierte Energie
        """
        try:
            timestamp_present = time.time()
            power_previous = 0
            timestamp_previous = 0.0
            start_new = True
            if os.path.isfile('/var/www/html/openWB/ramdisk/'+prefix+'sec0'):
                timestamp_previous = float(self.read_ramdisk_file(prefix+'sec0'))
                power_previous = int(float(self.read_ramdisk_file(prefix+'wh0')))
                try:
                    counter_import_present = int(float(self.read_ramdisk_file(prefix+'watt0pos')))
                except:
                    counter_import_present = self.restore("watt0pos", prefix)
                counter_import_previous = counter_import_present
                try:
                    counter_export_present = int(float(self.read_ramdisk_file(prefix+'watt0neg')))
                except:
                    counter_export_present = self.restore("watt0neg", prefix)
                if counter_export_present < 0:
                    # runs/simcount.py speichert das Zwischenergebnis des Exports negativ ab.
                    counter_export_present = counter_export_present * -1
                counter_export_previous = counter_export_present
                log.MainLogger().debug("simcount Zwischenergebnisse letzte Berechnung: Import: "+str(counter_import_previous)+" Export: "+str(counter_export_previous)+" Power: "+str(power_previous))
                start_new = False
            self.write_ramdisk_file(prefix+'sec0', "%22.6f" % timestamp_present)
            self.write_ramdisk_file(prefix+'wh0', power_present)

            if start_new == False:
                timestamp_previous = timestamp_previous+1
                seconds_since_previous = timestamp_present - timestamp_previous
                imp_exp = calculate_import_export(seconds_since_previous, power_previous, power_present)
                counter_export_present = counter_export_present + imp_exp[1]
                counter_import_present = counter_import_present + imp_exp[0]
                log.MainLogger().debug("simcount aufsummierte Energie: Bezug[Ws]: "+str(counter_import_present)+", Einspeisung[Ws]: "+str(counter_export_present))
                wattposkh = counter_import_present/3600
                wattnegkh = counter_export_present/3600
                log.MainLogger().info("simcount Ergebnis: Bezug[Wh]: "+str(wattposkh)+", Einspeisung[Wh]: "+str(wattnegkh))

                topic = self.__get_topic(prefix)
                log.MainLogger().debug("simcount Zwischenergebnisse atkuelle Berechnung: Import: "+str(counter_import_present)+" Export: "+str(counter_export_present)+" Power: "+str(power_present))
                self.write_ramdisk_file(prefix+'watt0pos', counter_import_present)
                if counter_import_present != counter_import_previous:
                    pub.pub_single("openWB/"+topic+"/WHImported_temp", counter_import_present, no_json=True)
                self.write_ramdisk_file(prefix+'watt0neg', counter_export_present)
                if counter_export_present != counter_export_previous:
                    pub.pub_single("openWB/"+topic+"/WHExport_temp", counter_export_present, no_json=True)
                return wattposkh, wattnegkh
            else:
                return 0, 0
        except:
           log.MainLogger().exception("Fehler im Modul simcount")

    def __get_topic(self, prefix:str) -> str:
        """ ermittelt das zum Präfix gehörende Topic."""
        try:
            if prefix == "bezug":
                topic = "evu"
            elif prefix == "pv":
                topic = prefix
            elif prefix == "speicher":
                topic = "housebattery"
            else:
                log.MainLogger().error("Fehler im Modul simcount: Unbekannter Präfix")
            return topic
        except Exception as e:
            log.MainLogger().error("Fehler im Modul simcount", e)

    def read_ramdisk_file(self, name: str):
        try:
            with open('/var/www/html/openWB/ramdisk/' + name, 'r') as f:
                return f.read()
        except:
           log.MainLogger().exception("Fehler im Modul simcount")

    def write_ramdisk_file(self, name: str, value):
        try:
            with open('/var/www/html/openWB/ramdisk/' + name, 'w') as f:
                f.write(str(value))
        except:
           log.MainLogger().exception("Fehler im Modul simcount")

    def restore(self, value, prefix: str):
        """ stellt die Werte vom Broker wieder her.
        """
        try:
            signal.signal(signal.SIGALRM, self.abort)
            signal.alarm(3)
            try:
                topic = self.__get_topic(prefix)
                if value == "watt0pos":
                    temp = subscribe.simple("openWB/"+topic+"/WHImported_temp", hostname="localhost")
                else:
                    temp = subscribe.simple("openWB/"+topic+"/WHExport_temp", hostname="localhost")
            except Exception as e:
                log.MainLogger().error("Fehler im Modul simcount", e)
            # Signal-Handler stoppen
            signal.alarm(0)
            temp = int(float(temp.payload.decode("utf-8")))
            ra = '^-?[0-9]+$'
            if re.search(ra, str(temp)) == None:
                temp = "0"
            self.write_ramdisk_file(prefix+value, temp)
            if value == "watt0pos":
                log.MainLogger().info("loadvars read openWB/"+topic+"/WHImported_temp from mosquito "+str(temp))
            else:
                log.MainLogger().info("loadvars read openWB/"+topic+"/WHExport_temp from mosquito "+str(temp))
            return temp
        except:
           log.MainLogger().exception("Fehler im Modul simcount")

    def abort(self, signal, frame):
        raise TimeoutError


class SimCount:
    def sim_count(self, power_present: float, topic: str = "", data: dict = {}, prefix: str = "") -> typing.Tuple[float, float]:
        """ emulate import export

        Parameters
        ----------
        power_present: aktuelle Leistung
        topic: str Topic, an das gepublished werden soll
        data: Komponenten-Daten
        Return
        ------
        imported: importierte Energie
        exported: exportierte Energie
        """
        try:
            timestamp_present = time.time()
            power_previous = 0
            timestamp_previous = 0.0
            start_new = True
            if "timestamp_present" in data:
                timestamp_previous = float(data["timestamp_present"])
                power_previous = int(data["power_present"])
                if "present_imported" in data:
                    counter_import_present = int(data["present_imported"])
                else:
                    counter_import_present = 0
                if "present_exported" in data:
                    counter_export_present = int(data["present_exported"])
                else:
                    counter_export_present = 0
                log.MainLogger().debug("Fortsetzen der Simulation: Importzaehler: "+str(counter_import_present)+"Ws, Export-Zaehler: "+str(counter_export_present)+"Ws")
                start_new = False
            pub.pub(topic+"simulation/timestamp_present", "%22.6f" % timestamp_present)
            pub.pub(topic+"simulation/power_present", power_present)

            if start_new == False:
                timestamp_previous = timestamp_previous+1
                seconds_since_previous = timestamp_present - timestamp_previous
                imp_exp = calculate_import_export(seconds_since_previous, power_previous, power_present)
                counter_export_present = counter_export_present + imp_exp[1]
                counter_import_present = counter_import_present + imp_exp[0]
                log.MainLogger().debug("simcount aufsummierte Energie: Bezug[Ws]: "+str(counter_import_present)+", Einspeisung[Ws]: "+str(counter_export_present))
                wattposkh = counter_import_present/3600
                wattnegkh = counter_export_present/3600
                log.MainLogger().info("simcount Ergebnis: Bezug[Wh]: "+str(wattposkh)+", Einspeisung[Wh]: "+str(wattnegkh))
                log.MainLogger().debug("simcount Zwischenergebnisse atkuelle Berechnung: Import: "+str(counter_import_present)+" Export: "+str(counter_export_present)+" Power: "+str(power_present))
                pub.pub(topic+"simulation/present_imported", counter_import_present)
                pub.pub(topic+"simulation/present_exported", counter_export_present)
                return wattposkh, wattnegkh
            else:
                log.MainLogger().debug("Neue Simulation")
                pub.pub(topic+"simulation/present_imported", 0)
                pub.pub(topic+"simulation/present_exported", 0)
                return 0, 0
        except:
           log.MainLogger().exception("Fehler im Modul simcount")


Number = typing.Union[int, float]


def calculate_import_export(seconds_since_previous: Number, power1: Number, power2: Number) -> typing.Tuple[Number, Number]:
    try:
        log.MainLogger().debug("simcount Berechnungsgrundlage: vergangene Zeit [s]"+str(seconds_since_previous)+", vorherige Leistung[W]: "+str(power1)+", aktuelle Leistung[W]: "+str(power2))
        power_low = min(power1, power2)
        power_high = max(power1, power2)
        gradient = (power_high - power_low) / seconds_since_previous
        # Berechnung der Gesamtfläche (ohne Beträge, Fläche unterhalb der x-Achse reduziert die Fläche oberhalb der x-Achse)
        def energy_function(seconds): return .5 * gradient * seconds ** 2 + power_low * seconds

        energy_total = energy_function(seconds_since_previous)
        log.MainLogger().debug("simcount Gesamtenergie im Zeitintervall: "+str(energy_total))
        if power_low < 0 < power_high:
            # Berechnung der Fläche im vierten Quadranten -> Export
            power_zero_seconds = -power_low / gradient
            energy_exported = energy_function(power_zero_seconds)
            log.MainLogger().debug("simcount exportierte Energie im Zeitintervall: "+str(energy_exported))
            # Betragsmäßige Gesamtfläche: oberhalb der x-Achse = Import, unterhalb der x-Achse: Export
            return energy_total - energy_exported, energy_exported * -1
        return (energy_total, 0) if energy_total >= 0 else (0, -energy_total)
    except:
       log.MainLogger().exception("Fehler im Modul simcount")


if __name__ == "__main__":
    try:
        SimCountLegacy.sim_count(int(sys.argv[1]), prefix=str(sys.argv[2]))
    except:
       log.MainLogger().exception("Fehler im Modul simcount")
