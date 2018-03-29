## row_to_geojson
Convert a pandas dataframe row to a geojson format object. Converts all datetimes to epoch seconds.

### Params
**row_to_geojson**(_row, lon, lat_)

Parameter | Description
--|--
row | Pandas dataframe row.
lon | Name of dataframe column containing latitude values.
lat | Name of dataframe column containing longitude values.

## df_to_geojson
Convert a Pandas dataframe to a geojson format Python dictionary or as a line-delimited geojson file.

### Params
**df_to_geojson**(_df, properties=None, lat='lat', lon='lon', precision=None, filename=None_)

Parameter | Description
--|--
df | Pandas dataframe
properties | List of dataframe columns to include as object properties. Does not accept lat or lon as a valid property.
lon | Name of dataframe column containing latitude values.
lat | Name of dataframe column containing longitude values.
precision | Accuracy of lat/lon values. Values are rounded to the desired precision.
filename | Name of file for writing geojson data. Data is stored as an object if filename is not provided.

### Usage

```python
import pandas as pd
from mapboxgl.utils import *

# Load gage data from sample csv
data_url = "https://raw.githubusercontent.com/mapbox/mapboxgl-jupyter/master/examples/cdec.csv"
df = pd.read_csv(data_url)

# Convert Elevation series to float
df['Elevation (feet)'] = df['Elevation (feet)'].astype(float)

# Clean up by dropping null rows
df.dropna(axis=1, how='all', inplace=True)

# Create geojson file output
df_to_geojson(
      df.fillna(''),
      filename="cdec.geojson",
      properties=['CDEC ID', 'CNRFC ID', 'Gage Type', 'Elevation (feet)'],
      precision=4
)
>>> {'feature_count': 2353, 'filename': 'cdec.geojson', 'type': 'file'}

# Create geojson python dict saved to a variable named data
data = df_to_geojson(
      df.fillna(''),
      properties=['CDEC ID', 'CNRFC ID', 'Gage Type', 'Elevation (feet)'],
      precision=4
)
```

## scale_between
Scale a minimum and maximum value to an equal interval domain list, with `numStops` values in in the list.

### Params
**scale_between**(_minval, maxval, numStops_)

Parameter | Description
--|--
minval | minimum value
maxval | maximum value
numStops | number of intervals

## create_radius_stops
Convert a Python list of a data domain (such as `[0, 1, 5, 100, 10000]`) into a radius ramp between a minimum and maxium radius value. 

### Params
**create_radius_stops**(_breaks, min_radius, max_radius_)

Parameter | Description
--|--
breaks | List of float values
min_radius | Minimum radius value
max_radius | Maximum radius value

## create_weight_stops
Convert a Python list of a data domain (such as `[0, 1, 5, 100, 10000]`) into a weight-ramp for a heatmap.

### Params
**create_weight_stops**(_breaks_)

Parameter | Description
--|--
breaks | List of float values

## create_color_stops
Convert a Python list of a data domain (such as `[0, 1, 5, 100, 10000]`) into color ramp stops.  Color ramps can be from colorBrewer, or a custom list of color values.

### Params
**create_color_stops**(_breaks, colors='RdYlGn'_)

Parameter | Description
--|--
breaks | List of float values
colors | String value for color ramp OR a list of colors as hex, RGB, or RGBA strings.

### Color Options

**Multi-Hue** | **Single Hue** | **Diverging** | **Qualitative**
--|--|--|--
YlGn | Blues | BrBG | Accent
YlGnB | Greens | PiYG | Dark2
BuGn | Greys | PRGn | Paired
BuPu | Oranges | PuOr | Pastel1
GnBu | Purples | RdBu | Pastel2
OrRd | Reds | RdGy | Set1
PuBu |  | RdYlBu | Set2
PuBuGn |  | RdYlGn | Set3
PuRd |  | Spectral |
RdPu |  |  |
YlGn |  |  |
YlOrBr |  |  |
YlOrRd |  |  |

### Usage
```python
from mapboxgl.utils import *
import pandas as pd

# Load data from sample csv
data_url = 'https://raw.githubusercontent.com/mapbox/mapboxgl-jupyter/master/examples/points.csv'
df = pd.read_csv(data_url)

# Generate a new data domain breaks and a new color palette from colorBrewer2
color_breaks = [0,10,100,1000,10000]
color_stops = create_color_stops(color_breaks, colors='YlOrRd')
```

## rgb_tuple_from_str
Convert color represented as a string in format 'rgb(RRR,GGG,BBB)', 'rgba(RRR,GGG,BBB,alpha)', '#RRGGBB' or limited English color name (eg 'red') to tuple of integers from 0 to 255, (RRR, GGG, BBB).

### Params
**rgb_tuple_from_str**(_rgb_string_)

Parameter | Description
--|--
rgb_string | color represented as string in form 'rgb(RRR,GGG,BBB)', 'rgba(RRR,GGG,BBB,alpha)', '#RRGGBB', or limited HTML color names (eg 'red')

### Usage
```python
from mapboxgl.utils import rgb_tuple_from_str

# convert color string to tuple of integers
rgb_tuple_from_str('rgb(255,143,17')
```

## color_map
Convert color represented as a string in format 'rgb(RRR,GGG,BBB)' to tuple of integers from 0 to 255, (RRR, GGG, BBB).

### Params
**color_map**(_lookup, color_stops, default_color='rgb(122,122,122)'_)

Parameter | Description
--|--
lookup | value is numeric for interpolated colors or string for categorical color stops
color_stops | color ramp stops generated from `create_color_stops`, or custom list of numeric or categorical stops with paired colors
default_color | representation of color as hex, RGB, or RGBA strings

### Usage
```python
from mapboxgl.utils import create_color_stops, color_map

# interpolate color for numeric color_stops
color_stops = create_color_stops([0, 50, 100, 500, 1500], colors='YlOrRd')
color = color_map(73, color_stops)

# categorical look up
match_color_stops = [
    ['Massachusetts', 'rgb(46,204,113)'],
    ['Utah', 'rgb(231,76,60)'],
    ['California', 'rgb(142,68,173)'],
]
color = color_map('California', match_color_stops, default_color='grey)')
```
