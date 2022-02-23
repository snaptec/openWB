""" Sim Count
Berechnet die importierte und exportierte Leistung, wenn der Zähler / PV-Modul / Speicher diese nicht liefert.
"""
import os
import paho.mqtt.client as mqtt
import time
import typing

from helpermodules import compatibility
from helpermodules import log
from helpermodules import pub
from helpermodules.cli import run_using_positional_cli_args
from modules.common.fault_state import FaultState


def process_error(e):
    raise FaultState.error(__name__+" "+str(type(e))+" "+str(e)) from e


class SimCountFactory:
    def get_sim_counter(self):
        try:
            ramdisk = compatibility.is_ramdisk_in_use()
            return SimCountLegacy if ramdisk else SimCount
        except Exception as e:
            process_error(e)


def get_topic(prefix: str) -> str:
    """ ermittelt das zum Präfix gehörende Topic."""
    try:
        if prefix == "bezug":
            topic = "evu"
        elif prefix == "pv":
            topic = prefix
        elif prefix == "speicher":
            topic = "housebattery"
        else:
            raise FaultState.error("Fehler im Modul simcount: Unbekannter Präfix")
        return topic
    except Exception as e:
        process_error(e)


def read_ramdisk_file(name: str):
    try:
        with open('/var/www/html/openWB/ramdisk/' + name, 'r') as f:
            return f.read()
    except Exception as e:
        process_error(e)


def write_ramdisk_file(name: str, value):
    try:
        with open('/var/www/html/openWB/ramdisk/' + name, 'w') as f:
            f.write(str(value))
    except Exception as e:
        process_error(e)


class SimCountLegacy:
    def sim_count(
        self, power_present: float, topic: str = "", data: dict = {}, prefix: str = ""
    ) -> typing.Tuple[float, float]:
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
            power_previous, counter_export_present, counter_export_previous = 0, 0, 0
            counter_import_present, counter_import_previous = 0, 0
            timestamp_previous = 0.0
            start_new = True
            if os.path.isfile('/var/www/html/openWB/ramdisk/'+prefix+'sec0'):
                timestamp_previous = float(read_ramdisk_file(prefix+'sec0'))
                power_previous = int(float(read_ramdisk_file(prefix+'wh0')))
                try:
                    counter_import_present = int(float(read_ramdisk_file(prefix+'watt0pos')))
                except Exception:
                    counter_import_present = int(Restore().restore_value("watt0pos", prefix))
                counter_import_previous = counter_import_present
                try:
                    counter_export_present = int(float(read_ramdisk_file(prefix+'watt0neg')))
                except Exception:
                    counter_export_present = int(Restore().restore_value("watt0neg", prefix))
                if counter_export_present < 0:
                    # runs/simcount.py speichert das Zwischenergebnis des Exports negativ ab.
                    counter_export_present = counter_export_present * -1
                counter_export_previous = counter_export_present
                log.MainLogger().debug("simcount Zwischenergebnisse letzte Berechnung: Import: " +
                                       str(counter_import_previous) + " Export: " + str(counter_export_previous) +
                                       " Leistung: " + str(power_previous))
                start_new = False
            write_ramdisk_file(prefix+'sec0', "%22.6f" % timestamp_present)
            write_ramdisk_file(prefix+'wh0', int(power_present))

            if start_new:
                log.MainLogger().debug("Neue Simulation starten.")
                if prefix == "bezug":
                    imported = get_existing_imports_exports('bezugkwh')
                    exported = get_existing_imports_exports('einspeisungkwh')
                elif prefix == "pv":
                    imported = 0
                    exported = get_existing_imports_exports('pvkwh')
                else:
                    imported = get_existing_imports_exports('speicherikwh')
                    exported = get_existing_imports_exports('speicherekwh')
                return imported, exported
            else:
                # timestamp_previous = timestamp_previous + 1  # do not increment time if calculating areas!
                seconds_since_previous = timestamp_present - timestamp_previous
                imp_exp = calculate_import_export(
                    seconds_since_previous, power_previous, power_present)
                counter_export_present = counter_export_present + imp_exp[1]
                counter_import_present = counter_import_present + imp_exp[0]
                log.MainLogger().debug(
                    "simcount aufsummierte Energie: Bezug[Ws]: " + str(counter_import_present) + ", Einspeisung[Ws]: " +
                    str(counter_export_present)
                )
                energy_positive_kWh = counter_import_present / 3600
                energy_negative_kWh = counter_export_present / 3600
                log.MainLogger().info(
                    "simcount Ergebnis: Bezug[Wh]: " + str(energy_positive_kWh) +
                    ", Einspeisung[Wh]: " + str(energy_negative_kWh)
                )

                topic = get_topic(prefix)
                log.MainLogger().debug(
                    "simcount Zwischenergebnisse aktuelle Berechnung: Import: " + str(counter_import_present) +
                    " Export: " + str(counter_export_present) + " Leistung: " + str(power_present)
                )
                write_ramdisk_file(prefix+'watt0pos', counter_import_present)
                if counter_import_present != counter_import_previous:
                    pub.pub_single("openWB/"+topic+"/WHImported_temp", counter_import_present, no_json=True)
                write_ramdisk_file(prefix+'watt0neg', counter_export_present)
                if counter_export_present != counter_export_previous:
                    pub.pub_single("openWB/"+topic+"/WHExport_temp",
                                   counter_export_present, no_json=True)
                return energy_positive_kWh, energy_negative_kWh
        except Exception as e:
            process_error(e)


