import os

import pandas as pd

from mapboxgl.utils import df_to_geojson
from mapboxgl.viz import *

token = os.environ.get('MAPBOX_ACCESS_TOKEN', '')


@pd.api.extensions.register_dataframe_accessor('mapbox')
class GeoAccessor(object):
    """
    https://pandas.pydata.org/pandas-docs/stable/extending.html
    """
    
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    @property
    def center(self):
        # return the geographic center point of this DataFrame
        lat = self._obj.lat
        lon = self._obj.lon
        return (float(lon.mean()), float(lat.mean()))

    def draw_map(self, color_property, color_stops):
        
        data = df_to_geojson(self._obj, 
                             properties=['Avg Medicare Payments', 
                                         'Avg Covered Charges', 
                                         'date'], 
                             lat='lat', 
                             lon='lon', 
                             precision=3)
        
        viz = CircleViz(data, 
                        access_token=token, 
                        color_property=color_property,
                        color_stops=color_stops,
                        radius=2, 
                        center=(-95, 40), 
                        zoom=3)
        
        viz.show()

