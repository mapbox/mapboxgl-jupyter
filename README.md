# mapboxgl-jupyter

[![Build Status](https://travis-ci.org/mapbox/mapboxgl-jupyter.svg?branch=master)](https://travis-ci.org/mapbox/mapboxgl-jupyter)
[![Coverage Status](https://coveralls.io/repos/github/mapbox/mapboxgl-jupyter/badge.svg?branch=master)](https://coveralls.io/github/mapbox/mapboxgl-jupyter?branch=master)
[![PyPI version](https://badge.fury.io/py/mapboxgl.svg)](https://badge.fury.io/py/mapboxgl)

Create [Mapbox GL JS](https://www.mapbox.com/mapbox-gl-js/api/) data visualizations natively in your Jupyter Notebook workflows with Python, GeoJSON and Pandas dataframes.  Mapboxgl aims to be a data visualization focused mapping library built on top of the [Mapbox GL JS SDK](https://www.mapbox.com/mapbox-gl-js/api/), similar to [Folium](https://github.com/python-visualization/folium) built on top of [Leaflet](http://leafletjs.com/).

Currently supported map visualization types:

1. Circles
2. Graduated Circles
3. Heatmaps


![image](https://raw.githubusercontent.com/mapbox/mapboxgl-jupyter/master/examples/screenshot.png)



## Installation

`pip install mapboxgl`

## Development

Install the python library locally with pip:

`pip install -e .`

To run tests use pytest:

`pytest`

To run the jupiter examples, 

1. `cd examples`
2. `pip install jupyter`
2. `jupyter notebook`

## Usage

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

## Status

Under heavy development. As we move towards a 1.0 release, expect
API changes. If you're interested in contributing and are 
curious about the direction of the project, check out `ROADMAP.md`.

## Running the Examples

1. Install Python3.4+
2. `pip install mapboxgl`
2. cd to /example directory of mapboxgl-jupyter repo
4. Open the `test-python.ipynb` workbook
5. Put your [Mapbox GL Access Token](https://www.mapbox.com/help/how-access-tokens-work/) (it's free for developers!) into the notebook, cell 4.
6. Run all cells in the notebook and enjoy the interactive maps.