def get_existing_imports_exports(file: str) -> float:
    if os.path.isfile('/var/www/html/openWB/ramdisk/'+file):
        value = float(read_ramdisk_file(file))
        log.MainLogger().info("Es wurde ein vorhandener Zählerstand in "+file+" gefunden: "+str(value)+"Wh")
    else:
        value = 0
    return value


class Restore():
    def restore_value(self, value: str, prefix: str) -> float:
        result = 0
        self.temp = ""
        try:
            self.value = value
            self.prefix = prefix
            client = mqtt.Client("openWB-simcount_restore-" + str(self.__getserial()))

            client.on_connect = self.__on_connect
            client.on_message = self.__on_message

            client.connect("localhost", 1883)
            client.loop_start()
            time.sleep(0.5)
            client.loop_stop()
            try:
                result = float(self.temp)
                if value == "watt0pos":
                    log.MainLogger().info(
                        "loadvars read openWB/"+get_topic(self.prefix)+"/WHImported_temp from mosquito "+str(self.temp))
                else:
                    log.MainLogger().info(
                        "loadvars read openWB/"+get_topic(self.prefix)+"/WHExport_temp from mosquito "+str(self.temp))
            except ValueError:
                log.MainLogger().info("Keine Werte auf dem Broker gefunden.")
                if prefix == "bezug":
                    file = "bezugkwh" if value == "watt0pos" else "einspeisungkwh"
                elif prefix == "pv":
                    file = "pvkwh"
                else:
                    file = "speicherikwh" if value == "watt0pos" else "speicherekwh"
                if os.path.isfile('/var/www/html/openWB/ramdisk/'+file):
                    result = get_existing_imports_exports(file) * 3600
                    self.temp = str(result)
            write_ramdisk_file(prefix+value, self.temp)
        except Exception:
            log.MainLogger().exception("Fehler in der Restore-Klasse")
        finally:
            return result

    def __on_connect(self, client, userdata, flags, rc):
        """ connect to broker and subscribe to set topics
        """
        try:
            topic = get_topic(self.prefix)
            if self.value == "watt0pos":
                client.subscribe("openWB/"+topic+"/WHImported_temp", 2)
            else:
                client.subscribe("openWB/"+topic+"/WHExport_temp", 2)
        except Exception:
            log.MainLogger().exception("Fehler in der Restore-Klasse")

    def __on_message(self, client, userdata, msg):
        """ wartet auf eingehende Topics.
        """
        self.temp = msg.payload

    def __getserial(self):
        """ Extract serial from cpuinfo file
        """
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line[0:6] == 'Serial':
                        return line[10:26]
                return "0000000000000000"
        except Exception:
            log.MainLogger().exception("Fehler in der Restore-Klasse")


