# mapboxgl-jupyter

Create [Mapbox GL JS](https://www.mapbox.com/mapbox-gl-js/api/) data visualizations natively in your Jupyter Notebook workflows with Python, GeoJSON and Pandas dataframes.


![image]()

## Installation

`pip install mapboxgl`

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
viz = CircleViz(data, color_property='Avg Total Payments',
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
2. cd to /example directory of mapboxgl-jupyter repo
2. `pip install jupyter`
3. `jupyter notebook`
4. Open `jupyter-mapboxgl-example` workbook
5. Put your [Mapbox GL Access Token](https://www.mapbox.com/help/how-access-tokens-work/) (it's free for developers!) into the notebook.
6. Run all cells in the notebook
7. View the location viz in the notebook in the final cell
    * ![](https://cl.ly/1r2s2t2Z2N0p/download/Image%202017-07-27%20at%203.06.54%20PM.png)


#### Notes on Mapbox Atlas

If you have access to Mapbox Atlas Server on your enterprise network, simply pass in your map stylesheet from your local Atlas URL as opposed to a `mapbox://` URL in cell 214.

```
# Put your Your Mapbox Access token here
# https://www.mapbox.com/help/how-access-tokens-work/
# If you use Mapbox Atlas, this isn't required.  Leave as an empty string.
mapbox_accesstoken = ''

# Map Style.  Point this to a local style, or a custom style on your Mapbox account or Atlas instance
mapStyle = "myAtlasUrl:myAtlasPort:/myStylesheetLocaiton"
```

