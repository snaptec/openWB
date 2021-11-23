from abc import abstractmethod

try:
    from ...helpermodules import log
    from ..common import modbus
    from ..common.module_error import ModuleError
except (ImportError, ValueError):
    from helpermodules import log
    from modules.common import modbus
    from modules.common.module_error import ModuleError


class AbstractDevice:
    COMPONENT_TYPE_TO_CLASS = {
    }

    def __init__(self, device: dict, client: modbus.ModbusClient) -> None:
        try:
            self.data = {"config": device,
                         "components": {}}
            self.client = client
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+device["name"])

    def instantiate_component(self, component_config: dict, factory) -> None:
        try:
            self.data["components"]["component"+str(component_config["id"])] = factory(
                self.data["config"]["id"], component_config, self.client
            )
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    def component_factory(self, component_type: str):
        try:
            if component_type in self.COMPONENT_TYPE_TO_CLASS:
                return self.COMPONENT_TYPE_TO_CLASS[component_type]
            raise Exception("illegal component type "+component_type+". Allowed values: "+','.join(
                self.COMPONENT_TYPE_TO_CLASS.keys()
            ))
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    @abstractmethod
    def add_component(self, component_config: dict) -> None:
        pass

    def update_values(self):
        try:
            log.MainLogger().debug("Start device reading"+str(self.data["components"]))
            if self.data["components"]:
                for component in self.data["components"]:
                    self.data["components"][component].update_values()
            else:
                log.MainLogger().warning(
                    self.data["config"]["name"] +
                    ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
                )
        except ModuleError:
            log.MainLogger().error(
                "Beim Auslesen eines Moduls ist ein Fehler aufgetreten. Auslesen des Devices %s beendet." %
                self.data["config"]["name"]
            )
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])
