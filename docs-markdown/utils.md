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
Serialize a Pandas dataframe to a geojson format Python dictionary

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

# Load sample gage data (https://cdec.water.ca.gov/cgi-progs/staSearch)
df = pd.read_csv('cdec.csv')

# Convert Elevation series to float
df['Elevation (feet)'] = df['Elevation (feet)'].astype(float)

# Clean up by dropping null rows
df = df.dropna(axis=1, how='all')

# Create geojson data object
df_to_geojson(
      df.fillna(''),
      filename="cdec.geojson",
      properties=['CDEC ID', 'CNRFC ID', 'Gage Type', 'Elevation (feet)'],
      precision=4
)
>>> {'feature_count': 2353, 'filename': 'cdec.geojson', 'type': 'file'}
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
breaks |
min_radius |
max_radius |

## create_weight_stops
Convert data breaks into a heatmap-weight ramp

### Params
**create_weight_stops**(_breaks_)

Parameter | Description
--|--
breaks |

## create_color_stops
Convert a list of breaks into color stops using colors from colorBrewer see www.colorbrewer2.org for a list of color options to pass

### Params
**create_color_stops**(_breaks, colors='RdYlGn', color_ramps=color_ramps_)

Parameter | Description
--|--
breaks |
colors |
color_ramps |
