## Quick start
1. Signup for a [Mapbox Account](https://www.mapbox.com/signup/).
    * If you already have an account, grab your access token from the [account dashboard](https://www.mapbox.com/account/).

![tokens](https://user-images.githubusercontent.com/11286381/36569461-be9b0454-17e2-11e8-89c9-43e5a50bb7d0.png)


2. Install dependencies:  
`pip install mapboxgl pandas jupyter`
* If you are using a hosted jupyter notebook environment, install libraries from Jupyter using the `!` command in a cell:
    - `!pip install mapboxgl pandas jupyter`
3. Open a jupyter notebook by calling `jupyter notebook` from your command prompt or terminal. If your browser does not open automatically, navigate to http://localhost:8888/ in your browser window.
4. Import `mapboxgl-jupyter` into your notebook:
* `from mapboxgl.utils import *`
* `from mapboxgl.viz import *`
5. Create a visualization using the examples and documentation below. You'll need your [Mapbox token](https://www.mapbox.com/account/) from the first step.

[Here](https://www.mapbox.com/labs/jupyter/) is an example workbook
## class MapViz

The `MapViz` class is the parent class of the various `mapboxgl-jupyter` visualizations. You can use this class to set default values for all visualizations rather than calling them directly from the other visualization objects.

### Params
**MapViz**(_data, access_token=None, center=(0, 0), below_layer='', opacity=1, div_id='map', height='500px', style='mapbox://styles/mapbox/light-v9?optimize=true', width='100%', zoom=0, min_zoom=0, max_zoom=24, pitch=0, bearing=0_)

Parameter | Description
--|--
data | GeoJSON Feature Collection
access_token | Mapbox GL JS access token.
center | map center point
style | url to mapbox style or stylesheet as a Python dictionary in JSON format
div_id | The HTML div id of the map container in the viz
width | The CSS width of the HTML div id in % or pixels.
height | The CSS height of the HTML map div in % or pixels.
zoom | starting zoom level for map
opacity | opacity of map data layer
pitch | starting pitch (in degrees) for map
bearing | starting bearing (in degrees) for map

### Methods
**as_iframe**(_self, html_data_)  
Return the MapViz HTML representation in an iframe container using the srcdoc iframe attribute.

**show**(_self, **kwargs_)    
Display the visual in an iframe result cell of a Jupyter Notebook.

**create_html**(_self_)  
Build the HTML text representation of the visual. The output of this is a valid HTML document containing the visual object.

## class CircleViz

The `CircleViz` class handles the creation of a circle map and is built on top of the `MapViz` class.

### Params
**CircleViz**(_data, label_property=None, label_size=8, label_color='#131516', label_halo_color='white', label_halo_width=1, radius=1, color_property=None, color_stops=None, color_default='grey', color_function_type='interpolate', stroke_color='grey', stroke_width=0.1, \*args, \*\*kwargs_)

Parameter | Description
--|--
data | name of GeoJson file or object
label_property | property to use for marker label.  No labels will be shown if omitted
label_size | size of text labels
label_color | color of text labels
label_halo_color | color of text halo outline
label_halo_width | width (in pixels) of text halo outline
color_property | property to determine circle color
color_stops | property to determine circle color
color_default | color of circle to use if no lookup value matches the property value. Only used for the **match** color_function_type.
color_function_type | property to determine `type` used by Mapbox to assign color. One of "interpolate" or "match". Default is interpolate
stroke_color | color of circle outline stroke
stroke_width | width (in pixels) of circle outline stroke

[View options](https://github.com/mapbox/mapboxgl-jupyter/blob/master/docs-markdown/viz.md#params)

### Usage
```python
import pandas as pd
import os
from mapboxgl.utils import *
from mapboxgl.viz import *

# Load data from sample csv
data_url = 'https://raw.githubusercontent.com/mapbox/mapboxgl-jupyter/master/examples/points.csv'
df = pd.read_csv(data_url)

# Must be a public token, starting with `pk`
token = os.getenv('MAPBOX_ACCESS_TOKEN')

# Create a geojson file export from a Pandas dataframe
df_to_geojson(df, filename='points.geojson',
              properties=['Avg Medicare Payments', 'Avg Covered Charges', 'date'],
                     lat='lat', lon='lon', precision=3)

# Generate data breaks and color stops from colorBrewer
color_breaks = [0,10,100,1000,10000]
color_stops = create_color_stops(color_breaks, colors='YlGnBu')

# Create the viz from the dataframe
viz = CircleViz('points.geojson',
                access_token=token,
                height='400px',
                color_property = "Avg Medicare Payments",
                color_stops = color_stops,
                label_property = 'Avg Medicare Payments',
                stroke_color = 'black',
                center = (-95, 40),
                zoom = 3,
                below_layer = 'waterway-label'
              )
viz.show()
```

![CircleViz](https://user-images.githubusercontent.com/11286381/36511701-8ea5e64a-171c-11e8-8f27-6bc2f50319c9.png)


## class ClusteredCircleViz

The `ClusteredCircleViz` object handles the creation of a clustered circle map and is built on top of the `MapViz` class.  Cluster radius and color are keyed on point density.

### Params
**ClusteredCircleViz**(_data, label_size=8, label_color='#131516', label_halo_color='white', label_halo_width=1, color_stops=None, radius_stops=None, cluster_radius=30, cluster_maxzoom=14, radius_default=2, color_default='black', stroke_color='grey', stroke_width=0.1, \*args, \*\*kwargs_)

Parameter | Description
--|--
data | name of GeoJson file or object
label_size | size of text labels
label_color | color of text labels
label_halo_color | color of text halo outline
label_halo_width | width (in pixels) of text halo outline
color_stops | property to determine circle color
radius_stops | property to determine circle radius
cluster_radius | property to determine radius of each cluster when clustering points
cluster_maxzoom | property to determine the max zoom to use for clustering points
radius_default | Radius of points not contained in a cluster
color_default | Color of points not contained in a cluster
stroke_color | Color of stroke outline on circles
stroke_width | Width of stroke outline on circles

[View options](https://github.com/mapbox/mapboxgl-jupyter/blob/master/docs-markdown/viz.md#params)

### Usage
```python
import pandas as pd
import os
from mapboxgl.utils import *
from mapboxgl.viz import *

# Load data from sample csv
data_url = 'https://raw.githubusercontent.com/mapbox/mapboxgl-jupyter/master/examples/points.csv'
df = pd.read_csv(data_url)

# Must be a public token, starting with `pk`
token = os.getenv('MAPBOX_ACCESS_TOKEN')

# Create a geojson file export from a Pandas dataframe
df_to_geojson(df, filename='points.geojson',
              properties=['Avg Medicare Payments', 'Avg Covered Charges', 'date'],
                     lat='lat', lon='lon', precision=3)

#Create a clustered circle map
color_stops = create_color_stops([1,10,50,100], colors='BrBG')

viz = ClusteredCircleViz('points.geojson',
                          access_token=token,
                          color_stops = color_stops,
                          radius_stops = [[1,5], [10, 10], [50, 15], [100, 20]],
                          radius_default = 2,
                          cluster_maxzoom = 10,
                          cluster_radius = 30,
                          label_size = 12,
                          opacity = 0.9,
                          center = (-95, 40),
                          zoom = 3
                        )

viz.show()
```
![ClusteredCircleViz](https://user-images.githubusercontent.com/11286381/36511731-a4ca9af6-171c-11e8-9cde-60ef59e7e3b9.png)


## class GraduatedCircleViz

The `GraduatedCircleViz` object handles the creation of a graduated map and is built on top of the `MapViz` class.

### Params
**GraduatedCircleViz**(_data, label_property=None, label_size=8, label_color='#131516', label_halo_color='white', label_halo_width=1, color_property=None, color_stops=None, color_default='grey', color_function_type='interpolate', stroke_color='grey', stroke_width=0.1, radius_property=None, radius_stops=None, radius_default=2, radius_function_type='interpolate', \*args, \*\*kwargs_)

Parameter | Description
--|--
data | name of GeoJson file or object
label_property | property to use for marker label.
label_size | size of text labels
label_color | color of text labels
label_halo_color | color of text halo outline
label_halo_width | width (in pixels) of text halo outline
color_property | property to determine circle color.
color_stops | property to determine circle color.
color_default | color of the circle to use if no lookup value matches the property value. Only used for the **match** color_function_type.
color_function_type | property to determine `type` used by Mapbox to assign color. One of "interpolate" or "match". Default is interpolate.
radius_property | property to determine circle radius.
radius_stops | property to determine circle radius.
radius_default | radius of the circle to use if no lookup value matches the property value. Only used for the **match** radius_function_type.
radius_function_type | property to determine `type` used by Mapbox to assign radius size. One of "interpolate" or "match". Default is interpolate.
stroke_color | Color of stroke outline on circles
stroke_width | Width of stroke outline on circles

[View options](https://github.com/mapbox/mapboxgl-jupyter/blob/master/docs-markdown/viz.md#params)

### Usage
```python
import pandas as pd
import os
from mapboxgl.utils import *
from mapboxgl.viz import *

# Load data from sample csv
data_url = 'https://raw.githubusercontent.com/mapbox/mapboxgl-jupyter/master/examples/points.csv'
df = pd.read_csv(data_url)

# Must be a public token, starting with `pk`
token = os.getenv('MAPBOX_ACCESS_TOKEN')

# Create a geojson file export from a Pandas dataframe
df_to_geojson(df, filename='points.geojson',
              properties=['Avg Medicare Payments', 'Avg Covered Charges', 'date'],
                     lat='lat', lon='lon', precision=3)

# Generate color stops from colorBrewer
measure_color = 'Avg Covered Charges'
color_breaks = [round(df[measure_color].quantile(q=x*0.1), 2) for x in range(2, 10)]
color_stops = create_color_stops(color_breaks, colors='Blues')

# Generate radius breaks from data domain and circle-radius range
measure_radius = 'Avg Medicare Payments'
radius_breaks = [round(df[measure_radius].quantile(q=x*0.1), 2) for x in range(2,10)]
radius_stops = create_radius_stops(radius_breaks, 0.5, 10)

# Create the viz
viz = GraduatedCircleViz('points.geojson',
                          access_token=token,
                          color_property = "Avg Covered Charges",
                          color_stops = color_stops,
                          radius_property = "Avg Medicare Payments",
                          stroke_color = 'black',
                          stroke_width = 0.5,
                          radius_stops = radius_stops,
                          center = (-95, 40),
                          zoom = 3,
                          below_layer = 'waterway-label'
                        )

viz.show()
```
![GraduatedCircleViz](https://user-images.githubusercontent.com/11286381/36511755-b58e6cc8-171c-11e8-9385-e90c3795be14.png)


## class HeatmapViz

The `HeatmapViz` object handles the creation of a heat map and is built on top of the `MapViz` class.

### Params
**HeatmapViz**(_data, weight_property=None, weight_stops=None, color_stops=None, radius_stops=None, intensity_stops=None, \*args, \*\*kwargs_)

Parameter | Description | Example
--|--|--
data | name of GeoJson file or object
weight_property | property to determine heatmap weight. | "population"
weight_stops | stops to determine heatmap weight. | [[10, 0], [100, 1]]
color_stops | stops to determine heatmap color. | [[0, "red"], [0.5, "blue"], [1, "green"]]
radius_stops | stops to determine heatmap radius based on zoom. | [[0, 1], [12, 30]]
intensity_stops | stops to determine the heatmap intensity based on zoom. EX: [[0, 0.1], [20, 5]]

[View options](https://github.com/mapbox/mapboxgl-jupyter/blob/master/docs-markdown/viz.md#params)

### Usage
```python
import pandas as pd
import os
from mapboxgl.utils import *
from mapboxgl.viz import *

# Load data from sample csv
data_url = 'https://raw.githubusercontent.com/mapbox/mapboxgl-jupyter/master/examples/points.csv'
df = pd.read_csv(data_url)

# Must be a public token, starting with `pk`
token = os.getenv('MAPBOX_ACCESS_TOKEN')

# Create a geojson file export from a Pandas dataframe
df_to_geojson(df, filename='points.geojson',
              properties=['Avg Medicare Payments', 'Avg Covered Charges', 'date'],
                     lat='lat', lon='lon', precision=3)

#Create a heatmap
heatmap_color_stops = create_color_stops([0.01,0.25,0.5,0.75,1], colors='RdPu')
heatmap_radius_stops = [[0,1], [15, 40]] #increase radius with zoom

color_breaks = [0,10,100,1000,10000]
color_stops = create_color_stops(color_breaks, colors='Spectral')

heatmap_weight_stops = create_weight_stops(color_breaks)

#Create a heatmap
viz = HeatmapViz('points.geojson',
                  access_token=token,
                  weight_property = "Avg Medicare Payments",
                  weight_stops = heatmap_weight_stops,
                  color_stops = heatmap_color_stops,
                  radius_stops = heatmap_radius_stops,
                  opacity = 0.9,
                  center = (-95, 40),
                  zoom = 3,
                  below_layer='waterway-label'
                )

viz.show()
```
![HeatmapViz](https://user-images.githubusercontent.com/11286381/36511775-cfc4d794-171c-11e8-86b9-5f1a6060a387.png)


## class ChoroplethViz

The `ChoroplethViz` object handles the creation of a choropleth map and inherits from the `MapViz` class. It applies a thematic map style to polygon features with color shading in proportion to the intensity of the data being displayed. Choropleth polygons can be initialized with geojson source or vector source styled using the data-join technique.

### Params
**ChoroplethViz**(_data, vector_url=None, vector_layer_name=None, vector_join_property=None, data_join_property=None, # vector only label_property=None, color_property=None, color_stops=None, color_default='grey', color_function_type='interpolate', line_color='white', line_stroke='solid', line_width=1, height_property=None, height_stops=None, height_default=0.0, height_function_type='interpolate', *args, **kwargs_)

Parameter | Description | Example
--|--|--
data | can be either GeoJSON (containing polygon features) or JSON for data-join technique with vector polygons |
vector_url | optional property to define vector polygon source | "mapbox://mapbox.us_census_states_2015"
vector_layer_name | property to define target layer of vector source if using vector polygon source | "states"
vector_join_property | property to aid in determining color for styling vector polygons | "STATEFP"
data_join_property | property of json data to use as link to vector features | "state_name"
label_property | property to use for marker label | "density"
color_property | property to determine fill color | "density"
color_stops | property to determine fill color | [[0, "red"], [0.5, "blue"], [1, "green"]]
color_default | property to determine default fill color in match lookups | "#F0F0F0"
color_function_type | property to determine type of expression used by Mapbox to assign color | "interpolate"
line_color | property to determine choropleth border line color | "#FFFFFF"
line_stroke | property to determine choropleth border line stroke (one of solid (-), dashed (--), dotted (:), dash dot (-.)) | "solid" or "-"
line_width | property to determine choropleth border line width | 1
height_property | feature property for determining polygon height in 3D extruded choropleth map | "density"
height_stops | property for determining 3D extrusion height | [[0, 0], [500, 50000], [1500, 150000]]
height_default | default height (in meters) for 3D extruded polygons on map | 1500.0
height_function_type | roperty to determine `type` used by Mapbox to assign height | "interpolate"

[View options](https://github.com/mapbox/mapboxgl-jupyter/blob/master/docs-markdown/viz.md#params)

### Usage
```python
import os
from mapboxgl.viz import *
from mapboxgl.utils import *

# Must be a public token, starting with `pk`
token = os.getenv('MAPBOX_ACCESS_TOKEN')

# Create Choropleth with GeoJSON Source
viz = ChoroplethViz('us-states.geojson', 
                     color_property='density',
                     color_stops=create_color_stops([0, 50, 100, 500, 1500], colors='YlOrRd'),
                     color_function_type='interpolate',
                     line_stroke='--',
                     line_color='rgb(128,0,38)',
                     line_width=1,
                     opacity=0.8,
                     center=(-96, 37.8),
                     zoom=3,
                     below_layer='waterway-label'
                    )
viz.show()
```
![ChoroplethViz](https://user-images.githubusercontent.com/13527707/37823022-73782a0a-2e45-11e8-9fdd-4a8ddd35cb92.png)


[Complete example](https://github.com/mapbox/mapboxgl-jupyter/blob/master/examples/choropleth-viz-example.ipynb)


## class ImageViz

The `ImageViz` object handles the creation of a simple image visualization on map and is built on top of the `MapViz` class.

### Params
**ImageViz**(image, coordinates, \*args, \*\*kwargs_)

Parameter | Description | Example
--|--|--
image | image url, path or numpy ndarray | "./my_image.png"
coordinates | property to image coordinates (UL, UR, LR, LL) | [[-80.425, 46.437], [-71.516, 46.437], [-71.516, 37.936], [-80.425, 37.936]]

[MapViz options](https://github.com/mapbox/mapboxgl-jupyter/blob/master/docs-markdown/viz.md#params)

### Usage
```python
from mapboxgl.viz import ImageViz

img_url = 'https://raw.githubusercontent.com/mapbox/mapboxgl-jupyter/master/examples/mosaic.jpg'

# Coordinates must be an array in the form of [UL, UR, LR, LL]
coordinates = [
    [-123.40515640309, 38.534294809274336],
    [-115.92938988349292, 38.534294809274336],
    [-115.92938988349292, 32.08296982365502],
    [-123.40515640309, 32.08296982365502]]

# Create the viz
viz = ImageViz(img_url, coordinates, access_token=token,
                height='600px',
                center = (-119, 35),
                zoom = 5,
                below_layer = 'waterway-label')
viz.show()
```
![ImageViz](https://user-images.githubusercontent.com/10407788/37532428-5c8ff7a8-2915-11e8-8d03-2b258a0a53a8.jpg)

[Complete example](https://github.com/mapbox/mapboxgl-jupyter/blob/master/examples/image-viz-types-example.ipynb)


## class RasterTilesViz

The `RasterTilesViz` object handles the creation of a simple raster tiles visualization on map and is built on top of the `MapViz` class.

### Params
**RasterTilesViz**(tiles\_url, \*args, \*\*kwargs_)

Parameter | Description | Example
--|--|--
tiles_url | tiles endpoint | "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
tiles_size | mapbox-gl tiles size | 256
tiles_bounds | tiles endpoint bounds | [124.97480681619507, 10.876763902260592, 124.99391704636035, 10.888369402219947]
tiles_minzoom | tiles endpoint min zoom | 0
tiles_maxzoom | tiles endpoint max zoom | 22



[MapViz options](https://github.com/mapbox/mapboxgl-jupyter/blob/master/docs-markdown/viz.md#params)

### Usage
```python
from mapboxgl.viz import RasterTilesViz

tiles_url = 'https://cogeo.remotepixel.ca/tiles/{z}/{x}/{y}.jpg?tile=256&nodata=0&url=http://oin-hotosm.s3.amazonaws.com/594ab0ba1b114600111194a3/0/d66720c4-148c-4e11-9d54-4ae2a6ba6351.tif'

# Define the tile endpoint bounds
tiles_bounds = [124.97480681619507, 10.876763902260592, 124.99391704636035, 10.888369402219947]
tiles_center = [124.9843619312777, 10.88256665224027]

viz = RasterTilesViz(tiles_url,
                     tiles_size=256,
                     tiles_bounds=tiles_bounds,
                     height='500px',
                     center=tiles_center,
                     tiles_minzoom=13,
                     tiles_maxzoom=18,
                     zoom=16)
viz.show()
```
![RasterTilesViz](https://user-images.githubusercontent.com/10407788/37537676-b055a108-2924-11e8-94cb-ad3203b736af.jpg)


[Complete example](https://github.com/mapbox/mapboxgl-jupyter/blob/master/examples/rastertile-viz-types-example.ipynb)


## class LinestringViz

The `LinestringViz` object handles the creation of a vector or GeoJSON-based Linestring visualization and inherits from the `MapViz` class.

### Params
**LinestringViz**(_data, vector_url=None, vector_layer_name=None, vector_join_property=None, data_join_property=None, label_property=None, label_size=8, label_color='#131516', label_halo_color='white', label_halo_width=1, color_property=None, color_stops=None, color_default='grey', color_function_type='interpolate', line_stroke='solid', line_width_property=None, line_width_stops=None, line_width_default=1, line_width_function_type='interpolate', *args, **kwargs_)


Parameter | Description | Example
--|--|--
data | can be either GeoJSON (containing polygon features) or JSON for data-join technique with vector polygons |
vector_url | optional property to define vector linestring source | "mapbox://mapbox.mapbox-terrain-v2"
vector_layer_name | property to define target layer of vector source if using vector linestring source | "contour"
vector_join_property | property to aid in determining color for styling vector lines | "ele"
data_join_property | property of json data to use as link to vector features | "elevation"
label_property | property to use for marker label | "elevation"
label_size | size of label text | 8
label_color | color of label text | '#131516'
label_halo_color | color of label text halo | 'white'
label_halo_width | width of label text halo | 1
color_property | property to determine line color | "elevation"
color_stops | property to determine line color | [[0, "red"], [0.5, "blue"], [1, "green"]]
color_default | property to determine default line color if match lookup fails | "#F0F0F0"
color_function_type | property to determine type of expression used by Mapbox to assign color | "interpolate"
line_stroke | property to determine line stroke (one of solid (-), dashed (--), dotted (:), dash dot (-.)) | "solid" or "-"
line_width_property | feature property for determining line width | "elevation"
line_width_stops | property to determine line width | [[0, 1], [50000, 2], [150000, 3]]
line_width_default | property to determine default line width if match lookup fails | 1.0
line_width_function_type | property to determine `type` used by Mapbox to assign line width | "interpolate"

[MapViz options](https://github.com/mapbox/mapboxgl-jupyter/blob/master/docs-markdown/viz.md#params)

### Usage
```python
import random
import os

from mapboxgl.viz import LinestringViz
from mapboxgl.utils import create_color_stops

# Must be a public token, starting with `pk`
token = os.getenv('MAPBOX_ACCESS_TOKEN')

# JSON join-data object
data = [{"elevation": x, "weight": random.randint(0,100)} for x in range(0, 21000, 10)]

viz = LinestringViz(data, 
                    vector_url='mapbox://mapbox.mapbox-terrain-v2',
                    vector_layer_name='contour',
                    vector_join_property='ele',
                    data_join_property='elevation',
                    color_property='elevation',
                    color_stops=create_color_stops([0, 25, 50, 75, 100], colors='YlOrRd'),
                    line_stroke='-',
                    line_width_default=2,
                    opacity=0.8,
                    center=(-122.48, 37.83),
                    zoom=16,
                    below_layer='waterway-label'
                   )
viz.show()
```

![LinestringViz](https://user-images.githubusercontent.com/13527707/39278071-02b6b2fc-48a6-11e8-8492-ae1f991b4b9e.png)


[Complete example](https://github.com/mapbox/mapboxgl-jupyter/blob/master/examples/notebooks/linestring-viz.ipynb)

