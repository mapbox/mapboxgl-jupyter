import json

import pytest

from mapboxgl.utils import df_to_geojson


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
    assert len(features) == 2


def test_df_properties(df):
    features = df_to_geojson(df, properties=['Avg Medicare Payments'])['features']
    assert tuple(features[0]['properties'].keys()) == ('Avg Medicare Payments',)
