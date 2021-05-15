#  Utilities for integration with Home Assistant (directly or via MQTT)

import logging

from .util import camel2slug

_LOGGER = logging.getLogger(__name__)


# fixme: move (mapping to) hass component names to config file instead


class Instrument:
    def __init__(self, component, attr, name, icon=None):
        self.attr = attr
        self.component = component
        self.name = name
        self.vehicle = None
        self.icon = icon

    def __repr__(self):
        return self.full_name

    def configurate(self, **args):
        pass

    @property
    def slug_attr(self):
        return camel2slug(self.attr.replace(".", "_"))

    def setup(self, vehicle, mutable=True, **config):
        self.vehicle = vehicle

        if not mutable and self.is_mutable:
            _LOGGER.info("Skipping %s because mutable", self)
            return False

        if not self.is_supported:
            _LOGGER.debug(
                "%s (%s:%s) is not supported",
                self,
                type(self).__name__,
                self.attr,
            )
            return False

        _LOGGER.debug("%s is supported", self)

        self.configurate(**config)

        return True

    @property
    def vehicle_name(self):
        return self.vehicle.registration_number or self.vehicle.vin

    @property
    def full_name(self):
        return "%s %s" % (self.vehicle_name, self.name)

    @property
    def is_mutable(self):
        raise NotImplementedError("Must be set")

    @property
    def is_supported(self):
        supported = "is_" + self.attr + "_supported"
        if hasattr(self.vehicle, supported):
            return getattr(self.vehicle, supported)
        if hasattr(self.vehicle, self.attr):
            return True
        return self.vehicle.has_attr(self.attr)

    @property
    def str_state(self):
        return self.state

    @property
    def state(self):
        if hasattr(self.vehicle, self.attr):
            return getattr(self.vehicle, self.attr)
        return self.vehicle.get_attr(self.attr)

    @property
    def attributes(self):
        return {}


class Sensor(Instrument):
    def __init__(self, attr, name, icon, unit):
        super().__init__(component="sensor", attr=attr, name=name, icon=icon)
        self.unit = unit

    def configurate(self, scandinavian_miles=False, **config):
        if self.unit and scandinavian_miles and "km" in self.unit:
            self.unit = "mil"

    @property
    def is_mutable(self):
        return False

    @property
    def str_state(self):
        if self.unit:
            return "%s %s" % (self.state, self.unit)
        else:
            return "%s" % self.state

    @property
    def state(self):
        val = super().state
        if val and "mil" in self.unit:
            return val / 10
        else:
            return val


class FuelConsumption(Sensor):
    def __init__(self):
        super().__init__(
            attr="averageFuelConsumption",
            name="Fuel consumption",
            icon="mdi:gas-station",
            unit="L/100 km",
        )

    def configurate(self, scandinavian_miles=False, **config):
        if scandinavian_miles:
            self.unit = "L/mil"

    @property
    def state(self):
        val = super().state
        decimals = 2 if "mil" in self.unit else 1
        if val:
            return round(val / 10, decimals)


class Odometer(Sensor):
    def __init__(self, attr="odometer", name="Odometer"):
        super().__init__(
            attr=attr, name=name, icon="mdi:speedometer", unit="km"
        )

    @property
    def state(self):
        val = super().state
        if val:
            return int(round(val / 1000))  # m->km
        return 0


class JournalLastTrip(Sensor):
    def __init__(self):
        super().__init__(
            attr="trips", name="Last trip", unit="", icon="mdi:book-open"
        )

    @property
    def is_supported(self):
        return self.vehicle.is_journal_supported

    @property
    def trip(self):
        if self.vehicle.trips:
            return self.vehicle.trips[0]["tripDetails"][0]

    @property
    def start_address(self):
        return "{}, {}".format(
            self.trip["startPosition"]["streetAddress"],
            self.trip["startPosition"]["city"],
        )

    @property
    def end_address(self):
        return "{}, {}".format(
            self.trip["endPosition"]["streetAddress"],
            self.trip["endPosition"]["city"],
        )

    @property
    def start_time(self):
        return self.trip["startTime"].astimezone(None)

    @property
    def end_time(self):
        return self.trip["endTime"].astimezone(None)

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def state(self):
        if self.trip:
            return self.end_time

    @property
    def attributes(self):
        if self.trip:
            return dict(
                start_address=self.start_address,
                start_time=str(self.start_time),
                end_address=self.end_address,
                end_time=str(self.end_time),
                duration=str(self.duration),
            )


class BinarySensor(Instrument):
    def __init__(self, attr, name, device_class):
        super().__init__(component="binary_sensor", attr=attr, name=name)
        self.device_class = device_class

    @property
    def is_mutable(self):
        return False

    @property
    def str_state(self):
        if self.device_class in ["door", "window"]:
            return "Open" if self.state else "Closed"
        if self.device_class == "safety":
            return "Warning!" if self.state else "OK"
        if self.device_class == "plug":
            return "Charging" if self.state else "Plug removed"
        if self.state is None:
            _LOGGER.error("Can not encode state %s:%s", self.attr, self.state)
            return "?"
        return "On" if self.state else "Off"

    @property
    def state(self):
        val = super().state
        if isinstance(val, (bool, list)):
            #  for list (e.g. bulb_failures):
            #  empty list (False) means no problem
            return bool(val)
        elif isinstance(val, str):
            return val != "Normal"
        return val

    @property
    def is_on(self):
        return self.state


class BatteryChargeStatus(BinarySensor):
    def __init__(self):
        super().__init__(
            "hvBattery.hvBatteryChargeStatusDerived",
            "Battery charging",
            "plug",
        )

    @property
    def state(self):
        return super(BinarySensor, self).state == "CablePluggedInCar_Charging"


