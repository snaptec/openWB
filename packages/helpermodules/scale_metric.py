"""Module for metric conversions according to SI prefices
"""

from typing import Union


def scale_metric(value: Union[float, int], metric: str, base_metric: str):

    # If no unit or too short unit or the base unit is not matching, return the unmodified value
    # This is crucial for fallback cases where no unit is given at all
    if metric is None or len(metric) != len(base_metric) + 1 or metric[1:] != base_metric:
        return value

    # scale is the first digit of metric, see https://en.wikipedia.org/wiki/Metric_prefix
    scale = metric[0]

    # not covering all here but most common ones
    if scale == 'm':
        return value / 1e3
    elif scale == 'k':
        return value * 1e3
    elif scale == 'M':
        return value * 1e6
    elif scale == 'G':
        return value * 1e9
    elif scale == 'T':
        return value * 1e12
    elif scale == 'n':
        return value / 1e9
    elif scale == 'p':
        return value / 1e12
    elif scale == 'f':
        return value / 1e15
    elif scale == 'P':
        return value * 1e15

    raise Exception("unknown scale <%s> in <%s>" % (scale, metric))
