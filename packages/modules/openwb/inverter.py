#!/usr/bin/env python3
import sys

try:
    from ...helpermodules import log
    from ..common import connect_tcp
    from ..common.module_error import ModuleError, ModuleErrorLevels
    from ..openwb_flex.inverter import PvKitFlex
except:
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from helpermodules import log
    from modules.common import connect_tcp
    from modules.common.module_error import ModuleError, ModuleErrorLevels
    from modules.openwb_flex.inverter import PvKitFlex


def get_default_config() -> dict:
    return {
        "name": "PV-Kit",
        "type": "inverter",
        "id": 0,
        "configuration":
            {
                "version": 2
            }
    }


class PvKit(PvKitFlex):
    def __init__(self, device_id: int, component_config: dict, tcp_client: connect_tcp.ConnectTcp) -> None:
        try:
            self.data = {"config": component_config}
            version = self.data["config"]["configuration"]["version"]
            if version == 0:
                id = 8
            elif version == 1:
                id = 0x08
            elif version == 2:
                id = 116
            else:
                raise ModuleError("Version "+str(version)+" unbekannt.", ModuleErrorLevels.ERROR)
            self.data["config"]["configuration"]["id"] = id

            super().__init__(device_id, self.data["config"], tcp_client)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["components"]["component0"]["name"])
