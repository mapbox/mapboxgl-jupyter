import codecs
import json
import os

from IPython.core.display import HTML, display

import numpy
import requests

from mapboxgl.errors import TokenError, LegendError
from mapboxgl.utils import color_map, numeric_map, img_encode, geojson_to_dict_list
from mapboxgl import templates


GL_JS_VERSION = 'v1.0.0'


class VectorMixin(object):

    def generate_vector_color_map(self):
        """Generate color stops array for use with match expression in mapbox template"""
        vector_stops = []

        # if join data specified as filename or URL, parse JSON to list of Python dicts
        if type(self.data) == str:
            self.data = geojson_to_dict_list(self.data)

        # loop through features in self.data to create join-data map
        for row in self.data:
            
            # map color to JSON feature using color_property
            color = color_map(row[self.color_property], self.color_stops, self.color_default)

            # link to vector feature using data_join_property (from JSON object)
            vector_stops.append([row[self.data_join_property], color])

        return vector_stops

    def generate_vector_numeric_map(self, numeric_property):
        """Generate stops array for use with match expression in mapbox template"""
        vector_stops = []
        
        function_type = getattr(self, '{}_function_type'.format(numeric_property))
        lookup_property = getattr(self, '{}_property'.format(numeric_property))
        numeric_stops = getattr(self, '{}_stops'.format(numeric_property))
        default = getattr(self, '{}_default'.format(numeric_property))

        if function_type == 'match':
            match_width = numeric_stops

        # if join data specified as filename or URL, parse JSON to list of Python dicts
        if type(self.data) == str:
            self.data = geojson_to_dict_list(self.data)

        for row in self.data:

            # map value to JSON feature using the numeric property
            value = numeric_map(row[lookup_property], numeric_stops, default)
            
            # link to vector feature using data_join_property (from JSON object)
            vector_stops.append([row[self.data_join_property], value])

        return vector_stops

    def check_vector_template(self):
        """Determines if features are defined as vector source based on MapViz arguments."""

        if self.vector_url is not None and self.vector_layer_name is not None:
            self.template = 'vector_' + self.template
            self.vector_source = True
        else:
            self.vector_source = False


