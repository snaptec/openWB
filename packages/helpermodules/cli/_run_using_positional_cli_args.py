import argparse
import inspect
from typing import Callable, Union, Dict, Optional, List

NoneType = type(None)


def _add_positional_parser_args(parser: argparse.ArgumentParser, function: Callable):
    arg_spec = inspect.getfullargspec(function)
    for argument_name in arg_spec.args:
        type = arg_spec.annotations[argument_name]
        if hasattr(type, "__origin__") and type.__origin__ is Union:
            type_arg, = filter(lambda candidate: candidate is not NoneType, type.__args__)
            parser.add_argument(argument_name, nargs='?', type=type_arg)
        else:
            parser.add_argument(argument_name, type=type)
    # We are using the parameter RUN in uppercase to avoid collision with any actual arguments. At any rate there
    # must not be any argument with the name RUN
    parser.set_defaults(RUN=lambda args: function(*[getattr(args, argument_name) for argument_name in arg_spec.args]))


def run_using_positional_cli_args(specification: Union[Callable, Dict[str, Callable]],
                                  argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser()
    if isinstance(specification, dict):
        sub_parsers = parser.add_subparsers(dest="command")
        sub_parsers.required = True
        for command_name, function in specification.items():
            _add_positional_parser_args(sub_parsers.add_parser(command_name), function)
    else:
        _add_positional_parser_args(parser, specification)

    args = parser.parse_args(argv)
    args.RUN(args)
