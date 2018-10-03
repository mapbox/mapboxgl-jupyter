from .map import Map
from .layers import (
    CircleLayer,
    GraduatedCircleLayer,
    HeatmapLayer,
    ClusteredCircleLayer,
    ImageLayer,
    RasterTilesLayer,
    ChoroplethLayer,
    LinestringLayer,
)

from IPython.core.display import HTML, display

class MapViz(object):

    def __init__(self,
                 data,
                 access_token=None,
                 center=(0, 0),
                 below_layer='',
                 opacity=1,
                 div_id='map',
                 height='500px',
                 style='mapbox://styles/mapbox/light-v9?optimize=true',
                 width='100%',
                 zoom=0,
                 pitch=0,
                 bearing=0,
                 box_zoom_on=True,
                 double_click_zoom_on=True,
                 scroll_zoom_on=True,
                 touch_zoom_on=True,
                 legend=True,
                 legend_layout='vertical',
                 legend_gradient=False,
                 legend_style='',
                 legend_fill='white',
                 legend_header_fill='white',
                 legend_text_color='#6e6e6e',
                 legend_text_numeric_precision=None,
                 legend_title_halo_color='white',
                 legend_key_shape='square',
                 legend_key_borders_on=True):
        """Construct a MapViz object

        :param data: GeoJSON Feature Collection
        :param access_token: Mapbox GL JS access token.
        :param center: map center point
        :param style: url to mapbox style or stylesheet as a Python dictionary in JSON format
        :param div_id: The HTML div id of the map container in the viz
        :param width: The CSS width of the HTML div id in % or pixels.
        :param height: The CSS height of the HTML map div in % or pixels.
        :param zoom: starting zoom level for map
        :param opacity: opacity of map data layer
        :param pitch: starting pitch (in degrees) for map
        :param bearing: starting bearing (in degrees) for map
        :param box_zoom_on: boolean indicating if map can be zoomed to a region by dragging a bounding box
        :param double_click_zoom_on: boolean indicating if map can be zoomed with double-click
        :param scroll_zoom_on: boolean indicating if map can be zoomed with the scroll wheel
        :param touch_zoom_on: boolean indicating if map can be zoomed with two-finger touch gestures
        :param legend: boolean for whether to show legend on map
        :param legend_layout: determines if horizontal or vertical legend used
        :param legend_style: reserved for future custom CSS loader
        :param legend_gradient: boolean to determine if legend keys are discrete or gradient
        :param legend_fill: string background color for legend, default is white
        :param legend_header_fill: string background color for legend header (in vertical layout), default is #eee
        :param legend_text_color: string color for legend text default is #6e6e6e
        :param legend_text_numeric_precision: decimal precision for numeric legend values
        :param legend_title_halo_color: color of legend title text halo
        :param legend_key_shape: shape of the legend item keys, default varies by viz type; one of square, contiguous_bar, rounded-square, circle, line
        :param legend_key_borders_on: boolean for whether to show/hide legend key borders

        """
        self.__dict__['map'] = Map(
            access_token=access_token,
            center=center,
            opacity=opacity,
            div_id=div_id,
            height=height,
            style=style,
            width=width,
            zoom=zoom,
            pitch=pitch,
            bearing=bearing,
            box_zoom_on=box_zoom_on,
            double_click_zoom_on=double_click_zoom_on,
            scroll_zoom_on=scroll_zoom_on,
            touch_zoom_on=touch_zoom_on,
            legend_fill=legend_fill,
            legend_header_fill=legend_header_fill,
            legend_text_color=legend_text_color,
            legend_title_halo_color=legend_title_halo_color,
            legend_key_borders_on=legend_key_borders_on
        )

        self.__dict__['layer'] = None

    def __setattr__(self, name, value):
        if hasattr(self.map, name):
            self.map.__dict__[name] = value
        elif hasattr(self.layer, name):
            self.layer.__dict__[name] = value


    def as_iframe(self, html_data):
        """Build the HTML representation for the mapviz."""
        return self.map.as_iframe(html_data)

    def show(self, **kwargs):
        # Load the HTML iframe
        self.map.show(**kwargs)

    def add_unique_template_variables(self, options):
        pass

    def create_html(self, filename=None):
        """Create a circle visual from a geojson data source"""
        return self.map.create_html(filename)


