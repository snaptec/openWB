# Utilities for integration with Home Assistant
# Thanks to molobrakos

import logging
from skodaconnect.utilities import camel2slug

_LOGGER = logging.getLogger(__name__)

class Instrument:
    def __init__(self, component, attr, name, icon=None):
        self.attr = attr
        self.component = component
        self.name = name
        self.vehicle = None
        self.icon = icon
        self.callback = None

    def __repr__(self):
        return self.full_name

    def configurate(self, **args):
        pass

    @property
    def slug_attr(self):
        return camel2slug(self.attr.replace(".", "_"))

    def setup(self, vehicle, **config):
        self.vehicle = vehicle
        if not self.is_supported:
            _LOGGER.debug("%s (%s:%s) is not supported", self, type(self).__name__, self.attr)
            return False

        _LOGGER.debug("%s is supported", self)
        self.configurate(**config)
        return True

    @property
    def vehicle_name(self):
        return self.vehicle.vin

    @property
    def full_name(self):
        return "%s %s" % (self.vehicle_name, self.name)

    @property
    def is_mutable(self):
        raise NotImplementedError("Must be set")

    @property
    def str_state(self):
        return self.state

    @property
    def state(self):
        if hasattr(self.vehicle, self.attr):
            return getattr(self.vehicle, self.attr)
        else:
            _LOGGER.debug(f'Could not find attribute "{self.attr}"')
        return self.vehicle.get_attr(self.attr)

    @property
    def attributes(self):
        return {}

    @property
    def is_supported(self):
        supported = 'is_' + self.attr + "_supported"
        if hasattr(self.vehicle, supported):
            return getattr(self.vehicle, supported)
        else:
            return False


class Sensor(Instrument):
    def __init__(self, attr, name, icon, unit):
        super().__init__(component="sensor", attr=attr, name=name, icon=icon)
        self.unit = unit
        self.convert = False

    def configurate(self, miles=False, **config):
        if self.unit and miles:
            if "km" == self.unit:
                self.unit = "mi"
                self.convert = True
            elif "km/h" == self.unit:
                self.unit = "mi/h"
                self.convert = True
            elif "l/100 km" == self.unit:
                self.unit = "l/100 mi"
                self.convert = True
            elif "kWh/100 km" == self.unit:
                self.unit = "kWh/100 mi"
                self.convert = True

        # Init placeholder for parking heater duration
        config.get('parkingheater', 30)
        if "pheater_duration" == self.attr:
            setValue = config.get('climatisation_duration', 30)
            self.vehicle.pheater_duration = setValue

    @property
    def is_mutable(self):
        return False

    @property
    def str_state(self):
        if self.unit:
            return f'{self.state} {self.unit}'
        else:
            return f'{self.state}'

    @property
    def state(self):
        val = super().state
        if val and self.unit and "mi" in self.unit and self.convert is True:
            return int(round(val / 1.609344))
        elif val and self.unit and "mi/h" in self.unit and self.convert is True:
            return int(round(val / 1.609344))
        elif val and self.unit and "gal/100 mi" in self.unit and self.convert is True:
            return round(val * 0.4251438, 1)
        elif val and self.unit and "kWh/100 mi" in self.unit and self.convert is True:
            return round(val * 0.4251438, 1)
        elif val and self.unit and "°F" in self.unit and self.convert is True:
            temp = round((val * 9 / 5) + 32, 1)
            return temp
        else:
            return val


class BinarySensor(Instrument):
    def __init__(self, attr, name, device_class, icon='', reverse_state=False):
        super().__init__(component="binary_sensor", attr=attr, name=name, icon=icon)
        self.device_class = device_class
        self.reverse_state = reverse_state

    @property
    def is_mutable(self):
        return False

    @property
    def str_state(self):
        if self.device_class in ["door", "window"]:
            return "Closed" if self.state else "Open"
        if self.device_class == "lock":
            return "Locked" if self.state else "Unlocked"
        if self.device_class == "safety":
            return "Warning!" if self.state else "OK"
        if self.device_class == "plug":
            return "Connected" if self.state else "Disconnected"
        if self.state is None:
            _LOGGER.error("Can not encode state %s:%s", self.attr, self.state)
            return "?"
        return "On" if self.state else "Off"

    @property
    def state(self):
        val = super().state

        if isinstance(val, (bool, list)):
            if self.reverse_state:
                if bool(val):
                    return False
                else:
                    return True
            else:
                return bool(val)
        elif isinstance(val, str):
            return val != "Normal"
        return val

    @property
    def is_on(self):
        return self.state


