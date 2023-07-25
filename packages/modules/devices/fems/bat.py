from requests import Session
from helpermodules.scale_metric import scale_metric
from modules.devices.fems.config import FemsBatSetup
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store


class FemsBat:
    def __init__(self, ip_address: str, component_config: FemsBatSetup) -> None:
        self.ip_address = ip_address
        self.component_config = component_config
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, session: Session) -> None:
        if self.component_config.configuration.num == 1:
            data = "ess0"
        else:
            data = "ess2"
        response = session.get(
            "http://" + self.ip_address + ":8084/rest/channel/"+data+"/(Soc|DcChargeEnergy|DcDischargeEnergy)",
            timeout=2).json()
        for singleValue in response:
            address = singleValue["address"]
            if (address == data+"/Soc"):
                soc = singleValue["value"]
            elif address == data+"/DcChargeEnergy":
                imported = scale_metric(singleValue['value'], singleValue.get('unit'), 'Wh')
            elif address == data+"/DcDischargeEnergy":
                exported = scale_metric(singleValue['value'], singleValue.get('unit'), 'Wh')

        response = session.get(
            "http://" + self.ip_address +
            ":8084/rest/channel/_sum/(GridActivePower|ProductionActivePower|ConsumptionActivePower)",
            timeout=2).json()
        for singleValue in response:
            address = singleValue["address"]
            if (address == "_sum/GridActivePower"):
                grid = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
            elif address == "_sum/ProductionActivePower":
                pv = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
            elif address == "_sum/ConsumptionActivePower":
                haus = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')

        # keine Berechnung im Gerät, da grid nicht der Leistung aus der Zählerkomponente entspricht.
        power = grid + pv - haus

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=FemsBatSetup)
