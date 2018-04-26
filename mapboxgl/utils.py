from .colors import color_ramps, common_html_colors
from chroma import Color, Scale
import geojson
import json
import base64
from io import BytesIO
import re
from matplotlib.image import imsave
from colour import Color as Colour


def row_to_geojson(row, lon, lat, precision):
    """Convert a pandas dataframe row to a geojson format object.  Converts all datetimes to epoch seconds.
    """

    # Let pandas handle json serialization
    row_json = json.loads(row.to_json(date_format='epoch', date_unit='s'))
    return geojson.Feature(geometry=geojson.Point((round(row_json[lon],precision), round(row_json[lat], precision))),
                           properties={key: row_json[key] for key in row_json.keys() if key not in [lon, lat]})


def df_to_geojson(df, properties=None, lat='lat', lon='lon', precision=6, filename=None):
    """Serialize a Pandas dataframe to a geojson format Python dictionary
    """

    if not properties:
        # if no properties are selected, use all properties in dataframe
        properties = [c for c in df.columns if c not in [lon, lat]]

    for prop in properties:
        # Check if list of properties exists in dataframe columns
        if prop not in list(df.columns):
            raise ValueError(
                'properties must be a valid list of column names from dataframe')
        if prop in [lon, lat]:
            raise ValueError(
                'properties cannot be the geometry longitude or latitude column')

    if filename:
        with open(filename, 'w') as f:
            # Overwrite file if it already exists
            pass

        with open(filename, 'a+') as f:

            # Write out file to line
            f.write('{"type": "FeatureCollection", "features": [\n')
            for idx, row in df[[lon, lat] + properties].iterrows():
                if idx == 0:
                    f.write(geojson.dumps(row_to_geojson(row, lon, lat, precision)) + '\n')
                else:
                    f.write(',' + geojson.dumps(row_to_geojson(row, lon, lat, precision)) + '\n')
            f.write(']}')

            return {
                "type": "file",
                "filename": filename,
                "feature_count": df.shape[0]
            }
    else:
        features = []
        df[[lon, lat] + properties].apply(lambda x: features.append(
            row_to_geojson(x, lon, lat, precision)), axis=1)
        return geojson.FeatureCollection(features)


def scale_between(minval, maxval, numStops):
    """ Scale a min and max value to equal interval domain with
        numStops discrete values
    """

    scale = []

    if numStops < 2:
        return [minval, maxval]
    elif maxval < minval:
        raise ValueError()
    else:
        domain = maxval - minval
        interval = float(domain) / float(numStops)
        for i in range(numStops):
            scale.append(round(minval + interval * i, 2))
        return scale


def create_radius_stops(breaks, min_radius, max_radius):
    """Convert a data breaks into a radius ramp
    """
    num_breaks = len(breaks)
    radius_breaks = scale_between(min_radius, max_radius, num_breaks)
    stops = []

    for i, b in enumerate(breaks):
        stops.append([b, radius_breaks[i]])
    return stops


def create_weight_stops(breaks):
    """Convert data breaks into a heatmap-weight ramp
    """
    num_breaks = len(breaks)
    weight_breaks = scale_between(0, 1, num_breaks)
    stops = []

    for i, b in enumerate(breaks):
        stops.append([b, weight_breaks[i]])
    return stops


def create_numeric_stops(breaks, min_value, max_value):
    """Convert data breaks into a general numeric ramp (height, radius, weight, etc.)
    """
    weight_breaks = scale_between(min_value, max_value, len(breaks))
    return [list(x) for x in zip(breaks, weight_breaks)]


