#!/usr/bin/env python3


try:
    from ...helpermodules import log
    from ..common import modbus
    from ..common.module_error import ModuleError, ModuleErrorLevel
    from ..openwb_flex.counter import EvuKitFlex
except (ImportError, ValueError):
    from helpermodules import log
    from modules.common import modbus
    from modules.common.module_error import ModuleError, ModuleErrorLevel
    from modules.openwb_flex.counter import EvuKitFlex


def get_default_config() -> dict:
    return {
        "name": "EVU-Kit",
        "type": "counter",
        "id": 0,
        "configuration":
            {
                "version": 2
            }
    }


class EvuKit(EvuKitFlex):
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        try:
            self.data = {"config": component_config}
            version = self.data["config"]["configuration"]["version"]
            if version == 0:
                id = 5
            elif version == 1:
                id = 0x02
            elif version == 2:
                id = 115
            else:
                raise ModuleError("Version "+str(version) +
                                  " unbekannt.", ModuleErrorLevel.ERROR)
            self.data["config"]["configuration"]["id"] = id

            super().__init__(device_id, self.data["config"], tcp_client)
        except Exception:
            log.MainLogger().exception("Fehler im Modul " +
                                       self.data["config"]["components"]["component0"]["name"])