class Switch(Instrument):
    def __init__(self, attr, name, icon):
        super().__init__(component="switch", attr=attr, name=name, icon=icon)

    @property
    def is_mutable(self):
        return True

    @property
    def str_state(self):
        return "On" if self.state else "Off"

    def is_on(self):
        return self.state

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    @property
    def assumed_state(self):
        return True


class Climate(Instrument):
    def __init__(self, attr, name, icon):
        super().__init__(component="climate", attr=attr, name=name, icon=icon)

    @property
    def hvac_mode(self):
        pass

    @property
    def target_temperature(self):
        pass

    def set_temperature(self, **kwargs):
        pass

    def set_hvac_mode(self, hvac_mode):
        pass


class ElectricClimatisationClimate(Climate):
    def __init__(self):
        super().__init__(attr="electric_climatisation", name="Electric Climatisation", icon="mdi:radiator")

    @property
    def hvac_mode(self):
        return self.vehicle.electric_climatisation

    @property
    def target_temperature(self):
        return self.vehicle.climatisation_target_temperature

    async def set_temperature(self, temperature):
        await self.vehicle.climatisation_target(temperature)

    async def set_hvac_mode(self, hvac_mode):
        if hvac_mode:
            await self.vehicle.climatisation('electric')
        else:
            await self.vehicle.climatisation('off')


class CombustionClimatisationClimate(Climate):
    def __init__(self):
        super().__init__(attr="pheater_heating", name="Parking Heater Climatisation", icon="mdi:radiator")

    def configurate(self, **config):
        self.spin = config.get('spin', '')
        self.duration = config.get('combustionengineheatingduration', 30)

    @property
    def hvac_mode(self):
        return self.vehicle.pheater_heating

    @property
    def target_temperature(self):
        return self.vehicle.climatisation_target_temperature

    async def set_temperature(self, temperature):
        await self.vehicle.setClimatisationTargetTemperature(temperature)

    async def set_hvac_mode(self, hvac_mode):
        if hvac_mode:
            await self.vehicle.pheater_climatisation(spin=self.spin, duration=self.duration, mode='heating')
        else:
            await self.vehicle.pheater_climatisation(spin=self.spin, mode='off')


class Position(Instrument):
    def __init__(self):
        super().__init__(component="device_tracker", attr="position", name="Position")

    @property
    def is_mutable(self):
        return False

    @property
    def state(self):
        state = super().state #or {}
        return (
            state.get("lat", "?"),
            state.get("lng", "?"),
            state.get("timestamp", None),
        )

    @property
    def str_state(self):
        state = super().state #or {}
        ts = state.get("timestamp", None)
        return (
            state.get("lat", "?"),
            state.get("lng", "?"),
            str(ts.astimezone(tz=None)) if ts else None,
        )


class DoorLock(Instrument):
    def __init__(self):
        super().__init__(component="lock", attr="door_locked", name="Door locked")

    def configurate(self, **config):
        self.spin = config.get('spin', '')

    @property
    def is_mutable(self):
        return True

    @property
    def str_state(self):
        return "Locked" if self.state else "Unlocked"

    @property
    def state(self):
        return self.vehicle.door_locked

    @property
    def is_locked(self):
        return self.state

    async def lock(self):
        try:
            response = await self.vehicle.set_lock('lock', self.spin)
            await self.vehicle.update()
            if self.callback is not None:
                self.callback()
            return response
        except Exception as e:
            _LOGGER.error("Lock failed: %", e.args[0])
            return False

    async def unlock(self):
        try:
            response = await self.vehicle.set_lock('unlock', self.spin)
            await self.vehicle.update()
            if self.callback is not None:
                self.callback()
            return response
        except Exception as e:
            _LOGGER.error("Unlock failed: %", e.args[0])
            return False

    @property
    def attributes(self):
        return dict(last_result = self.vehicle.lock_action_status)