def create_color_stops(breaks, colors='RdYlGn', color_ramps=color_ramps):
    """Convert a list of breaks into color stops using colors from colorBrewer
    or a custom list of color values in RGB, RGBA, HSL, CSS text, or HEX format.
    See www.colorbrewer2.org for a list of color options to pass
    """

    num_breaks = len(breaks)
    stops = []

    if isinstance(colors, list):
        # Check if colors contain a list of color values
        if len(colors) == 0 or len(colors) != num_breaks:
            raise ValueError(
                'custom color list must be of same length as breaks list')

        for color in colors:
            # Check if color is valid string
            try:
                Colour(color)
            except:
                raise ValueError(
                    'The color code {color} is in the wrong format'.format(color=color))

        for i, b in enumerate(breaks):
            stops.append([b, colors[i]])

    else:
        if colors not in color_ramps.keys():
            raise ValueError('color does not exist in colorBrewer!')
        else:

            try:
                ramp = color_ramps[colors][num_breaks]
            except KeyError:
                raise ValueError("Color ramp {} does not have a {} breaks".format(
                    colors, num_breaks))

            for i, b in enumerate(breaks):
                stops.append([b, ramp[i]])

    return stops


def rgb_tuple_from_str(color_string):
    """Convert color in format 'rgb(RRR,GGG,BBB)', 'rgba(RRR,GGG,BBB,alpha)',  
    '#RRGGBB', or limited English color name (eg 'red') to tuple (RRR, GGG, BBB)
    """
    try:
        # English color names (limited)
        rgb_string = common_html_colors[color_string]
        return tuple([float(x) for x in re.findall(r'\d{1,3}', rgb_string)]) 
    
    except KeyError:
        try:
            # HEX color code
            hex_string = color_string.lstrip('#')
            return tuple(int(hex_string[i:i+2], 16) for i in (0, 2 ,4))
        
        except ValueError:
            # RGB or RGBA formatted strings
            return tuple([int(x) if float(x) > 1 else float(x) 
                          for x in re.findall(r"[-+]?\d*\.*\d+", color_string)])


def color_map(lookup, color_stops, default_color='rgb(122,122,122)'):
    """Return an rgb color value interpolated from given color_stops;
    assumes colors in color_stops provided as strings of form 'rgb(RRR,GGG,BBB)'
    or in hex: '#RRGGBB'
    """
    # if no color_stops, use default color
    if len(color_stops) == 0:
        return default_color
    
    # dictionary to lookup color from match-type color_stops
    match_map = dict((x, y) for (x, y) in color_stops)

    # if lookup matches stop exactly, return corresponding color (first priority)
    # (includes non-numeric color_stop "keys" for finding color by match)
    if lookup in match_map.keys():
        return match_map.get(lookup)

    # if lookup value numeric, map color by interpolating from color scale
    if isinstance(lookup, (int, float, complex)):

        # try ordering stops 
        try:
            stops, colors = zip(*sorted(color_stops))
        
        # if not all stops are numeric, attempt looking up as if categorical stops
        except TypeError:
            return match_map.get(lookup, default_color)

        # for interpolation, all stops must be numeric
        if not all(isinstance(x, (int, float, complex)) for x in stops):
            return default_color

        # check if lookup value in stops bounds
        if float(lookup) <= stops[0]:
            return colors[0]
        
        elif float(lookup) >= stops[-1]:
            return colors[-1]
        
        # check if lookup value matches any stop value
        elif float(lookup) in stops:
            return colors[stops.index(lookup)]
        
        # interpolation required
        else:

            rgb_tuples = [Color(rgb_tuple_from_str(x)) for x in colors]

            # identify bounding color stop values
            lower = max([stops[0]] + [x for x in stops if x < lookup])
            upper = min([stops[-1]] + [x for x in stops if x > lookup])
            
            # colors from bounding stops
            lower_color = rgb_tuples[stops.index(lower)]
            upper_color = rgb_tuples[stops.index(upper)]
            
            # generate color scale for mapping lookup value to interpolated color
            scale = Scale(Color(lower_color), Color(upper_color))

            # compute linear "relative distance" from lower bound color to upper bound color
            distance = (lookup - lower) / (upper - lower)

            # return string representing rgb color value
            return scale(distance).to_string().replace(', ', ',')

    # default color value catch-all
    return default_color


