#!/usr/bin/env python3
from enum import Enum
from typing import Optional


class MeterLocation(Enum):
    # 0...grid interconnection point (primary meter)
    grid = 0
    # 1...load (primary meter)
    load = 1
    # 3...external generator (secondary meters)(multiple)
    external = 3
    # 256-511 subloads (secondary meters)(unique)
    subload = 256

    @classmethod
    def get(self, value):
        return MeterLocation(256 if 256 <= value <= 511 else value)


class FroniusConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class Fronius:
    def __init__(self,
                 name: str = "Fronius",
                 type: str = "fronius",
                 id: int = 0,
                 configuration: FroniusConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or FroniusConfiguration()


class FroniusBatConfiguration:
    def __init__(self, meter_id: int = 0):
        self.meter_id = meter_id


class FroniusBatSetup:
    def __init__(self,
                 name: str = "Fronius Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: FroniusBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or FroniusBatConfiguration()


class FroniusS0CounterConfiguration:
    def __init__(self):
        pass


class FroniusS0CounterSetup:
    def __init__(self,
                 name: str = "Fronius S0 Zähler",
                 type: str = "counter_s0",
                 id: int = 0,
                 configuration: FroniusS0CounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or FroniusS0CounterConfiguration()


class FroniusSmCounterConfiguration:
    def __init__(self, meter_id: int = 0, variant: int = 0):
        self.meter_id = meter_id
        self.variant = variant


class FroniusSmCounterSetup:
    def __init__(self,
                 name: str = "Fronius SM Zähler",
                 type: str = "counter_sm",
                 id: int = 0,
                 configuration: FroniusSmCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or FroniusSmCounterConfiguration()


class FroniusInverterConfiguration:
    def __init__(self):
        pass


class FroniusInverterSetup:
    def __init__(self,
                 name: str = "Fronius Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: FroniusInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or FroniusInverterConfiguration()
