import sys
from typing import Optional
from unittest.mock import Mock

import pytest

from helpermodules.cli import run_using_positional_cli_args


def create_int_arg_function(mock: Mock):
    def int_arg(arg: int):
        mock(arg)
    return int_arg


def create_float_arg_function(mock: Mock):
    def float_arg(arg: float):
        mock(arg)
    return float_arg


def create_str_arg_function(mock: Mock):
    def str_arg(arg: str):
        mock(arg)
    return str_arg


def create_optional_arg_function(mock: Mock):
    def optional_arg(arg: Optional[int]):
        mock(arg)
    return optional_arg


def create_multi_arg_function(mock: Mock):
    def multi_arg(arg_str: str, arg_int: int, optional_str: Optional[str], optional_int: Optional[int]):
        mock((arg_str, arg_int, optional_str, optional_int))
    return multi_arg


@pytest.mark.parametrize(
    "function_factory,argv,arg_parsed", [
        (create_int_arg_function, ["42"], 42),
        (create_float_arg_function, ["12.34"], 12.34),
        (create_str_arg_function, ["some string"], "some string"),
        (create_optional_arg_function, [], None),
        (create_optional_arg_function, ["21"], 21),
        (create_multi_arg_function, ["some string", "42"], ("some string", 42, None, None)),
        (create_multi_arg_function, ["some string", "42", "other str"], ("some string", 42, "other str", None)),
        (create_multi_arg_function, ["some string", "42", "other str", "21"], ("some string", 42, "other str", 21)),
    ]
)
def test_run_using_cli_args_int_arg(monkeypatch, function_factory, argv, arg_parsed):
    # setup
    argv.insert(0, "dummy")
    monkeypatch.setattr(sys, "argv", argv)
    mock = Mock()
    function = function_factory(mock)

    # execution
    run_using_positional_cli_args(function)

    # evaluation
    mock.assert_called_once_with(arg_parsed)


def test_run_using_cli_args_multi_command(monkeypatch):
    # setup
    monkeypatch.setattr(sys, "argv", ["dummy", "a", "42"])
    mock_a = Mock()
    mock_b = Mock()
    commands = {"a": create_int_arg_function(mock_a), "b": create_str_arg_function(mock_b)}

    # execution
    run_using_positional_cli_args(commands)

    # evaluation
    mock_a.assert_called_once_with(42)
    mock_b.assert_not_called()