class MapViz(object):

    def __init__(self,
                 data,
                 vector_url=None,
                 vector_layer_name=None,
                 vector_join_property=None,
                 data_join_property=None,
                 disable_data_join=False,
                 access_token=None,
                 center=(0, 0),
                 below_layer='',
                 opacity=1,
                 div_id='map',
                 height='500px',
                 style='mapbox://styles/mapbox/light-v10?optimize=true',
                 label_property=None,
                 label_size=8,
                 label_color='#131516',
                 label_halo_color='white',
                 label_halo_width=1,
                 width='100%',
                 zoom=0,
                 min_zoom=0,
                 max_zoom=24,
                 pitch=0,
                 bearing=0,
                 box_zoom_on=True,
                 double_click_zoom_on=True,
                 scroll_zoom_on=True,
                 touch_zoom_on=True,
                 legend=True,
                 legend_layout='vertical',
                 legend_function='color',
                 legend_gradient=False,
                 legend_style='',
                 legend_fill='white',
                 legend_header_fill='white',
                 legend_text_color='#6e6e6e',
                 legend_text_numeric_precision=None,
                 legend_title_halo_color='white',
                 legend_key_shape='square',
                 legend_key_borders_on=True, 
                 scale=False,
                 scale_unit_system='metric',
                 scale_position='bottom-left',
                 scale_border_color='#6e6e6e', 
                 scale_background_color='white',
                 scale_text_color='#131516',
                 popup_open_action='hover',
                 add_snapshot_links=False):
        """Construct a MapViz object

        :param data: GeoJSON Feature Collection
        :param vector_url: optional property to define vector data source
        :param vector_layer_name: property to define target layer of vector source
        :param vector_join_property: property to aid in determining color for styling vector layer
        :param data_join_property: property to join json data to vector features
        :param disable_data_join: property to switch off default data-join technique using vector layer and JSON join-data; 
                                  also determines if a layer filter based on joined data is applied to features in vector layer
        :param access_token: Mapbox GL JS access token.
        :param center: map center point
        :param style: url to mapbox style or stylesheet as a Python dictionary in JSON format
        :param label_property: property to use for marker label
        :param label_size: size of label text
        :param label_color: color of label text
        :param label_halo_color: color of label text halo
        :param label_halo_width: width of label text halo
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
        :param legend_function: controls whether legend is color or radius-based
        :param legend_style: reserved for future custom CSS loader
        :param legend_gradient: boolean to determine if legend keys are discrete or gradient
        :param legend_fill: string background color for legend, default is white
        :param legend_header_fill: string background color for legend header (in vertical layout), default is #eee
        :param legend_text_color: string color for legend text default is #6e6e6e
        :param legend_text_numeric_precision: decimal precision for numeric legend values
        :param legend_title_halo_color: color of legend title text halo
        :param legend_key_shape: shape of the legend item keys, default varies by viz type; one of square, contiguous_bar, rounded-square, circle, line
        :param legend_key_borders_on: boolean for whether to show/hide legend key borders
        :param scale: add map control showing current scale of map
        :param scale_unit_system: choose units for scale display (metric, nautical or imperial)
        :param scale_position: location of the scale annotation
        :param scale_border_color: border color of the scale annotation
        :param scale_background_color: fill color of the scale annotation
        :param scale_text_color: text color the scale annotation
        :param popup_open_action: controls behavior of opening and closing feature popups; one of 'hover' or 'click'
        :param add_snapshot_links: boolean switch for adding buttons to download screen captures of map or legend

        """
        if access_token is None:
            access_token = os.environ.get('MAPBOX_ACCESS_TOKEN', '')
        if access_token.startswith('sk'):
            raise TokenError('Mapbox access token must be public (pk), not secret (sk). ' \
                             'Please sign up at https://www.mapbox.com/signup/ to get a public token. ' \
                             'If you already have an account, you can retreive your token at https://www.mapbox.com/account/.')
        self.access_token = access_token

        self.data = data
        
        self.vector_url = vector_url
        self.vector_layer_name = vector_layer_name
        self.vector_join_property = vector_join_property
        self.data_join_property = data_join_property
        self.disable_data_join = disable_data_join

        self.template = 'map'
        try:
            self.check_vector_template()
        except AttributeError:
            self.vector_source = False

        self.div_id = div_id
        self.width = width
        self.height = height
        self.style = style
        self.center = center
        self.zoom = zoom
        self.below_layer = below_layer
        self.opacity = opacity
        self.label_property = label_property
        self.label_color = label_color
        self.label_size = label_size
        self.label_halo_color = label_halo_color
        self.label_halo_width = label_halo_width
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.pitch = pitch
        self.bearing = bearing
        self.box_zoom_on = box_zoom_on
        self.double_click_zoom_on = double_click_zoom_on
        self.scroll_zoom_on = scroll_zoom_on
        self.touch_zoom_on = touch_zoom_on

        # legend configuration
        self.legend = legend
        self.legend_layout = legend_layout
        self.legend_function = legend_function
        self.legend_style = legend_style
        self.legend_gradient = legend_gradient
        self.legend_fill = legend_fill
        self.legend_header_fill = legend_header_fill
        self.legend_text_color = legend_text_color
        self.legend_text_numeric_precision = legend_text_numeric_precision
        self.legend_title_halo_color = legend_title_halo_color
        self.legend_key_shape = legend_key_shape
        self.legend_key_borders_on = legend_key_borders_on
        self.popup_open_action = popup_open_action
        self.add_snapshot_links = add_snapshot_links

        # scale configuration
        self.scale = scale
        self.scale_unit_system = scale_unit_system
        self.scale_position = scale_position
        self.scale_border_color = scale_border_color
        self.scale_background_color = scale_background_color
        self.scale_text_color = scale_text_color

    def as_iframe(self, html_data):
        """Build the HTML representation for the mapviz."""

        srcdoc = html_data.replace('"', "'")
        return ('<iframe id="{div_id}", srcdoc="{srcdoc}" style="width: {width}; '
                'height: {height};"></iframe>'.format(
                    div_id=self.div_id,
                    srcdoc=srcdoc,
                    width=self.width,
                    height=self.height))

    def show(self, **kwargs):
        # Load the HTML iframe
        html = self.create_html(**kwargs)
        map_html = self.as_iframe(html)

        # Display the iframe in the current jupyter notebook view
        display(HTML(map_html))

    def add_unique_template_variables(self, options):
        pass

    def create_html(self, filename=None):
        """Create a circle visual from a geojson data source"""
        
        if isinstance(self.style, str):
            style = "'{}'".format(self.style)
        else:
            style = self.style
        
        options = dict(
            gl_js_version=GL_JS_VERSION,
            accessToken=self.access_token,
            div_id=self.div_id,
            style=style,
            center=list(self.center),
            zoom=self.zoom,
            geojson_data=json.dumps(self.data, ensure_ascii=False),
            belowLayer=self.below_layer,
            opacity=self.opacity,
            minzoom=self.min_zoom,
            maxzoom=self.max_zoom,
            pitch=self.pitch, 
            bearing=self.bearing,
            boxZoomOn=json.dumps(self.box_zoom_on),
            doubleClickZoomOn=json.dumps(self.double_click_zoom_on),
            scrollZoomOn=json.dumps(self.scroll_zoom_on),
            touchZoomOn=json.dumps(self.touch_zoom_on),
            popupOpensOnHover=self.popup_open_action=='hover',
            includeSnapshotLinks=self.add_snapshot_links,
            preserveDrawingBuffer=json.dumps(self.add_snapshot_links),
            showScale=self.scale,
            scaleUnits=self.scale_unit_system,
            scaleBorderColor=self.scale_border_color,
            scalePosition=self.scale_position,
            scaleFillColor=self.scale_background_color,
            scaleTextColor=self.scale_text_color,
        )

        if self.legend:

            if all([self.legend, self.legend_gradient, self.legend_function == 'radius']):
                raise LegendError(' '.join(['Gradient legend format not compatible with a variable radius legend.',
                                            'Please either change `legend_gradient` to False or `legend_function` to "color".']))

            options.update(
                showLegend=self.legend,
                legendLayout=self.legend_layout,
                legendFunction=self.legend_function,
                legendStyle=self.legend_style, # reserve for custom CSS
                legendGradient=json.dumps(self.legend_gradient),
                legendFill=self.legend_fill,
                legendHeaderFill=self.legend_header_fill,
                legendTextColor=self.legend_text_color,
                legendNumericPrecision=json.dumps(self.legend_text_numeric_precision),
                legendTitleHaloColor=self.legend_title_halo_color,
                legendKeyShape=self.legend_key_shape,
                legendKeyBordersOn=json.dumps(self.legend_key_borders_on)
            )

        if self.vector_source:
            options.update(
                vectorUrl=self.vector_url,
                vectorLayer=self.vector_layer_name,
                vectorJoinDataProperty=self.vector_join_property,
                joinData=json.dumps(False),
                dataJoinProperty=self.data_join_property,
                enableDataJoin=not self.disable_data_join
            )
            data = geojson_to_dict_list(self.data)
            if bool(data):
                options.update(joinData=json.dumps(data, ensure_ascii=False))

        if self.label_property is None:
            options.update(labelProperty=None)
        else:
            options.update(labelProperty='{' + self.label_property + '}')
        
        options.update(
            labelColor=self.label_color,
            labelSize=self.label_size,
            labelHaloColor=self.label_halo_color,
            labelHaloWidth=self.label_halo_width
        )

        self.add_unique_template_variables(options)

        if filename:
            html = templates.format(self.template, **options)
            with codecs.open(filename, "w", "utf-8-sig") as f:
                f.write(html)
            return None
        else:
            return templates.format(self.template, **options)


