from abc import abstractmethod
from typing import Union
try:
    from ...helpermodules import log
    from ..common import modbus
    from ..common import lovato
    from ..common import mpm3pm
    from ..common import simcount
    from ..common import sdm630
    from ..common import store
    from ..common.module_error import ModuleError, ModuleErrorLevel
    from component_state import BatState, CounterState, InverterState
except (ImportError, ValueError):
    from helpermodules import log
    from modules.common import modbus
    from modules.common import lovato
    from modules.common import mpm3pm
    from modules.common import simcount
    from modules.common import sdm630
    from modules.common import store
    from modules.common.module_error import ModuleError, ModuleErrorLevel
    from .component_state import BatState, CounterState, InverterState


class AbstractComponent:
    def __init__(
        self,
        device_id: int,
        component_config: dict,
        client: Union[modbus.ModbusClient, mpm3pm.Mpm3pm, lovato.Lovato, sdm630.Sdm630]
    ) -> None:
        try:
            self.device_id = device_id
            self.client = client
            self.data = {"config": component_config,
                         "simulation": {}}
            self.value_store = (store.ValueStoreFactory().get_storage(component_config["type"]))(
                self.data["config"]["id"]
            )
            simcount_factory = simcount.SimCountFactory().get_sim_counter()
            self.sim_count = simcount_factory()
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    @abstractmethod
    def get_values(self) -> Union[BatState, CounterState, InverterState]:
        pass

    def update_values(self) -> Union[BatState, CounterState, InverterState]:
        try:
            state = self.get_values()
            self.value_store.set(state)
        except ModuleError as e:
            e.store_error(self.data["config"]["id"], self.data["config"]["type"], self.data["config"]["name"])
            raise ModuleError("", ModuleErrorLevel.ERROR)
        except Exception as e:
            self.process_error(e)
            raise ModuleError("", ModuleErrorLevel.ERROR)
        else:
            ModuleError("Kein Fehler.", ModuleErrorLevel.NO_ERROR).store_error(
                self.data["config"]["id"], self.data["config"]["type"], self.data["config"]["name"]
            )
            return state

    def process_error(self, e):
        ModuleError(str(type(e))+" "+str(e), ModuleErrorLevel.ERROR).store_error(
            self.data["config"]["id"], self.data["config"]["type"], self.data["config"]["name"]
        )

    def kit_version_factory(self, version: int, id: int, tcp_client: modbus.ModbusClient) -> Union[
        mpm3pm.Mpm3pm, lovato.Lovato, sdm630.Sdm630
    ]:
        try:
            if version == 0:
                return mpm3pm.Mpm3pm(id, tcp_client)
            elif version == 1:
                return lovato.Lovato(id, tcp_client)
            elif version == 2:
                return sdm630.Sdm630(id, tcp_client)
            else:
                raise ModuleError("Version "+str(version)+" unbekannt.", ModuleErrorLevel.ERROR)
        except Exception as e:
            self.process_error(e)


class AbstractBat(AbstractComponent):
    def __init__(self,
                 device_id: int,
                 component_config: dict,
                 client: Union[modbus.ModbusClient, mpm3pm.Mpm3pm, lovato.Lovato, sdm630.Sdm630]) -> None:
        super().__init__(device_id, component_config, client)

    @abstractmethod
    def get_values(self) -> BatState:
        pass

    def update_values(self) -> BatState:
        return super().update_values()


class AbstractCounter(AbstractComponent):
    def __init__(self,
                 device_id: int,
                 component_config: dict,
                 client: Union[modbus.ModbusClient, mpm3pm.Mpm3pm, lovato.Lovato, sdm630.Sdm630]) -> None:
        super().__init__(device_id, component_config, client)

    @abstractmethod
    def get_values(self) -> CounterState:
        pass

    def update_values(self) -> CounterState:
        return super().update_values()


class AbstractInverter(AbstractComponent):
    def __init__(self,
                 device_id: int,
                 component_config: dict,
                 client: Union[modbus.ModbusClient, mpm3pm.Mpm3pm, lovato.Lovato, sdm630.Sdm630]) -> None:
        super().__init__(device_id, component_config, client)

    @abstractmethod
    def get_values(self) -> InverterState:
        pass

    def update_values(self) -> InverterState:
        return super().update_values()