class SimCount:
    def sim_count(
        self, power_present: float, topic: str = "", data: dict = {}, prefix: str = ""
    ) -> typing.Tuple[float, float]:
        """ emulate import export

        Parameters
        ----------
        power_present: aktuelle Leistung
        topic: str Topic, in welches veröffentlicht werden soll
        data: Komponenten-Daten
        Return
        ------
        imported: importierte Energie
        exported: exportierte Energie
        """
        try:
            timestamp_present = time.time()
            power_previous, counter_export_present, counter_import_present = 0, 0, 0
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
                log.MainLogger().debug(
                    "Fortsetzen der Simulation: Importzähler: " + str(counter_import_present)+"Ws, Export-Zähler: " +
                    str(counter_export_present) + "Ws"
                )
                start_new = False
            pub.Pub().pub(topic+"simulation/timestamp_present", "%22.6f" % timestamp_present)
            pub.Pub().pub(topic+"simulation/power_present", power_present)

            if start_new:
                log.MainLogger().debug("Neue Simulation")
                pub.Pub().pub(topic+"simulation/present_imported", 0)
                pub.Pub().pub(topic+"simulation/present_exported", 0)
                return 0, 0
            else:
                # timestamp_previous = timestamp_previous + 1  # do not increment time if calculating areas!
                seconds_since_previous = timestamp_present - timestamp_previous
                imp_exp = calculate_import_export(seconds_since_previous, power_previous, power_present)
                counter_export_present = counter_export_present + imp_exp[1]
                counter_import_present = counter_import_present + imp_exp[0]
                log.MainLogger().debug(
                    "simcount aufsummierte Energie: Bezug[Ws]: " + str(counter_import_present) +
                    ", Einspeisung[Ws]: " +
                    str(counter_export_present)
                )
                energy_positive_kWh = counter_import_present / 3600
                energy_negative_kWh = counter_export_present / 3600
                log.MainLogger().info(
                    "simcount Ergebnis: Bezug[Wh]: " + str(energy_positive_kWh) +
                    ", Einspeisung[Wh]: " + str(energy_negative_kWh)
                )
                log.MainLogger().debug(
                    "simcount Zwischenergebnisse aktuelle Berechnung: Import: " + str(counter_import_present) +
                    " Export: " + str(counter_export_present) + " Power: " + str(power_present)
                )
                pub.Pub().pub(topic+"simulation/present_imported", counter_import_present)
                pub.Pub().pub(topic+"simulation/present_exported", counter_export_present)
                return energy_positive_kWh, energy_negative_kWh
        except Exception as e:
            process_error(e)


Number = typing.Union[int, float]


def calculate_import_export(
    seconds_since_previous: Number, power1: Number, power2: Number
) -> typing.Tuple[Number, Number]:
    try:
        log.MainLogger().debug(
            "simcount Berechnungsgrundlage: vergangene Zeit [s]" + str(seconds_since_previous) +
            ", vorherige Leistung[W]: " + str(power1) + ", aktuelle Leistung[W]: " + str(power2)
        )
        power_low = min(power1, power2)
        power_high = max(power1, power2)
        gradient = (power_high - power_low) / seconds_since_previous
        # Berechnung der Gesamtfläche (ohne Beträge, Fläche unterhalb der x-Achse reduziert die Fläche oberhalb der
        # x-Achse)
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
    except Exception as e:
        process_error(e)


def run_cli(power_present: int, prefix: str):
    SimCountLegacy().sim_count(power_present=power_present, prefix=prefix)


if __name__ == "__main__":
    try:
        run_using_positional_cli_args(run_cli)
    except Exception as e:
        process_error(e)
