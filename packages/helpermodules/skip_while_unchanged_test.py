import itertools
from unittest.mock import Mock, call

import pytest

from helpermodules.skip_while_unchanged import skip_while_unchanged


def test_skip_while_unchanged_calls_original_with_arguments():
    # setup
    mock = Mock()

    # execution
    decorated = skip_while_unchanged(itertools.count().__next__)(mock)
    decorated(1, 2, some_key="some value")
    decorated(3)

    # evaluation
    expected_calls = [call(1, 2, some_key="some value"), call(3)]
    mock.assert_has_calls(expected_calls)
    assert mock.call_count == len(expected_calls)


def test_skip_while_unchanged_skips_calls_on_no_change():
    # setup
    mock = Mock()

    # execution
    decorated = skip_while_unchanged([1, 1, 1, 2, 2].__iter__().__next__)(mock)
    decorated(1)
    decorated(2)
    decorated(3)
    decorated(4)
    decorated(5)

    # evaluation
    expected_calls = [call(1), call(4)]
    mock.assert_has_calls(expected_calls)
    assert mock.call_count == len(expected_calls)


def test_skip_while_unchanged_recalls_if_function_throws_exception():
    # setup
    mock = Mock(side_effect=Exception("dummy"))

    # execution
    decorated = skip_while_unchanged(itertools.count().__next__)(mock)
    for i in range(1, 3):
        with pytest.raises(Exception):
            decorated(i)

    # evaluation
    expected_calls = [call(1), call(2)]
    mock.assert_has_calls(expected_calls)
    assert mock.call_count == len(expected_calls)
