#!/usr/bin/env python3
import sys


try:
    from ...helpermodules import log
    from ..openwb_flex.counter import EvuKitFlex
except:
    from pathlib import Path
    import os
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from modules.openwb_flex.inverter import PvKitFlex


def get_default_config() -> dict:
    return {
        "name": "PV-Kit",
        "type": "inverter",
        "id": None,
        "configuration":
            {
                "version": 2
            }
    }


class PvKit(PvKitFlex):
    def __init__(self, device_id: int, component_config: dict, tcp_client) -> None:
        try:
            self.data = {}
            self.data["config"] = component_config
            version = self.data["config"]["configuration"]["version"]
            if version == 0:
                id = 8
            elif version == 1:
                id = 0x08
            elif version == 2:
                id = 116
            self.data["config"]["configuration"]["id"] = id

            super().__init__(device_id, self.data["config"], tcp_client)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["components"]["component0"]["name"])
