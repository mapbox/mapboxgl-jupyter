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
Convert a Pandas dataframe to a geojson Python dictionary as a file

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
Scale a min and max value to equal interval domain with numStops discrete values

### Params
**scale_between**(_minval, maxval, numStops_)

Parameter | Description
--|--
minval | minimum value
maxval | maximum value
numStops | number of intervals

## create_radius_stops
Convert a data breaks into a radius ramp

### Params
**create_radius_stops**(_breaks, min_radius, max_radius_)

Parameter | Description
--|--
breaks | List of float values
min_radius | Minimum radius value
max_radius | Maximum radius value

## create_weight_stops
Convert data breaks into a heatmap-weight ramp

### Params
**create_weight_stops**(_breaks_)

Parameter | Description
--|--
breaks | List of float values

## create_color_stops
Convert a list of breaks into color stops using colors from colorBrewer.

### Params
**create_color_stops**(_breaks, colors='RdYlGn'_)

Parameter | Description
--|--
breaks | List of float values
colors | String value for color ramp.

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
