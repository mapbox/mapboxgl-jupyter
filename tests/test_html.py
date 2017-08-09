import json
from mock import patch

import pytest

from mapboxgl.viz import CircleViz, GraduatedCircleViz
from mapboxgl.errors import TokenError


@pytest.fixture()
def data():
    with open('tests/points.geojson') as fh:
        return json.loads(fh.read())


TOKEN = 'pk.abc123'


def test_secret_key(data):
    """Secret key raises a token error
    """
    secret = 'sk.abc123'
    with pytest.raises(TokenError):
        CircleViz(data, access_token=secret)


def test_token_env(monkeypatch, data):
    """Viz can get token from environment if not specified
    """
    monkeypatch.setenv('MAPBOX_ACCESS_TOKEN', TOKEN)
    viz = CircleViz(data, color_property="Avg Medicare Payments")
    assert TOKEN in viz.create_html()


def test_html_color(data):
    viz = CircleViz(data,
                    color_property="Avg Medicare Payments",
                    access_token=TOKEN)
    assert "<html>" in viz.create_html()


def test_html_graduatedCricleViz(data):
    viz = GraduatedCircleViz(data,
                             color_property="Avg Medicare Payments",
                             radius_property="Avg Covered Charges",
                             access_token=TOKEN)
    assert "<html>" in viz.create_html()


@patch('mapboxgl.viz.display')
def test_display(display, data):
    """Assert that show calls the mocked display function
    """
    viz = CircleViz(data,
                    color_property="Avg Medicare Payments",
                    access_token=TOKEN)
    viz.show()
    display.assert_called_once()