class CircleViz(MapViz):
    """Create a circle map"""

    def __init__(self,
                 data,
                 label_property=None,
                 label_size=8,
                 label_color='#131516',
                 label_halo_color='white',
                 label_halo_width=1,
                 radius=1,
                 color_property=None,
                 color_stops=None,
                 color_default='grey',
                 color_function_type='interpolate',
                 stroke_color='grey',
                 stroke_width=0.1,
                 legend_key_shape='circle',
                 min_zoom=0,
                 max_zoom=24,
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param label_property: property to use for marker label
        :param label_size: size of label text
        :param label_color: color of label text
        :param label_halo_color: color of label text halo
        :param label_halo_width: width of label text halo
        :param color_property: property to determine circle color
        :param color_stops: property to determine circle color
        :param color_default: property to determine default circle color if match lookup fails
        :param color_function_type: property to determine `type` used by Mapbox to assign color
        :param radius: radius of circle
        :param stroke_color: color of circle stroke outline
        :param stroke_width: with of circle stroke outline

        """
        super(CircleViz, self).__init__(data, *args, **kwargs)

        self.__dict__['layer'] = CircleLayer(
            data=data,
            label_property=label_property,
            label_color=label_color,
            label_size=label_size,
            label_halo_color=label_halo_color,
            label_halo_width=label_halo_width,
            color_property=color_property,
            color_stops=color_stops,
            radius=radius,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            color_function_type=color_function_type,
            color_default=color_default,
            legend_key_shape=legend_key_shape,
            min_zoom=min_zoom,
            max_zoom=max_zoom,
            *args,
            **kwargs
        )

        self.map.add_layer(self.layer)


class GraduatedCircleViz(MapViz):
    """Create a graduated circle map"""

    def __init__(self,
                 data,
                 label_property=None,
                 label_size=8,
                 label_color='#131516',
                 label_halo_color='white',
                 label_halo_width=1,
                 color_property=None,
                 color_stops=None,
                 color_default='grey',
                 color_function_type='interpolate',
                 stroke_color='grey',
                 stroke_width=0.1,
                 radius_property=None,
                 radius_stops=None,
                 radius_default=2,
                 radius_function_type='interpolate',
                 legend_key_shape='circle',
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param label_property: property to use for marker label
        :param color_property: property to determine circle color
        :param color_stops: property to determine circle color
        :param color_default: property to determine default circle color if match lookup fails
        :param color_function_type: property to determine `type` used by Mapbox to assign color
        :param radius_property: property to determine circle radius
        :param radius_stops: property to determine circle radius
        :param radius_default: property to determine default circle radius if match lookup fails
        :param radius_function_type: property to determine `type` used by Mapbox to assign radius size
        :param stroke_color: color of circle stroke outline
        :param stroke_width: with of circle stroke outline

        """
        super(GraduatedCircleViz, self).__init__(data, *args, **kwargs)

        self.__dict__['layer'] = GraduatedCircleLayer(
            data=data,
            label_property=label_property,
            label_color=label_color,
            label_size=label_size,
            label_halo_color=label_halo_color,
            label_halo_width=label_halo_width,
            color_property=color_property,
            color_stops=color_stops,
            radius_property=radius_property,
            radius_stops=radius_stops,
            color_function_type=color_function_type,
            color_default=color_default,
            radius_function_type=radius_function_type,
            radius_default=radius_default,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            legend_key_shape=legend_key_shape,
            *args,
            **kwargs
        )

        self.map.add_layer(self.layer)


class HeatmapViz(MapViz):
    """Create a heatmap viz"""

    def __init__(self,
                 data,
                 weight_property=None,
                 weight_stops=None,
                 color_stops=None,
                 radius_stops=None,
                 intensity_stops=None,
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param weight_property: property to determine heatmap weight. EX. "population"
        :param weight_stops: stops to determine heatmap weight.  EX. [[10, 0], [100, 1]]
        :param color_stops: stops to determine heatmap color.  EX. [[0, "red"], [0.5, "blue"], [1, "green"]]
        :param radius_stops: stops to determine heatmap radius based on zoom.  EX: [[0, 1], [12, 30]]
        :param intensity_stops: stops to determine the heatmap intensity based on zoom. EX: [[0, 0.1], [20, 5]]
        
        """
        super(HeatmapViz, self).__init__(data, *args, **kwargs)

        self.__dict__['layer'] = HeatmapLayer(
            data=data,
            weight_property=weight_property,
            weight_stops=weight_stops,
            color_stops=color_stops,
            radius_stops=radius_stops,
            intensity_stops=intensity_stops,
            *args,
            **kwargs
        )

        self.map.add_layer(self.layer)


class ClusteredCircleViz(MapViz):
    """Create a clustered circle map"""

    def __init__(self,
                 data,
                 label_size=8,
                 label_color='#131516',
                 label_halo_color='white',
                 label_halo_width=1,
                 color_stops=None,
                 radius_stops=None,
                 cluster_radius=30,
                 cluster_maxzoom=14,
                 radius_default=2,
                 color_default='black',
                 stroke_color='grey',
                 stroke_width=0.1,
                 legend_key_shape='circle',
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param color_property: property to determine circle color
        :param color_stops: property to determine circle color
        :param radius_property: property to determine circle radius
        :param radius_stops: property to determine circle radius
        :param stroke_color: color of circle stroke outline
        :param stroke_width: with of circle stroke outline
        :param radius_default: radius of circles not contained in a cluster
        :param color_default: color of circles not contained in a cluster

        """
        super(ClusteredCircleViz, self).__init__(data, *args, **kwargs)

        self.__dict__['layer'] = ClusteredCircleLayer(
            data=data,
            label_color=label_color,
            label_size=label_size,
            label_halo_color=label_halo_color,
            label_halo_width=label_halo_width,
            color_stops=color_stops,
            radius_stops=radius_stops,
            cluster_radius=cluster_radius,
            cluster_maxzoom=cluster_maxzoom,
            radius_default=radius_default,
            color_default=color_default,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            legend_key_shape=legend_key_shape,
            *args,
            **kwargs
        )

        self.map.add_layer(self.layer)


class ChoroplethViz(MapViz):
    """Create a choropleth viz"""

    def __init__(self,
                 data,
                 vector_url=None,
                 vector_layer_name=None,
                 vector_join_property=None,
                 data_join_property=None, # vector only
                 label_property=None,
                 color_property=None,
                 color_stops=None,
                 color_default='grey',
                 color_function_type='interpolate',
                 line_color='white',
                 line_stroke='solid',
                 line_width=1,
                 height_property=None,
                 height_stops=None,
                 height_default=0.0,
                 height_function_type='interpolate',
                 legend_key_shape='rounded-square',
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param data: can be either GeoJSON (containing polygon features) or JSON for data-join technique with vector polygons
        :param vector_url: optional property to define vector polygon source
        :param vector_layer_name: property to define target layer of vector source
        :param vector_join_property: property to aid in determining color for styling vector polygons
        :param data_join_property: property to join json data to vector features
        :param label_property: property to use for marker label
        :param color_property: property to determine polygon color
        :param color_stops: property to determine polygon color
        :param color_default: property to determine default polygon color if match lookup fails
        :param color_function_type: property to determine `type` used by Mapbox to assign color
        :param line_color: property to determine choropleth line color
        :param line_stroke: property to determine choropleth line stroke (solid, dashed, dotted, dash dot)
        :param line_width: property to determine choropleth line width
        :param height_property: feature property for determining polygon height in 3D extruded choropleth map
        :param height_stops: property for determining 3D extrusion height
        :param height_default: default height for 3D extruded polygons
        :param height_function_type: roperty to determine `type` used by Mapbox to assign height
        
        """
        super(ChoroplethViz, self).__init__(data, *args, **kwargs)

        self.__dict__['layer'] = ChoroplethLayer(
            data=data,
            vector_url=vector_url,
            vector_layer_name=vector_layer_name,
            vector_join_property=vector_join_property,
            data_join_property=data_join_property,  # vector only
            label_property=label_property,
            color_property=color_property,
            color_stops=color_stops,
            color_default=color_default,
            color_function_type=color_function_type,
            line_color=line_color,
            line_stroke=line_stroke,
            line_width=line_width,
            height_property=height_property,
            height_stops=height_stops,
            height_default=height_default,
            height_function_type=height_function_type,
            legend_key_shape=legend_key_shape,
            *args,
            **kwargs
        )

        self.map.add_layer(self.layer)

    def generate_vector_color_map(self):
        """Generate color stops array for use with match expression in mapbox template"""
        return self.layer.generate_vector_color_map()

    def generate_vector_height_map(self):
        """Generate height stops array for use with match expression in mapbox template"""
        return self.layer.generate_vector_height_map()


class ImageViz(MapViz):
    """Create a image viz"""

    def __init__(self,
                 image,
                 coordinates,
                 legend=False,
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param coordinates: property to determine image coordinates (UL, UR, LR, LL).
            EX. [[-80.425, 46.437], [-71.516, 46.437], [-71.516, 37.936], [-80.425, 37.936]]
        :param image: url, local path or a numpy ndarray
        :param legend: default setting is to hide heatmap legend

        """
        super(ImageViz, self).__init__(None, *args, **kwargs)

        self.__dict__['layer'] = ImageLayer(
            image=image,
            coordinates=coordinates,
        )

        self.map.add_layer(self.layer)


class RasterTilesViz(MapViz):
    """Create a rastertiles map"""

    def __init__(self,
                 tiles_url,
                 tiles_size=256,
                 tiles_bounds=None,
                 tiles_minzoom=0,
                 tiles_maxzoom=22,
                 legend=False,
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param tiles_url: property to determine tiles url endpoint
        :param tiles_size: property to determine displayed tiles size
        :param tiles_bounds: property to determine the tiles endpoint bounds
        :param tiles_minzoom: property to determine the tiles endpoint min zoom
        :param tiles_max: property to determine the tiles endpoint max zoom
        :param legend: default setting is to hide heatmap legend

        """
        super(RasterTilesViz, self).__init__(None, *args, **kwargs)

        self.__dict__['layer'] = RasterTilesLayer(
            tiles_url=tiles_url,
            tiles_size=tiles_size,
            tiles_bounds=tiles_bounds,
            tiles_minzoom=tiles_minzoom,
            tiles_maxzoom=tiles_maxzoom
        )

        self.map.add_layer(self.layer)


class LinestringViz(MapViz):
    """Create a linestring viz"""

    def __init__(self,
                 data,
                 vector_url=None,
                 vector_layer_name=None,
                 vector_join_property=None,
                 data_join_property=None,
                 label_property=None,
                 label_size=8,
                 label_color='#131516',
                 label_halo_color='white',
                 label_halo_width=1,
                 color_property=None,
                 color_stops=None,
                 color_default='grey',
                 color_function_type='interpolate',
                 line_stroke='solid',
                 line_width_property=None,
                 line_width_stops=None,
                 line_width_default=1,
                 line_width_function_type='interpolate',
                 legend_key_shape='line',
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param data: can be either GeoJSON (containing polygon features) or JSON for data-join technique with vector polygons
        :param vector_url: optional property to define vector linestring source
        :param vector_layer_name: property to define target layer of vector source
        :param vector_join_property: property to aid in determining color for styling vector lines
        :param data_join_property: property to join json data to vector features
        :param label_property: property to use for marker label
        :param label_size: size of label text
        :param label_color: color of label text
        :param label_halo_color: color of label text halo
        :param label_halo_width: width of label text halo
        :param color_property: property to determine line color
        :param color_stops: property to determine line color
        :param color_default: property to determine default line color if match lookup fails
        :param color_function_type: property to determine `type` used by Mapbox to assign color
        :param line_stroke: property to determine line stroke (solid, dashed, dotted, dash dot)
        :param line_width_property: property to determine line width
        :param line_width_stops: property to determine line width
        :param line_width_default: property to determine default line width if match lookup fails
        :param line_width_function_type: property to determine `type` used by Mapbox to assign line width

        """
        super(LinestringViz, self).__init__(data, *args, **kwargs)

        self.__dict__['layer'] = LinestringLayer(
            data=data,
            vector_url=vector_url,
            vector_layer_name=vector_layer_name,
            vector_join_property=vector_join_property,
            data_join_property=data_join_property,
            label_property=label_property,
            label_size=label_size,
            label_color=label_color,
            label_halo_color=label_halo_color,
            label_halo_width=label_halo_width,
            color_property=color_property,
            color_stops=color_stops,
            color_default=color_default,
            color_function_type=color_function_type,
            line_stroke=line_stroke,
            line_width_property=line_width_property,
            line_width_stops=line_width_stops,
            line_width_default=line_width_default,
            line_width_function_type=line_width_function_type,
            legend_key_shape=legend_key_shape,
        )

        self.map.add_layer(self.layer)

    def generate_vector_color_map(self):
        """Generate color stops array for use with match expression in mapbox template"""
        return self.layer.generate_vector_color_map()

    def generate_vector_width_map(self):
        """Generate width stops array for use with match expression in mapbox template"""
        return self.layer.generate_vector_width_map()
