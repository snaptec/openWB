from enum import IntEnum
import functools
import logging
import RPi.GPIO as GPIO
import time
from typing import Callable, Dict, Tuple

from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_state import ChargepointState
from modules.chargepoints.internal_openwb.chargepoint_module import ChargepointModule, InternalOpenWB

log = logging.getLogger(__name__)


def get_default_config() -> Dict:
    return {"id": 0,
            "connection_module": {
                "type": "internal_openwb",
                "configuration": {}
            },
            "power_module": {}}


class RateLimiter:
    def __init__(self, max_calls: int, max_seconds: int):
        self.movement_times = [0.0]*max_calls
        self.max_seconds = max_seconds
        self.counter = 0

    def __call__(self, delegate: Callable):
        @functools.wraps(delegate)
        def wrapper(*args, **kwargs):
            now = time.time()
            sleep_needed = self.max_seconds - (now - self.movement_times[self.counter])
            if sleep_needed > 0:
                log.debug("Actor cooldown. Don't move actor.")
                return None
            else:
                self.movement_times[self.counter] = time.time()
                self.counter = (self.counter + 1) % len(self.movement_times)
                return delegate(*args, **kwargs)
        return wrapper


class ActorState(IntEnum):
    CLOSED = 0,
    OPENED = 1


class Socket(ChargepointModule):
    def __init__(self, socket_max_current: int, config: InternalOpenWB) -> None:
        log.debug("Konfiguration als Buchse.")
        self.socket_max_current = socket_max_current
        super().__init__(config)

    def set_current(self, current: float) -> None:
        with SingleComponentUpdateContext(self.component_info):
            try:
                actor = ActorState(GPIO.input(19))
            except Exception:
                log.error("Error getting actor status! Using default 'opened'.")
                actor = ActorState.OPENED

            if actor == ActorState.CLOSED or self.chargepoint_state.plug_state is False:
                if current == self.set_current_evse:
                    return
            else:
                current = 0
            super().set_current(min(current, self.socket_max_current))

    def get_values(self, phase_switch_cp_active: bool) -> Tuple[ChargepointState, float]:
        try:
            actor = ActorState(GPIO.input(19))
        except Exception:
            log.error("Error getting actor status! Using default 'opened'.")
            actor = ActorState.OPENED
        log.debug("Actor: "+str(actor))
        self.chargepoint_state, self.set_current_evse = super().get_values(phase_switch_cp_active)
        if phase_switch_cp_active:
            log.debug("Keine Actor-Bewegung, da CP-Unterbrechung oder Phasenumschaltung aktiv.")
        else:
            if self.chargepoint_state.plug_state is True and actor == ActorState.OPENED:
                self.__close_actor()
            if self.chargepoint_state.plug_state is False and actor == ActorState.CLOSED:
                self.__open_actor()
        return self.chargepoint_state, self.set_current_evse

    def __open_actor(self):
        self.__set_actor(open=True)

    def __close_actor(self):
        self.__set_actor(open=False)

    @RateLimiter(max_calls=10, max_seconds=300)
    def __set_actor(self, open: bool):
        GPIO.output(23, GPIO.LOW if open else GPIO.HIGH)
        GPIO.output(26, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(26, GPIO.LOW)
        log.debug("Actor opened" if open else "Actor closed")
