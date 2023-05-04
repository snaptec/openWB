from helpermodules.scale_metric import scale_metric
from modules.devices.fems.config import FemsInverterSetup
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.common import req


class FemsInverter:
    def __init__(self, password: str, ip_address: str, component_config: FemsInverterSetup) -> None:
        self.password = password
        self.ip_address = ip_address
        self.component_config = component_config
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        response = req.get_http_session().get(
            'http://'+self.ip_address+':8084/rest/channel/_sum/ProductionActivePower',
            auth=("x", self.password)).json()
        power = scale_metric(response["value"], response.get("unit"), 'W') * -1

        response = req.get_http_session().get(
            'http://'+self.ip_address+':8084/rest/channel/_sum/ProductionActiveEnergy',
            auth=("x", self.password)).json()
        exported = scale_metric(response["value"], response.get("unit"), 'Wh')
        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=FemsInverterSetup)
