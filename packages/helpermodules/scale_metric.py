"""Module for metric conversions according to SI prefices
"""

from typing import Union
from typing import Optional

scale_factors = {
    'f': 1e-15,  # femto
    'p': 1e-12,  # pico
    'n': 1e-9,   # nano
    'µ': 1e-6,   # micro
    'm': 1e-3,   # milli
    'k': 1e3,    # kilo
    'M': 1e6,    # mega
    'G': 1e9,    # giga
    'T': 1e12,   # tera
    'P': 1e15    # peta
}


def scale_metric(value: Union[float, int], metric: Optional[str], base_metric: str):

    # If no unit or too short unit or the base unit is not matching, return the unmodified value
    # This is crucial for fallback cases where no unit is given at all
    if metric is None or len(metric) != len(base_metric) + 1 or metric[1:] != base_metric:
        return value

    # unit is the first digit of metric, see https://en.wikipedia.org/wiki/Metric_prefix
    prefix = metric[0]

    # not covering all here but most common ones
    factor = scale_factors.get(prefix)
    if factor is None:
        raise Exception("unknown unit prefix <%s> in <%s>" % (prefix, metric))

    return value * factor
