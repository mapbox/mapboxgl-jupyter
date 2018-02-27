import json
import pytest
import pandas as pd
from pandas.util.testing import assert_frame_equal

from mapboxgl.utils import df_to_geojson, scale_between, create_radius_stops, create_weight_stops


@pytest.fixture()
def df():
    return pd.read_csv('tests/points.csv')

@pytest.fixture()
def df_no_properties():
    df = pd.read_csv('tests/points.csv')
    return df[['lon', 'lat']]


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

def test_df_geojson_file(df):
    features = df_to_geojson(df, filename='out.geojson')
    with open('out.geojson', 'r') as f:
        testdata = json.load(f)
    assert len(testdata['features']) == 3


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


def test_create_weight_stops(df):
    res = create_weight_stops([1, 2, 3, 4])
    assert res == [[1, 0.0], [2, 0.25], [3, 0.5], [4, 0.75]]