class CircleViz(VectorMixin, MapViz):
    """Create a circle map"""

    def __init__(self,
                 data,
                 radius=1,
                 color_property=None,
                 color_stops=None,
                 color_default='grey',
                 color_function_type='interpolate',
                 stroke_color='grey',
                 stroke_width=0.1,
                 legend_key_shape='circle',
                 highlight_color='black',
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param color_property: property to determine circle color
        :param color_stops: property to determine circle color
        :param color_default: property to determine default circle color if match lookup fails
        :param color_function_type: property to determine `type` used by Mapbox to assign color
        :param radius: radius of circle
        :param stroke_color: color of circle stroke outline
        :param stroke_width: with of circle stroke outline
        :param highlight_color: color for feature selection, hover, or highlight

        """
        super(CircleViz, self).__init__(data, *args, **kwargs)

        self.template = 'circle'
        self.check_vector_template()

        self.color_property = color_property
        self.color_stops = color_stops
        self.radius = radius
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.color_function_type = color_function_type
        self.color_default = color_default
        self.legend_key_shape = legend_key_shape
        self.highlight_color = highlight_color

    def add_unique_template_variables(self, options):
        """Update map template variables specific to circle visual"""
        options.update(dict(
            geojson_data=json.dumps(self.data, ensure_ascii=False),
            colorProperty=self.color_property,
            colorType=self.color_function_type,
            colorStops=self.color_stops,
            strokeWidth=self.stroke_width,
            strokeColor=self.stroke_color,
            radius=self.radius,
            defaultColor=self.color_default,
            highlightColor=self.highlight_color
        ))

        if self.vector_source:
            options.update(vectorColorStops=self.generate_vector_color_map())


class GraduatedCircleViz(VectorMixin, MapViz):
    """Create a graduated circle map"""

    def __init__(self,
                 data,
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
                 highlight_color='black',
                 *args,
                 **kwargs):
        """Construct a Mapviz object

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
        :param highlight_color: color for feature selection, hover, or highlight

        """
        super(GraduatedCircleViz, self).__init__(data, *args, **kwargs)

        self.template = 'graduated_circle'
        self.check_vector_template()

        self.color_property = color_property
        self.color_stops = color_stops
        self.radius_property = radius_property
        self.radius_stops = radius_stops
        self.color_function_type = color_function_type
        self.color_default = color_default
        self.radius_function_type = radius_function_type
        self.radius_default = radius_default
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.legend_key_shape = legend_key_shape
        self.highlight_color = highlight_color

    def add_unique_template_variables(self, options):
        """Update map template variables specific to graduated circle visual"""
        options.update(dict(
            colorProperty=self.color_property,
            colorStops=self.color_stops,
            colorType=self.color_function_type,
            radiusType=self.radius_function_type,
            defaultColor=self.color_default,
            defaultRadius=self.radius_default,
            radiusProperty=self.radius_property,
            radiusStops=self.radius_stops,
            strokeWidth=self.stroke_width,
            strokeColor=self.stroke_color,
            highlightColor=self.highlight_color
        ))
        if self.vector_source:
            options.update(dict(
                vectorColorStops=self.generate_vector_color_map(),
                vectorRadiusStops=self.generate_vector_numeric_map('radius')))


class HeatmapViz(VectorMixin, MapViz):
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

        self.template = 'heatmap'
        self.check_vector_template()

        self.weight_property = weight_property
        self.weight_stops = weight_stops
        if color_stops:
            # Make the first color stop in a heatmap have opacity 0 for good visual effect
            self.color_stops = [[0.00001, 'rgba(0,0,0,0)']] + color_stops
        self.radius_stops = radius_stops
        self.intensity_stops = intensity_stops

    def add_unique_template_variables(self, options):
        """Update map template variables specific to heatmap visual"""
        options.update(dict(
            colorStops=self.color_stops,
            radiusStops=self.radius_stops,
            weightProperty=self.weight_property,
            weightStops=self.weight_stops,
            intensityStops=self.intensity_stops,
        ))
        if self.vector_source:
            options.update(dict(
                vectorWeightStops=self.generate_vector_numeric_map('weight')))

    def generate_vector_numeric_map(self, numeric_property):
        """Generate stops array for use with match expression in mapbox template"""
        vector_stops = []
        
        lookup_property = getattr(self, '{}_property'.format(numeric_property))
        numeric_stops = getattr(self, '{}_stops'.format(numeric_property))

        # if join data specified as filename or URL, parse JSON to list of Python dicts
        if type(self.data) == str:
            self.data = geojson_to_dict_list(self.data)

        for row in self.data:

            # map value to JSON feature using the numeric property
            value = numeric_map(row[lookup_property], numeric_stops, 0)
            
            # link to vector feature using data_join_property (from JSON object)
            vector_stops.append([row[self.data_join_property], value])

        return vector_stops


class ClusteredCircleViz(MapViz):
    """Create a clustered circle map (geojson only)"""

    def __init__(self,
                 data,
                 color_stops=None,
                 radius_stops=None,
                 cluster_radius=30,
                 cluster_maxzoom=14,
                 radius_default=2,
                 color_default='black',
                 stroke_color='grey',
                 stroke_width=0.1,
                 legend_key_shape='circle',
                 highlight_color='black',
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
        :param highlight_color: color for feature selection, hover, or highlight

        """
        super(ClusteredCircleViz, self).__init__(data, *args, **kwargs)

        self.template = 'clustered_circle'
        self.color_stops = color_stops
        self.radius_stops = radius_stops
        self.clusterRadius = cluster_radius
        self.clusterMaxZoom = cluster_maxzoom
        self.radius_default = radius_default
        self.color_default = color_default
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.color_default = color_default
        self.legend_key_shape = legend_key_shape
        self.highlight_color = highlight_color

    def add_unique_template_variables(self, options):
        """Update map template variables specific to a clustered circle visual"""
        options.update(dict(
            colorStops=self.color_stops,
            colorDefault=self.color_default,
            radiusStops=self.radius_stops,
            clusterRadius=self.clusterRadius,
            clusterMaxZoom=self.clusterMaxZoom,
            strokeWidth=self.stroke_width,
            strokeColor=self.stroke_color,
            radiusDefault=self.radius_default,
            highlightColor=self.highlight_color
        ))


class ChoroplethViz(VectorMixin, MapViz):
    """Create a choropleth viz"""

    def __init__(self,
                 data,
                 color_property=None,
                 color_stops=None,
                 color_default='grey',
                 color_function_type='interpolate',
                 line_color='white',
                 line_stroke='solid',
                 line_width=1,
                 line_opacity=1,
                 height_property=None,      
                 height_stops=None,
                 height_default=0.0,
                 height_function_type='interpolate',
                 legend_key_shape='rounded-square',
                 highlight_color='black',
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param data: can be either GeoJSON (containing polygon features) or JSON for data-join technique with vector polygons
        :param vector_url: optional property to define vector polygon source
        :param vector_layer_name: property to define target layer of vector source
        :param vector_join_property: property to aid in determining color for styling vector polygons
        :param data_join_property: property to join json data to vector features
        :param color_property: property to determine polygon color
        :param color_stops: property to determine polygon color
        :param color_default: property to determine default polygon color if match lookup fails
        :param color_function_type: property to determine `type` used by Mapbox to assign color
        :param line_color: property to determine choropleth line color
        :param line_stroke: property to determine choropleth line stroke (solid, dashed, dotted, dash dot)
        :param line_width: property to determine choropleth line width
        :param line_opacity: opacity of choropleth line layer
        :param height_property: feature property for determining polygon height in 3D extruded choropleth map
        :param height_stops: property for determining 3D extrusion height
        :param height_default: default height for 3D extruded polygons
        :param height_function_type: property to determine `type` used by Mapbox to assign height
        :param highlight_color: color for feature selection, hover, or highlight
        """
        super(ChoroplethViz, self).__init__(data, *args, **kwargs)
        
        self.template = 'choropleth'
        self.check_vector_template()

        self.color_property = color_property
        self.color_stops = color_stops
        self.color_default = color_default
        self.color_function_type = color_function_type
        self.line_color = line_color
        self.line_stroke = line_stroke
        self.line_width = line_width
        self.line_opacity = line_opacity
        self.height_property = height_property
        self.height_stops = height_stops
        self.height_default = height_default
        self.height_function_type = height_function_type
        self.legend_key_shape = legend_key_shape
        self.highlight_color = highlight_color

    def add_unique_template_variables(self, options):
        """Update map template variables specific to heatmap visual"""

        # set line stroke dash interval based on line_stroke property
        if self.line_stroke in ["dashed", "--"]:
            self.line_dash_array = [6, 4]
        elif self.line_stroke in ["dotted", ":"]:
            self.line_dash_array = [0.5, 4]
        elif self.line_stroke in ["dash dot", "-."]:
            self.line_dash_array = [6, 4, 0.5, 4]
        elif self.line_stroke in ["solid", "-"]:
            self.line_dash_array = [1, 0]
        else:
            # default to solid line
            self.line_dash_array = [1, 0]

        # check if choropleth map should include 3-D extrusion
        self.extrude = all([bool(self.height_property), bool(self.height_stops)])

        # common variables for vector and geojson-based choropleths
        options.update(dict(
            colorStops=self.color_stops,
            colorProperty=self.color_property,
            colorType=self.color_function_type,
            defaultColor=self.color_default,
            lineColor=self.line_color,
            lineDashArray=self.line_dash_array,
            lineStroke=self.line_stroke,
            lineWidth=self.line_width,
            lineOpacity=self.line_opacity,
            extrudeChoropleth=self.extrude,
            highlightColor=self.highlight_color
        ))
        if self.extrude:
            options.update(dict(
                heightType=self.height_function_type,
                heightProperty=self.height_property,
                heightStops=self.height_stops,
                defaultHeight=self.height_default,
            ))

        # vector-based choropleth map variables
        if self.vector_source:
            options.update(vectorColorStops=self.generate_vector_color_map())
            
            if self.extrude:
                options.update(vectorHeightStops=self.generate_vector_numeric_map('height'))

        # geojson-based choropleth map variables
        else:
            options.update(geojson_data=json.dumps(self.data, ensure_ascii=False))


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

        if type(image) is numpy.ndarray:
            image = img_encode(image)

        self.template = 'image'
        self.image = image
        self.coordinates = coordinates

    def add_unique_template_variables(self, options):
        """Update map template variables specific to image visual"""
        options.update(dict(
            image=self.image,
            coordinates=self.coordinates))


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

        self.template = 'raster'
        self.tiles_url = tiles_url
        self.tiles_size = tiles_size
        self.tiles_bounds = tiles_bounds
        self.tiles_minzoom = tiles_minzoom
        self.tiles_maxzoom = tiles_maxzoom

    def add_unique_template_variables(self, options):
        """Update map template variables specific to a raster visual"""
        options.update(dict(
            tiles_url=self.tiles_url,
            tiles_size=self.tiles_size,
            tiles_minzoom=self.tiles_minzoom,
            tiles_maxzoom=self.tiles_maxzoom,
            tiles_bounds=self.tiles_bounds if self.tiles_bounds else 'undefined'))


class LinestringViz(VectorMixin, MapViz):
    """Create a linestring viz"""

    def __init__(self,
                 data,
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
                 highlight_color='black',
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param data: can be either GeoJSON (containing polygon features) or JSON for data-join technique with vector polygons
        :param vector_url: optional property to define vector linestring source
        :param vector_layer_name: property to define target layer of vector source
        :param vector_join_property: property to aid in determining color for styling vector lines
        :param data_join_property: property to join json data to vector features
        :param color_property: property to determine line color
        :param color_stops: property to determine line color
        :param color_default: property to determine default line color if match lookup fails
        :param color_function_type: property to determine `type` used by Mapbox to assign color
        :param line_stroke: property to determine line stroke (solid, dashed, dotted, dash dot)
        :param line_width_property: property to determine line width
        :param line_width_stops: property to determine line width
        :param line_width_default: property to determine default line width if match lookup fails
        :param line_width_function_type: property to determine `type` used by Mapbox to assign line width
        :param highlight_color: color for feature selection, hover, or highlight
        """
        super(LinestringViz, self).__init__(data, *args, **kwargs)
        
        self.template = 'linestring'
        self.check_vector_template()

        self.color_property = color_property
        self.color_stops = color_stops
        self.color_default = color_default
        self.color_function_type = color_function_type
        self.line_stroke = line_stroke
        self.line_width_property = line_width_property
        self.line_width_stops = line_width_stops
        self.line_width_default = line_width_default
        self.line_width_function_type = line_width_function_type
        self.legend_key_shape = legend_key_shape
        self.highlight_color = highlight_color

    def add_unique_template_variables(self, options):
        """Update map template variables specific to linestring visual"""

        # set line stroke dash interval based on line_stroke property
        if self.line_stroke in ["dashed", "--"]:
            self.line_dash_array = [6, 4]
        elif self.line_stroke in ["dotted", ":"]:
            self.line_dash_array = [0.5, 4]
        elif self.line_stroke in ["dash dot", "-."]:
            self.line_dash_array = [6, 4, 0.5, 4]
        elif self.line_stroke in ["solid", "-"]:
            self.line_dash_array = [1, 0]
        else:
            # default to solid line
            self.line_dash_array = [1, 0]

        # common variables for vector and geojson-based linestring maps
        options.update(dict(
            colorStops=self.color_stops,
            colorProperty=self.color_property,
            colorType=self.color_function_type,
            defaultColor=self.color_default,
            lineColor=self.color_default,
            lineDashArray=self.line_dash_array,
            lineStroke=self.line_stroke,
            widthStops=self.line_width_stops,
            widthProperty=self.line_width_property,
            widthType=self.line_width_function_type,
            defaultWidth=self.line_width_default,
            highlightColor=self.highlight_color
        ))

        # vector-based linestring map variables
        if self.vector_source:
            options.update(dict(
                vectorColorStops=[[0, self.color_default]],
                vectorWidthStops=[[0, self.line_width_default]],
            ))

            if self.color_property:
                options.update(vectorColorStops=self.generate_vector_color_map())
        
            if self.line_width_property:
                options.update(vectorWidthStops=self.generate_vector_numeric_map('line_width'))

        # geojson-based linestring map variables
        else:
            options.update(geojson_data=json.dumps(self.data, ensure_ascii=False))

