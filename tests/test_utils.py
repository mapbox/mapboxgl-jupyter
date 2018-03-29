import os
import json
import pytest
import pandas as pd
from pandas.util.testing import assert_frame_equal

from matplotlib.pyplot import imread

from mapboxgl.utils import (df_to_geojson, scale_between, create_radius_stops,
                            create_weight_stops, create_numeric_stops, create_color_stops, 
                            img_encode, rgb_tuple_from_str, color_map, height_map)


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
    image_path = os.path.join(os.path.dirname(__file__), 'mosaic.png')
    image = imread(image_path)
    assert img_encode(image).startswith('data:image/png;base64')


def test_rgb_tuple_from_str():
    """Extract RGB values as tuple from string RGB color representation"""
    assert rgb_tuple_from_str('rgb(122,43,17)') == (122, 43, 17)


def test_rgb_tuple_from_str_rgba():
    """Extract RGBA values as tuple from string RGBA color representation"""
    assert rgb_tuple_from_str('rgba(122,43,17,0.5)') == (122, 43, 17, 0.5)


def test_rgb_tuple_from_str_hex():
    """Extract RGB(A) values as tuple from string HEX color representation"""
    assert rgb_tuple_from_str('#bada55') == (186, 218, 85)


def test_rgb_tuple_from_str_english():
    """Extract RGB(A) values as tuple from limited English color name strings"""
    assert rgb_tuple_from_str('red') == (255, 0, 0)


def test_color_map():
    """Compute color for lookup value in gradient based on color_stops argument using categorical match"""
    match_stops = [[0.0, 'rgb(255,0,255)'],['CA', 'rgb(255,0,0)'], ['NY', 'rgb(255,255,0)'], ['MA', 'rgb(0,0,255)']]
    assert color_map('CA', match_stops, default_color='gray') == 'rgb(255,0,0)'


def test_color_map_numeric_default_color():
    """Default color when look up value does not match any stop in categorical color stops"""
    match_stops = [[0.0, 'rgb(255,0,255)'],['CA', 'rgb(255,0,0)'], ['NY', 'rgb(255,255,0)'], ['MA', 'rgb(0,0,255)']]
    assert color_map(17, match_stops, 'blue') == 'blue'


def test_color_map_default_color():
    """Default color when look up value does not match any stop in categorical color stops"""
    match_stops = [[0.0, 'rgb(255,0,255)'],['CA', 'rgb(255,0,0)'], ['NY', 'rgb(255,255,0)'], ['MA', 'rgb(0,0,255)']]
    assert color_map('MI', match_stops, 'gray') == 'gray'


def test_color_map_numeric_match():
    """Get color for numeric lookup value in categorical color stops if number exists in stops"""
    match_stops = [[0.0, 'rgb(255,0,255)'],['CA', 'rgb(255,0,0)'], ['NY', 'rgb(255,255,0)'], ['MA', 'rgb(0,0,255)']]
    assert color_map(0.0, match_stops, 'green') == 'rgb(255,0,255)'


def test_color_map_interp():
    """Compute color for lookup value by interpolation of color stops"""
    interp_stops = [[0.0, 'rgb(255,0,0)'], [50.0, 'rgb(255,255,0)'], [1000.0, 'rgb(0,0,255)']]
    assert color_map(17, interp_stops, 'orange') == 'rgb(255,87,0)'


def test_color_map_interp_exact():
    """Compute color for lookup value exactly matching numeric stop in color stops"""
    interp_stops = [[0.0, 'rgb(255,0,0)'], [50.0, 'rgb(255,255,0)'], [1000.0, 'rgb(0,0,255)']]
    assert color_map(0.0, interp_stops, 'rgb(32,32,32)') == 'rgb(255,0,0)'


def test_create_numeric_stops():
    """Create numeric stops from custom breaks"""
    domain = [7678.214347826088, 5793.63142857143, 1200]
    stops = create_numeric_stops(domain, 1, 10)
    assert stops == [[7678.214347826088, 1.0], [5793.63142857143, 4.0], [1200, 7.0]]


def test_height_map():
    """Interpolate height from numeric height stops"""
    stops = [[0.0, 0], [50.0, 5000.0], [1000.0, 100000.0]]
    assert height_map(117.0, stops, default_height=0.0) == 11700.0
