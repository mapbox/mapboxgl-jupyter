<a href="https://www.mapbox.com">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Mapbox_Logo.svg/1280px-Mapbox_Logo.svg.png" width="500"/>
</a>

# Data Visualization for Python and Jupyter Noteobok

[![Build Status](https://travis-ci.org/mapbox/mapboxgl-jupyter.svg?branch=master)](https://travis-ci.org/mapbox/mapboxgl-jupyter)
[![Coverage Status](https://coveralls.io/repos/github/mapbox/mapboxgl-jupyter/badge.svg?branch=master)](https://coveralls.io/github/mapbox/mapboxgl-jupyter?branch=master)
[![PyPI version](https://badge.fury.io/py/mapboxgl.svg)](https://badge.fury.io/py/mapboxgl)

Create [Mapbox GL JS](https://www.mapbox.com/mapbox-gl-js/api/) data visualizations natively in Jupyter Notebook workflows with Python and Pandas.  `mapboxgl` aims to be a high-performance, interactive data visualization tool that drops directly into your data science workflow.  It's similar to [Folium](https://github.com/python-visualization/folium) built on top of [Leaflet](http://leafletjs.com/), but can visualize much larger vector data sets easily.

Try out an example notebook [here](https://www.mapbox.com/labs/jupyter).

## Installation

`pip install mapboxgl`

# Documentation

Checkout the documentation for [mapboxgl visuals](https://github.com/mapbox/mapboxgl-jupyter/blob/master/docs-markdown/viz.md) and [mapboxgl utilities](https://github.com/mapbox/mapboxgl-jupyter/blob/master/docs-markdown/utils.md).

## Usage

The `examples/` directory contains sample Jupyter notebooks demonstrating usage.  

```
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

# Release process

- After merging all relevant PRs for the upcoming release, pull the master branch
    * `git checkout master`
    * `git pull`
- Update the version number in `mapboxgl/__init__.py` and push directly to master.
- Tag the release
    * `git tag <version>`
    * `git push --tags`
- Setup for pypi (one time only)
    * You'll need to `pip install twine` and set up your credentials in a [~/.pypirc](https://docs.python.org/2/distutils/packageindex.html#pypirc) [file](https://docs.python.org/2/distutils/packageindex.html#pypirc).
- Create the release files
    * `rm dist/*`  # clean out old releases if they exist
    * `python setup.py sdist bdist_wheel`
- Upload the release files
    * `twine upload dist/mapboxgl-*`
