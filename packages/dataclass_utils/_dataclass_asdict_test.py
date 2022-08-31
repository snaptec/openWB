import pytest

from dataclass_utils import asdict


class SingleValue:
    def __init__(self, value):
        self.value = value


class MultiValue:
    def __init__(self, a, b):
        self.a = a
        self.b = b


@pytest.mark.parametrize(["object", "expected_dict"], [
    # Test serialization of basic types:
    pytest.param(SingleValue("someString"), {"value": "someString"}, id="single string"),
    pytest.param(SingleValue(42), {"value": 42}, id="single int"),
    pytest.param(SingleValue(4.2), {"value": 4.2}, id="single float"),
    pytest.param(SingleValue(None), {"value": None}, id="single None"),
    pytest.param(SingleValue(["a", 2, None]), {"value": ["a", 2, None]}, id="single list"),
    pytest.param(SingleValue((None, "a", 2)), {"value": [None, "a", 2]}, id="single tuple"),
    pytest.param(SingleValue({"a": "a", "b": 2}), {"value": {"a": "a", "b": 2}}, id="single object"),

    # Test nesting:
    pytest.param(SingleValue(SingleValue("nested")), {"value": {"value": "nested"}}, id="nested object"),
    pytest.param({"a": SingleValue(42)}, {"a": {"value": 42}}, id="dict with nested dataclass"),

    # Test multiple values:
    pytest.param(MultiValue("aValue", 42), {"a": "aValue", "b": 42}, id="multi value"),
])
def test_asdict(object, expected_dict: dict):
    # execution
    actual = asdict(object)

    # evaluation
    assert actual == expected_dict
