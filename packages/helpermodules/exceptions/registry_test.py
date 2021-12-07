from typing import Type

import pytest

from helpermodules.exceptions.registry import ExceptionRegistry
from modules.common.fault_state import FaultState


class ErrorRoot(Exception):
    def __init__(self):
        super().__init__(self.__class__.__name__)


class ErrorA(Exception):
    pass


class ErrorB(ErrorA):
    pass


class ErrorC(ErrorA):
    pass


class ErrorD(ErrorB, ErrorC):
    pass


class ErrorF(ErrorD):
    pass


@pytest.mark.parametrize("exception,expected_message", [
    [ErrorRoot, "<class 'packages.helpermodules.exceptions.registry_test.ErrorRoot'> ErrorRoot"],
    [ErrorB, "B"],
    [ErrorC, "A"],
    [ErrorD, "B"],
    [ErrorF, "F"]
])
def test_uses_exact_match_if_available(exception: Type, expected_message: str):
    # setup
    registry = ExceptionRegistry()
    registry.add(ErrorA, "A")
    registry.add(ErrorB, "B")
    registry.add(ErrorF, "F")

    # execution
    actual = registry.translate_exception(exception())

    # evaluation
    assert actual.fault_str == expected_message


@pytest.mark.parametrize("handler", [
    pytest.param("msg", id="basic string"),
    pytest.param(lambda _: "msg", id="function returning string"),
    pytest.param(lambda _: FaultState.error("msg"), id="function returning fault state")
])
def test_accepts_all_supported_formats(handler):
    # setup
    registry = ExceptionRegistry()

    # execution
    registry.add(Exception, handler)
    actual = registry.translate_exception(Exception())

    # evaluation
    assert isinstance(actual, FaultState)
    assert actual.fault_str == "msg"
