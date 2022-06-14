from modules.common.component_state import CounterState

counter_state = CounterState(currents=[-5, -5, 5], powers=[-1150, -1150, 1150])


def test_current_sign():
    assert vars(CounterState(currents=[-5, -5, 5], powers=[-1150, -1150, 1150])) == vars(counter_state)
    assert vars(CounterState(currents=[5, 5, 5], powers=[-1150, -1150, 1150])) == vars(counter_state)
