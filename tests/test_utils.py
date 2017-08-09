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
        return list(self.features[0]['properties'].keys())

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


def test_df_geojson(df):
    features = df_to_geojson(df)['features']
    assert len(features) == 3


def test_df_properties(df):
    features = df_to_geojson(df, properties=['Avg Medicare Payments'])[
        'features']
    assert tuple(features[0]['properties'].keys()) == ('Avg Medicare Payments',)


def test_scale_between():
    scale = scale_between(0, 1, 4)
    assert scale == list(0.0, 0.33, 0.67)


def test_create_radius_stops(df):
    domain = df['Avg Medicare Payments'].tolist()
    radius_stops = create_radius_stops(domain, 1, 10)
    assert radius_stops == [[7678.214347826088, 1.0], [5793.63142857143, 4.0], [1200, 7.0]]