class TrunkLock(Instrument):
    def __init__(self):
        super().__init__(component="lock", attr="trunk_locked", name="Trunk locked")

    @property
    def is_mutable(self):
        return True

    @property
    def str_state(self):
        return "Locked" if self.state else "Unlocked"

    @property
    def state(self):
        return self.vehicle.trunk_locked

    @property
    def is_locked(self):
        return self.state

    async def lock(self):
        return None

    async def unlock(self):
        return None

# Switches

class RequestUpdate(Switch):
    def __init__(self):
        super().__init__(attr="refresh_data", name="Force data refresh", icon="mdi:car-connected")

    @property
    def state(self):
        return self.vehicle.refresh_data

    async def turn_on(self):
        await self.vehicle.set_refresh()
        await self.vehicle.update()
        if self.callback is not None:
            self.callback()

    async def turn_off(self):
        pass

    @property
    def assumed_state(self):
        return False

    @property
    def attributes(self):
        return dict(last_result = self.vehicle.refresh_action_status)


class ElectricClimatisation(Switch):
    def __init__(self):
        super().__init__(attr="electric_climatisation", name="Electric Climatisation", icon="mdi:radiator")

    @property
    def state(self):
        return self.vehicle.electric_climatisation

    async def turn_on(self):
        await self.vehicle.set_climatisation('electric')
        await self.vehicle.update()

    async def turn_off(self):
        await self.vehicle.set_climatisation('off')
        await self.vehicle.update()

    @property
    def assumed_state(self):
        return False

    @property
    def attributes(self):
        return dict(last_result = self.vehicle.climater_action_status)


class AuxiliaryClimatisation(Switch):
    def __init__(self):
        super().__init__(attr="auxiliary_climatisation", name="Auxiliary Climatisation", icon="mdi:radiator")

    def configurate(self, **config):
        self.spin = config.get('spin', '')

    @property
    def state(self):
        return self.vehicle.auxiliary_climatisation

    async def turn_on(self):
        await self.vehicle.set_climatisation('auxiliary', self.spin)
        await self.vehicle.update()

    async def turn_off(self):
        await self.vehicle.set_climatisation('off')
        await self.vehicle.update()

    @property
    def assumed_state(self):
        return False

    @property
    def attributes(self):
        return dict(last_result = self.vehicle.climater_action_status)


class Charging(Switch):
    def __init__(self):
        super().__init__(attr="charging", name="Charging", icon="mdi:battery")

    @property
    def state(self):
        return self.vehicle.charging

    async def turn_on(self):
        await self.vehicle.set_charger('start')
        await self.vehicle.update()

    async def turn_off(self):
        await self.vehicle.set_charger('stop')
        await self.vehicle.update()

    @property
    def assumed_state(self):
        return False

    @property
    def attributes(self):
        return dict(last_result = self.vehicle.charger_action_status)


class WindowHeater(Switch):
    def __init__(self):
        super().__init__(attr="window_heater", name="Window Heater", icon="mdi:car-defrost-rear")

    @property
    def state(self):
        return self.vehicle.window_heater

    async def turn_on(self):
        await self.vehicle.set_window_heating('start')
        await self.vehicle.update()

    async def turn_off(self):
        await self.vehicle.set_window_heating('stop')
        await self.vehicle.update()

    @property
    def assumed_state(self):
        return False

    @property
    def attributes(self):
        return dict(last_result = self.vehicle.climater_action_status)


class BatteryClimatisation(Switch):
    def __init__(self):
        super().__init__(attr="climatisation_without_external_power", name="Climatisation from battery", icon="mdi:power-plug")

    @property
    def state(self):
        return self.vehicle.climatisation_without_external_power

    async def turn_on(self):
        await self.vehicle.set_battery_climatisation(True)
        await self.vehicle.update()

    async def turn_off(self):
        await self.vehicle.set_battery_climatisation(False)
        await self.vehicle.update()

    @property
    def assumed_state(self):
        return False

    @property
    def attributes(self):
        return dict(last_result = self.vehicle.climater_action_status)


