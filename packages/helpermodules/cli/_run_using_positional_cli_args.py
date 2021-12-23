import argparse
import inspect
from typing import Callable, Union

NoneType = type(None)


def run_using_positional_cli_args(function: Callable):
    arg_spec = inspect.getfullargspec(function)
    parser = argparse.ArgumentParser()
    for argument_name in arg_spec.args:
        type = arg_spec.annotations[argument_name]
        if hasattr(type, "__origin__") and type.__origin__ is Union:
            type_arg, = filter(lambda candidate: candidate is not NoneType, type.__args__)
            parser.add_argument(argument_name, nargs='?', type=type_arg)
        else:
            parser.add_argument(argument_name, type=type)
    args = parser.parse_args()
    function(*[getattr(args, argument_name) for argument_name in arg_spec.args])
