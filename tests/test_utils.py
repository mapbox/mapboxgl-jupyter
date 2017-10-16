import json

import pytest

from mapboxgl.utils import df_to_geojson, scale_between, create_radius_stops


class MockDataframe(object):
    """Mock the attrs we need, avoid pandas dependency
    """

    def __init__(self, features, lat="lat", lon="lon"):
        self.features = features
        self.lat = lat
        self.lon = lon

    @property
    def columns(self):
        properties = list(self.features[0]['properties'].keys())
        properties.extend([self.lat, self.lon])
        return properties

    def iterrows(self):
        for i, row in enumerate(self.features):
            newrow = row['properties'].copy()
            # assumes points
            newrow['lon'] = row['geometry']['coordinates'][0]
            newrow['lat'] = row['geometry']['coordinates'][1]
            yield i, newrow


@pytest.fixture()
def df():
    with open('tests/points.geojson') as fh:
        data = json.loads(fh.read())

    return MockDataframe(data['features'])

@pytest.fixture()
def df_no_properties():
    with open('tests/points.geojson') as fh:
        data = json.loads(fh.read())

    for feature in data['features']:
        feature['properties'] = {}

    return MockDataframe(data['features'])


def test_df_geojson(df):
    features = df_to_geojson(df)['features']
    assert len(features) == 3


def test_df_properties(df):
    features = df_to_geojson(df, properties=['Avg Medicare Payments'])[
        'features']
    assert tuple(features[0]['properties'].keys()) == ('Avg Medicare Payments',)


def test_df_no_properties(df_no_properties):
    features = df_to_geojson(df_no_properties)[
        'features']
    assert tuple(features[0]['properties'].keys()) == ()


def test_scale_between():
    scale = scale_between(0, 1, 4)
    assert scale == [0.0, 0.25, 0.5, 0.75]


def test_scale_between_valueError():
    """Create radius stops raises ValueError"""
    with pytest.raises(ValueError):
        scale_between(1, 0, 10)


def test_scale_between_maxMin():
    """Create radius stops raises ValueError"""
    scale = scale_between(0,1,1)
    assert scale == [0,1]


def test_create_radius_stops(df):
    domain = [7678.214347826088, 5793.63142857143, 1200]
    radius_stops = create_radius_stops(domain, 1, 10)
    assert radius_stops == [[7678.214347826088, 1.0], [5793.63142857143, 4.0], [1200, 7.0]]
