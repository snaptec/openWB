from requests import Session

from modules.common.component_state import CounterState


def get_last_reading(session: Session, meter_id: str):
    values = session.get(
        "https://api.discovergy.com/public/v1/last_reading",
        params={"meterId": meter_id},
        timeout=3
    ).json()["values"]

    def read_phases(*args: str):
        for format in args:
            try:
                return [values[format % phase] / 1000 for phase in range(1, 4)]
            except KeyError:
                pass

    voltages = read_phases("voltage%i", "phase%iVoltage")
    powers = read_phases("power%i", "phase%iPower")

    return CounterState(
        imported=values["energy"] / 10000000,
        exported=values["energyOut"] / 10000000,
        power=values["power"] / 1000,
        voltages=voltages,
        powers=powers
    )
