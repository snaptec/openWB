from abc import abstractmethod

try:
    from ...helpermodules import log
    from ..common.module_error import ModuleError
except (ImportError, ValueError, SystemError):
    from helpermodules import log
    from modules.common.module_error import ModuleError


class AbstractDevice:
    @abstractmethod
    def __init__(self, device_config: dict) -> None:
        pass

    @abstractmethod
    def add_component(self, component_config: dict) -> None:
        pass


class DeviceUpdater:
    def __init__(self, device) -> None:
        self.device = device

    def get_values(self):
        try:
            self.device.get_values()
        except ModuleError:
            log.MainLogger().exception(
                "Beim Auslesen eines Moduls ist ein Fehler aufgetreten. Auslesen des Devices "
                + self.device.device_config["name"] + " beendet.")
        except Exception:
            log.MainLogger().exception("Fehler im Modul " + self.device.device_config["name"])
