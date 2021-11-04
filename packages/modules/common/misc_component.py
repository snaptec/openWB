from abc import abstractmethod
from typing import Union
try:
    from ...helpermodules import log
    from ..common import connect_tcp
    from ..common import lovato
    from ..common import mpm3pm
    from ..common import simcount
    from ..common import sdm630
    from ..common import store
    from ..common.module_error import ModuleError, ModuleErrorLevels
except:
    from pathlib import Path
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from modules.common import connect_tcp
    from modules.common import lovato
    from modules.common import mpm3pm
    from modules.common import simcount
    from modules.common import sdm630
    from modules.common import store
    from modules.common.module_error import ModuleError, ModuleErrorLevels


class MiscComponent():
    def __init__(self, device_id: int, component_config: dict, client: Union[connect_tcp.ConnectTcp, mpm3pm.Mpm3pm, lovato.Lovato, sdm630.Sdm630]) -> None:
        try:
            self.device_id = device_id
            self.client = client
            self.data = {}
            self.data["config"] = component_config
            self.data["simulation"] = {}
            self.value_store = (store.ValueStoreFactory().get_storage(component_config["type"]))(self.data["config"]["id"])
            simcount_factory = simcount.SimCountFactory().get_sim_counter()
            self.sim_count = simcount_factory()
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    @abstractmethod
    def update_values(self):
        pass

    def process_error(self, e):
        ModuleError(str(type(e))+" "+str(e), ModuleErrorLevels.ERROR).store_error(self.data["config"]["id"], "counter", self.data["config"]["name"])

    def kit_version_factory(self, version: int, id: int, tcp_client: connect_tcp.ConnectTcp) -> Union[mpm3pm.Mpm3pm, lovato.Lovato, sdm630.Sdm630]:
        try:
            if version == 0:
                return mpm3pm.Mpm3pm(id, tcp_client)
            elif version == 1:
                return lovato.Lovato(id, tcp_client)
            elif version == 2:
                return sdm630.Sdm630(id, tcp_client)
        except Exception as e:
            self.process_error(e)
