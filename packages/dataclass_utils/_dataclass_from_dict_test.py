from typing import Type, TypeVar, Generic

import pytest

from dataclass_utils import dataclass_from_dict

T = TypeVar('T')


class SimpleSample:
    def __init__(self, a: str, b="bDefault"):
        self.a = a
        self.b = b


class NestedSample:
    def __init__(self, normal: str, nested: SimpleSample):
        self.normal = normal
        self.nested = nested


class Base(Generic[T]):
    def __init__(self, a: T):
        self.a = a


class Extends(Base[str]):
    def __init__(self, a: str):
        super().__init__(a)


def test_from_dict_simple():
    # execution
    actual = dataclass_from_dict(SimpleSample, {"b": "bValue", "a": "aValue"})

    # evaluation
    assert actual.a == "aValue"
    assert actual.b == "bValue"


def test_default_values_can_be_used():
    # execution
    actual = dataclass_from_dict(SimpleSample, {"a": "aValue"})

    # evaluation
    assert actual.a == "aValue"
    assert actual.b == "bDefault"


def test_from_dict_nested():
    # execution
    actual = dataclass_from_dict(NestedSample, {"normal": "normalValue", "nested": {"b": "bValue", "a": "aValue"}})

    # evaluation
    assert actual.normal == "normalValue"
    assert actual.nested.a == "aValue"
    assert actual.nested.b == "bValue"


def test_from_dict_returns_args_if_type_correct():
    # setup
    sample = SimpleSample("a")

    # execution
    actual = dataclass_from_dict(SimpleSample, sample)

    # evaluation
    assert actual is sample


def test_from_dict_extends_generic():
    # execution
    actual = dataclass_from_dict(Extends, {"a": "aValue"})

    # evaluation
    assert actual.a == "aValue"


@pytest.mark.parametrize(["type", "invalid_parameter"], [
    pytest.param(SimpleSample, "a", id="class with some default values"),
    pytest.param(NestedSample, "normal", id="class with no default values"),
])
def test_from_dict_fails_on_invalid_properties(type: Type[T], invalid_parameter: str):
    # execution & evaluation
    with pytest.raises(Exception) as e:
        dataclass_from_dict(type, {"invalid": "dict"})
    assert str(e.value) == "Cannot determine value for parameter " + invalid_parameter + \
           ": not given in {'invalid': 'dict'} and no default value specified"
