import inspect
from inspect import FullArgSpec
from typing import TypeVar, Type, Union

T = TypeVar('T')


def dataclass_from_dict(cls: Type[T], args: Union[dict, T]) -> T:
    """Creates a @dataclass or normal class from a dictionary with constructor arguments

    This function is primarily intended to be used to construct Python 3.7-@dataclass objects from a dictionary.
    However, for compatibility with Python 3.5 this function can also create objects of other types that are used in the
    same way as @dataclass

    In case the supplied `args` is already of the desired type, `args` is returned unchanged
    """
    if isinstance(args, cls):
        return args
    arg_spec = inspect.getfullargspec(cls.__init__)
    return cls(*[_get_argument_value(arg_spec, index, args) for index in range(1, len(arg_spec.args))])


def _get_argument_value(arg_spec: FullArgSpec, index: int, parameters: dict):
    argument_name = arg_spec.args[index]
    try:
        value = parameters[argument_name]
    except KeyError:
        try:
            value = arg_spec.defaults[-len(arg_spec.args) + index]
        except (IndexError, TypeError):
            # If none of the parameters have a default value, then `arg_spec.defaults` is None and we get a `TypeError`.
            # If there are parameters with default value, but not the one requested, we get an `IndexError`.
            raise Exception(
                "Cannot determine value for parameter %s: not given in %s and no default value specified" % (
                    argument_name, parameters))
    return _dataclass_from_dict_recurse(value, arg_spec.annotations.get(argument_name))


def _dataclass_from_dict_recurse(value, requested_type: Type[T]):
    return dataclass_from_dict(requested_type, value) \
        if isinstance(value, dict) and not issubclass(requested_type, dict) \
        else value
