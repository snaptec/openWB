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
    from modules.openwb_flex.counter import EvuKitFlex

def get_default() -> dict:
    return {
            "name": "EVU-Kit",
            "type": "counter",
            "id": None,
            "configuration":
            {
                "version": 2
            }
        }

class EvuKit(EvuKitFlex):
    def __init__(self, device_id: int, component_config: dict, tcp_client) -> None:
        try:
            self.data = {}
            self.data["config"] = component_config
            version = self.data["config"]["configuration"]["version"]
            if version == 0:
                id = 5
            elif version == 1:
                id = 0x02
            elif version == 2:
                id = 115
            self.data["config"]["configuration"]["id"] = id

            super().__init__(device_id, self.data["config"], tcp_client)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["components"]["component0"]["name"])
