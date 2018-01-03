import pytest

from mapboxgl.utils import create_color_stops


def test_colors():
    assert create_color_stops([1, 2, 3], colors='PuOr') == \
        [[1, 'rgb(241,163,64)'], [2, 'rgb(247,247,247)'], [3, 'rgb(153,142,195)']]


def test_bad_ramp():
    with pytest.raises(ValueError):
        create_color_stops([1, 2, 3], colors='DoubleRainbow')


def test_too_many_colors():
    with pytest.raises(ValueError):
        create_color_stops(list(range(100)), colors='PuOr')
