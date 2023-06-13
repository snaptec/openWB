from requests import Session
from helpermodules.scale_metric import scale_metric
from modules.devices.fems.config import FemsCounterSetup
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store


class FemsCounter:
    def __init__(self, ip_address: str, component_config: FemsCounterSetup) -> None:
        self.ip_address = ip_address
        self.component_config = component_config
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, session: Session) -> None:
        try:
            # Grid meter values
            response = session.get('http://' + self.ip_address +
                                   ':8084/rest/channel/meter0/(ActivePower.*|VoltageL.|Frequency)',
                                   timeout=1).json()

            # ATTENTION: Recent FEMS versions started using the "unit" field (see example response below) and
            #            kind-of arbitrarily return either Volts, Kilowatthours or Hz or Millivolts, Watthours or
            #            Millihertz
            #            Others units (kW, kV) have not yet been observed but are coded just to be future-proof.
            powers, voltages = [0]*3, [0]*3
            for singleValue in response:
                address = singleValue['address']
                if (address == 'meter0/Frequency'):
                    frequency = scale_metric(singleValue['value'], singleValue.get('unit'), 'Hz')
                elif (address == 'meter0/ActivePower'):
                    power = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
                elif (address == 'meter0/ActivePowerL1'):
                    powers[0] = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
                elif (address == 'meter0/ActivePowerL2'):
                    powers[1] = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
                elif (address == 'meter0/ActivePowerL3'):
                    powers[2] = scale_metric(singleValue['value'], singleValue.get('unit'), 'W')
                elif (address == 'meter0/VoltageL1'):
                    voltages[0] = scale_metric(singleValue['value'], singleValue.get('unit'), 'V')
                elif (address == 'meter0/VoltageL2'):
                    voltages[1] = scale_metric(singleValue['value'], singleValue.get('unit'), 'V')
                elif (address == 'meter0/VoltageL3'):
                    voltages[2] = scale_metric(singleValue['value'], singleValue.get('unit'), 'V')

            # Grid total energy sums
            response = session.get(
                'http://'+self.ip_address+':8084/rest/channel/_sum/Grid.+ActiveEnergy',
                timeout=1).json()

            for singleValue in response:
                address = singleValue['address']
                if (address == '_sum/GridBuyActiveEnergy'):
                    imported = scale_metric(singleValue['value'], singleValue.get('unit'), 'Wh')
                elif (address == '_sum/GridSellActiveEnergy'):
                    exported = scale_metric(singleValue['value'], singleValue.get('unit'), 'Wh')
            counter_state = CounterState(
                imported=imported,
                exported=exported,
                power=power,
                powers=powers,
                voltages=voltages,
                frequency=frequency
            )
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            # nicht alle FEMS-Module unterstützen Regex-Requests
            def get_value(url):
                response = session.get('http://x:'+self.password+'@'+self.ip_address +
                                       ':8084/rest/channel/'+url, timeout=2).json()
                return response["value"]

            power = get_value('meter0/ActivePower')
            imported = get_value('_sum/GridBuyActiveEnergy')
            exported = get_value('_sum/GridSellActiveEnergy')
            voltages = [get_value('meter0/VoltageL1'), get_value('meter0/VoltageL2'), get_value('meter0/VoltageL3')]
            currents = [get_value('meter0/CurrentL1'), get_value('meter0/CurrentL2'), get_value('meter0/CurrentL3')]
            powers = [get_value('meter0/ActivePowerL1'), get_value('meter0/ActivePowerL2'),
                      get_value('meter0/ActivePowerL3')]

            counter_state = CounterState(
                imported=imported,
                exported=exported,
                power=power,
                powers=powers,
                voltages=voltages,
                currents=currents
            )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=FemsCounterSetup)