class PHeaterHeating(Switch):
    def __init__(self):
        super().__init__(attr="pheater_heating", name="Parking Heater Heating", icon="mdi:radiator")

    def configurate(self, **config):
        self.spin = config.get('spin', '')
        self.duration = config.get('combustionengineheatingduration', 30)

    @property
    def state(self):
        return self.vehicle.pheater_heating

    async def turn_on(self):
        await self.vehicle.set_pheater(mode='heating', spin=self.spin)
        await self.vehicle.update()

    async def turn_off(self):
        await self.vehicle.set_pheater(mode='off', spin=self.spin)
        await self.vehicle.update()

    @property
    def assumed_state(self):
        return False

    @property
    def attributes(self):
        return dict(last_result = self.vehicle.pheater_action_status)


class PHeaterVentilation(Switch):
    def __init__(self):
        super().__init__(attr="pheater_ventilation", name="Parking Heater Ventilation", icon="mdi:radiator")

    def configurate(self, **config):
        self.spin = config.get('spin', '')
        self.duration = config.get('combustionengineclimatisationduration', 30)

    @property
    def state(self):
        return self.vehicle.pheater_ventilation

    async def turn_on(self):
        await self.vehicle.set_pheater(mode='ventilation', spin=self.spin)
        await self.vehicle.update()

    async def turn_off(self):
        await self.vehicle.set_pheater(mode='off', spin=self.spin)
        await self.vehicle.update()

    @property
    def assumed_state(self):
        return False

    @property
    def attributes(self):
        return dict(last_result = self.vehicle.pheater_action_status)


class DepartureTimer1(Switch):
    def __init__(self):
        super().__init__(attr="departure1", name="Departure timer 1", icon="mdi:radiator")

    def configurate(self, **config):
        self.spin = config.get('spin', '')

    @property
    def state(self):
        status = self.vehicle.departure1.get("timerProgrammedStatus", "")
        if status == "programmed":
            return True
        else:
            return False

    async def turn_on(self):
        await self.vehicle.set_timer_active(id=1, action="on")
        await self.vehicle.update()

    async def turn_off(self):
        await self.vehicle.set_timer_active(id=1, action="off")
        await self.vehicle.update()

    @property
    def assumed_state(self):
        return False

    @property
    def attributes(self):
        return dict(self.vehicle.departure1)


class DepartureTimer2(Switch):
    def __init__(self):
        super().__init__(attr="departure2", name="Departure timer 2", icon="mdi:radiator")

    def configurate(self, **config):
        self.spin = config.get('spin', '')

    @property
    def state(self):
        status = self.vehicle.departure2.get("timerProgrammedStatus", "")
        if status == "programmed":
            return True
        else:
            return False

    async def turn_on(self):
        await self.vehicle.set_timer_active(id=2, action="on")
        await self.vehicle.update()

    async def turn_off(self):
        await self.vehicle.set_timer_active(id=2, action="off")
        await self.vehicle.update()

    @property
    def assumed_state(self):
        return False

    @property
    def attributes(self):
        return dict(self.vehicle.departure2)

class DepartureTimer3(Switch):
    def __init__(self):
        super().__init__(attr="departure3", name="Departure timer 3", icon="mdi:radiator")

    def configurate(self, **config):
        self.spin = config.get('spin', '')

    @property
    def state(self):
        status = self.vehicle.departure3.get("timerProgrammedStatus", "")
        if status == "programmed":
            return True
        else:
            return False

    async def turn_on(self):
        await self.vehicle.set_timer_active(id=3, action="on")
        await self.vehicle.update()

    async def turn_off(self):
        await self.vehicle.set_timer_active(id=3, action="off")
        await self.vehicle.update()

    @property
    def assumed_state(self):
        return False

    @property
    def attributes(self):
        return dict(self.vehicle.departure3)


class RequestResults(Sensor):
    def __init__(self):
        super().__init__(attr="request_results", name="Request results", icon="mdi:chat-alert", unit="")

    @property
    def state(self):
        if self.vehicle.request_results.get('state', False):
            return self.vehicle.request_results.get('state')
        return 'Unknown'

    @property
    def assumed_state(self):
        return False

    @property
    def attributes(self):
        return dict(self.vehicle.request_results)


