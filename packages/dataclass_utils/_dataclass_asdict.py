def asdict(value):
    """Converts an object to a dict

    This function is a simple replacement for the `dataclasses.asdict` function introduced in Python 3.7. This function
    is introduced, because openWB still requires compatibility with Python 3.5
    This function should be replaced when switching to actual Python 3.7 dataclasses.
    """
    if isinstance(value, (str, int, float)):
        return value
    if isinstance(value, (list, tuple)):
        return [None if v is None else asdict(v) for v in value]
    if not isinstance(value, dict):
        value = vars(value)
    return {key: None if value is None else asdict(value) for key, value in value.items()}