def numeric_map(lookup, numeric_stops, default=0.0):
    """Return a number value interpolated from given numeric_stops
    """
    # if no numeric_stops, use default
    if len(numeric_stops) == 0:
        return default
    
    # dictionary to lookup value from match-type numeric_stops
    match_map = dict((x, y) for (x, y) in numeric_stops)

    # if lookup matches stop exactly, return corresponding stop (first priority)
    # (includes non-numeric numeric_stop "keys" for finding value by match)
    if lookup in match_map.keys():
        return match_map.get(lookup)

    # if lookup value numeric, map value by interpolating from scale
    if isinstance(lookup, (int, float, complex)):

        # try ordering stops 
        try:
            stops, values = zip(*sorted(numeric_stops))
        
        # if not all stops are numeric, attempt looking up as if categorical stops
        except TypeError:
            return match_map.get(lookup, default)

        # for interpolation, all stops must be numeric
        if not all(isinstance(x, (int, float, complex)) for x in stops):
            return default

        # check if lookup value in stops bounds
        if float(lookup) <= stops[0]:
            return values[0]
        
        elif float(lookup) >= stops[-1]:
            return values[-1]
        
        # check if lookup value matches any stop value
        elif float(lookup) in stops:
            return values[stops.index(lookup)]
        
        # interpolation required
        else:

            # identify bounding stop values
            lower = max([stops[0]] + [x for x in stops if x < lookup])
            upper = min([stops[-1]] + [x for x in stops if x > lookup])
            
            # values from bounding stops
            lower_value = values[stops.index(lower)]
            upper_value = values[stops.index(upper)]
            
            # compute linear "relative distance" from lower bound to upper bound
            distance = (lookup - lower) / (upper - lower)

            # return interpolated value
            return lower_value + distance * (upper_value - lower_value)

    # default value catch-all
    return default


def img_encode(arr, **kwargs):
    """Encode ndarray to base64 string image data
    
    Parameters
    ----------
    arr: ndarray (rows, cols, depth)
    kwargs: passed directly to matplotlib.image.imsave
    """
    sio = BytesIO()
    imsave(sio, arr, **kwargs)
    sio.seek(0)
    img_format = kwargs['format'] if kwargs.get('format') else 'png'
    img_str = base64.b64encode(sio.getvalue()).decode()

    return 'data:image/{};base64,{}'.format(img_format, img_str)


def height_map(lookup, height_stops, default_height=0.0):
    """Return a height value (in meters) interpolated from given height_stops;
    for use with vector-based visualizations using fill-extrusion layers
    """
    # if no height_stops, use default height
    if len(height_stops) == 0:
        return default_height
    
    # dictionary to lookup height from match-type height_stops
    match_map = dict((x, y) for (x, y) in height_stops)

    # if lookup matches stop exactly, return corresponding height (first priority)
    # (includes non-numeric height_stop "keys" for finding height by match)
    if lookup in match_map.keys():
        return match_map.get(lookup)

    # if lookup value numeric, map height by interpolating from height scale
    if isinstance(lookup, (int, float, complex)):

        # try ordering stops 
        try:
            stops, heights = zip(*sorted(height_stops))
        
        # if not all stops are numeric, attempt looking up as if categorical stops
        except TypeError:
            return match_map.get(lookup, default_height)

        # for interpolation, all stops must be numeric
        if not all(isinstance(x, (int, float, complex)) for x in stops):
            return default_height

        # check if lookup value in stops bounds
        if float(lookup) <= stops[0]:
            return heights[0]
        
        elif float(lookup) >= stops[-1]:
            return heights[-1]
        
        # check if lookup value matches any stop value
        elif float(lookup) in stops:
            return heights[stops.index(lookup)]
        
        # interpolation required
        else:

            # identify bounding height stop values
            lower = max([stops[0]] + [x for x in stops if x < lookup])
            upper = min([stops[-1]] + [x for x in stops if x > lookup])
            
            # heights from bounding stops
            lower_height = heights[stops.index(lower)]
            upper_height = heights[stops.index(upper)]
            
            # compute linear "relative distance" from lower bound height to upper bound height
            distance = (lookup - lower) / (upper - lower)

            # return string representing rgb height value
            return lower_height + distance * (upper_height - lower_height)

    # default height value catch-all
    return default_height
