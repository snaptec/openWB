#!/usr/bin/env python3
import sys


try:
    from ...helpermodules import log
    from ..openwb_flex.evu_kit import EvuKitFlex
except:
    from pathlib import Path
    import os
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from modules.openwb_flex.evu_kit import EvuKitFlex


class EvuKit(EvuKitFlex):
    def __init__(self, device_config: dict) -> None:
        try:
            self.data = {}
            self.data["config"] = device_config
            version = self.data["config"]["components"]["component0"]["configuration"]["version"]
            if version == 0:
                ip_address = "192.168.193.15"
                id = 5
            elif version == 1:
                ip_address = "192.168.193.15"
                id = 0x02
            elif version == 2:
                ip_address = "192.168.193.15"
                id = 115
            self.data["config"]["configuration"] = {}
            self.data["config"]["configuration"]["ip_address"] = ip_address
            self.data["config"]["configuration"]["port"] = 8899
            self.data["config"]["components"]["component0"]["configuration"]["id"] = id
            self.data["config"]["components"]["component0"]["name"] = "EVU-Kit0"

            super().__init__(self.data["config"])
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.data["config"]["components"]["component0"]["name"], e)