class Lock(Instrument):
    def __init__(self):
        super().__init__(component="lock", attr="lock", name="Door lock")

    @property
    def is_mutable(self):
        return True

    @property
    def str_state(self):
        return "Locked" if self.state else "Unlocked"

    @property
    def state(self):
        return self.vehicle.is_locked

    @property
    def is_locked(self):
        return self.state

    async def lock(self):
        await self.vehicle.lock()

    async def unlock(self):
        await self.vehicle.unlock()


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


class Heater(Switch):
    def __init__(self):
        super().__init__(attr="heater", name="Heater", icon="mdi:radiator")

    @property
    def state(self):
        return self.vehicle.is_heater_on

    async def turn_on(self):
        await self.vehicle.start_heater()

    async def turn_off(self):
        await self.vehicle.stop_heater()


class EngineStart(Switch):
    def __init__(self):
        super().__init__(
            attr="is_engine_running", name="Engine", icon="mdi:engine"
        )

    @property
    def is_supported(self):
        return self.vehicle.is_engine_start_supported

    async def turn_on(self):
        await self.vehicle.start_engine()

    async def turn_off(self):
        await self.vehicle.stop_engine()


class Position(Instrument):
    def __init__(self):
        super().__init__(
            component="device_tracker", attr="position", name="Position"
        )

    @property
    def is_mutable(self):
        return False

    @property
    def state(self):
        state = super().state or {}
        return (
            state.get("latitude", "?"),
            state.get("longitude", "?"),
            state.get("timestamp", None),
            state.get("speed", None),
            state.get("heading", None),
        )

    @property
    def str_state(self):
        state = super().state or {}
        ts = state.get("timestamp")
        return (
            state.get("latitude", "?"),
            state.get("longitude", "?"),
            str(ts.astimezone(tz=None)) if ts else None,
            state.get("speed", None),
            state.get("heading", None),
        )


#  FIXME: Maybe make this list configurable as external yaml
def create_instruments():
    return [
        Position(),
        Lock(),
        Heater(),
        Odometer(),
        Odometer(attr="tripMeter1", name="Trip meter 1"),
        Odometer(attr="tripMeter2", name="Trip meter 2"),
        Sensor(
            attr="fuelAmount",
            name="Fuel amount",
            icon="mdi:gas-station",
            unit="L",
        ),
        Sensor(
            attr="fuelAmountLevel",
            name="Fuel level",
            icon="mdi:water-percent",
            unit="%",
        ),
        FuelConsumption(),
        Sensor(
            attr="distanceToEmpty", name="Range", icon="mdi:ruler", unit="km"
        ),
        Sensor(
            attr="averageSpeed",
            name="Average speed",
            icon="mdi:ruler",
            unit="km/h",
        ),
        Sensor(
            attr="hvBattery.distanceToHVBatteryEmpty",
            name="Battery range",
            icon="mdi:ruler",
            unit="km",
        ),
        Sensor(
            attr="hvBattery.hvBatteryLevel",
            name="Battery level",
            icon="mdi:battery",
            unit="%",
        ),
        Sensor(
            attr="hvBattery.timeToHVBatteryFullyCharged",
            name="Time to fully charged",
            icon="mdi:clock",
            unit="minutes",
        ),
        BatteryChargeStatus(),
        EngineStart(),
        JournalLastTrip(),
        BinarySensor(
            attr="is_engine_running", name="Engine", device_class="power"
        ),
        BinarySensor(attr="is_locked", name="Door lock", device_class="lock"),
        BinarySensor(attr="doors.hoodOpen", name="Hood", device_class="door"),
        BinarySensor(
            attr="doors.tailgateOpen", name="Tailgate", device_class="door"
        ),
        BinarySensor(
            attr="doors.frontLeftDoorOpen",
            name="Front left door",
            device_class="door",
        ),
        BinarySensor(
            attr="doors.frontRightDoorOpen",
            name="Front right door",
            device_class="door",
        ),
        BinarySensor(
            attr="doors.rearLeftDoorOpen",
            name="Rear left door",
            device_class="door",
        ),
        BinarySensor(
            attr="doors.rearRightDoorOpen",
            name="Rear right door",
            device_class="door",
        ),
        BinarySensor(
            attr="windows.frontLeftWindowOpen",
            name="Front left window",
            device_class="window",
        ),
        BinarySensor(
            attr="windows.frontRightWindowOpen",
            name="Front right window",
            device_class="window",
        ),
        BinarySensor(
            attr="windows.rearLeftWindowOpen",
            name="Rear left window",
            device_class="window",
        ),
        BinarySensor(
            attr="windows.rearRightWindowOpen",
            name="Rear right window",
            device_class="window",
        ),
        BinarySensor(
            attr="tyrePressure.frontRightTyrePressure",
            name="Front right tyre",
            device_class="safety",
        ),
        BinarySensor(
            attr="tyrePressure.frontLeftTyrePressure",
            name="Front left tyre",
            device_class="safety",
        ),
        BinarySensor(
            attr="tyrePressure.rearRightTyrePressure",
            name="Rear right tyre",
            device_class="safety",
        ),
        BinarySensor(
            attr="tyrePressure.rearLeftTyrePressure",
            name="Rear left tyre",
            device_class="safety",
        ),
        BinarySensor(
            attr="washerFluidLevel", name="Washer fluid", device_class="safety"
        ),
        BinarySensor(
            attr="brakeFluid", name="Brake Fluid", device_class="safety"
        ),
        BinarySensor(
            attr="serviceWarningStatus", name="Service", device_class="safety"
        ),
        BinarySensor(attr="bulbFailures", name="Bulbs", device_class="safety"),
        BinarySensor(attr="any_door_open", name="Doors", device_class="door"),
        BinarySensor(
            attr="any_window_open", name="Windows", device_class="window"
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
