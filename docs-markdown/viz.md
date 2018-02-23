## Quick start
1. Signup for a [Mapbox Account](https://www.mapbox.com/signup/). 
    * If you already have an account, grab your access token from the [account dashboard](https://www.mapbox.com/account/).

<img width="1175" alt="e3b76b4e9effe60170379326885d7144 _image 2018-02-22 at 3 11 09 pm" src="https://user-images.githubusercontent.com/11286381/36569461-be9b0454-17e2-11e8-89c9-43e5a50bb7d0.png">


2. Install dependencies:  
`pip install mapboxgl pandas jupyter`
* If you are using a hosted jupyter notebook environment, install libraries from Jupyter using the `!` command in a cell:
    - `!pip install mapboxgl pandas jupyter`
3. Open a jupyter notebook by calling `jupyter notebook` from your command prompt of terminal. If your browser does not open automatically, go to http://localhost:8888/ in your browser window.
4. Import `mapboxgl-jupyter` with:
* `from mapboxgl.utils import *`
* `from mapboxgl.viz import *`
5. Create a visualization using the examples and documentation below. You'll need your [Mapbox token](https://www.mapbox.com/account/) from the first step.

[Here](https://www.mapbox.com/labs/jupyter/) is an example workbook
## class MapViz

The `MapViz` class is the parent class of the various `mapboxgl-jupyter` visualizations. You can use this class to set default values for all visualizations rather than calling them directly from the other visualization objects.

### Params
**MapViz**(_data, access_token=None, center=(0, 0), below_layer='', opacity=1, div_id='map', height='500px', style_url='mapbox://styles/mapbox/light-v9?optimize=true', width='100%', zoom=0, min_zoom=0, max_zoom=24_)

Parameter | Description
--|--
data | GeoJSON Feature Collection
access_token | Mapbox GL JS access token.
center | map center point
style_url | url to mapbox style
div_id | The HTML div id of the map container in the viz
width | The CSS width of the HTML div id in % or pixels.
height | The CSS height of the HTML map div in % or pixels.
zoom | starting zoom level for map
opacity | opacity of map data layer

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
**CircleViz**(_data, label_property=None, color_property=None, color_stops=None, color_default='grey', color_function_type='interpolate', *args, **kwargs_)

Parameter | Description
--|--
data | name of GeoJson file or object
label_property | property to use for marker label
color_property | property to determine circle color
color_stops | property to determine circle color
color_default | color of circle to use if no lookup value matches the property value. Only used for the **match** color_function_type.
color_function_type | property to determine `type` used by Mapbox to assign color. One of "interpolate" or "match". Default is interpolate

[View options](https://github.com/mapbox/mapboxgl-jupyter/blob/add-markdown-docs/docs-markdown/viz.md#params-4)

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
                center = (-95, 40),
                zoom = 3,
                below_layer = 'waterway-label'
              )
viz.show()
```

![screen shot 2018-02-21 at 3 02 44 pm](https://user-images.githubusercontent.com/11286381/36511701-8ea5e64a-171c-11e8-8f27-6bc2f50319c9.png)


## class ClusteredCircleViz

The `ClusteredCircleViz` object handles the creation of a clustered circle map and is built on top of the `MapViz` class.

### Params
**ClusteredCircleViz**(_data, color_stops=None, radius_stops=None, cluster_radius=30, cluster_maxzoom=14, *args, **kwargs_)

Parameter | Description
--|--
data | name of GeoJson file or object
color_property | property to determine circle color
color_stops | property to determine circle color
radius_property | property to determine circle radius
radius_stops | property to determine circle radius

[View options](https://github.com/mapbox/mapboxgl-jupyter/blob/add-markdown-docs/docs-markdown/viz.md#params-4)

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
                          cluster_maxzoom = 10,
                          cluster_radius = 30,
                          opacity = 0.9,
                          center = (-95, 40),
                          zoom = 3
                        )

viz.show()
```
![screen shot 2018-02-21 at 3 33 46 pm](https://user-images.githubusercontent.com/11286381/36511731-a4ca9af6-171c-11e8-9cde-60ef59e7e3b9.png)


## class GraduatedCircleViz

The `GraduatedCircleViz` object handles the creation of a graduated map and is built on top of the `MapViz` class.

### Params
**GraduatedCircleViz**(_data, label_property=None, color_property=None, color_stops=None, color_default='grey', color_function_type='interpolate', radius_property=None, radius_stops=None, radius_default=None, radius_function_type='interpolate', *args, **kwargs_)

Parameter | Description
--|--
data | name of GeoJson file or object
label_property | property to use for marker label.
color_property | property to determine circle color.
color_stops | property to determine circle color.
color_default | color of the circle to use if no lookup value matches the property value. Only used for the **match** color_function_type.
color_function_type | property to determine `type` used by Mapbox to assign color. One of "interpolate" or "match". Default is interpolate.
radius_property | property to determine circle radius.
radius_stops | property to determine circle radius.
radius_default | radius of the circle to use if no lookup value matches the property value. Only used for the **match** radius_function_type.
radius_function_type | property to determine `type` used by Mapbox to assign radius size. One of "interpolate" or "match". Default is interpolate.

[View options](https://github.com/mapbox/mapboxgl-jupyter/blob/add-markdown-docs/docs-markdown/viz.md#params-4)

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

# Generate radius breaks from data domain and circle-radius range
radius_breaks = [0,10,100,1000,10000]
radius_stops = create_radius_stops(radius_breaks, 1, 10)

# Create the viz
viz = GraduatedCircleViz('points.geojson',
                          access_token=token,
                          color_property = "Avg Covered Charges",
                          color_stops = color_stops,
                          radius_property = "Avg Medicare Payments",
                          radius_stops = radius_stops,
                          center = (-95, 40),
                          zoom = 3,
                          below_layer = 'waterway-label'
                        )

viz.show()
```
![screen shot 2018-02-21 at 3 34 18 pm](https://user-images.githubusercontent.com/11286381/36511755-b58e6cc8-171c-11e8-9385-e90c3795be14.png)


## class HeatmapViz

The `HeatmapViz` object handles the creation of a heat map and is built on top of the `MapViz` class.

### Params
**HeatmapViz**(_data, weight_property=None, weight_stops=None, color_stops=None, radius_stops=None, *args, **kwargs_)

Parameter | Description | Example
--|--|--
data | name of GeoJson file or object
weight_property | property to determine heatmap weight. | "population"
weight_stops | stops to determine heatmap weight. | [[10, 0], [100, 1]]
color_stops | stops to determine heatmap color. | [[0, "red"], [0.5, "blue"], [1, "green"]]
radius_stops | stops to determine heatmap radius based on zoom. | [[0, 1], [12, 30]]

[View options](https://github.com/mapbox/mapboxgl-jupyter/blob/add-markdown-docs/docs-markdown/viz.md#params-4)

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
![screen shot 2018-02-21 at 3 34 55 pm](https://user-images.githubusercontent.com/11286381/36511775-cfc4d794-171c-11e8-86b9-5f1a6060a387.png)
