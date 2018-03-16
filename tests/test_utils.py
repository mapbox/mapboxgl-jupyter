import os
import json
import pytest
import pandas as pd
from pandas.util.testing import assert_frame_equal

from matplotlib.pyplot import imread

from mapboxgl.utils import (df_to_geojson, scale_between, create_radius_stops,
                            create_weight_stops, create_color_stops, img_encode)


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

def test_color_stops():
    """Create color stops from breaks using colorBrewer"""
    stops = create_color_stops([0, 1, 2], colors='YlGn')
    assert stops == [[0,"rgb(247,252,185)"], [1,"rgb(173,221,142)"], [2,"rgb(49,163,84)"]]

def test_color_stops_custom():
    """Create color stops from custom color breaks"""
    stops = create_color_stops([0, 1, 2], colors=['red', 'yellow', 'green'])
    assert stops == [[0,"red"], [1,"yellow"], [2,"green"]]

def test_color_stops_custom_invalid():
    """Create invalid color stops from custom color breaks and throw value error"""
    with pytest.raises(ValueError):
        create_color_stops([0, 1, 2], colors=['x', 'yellow', 'green'])

def test_color_stops_custom_null():
    """Create invalid number of color stops that do not match the number of breaks"""
    with pytest.raises(ValueError):
        create_color_stops([0, 1, 2], colors=['red', 'yellow', 'green', 'grey'])

def test_create_radius_stops(df):
    domain = [7678.214347826088, 5793.63142857143, 1200]
    radius_stops = create_radius_stops(domain, 1, 10)
    assert radius_stops == [[7678.214347826088, 1.0], [5793.63142857143, 4.0], [1200, 7.0]]


def test_create_weight_stops(df):
    res = create_weight_stops([1, 2, 3, 4])
    assert res == [[1, 0.0], [2, 0.25], [3, 0.5], [4, 0.75]]


def test_img_encode():
    image_path = os.path.join(os.path.dirname(__file__), 'mosaic.jpg')
    image = imread(image_path)
    assert img_encode(image).startswith('data:image/png;base64')