def create_instruments():
    return [
        Position(),
        DoorLock(),
        TrunkLock(),
        RequestUpdate(),
        WindowHeater(),
        BatteryClimatisation(),
        ElectricClimatisation(),
        AuxiliaryClimatisation(),
        PHeaterVentilation(),
        PHeaterHeating(),
        #ElectricClimatisationClimate(),
        #CombustionClimatisationClimate(),
        Charging(),
        RequestResults(),
        DepartureTimer1(),
        DepartureTimer2(),
        DepartureTimer3(),
        Sensor(
            attr="distance",
            name="Odometer",
            icon="mdi:speedometer",
            unit="km",
        ),
        Sensor(
            attr="battery_level",
            name="Battery level",
            icon="mdi:battery",
            unit="%",
        ),
        Sensor(
            attr="adblue_level",
            name="Adblue level",
            icon="mdi:fuel",
            unit="km",
        ),
        Sensor(
            attr="fuel_level",
            name="Fuel level",
            icon="mdi:fuel",
            unit="%",
        ),
        Sensor(
            attr="service_inspection",
            name="Service inspection days",
            icon="mdi:garage",
            unit="days",
        ),
        Sensor(
            attr="service_inspection_distance",
            name="Service inspection distance",
            icon="mdi:garage",
            unit="km",
        ),
        Sensor(
            attr="oil_inspection",
            name="Oil inspection days",
            icon="mdi:oil",
            unit="days",
        ),
        Sensor(
            attr="oil_inspection_distance",
            name="Oil inspection distance",
            icon="mdi:oil",
            unit="km",
        ),
        Sensor(
            attr="last_connected",
            name="Last connected",
            icon="mdi:clock",
            unit="",
        ),
        Sensor(
            attr="parking_time",
            name="Parking time",
            icon="mdi:clock",
            unit="",
        ),
        Sensor(
            attr="charging_time_left",
            name="Charging time left",
            icon="mdi:battery-charging-100",
            unit="h",
        ),
        Sensor(
            attr="electric_range",
            name="Electric range",
            icon="mdi:car-electric",
            unit="km",
        ),
        Sensor(
            attr="combustion_range",
            name="Combustion range",
            icon="mdi:car",
            unit="km",
        ),
        Sensor(
            attr="combined_range",
            name="Combined range",
            icon="mdi:car",
            unit="km",
        ),
        Sensor(
            attr="charge_max_ampere",
            name="Charger max ampere",
            icon="mdi:flash",
            unit="A",
        ),
        Sensor(
            attr="climatisation_target_temperature",
            name="Climatisation target temperature",
            icon="mdi:thermometer",
            unit="°C",
        ),
        Sensor(
            attr="trip_last_average_speed",
            name="Last trip average speed",
            icon="mdi:speedometer",
            unit="km/h",
        ),
        Sensor(
            attr="trip_last_average_electric_consumption",
            name="Last trip average electric consumption",
            icon="mdi:car-battery",
            unit="kWh/100 km",
        ),
        Sensor(
            attr="trip_last_average_fuel_consumption",
            name="Last trip average fuel consumption",
            icon="mdi:fuel",
            unit="l/100 km",
        ),
        Sensor(
            attr="trip_last_duration",
            name="Last trip duration",
            icon="mdi:clock",
            unit="min",
        ),
        Sensor(
            attr="trip_last_length",
            name="Last trip length",
            icon="mdi:map-marker-distance",
            unit="km",
        ),
        Sensor(
            attr="trip_last_recuperation",
            name="Last trip recuperation",
            icon="mdi:battery-plus",
            unit="kWh/100 km",
        ),
        Sensor(
            attr="trip_last_average_recuperation",
            name="Last trip average recuperation",
            icon="mdi:battery-plus",
            unit="kWh/100 km",
        ),
        Sensor(
            attr="trip_last_average_auxillary_consumption",
            name="Last trip average auxillary consumption",
            icon="mdi:flash",
            unit="kWh/100 km",
        ),
        Sensor(
            attr="trip_last_average_aux_consumer_consumption",
            name="Last trip average auxillary consumer consumption",
            icon="mdi:flash",
            unit="kWh/100 km",
        ),
        Sensor(
            attr="trip_last_total_electric_consumption",
            name="Last trip total electric consumption",
            icon="mdi:car-battery",
            unit="kWh/100 km",
        ),
        Sensor(
            attr="pheater_status",
            name="Parking Heater heating/ventilation status",
            icon="mdi:radiator",
            unit="",
        ),
        Sensor(
            attr="pheater_duration",
            name="Parking Heater heating/ventilation duration",
            icon="mdi:timer",
            unit="minutes",
        ),
        Sensor(
            attr="outside_temperature",
            name="Outside temperature",
            icon="mdi:thermometer",
            unit="°C",
        ),
        Sensor(
            attr="requests_remaining",
            name="Requests remaining",
            icon="mdi:chat-alert",
            unit="",
        ),
        BinarySensor(
            attr="external_power",
            name="External power",
            device_class="power"
        ),
        BinarySensor(
            attr="energy_flow",
            name="Energy flow",
            device_class="power"
        ),
        BinarySensor(
            attr="parking_light",
            name="Parking light",
            device_class="light",
            icon="mdi:car-parking-lights"
        ),
        BinarySensor(
            attr="door_locked",
            name="Doors locked",
            device_class="lock",
            reverse_state=False
        ),
        BinarySensor(
            attr="door_closed_left_front",
            name="Door closed left front",
            device_class="door",
            reverse_state=False,
            icon="mdi:car-door"
        ),
        BinarySensor(
            attr="door_closed_right_front",
            name="Door closed right front",
            device_class="door",
            reverse_state=False,
            icon="mdi:car-door"
        ),
        BinarySensor(
            attr="door_closed_left_back",
            name="Door closed left back",
            device_class="door",
            reverse_state=False,
            icon="mdi:car-door"
        ),
        BinarySensor(
            attr="door_closed_right_back",
            name="Door closed right back",
            device_class="door",
            reverse_state=False,
            icon="mdi:car-door"
        ),
        BinarySensor(
            attr="trunk_locked",
            name="Trunk locked",
            device_class="lock",
            reverse_state=False
        ),
        BinarySensor(
            attr="trunk_closed",
            name="Trunk closed",
            device_class="door",
            reverse_state=False
        ),
        BinarySensor(
            attr="hood_closed",
            name="Hood closed",
            device_class="door",
            reverse_state=False
        ),
        BinarySensor(
            attr="charging_cable_connected",
            name="Charging cable connected",
            device_class="plug",
            reverse_state=False
        ),
        BinarySensor(
            attr="charging_cable_locked",
            name="Charging cable locked",
            device_class="lock",
            reverse_state=False
        ),
        BinarySensor(
            attr="sunroof_closed",
            name="Sunroof closed",
            device_class="window",
            reverse_state=False
        ),
        BinarySensor(
            attr="windows_closed",
            name="Windows closed",
            device_class="window",
            reverse_state=False
        ),
        BinarySensor(
            attr="window_closed_left_front",
            name="Window closed left front",
            device_class="window",
            reverse_state=False
        ),
        BinarySensor(
            attr="window_closed_left_back",
            name="Window closed left back",
            device_class="window",
            reverse_state=False
        ),
        BinarySensor(
            attr="window_closed_right_front",
            name="Window closed right front",
            device_class="window",
            reverse_state=False
        ),
        BinarySensor(
            attr="window_closed_right_back",
            name="Window closed right back",
            device_class="window",
            reverse_state=False
        ),
        BinarySensor(
            attr="vehicle_moving",
            name="Vehicle Moving",
            device_class="moving"
        ),
        BinarySensor(
            attr="request_in_progress",
            name="Request in progress",
            device_class="connectivity"
        ),
    ]


class Dashboard:
    def __init__(self, vehicle, **config):
        _LOGGER.debug("Setting up dashboard with config :%s", config)
        self.instruments = [
            instrument
            for instrument in create_instruments()
            if instrument.setup(vehicle, **config)
        ]
