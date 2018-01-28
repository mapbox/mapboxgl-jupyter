# mapboxgl-jupyter

[![Build Status](https://travis-ci.org/mapbox/mapboxgl-jupyter.svg?branch=master)](https://travis-ci.org/mapbox/mapboxgl-jupyter)
[![Coverage Status](https://coveralls.io/repos/github/mapbox/mapboxgl-jupyter/badge.svg?branch=master)](https://coveralls.io/github/mapbox/mapboxgl-jupyter?branch=master)
[![PyPI version](https://badge.fury.io/py/mapboxgl.svg)](https://badge.fury.io/py/mapboxgl)

Create [Mapbox GL JS](https://www.mapbox.com/mapbox-gl-js/api/) data visualizations natively in your Jupyter Notebook workflows with Python, GeoJSON and Pandas dataframes.  Mapboxgl aims to be a data visualization focused mapping library built on top of the [Mapbox GL JS SDK](https://www.mapbox.com/mapbox-gl-js/api/), similar to [Folium](https://github.com/python-visualization/folium) built on top of [Leaflet](http://leafletjs.com/).

Try out an example notebook [here](https://www.mapbox.com/labs/jupyter)!

![image](https://raw.githubusercontent.com/mapbox/mapboxgl-jupyter/master/examples/screenshot.png)

## Installation

`pip install mapboxgl`

## Development

Install the python library locally with pip:

`pip install -e .`

To run tests use pytest:

`pip install pytest`
`pytest`

To run the jupiter examples, 

1. `cd examples`
2. `pip install jupyter`
2. `jupyter notebook`

## Usage

Import the mapboxgl library and helper functions to start:

```
from mapboxgl.viz import *
from mapboxgl.utils import *
from mapboxgl.colors import *
```

`mapboxgl` visualizations take GeoJSON data as input.
You can convert `pandas` dataframes to a GeoJSON feature collection:

```
data = df_to_geojson(df, ['Avg Total Payments'],
                     lat='latitude', lon='longitude')
```

Using the `CircleViz` visualization to view the data with
a color ramp for the total payment column. Within a Jupyter
notebook:

```
viz = CircleViz(data,
                color_property='Avg Total Payments',
                color_stops=color_stops,
                access_token=YOUR_PUBLIC_ACCESS_TOKEN)
viz.show()
```

The `examples/` directory contains Jupyter notebooks
demonstrating more advanced usage.

## API

### Viz Types

* CircleViz (data, access_token, center, color_property, color_stops,
             label_property, opacity, below_layer, div_id, height, 
             style_url, width, zoom)
* GraduatedCircleViz (data, access_token, center, color_property, color_stops,
             radius_property, radius_stops, opacity, below_layer, div_id, height, 
             style_url, width, zoom)
* HeatmapViz (data, access_token, center, weight_property, weight_stops, 
              color_stops, radius_stops, opacity, below_layer, div_id, height, 
              style_url, width, zoom)
* ClusteredCircleViz (data, access_token, center, color_stops, radius_stops,
              cluster_radius, cluster_maxzoom, opacity, below_layer, div_id, height, 
              style_url, width, zoom)

### Helper Functions

* df_to_geojson (df, properties, lat, lon, precision)
* scale_between (minval, maxval, numStops)
* create_radius_stops (breaks, min_radius, max_radius)
* create_weight_stops (breaks)

## Status

Under heavy development. As we move towards a 1.0 release, expect
API changes. If you're interested in contributing and are 
curious about the direction of the project, check out `ROADMAP.md`.

## Running Example

1. Install Python3.4+
2. `pip install mapboxgl && pip install pysal && pip install pandas`
2. cd to `/examples` directory of `mapboxgl-jupyter` repo
4. Open the `point-viz-types-example.ipynb` workbook
5. Put your [Mapbox GL Access Token](https://www.mapbox.com/help/how-access-tokens-work/) (it's free for developers!) or add it to your environment variables as `MAPBOX_ACCESS_TOKEN`.
6. Run all cells in the notebook and explore the interactive maps.

# Release process

- After merging all relevant PRs for the upcoming release, pull the master branch
    git checkout master
    git pull


- Update the version number in `mapboxgl/__init__.py` and push directly to master.


- Tag the release
    git tag <version>
    git push --tags


- Setup for pypi (one time only) - You'll need to `pip install twine` and set up your credentials in a `[~/.pypirc](https://docs.python.org/2/distutils/packageindex.html#pypirc)` [file](https://docs.python.org/2/distutils/packageindex.html#pypirc).


- Create the release files
    rm dist/*  # clean out old releases if they exist
    python setup.py sdist bdist_wheel


- Upload the release files
    twine upload dist/mapboxgl-*
