import json
import os

from IPython.core.display import HTML, display

from mapboxgl.errors import TokenError
from mapboxgl import templates

GL_JS_VERSION = 'v0.44.0'


class MapViz(object):

    def __init__(self,
                 data,
                 access_token=None,
                 center=(0, 0),
                 below_layer='',
                 opacity=1,
                 div_id='map',
                 height='500px',
                 style_url='mapbox://styles/mapbox/light-v9?optimize=true',
                 width='100%',
                 zoom=0):
        """Construct a MapViz object

        :param data: GeoJSON Feature Collection
        :param access_token: Mapbox GL JS access token.
        :param center: map center point
        :param style_url: url to mapbox style
        :param div_id: The HTML div id of the map container in the viz
        :param width: The CSS width of the HTML div id in % or pixels.
        :param height: The CSS height of the HTML map div in % or pixels.
        :param zoom: starting zoom level for map
        :param opacity: opacity of map data layer

        """
        if access_token is None:
            access_token = os.environ.get('MAPBOX_ACCESS_TOKEN', '')
        if not access_token.startswith('pk'):
            raise TokenError('Mapbox access token must be public (pk)')
        self.access_token = access_token
        
        self.template = 'base'
        self.data = data
        self.div_id = div_id
        self.width = width
        self.height = height
        self.style_url = style_url
        self.center = center
        self.zoom = zoom
        self.below_layer = below_layer
        self.opacity = opacity
        self.label_property = None

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

    def create_html(self):
        """Create a circle visual from a geojson data source"""
        options = dict(
            gl_js_version=GL_JS_VERSION,
            accessToken=self.access_token,
            div_id=self.div_id,
            styleUrl=self.style_url,
            center=list(self.center),
            zoom=self.zoom,
            geojson_data=json.dumps(self.data, ensure_ascii=False),
            belowLayer=self.below_layer,
            opacity=self.opacity)

        if self.label_property is None:
            options.update(labelProperty=None)
        else:
            options.update(labelProperty='{' + self.label_property + '}')

        self.add_unique_template_variables(options)

        return templates.format(self.template, **options)


class CircleViz(MapViz):
    """Create a circle map"""

    def __init__(self,
                 data,
                 label_property=None,
                 color_property=None,
                 color_stops=None,
                 color_default='grey',
                 color_function_type='interpolate',
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param label_property: property to use for marker label
        :param color_property: property to determine circle color
        :param color_stops: property to determine circle color
        :param color_default: property to determine default circle color if match lookup fails
        :param color_function_type: property to determine `type` used by Mapbox to assign color

        """
        super(CircleViz, self).__init__(data, *args, **kwargs)

        self.template = 'circle'
        self.label_property = label_property
        self.color_property = color_property
        self.color_stops = color_stops
        self.color_function_type = color_function_type
        self.color_default = color_default

    def add_unique_template_variables(self, options):
        """Update map template variables specific to circle visual"""
        options.update(dict(
            geojson_data=json.dumps(self.data, ensure_ascii=False),
            colorProperty=self.color_property,
            colorType=self.color_function_type,
            colorStops=self.color_stops,
            defaultColor=self.color_default
        ))


class GraduatedCircleViz(MapViz):
    """Create a graduated circle map"""

    def __init__(self,
                 data,
                 label_property=None,
                 color_property=None,
                 color_stops=None,
                 color_default='grey',
                 color_function_type='interpolate',
                 radius_property=None,
                 radius_stops=None,
                 radius_default=None,
                 radius_function_type='interpolate',
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

        """
        super(GraduatedCircleViz, self).__init__(data, *args, **kwargs)

        self.template = 'graduated_circle'
        self.label_property = label_property
        self.color_property = color_property
        self.color_stops = color_stops
        self.radius_property = radius_property
        self.radius_stops = radius_stops
        self.color_function_type = color_function_type
        self.color_default = color_default
        self.radius_function_type = radius_function_type
        self.radius_default = radius_default

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
        ))


class HeatmapViz(MapViz):
    """Create a heatmap viz"""

    def __init__(self,
                 data,
                 weight_property=None,
                 weight_stops=None,
                 color_stops=None,
                 radius_stops=None,
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param weight_property: property to determine heatmap weight. EX. "population"
        :param weight_stops: stops to determine heatmap weight.  EX. [[10, 0], [100, 1]]
        :param color_stops: stops to determine heatmap color.  EX. [[0, "red"], [0.5, "blue"], [1, "green"]]
        :param radius_stops: stops to determine heatmap radius based on zoom.  EX: [[0, 1], [12, 30]]

        """
        super(HeatmapViz, self).__init__(data, *args, **kwargs)

        self.template = 'heatmap'
        self.weight_property = weight_property
        self.weight_stops = weight_stops
        self.color_stops = color_stops
        self.radius_stops = radius_stops

    def add_unique_template_variables(self, options):
        """Update map template variables specific to heatmap visual"""
        options.update(dict(
            colorStops=self.color_stops,
            radiusStops=self.radius_stops,
            weightProperty=self.weight_property,
            weightStops=self.weight_stops
        ))


class ClusteredCircleViz(MapViz):
    """Create a clustered circle map"""

    def __init__(self,
                 data,
                 color_stops=None,
                 radius_stops=None,
                 cluster_radius=30,
                 cluster_maxzoom=14,
                 *args,
                 **kwargs):
        """Construct a Mapviz object

        :param color_property: property to determine circle color
        :param color_stops: property to determine circle color
        :param radius_property: property to determine circle radius
        :param radius_stops: property to determine circle radius

        """
        super(ClusteredCircleViz, self).__init__(data, *args, **kwargs)

        self.template = 'clustered_circle'
        self.color_stops = color_stops
        self.radius_stops = radius_stops
        self.clusterRadius = cluster_radius
        self.clusterMaxZoom = cluster_maxzoom

    def add_unique_template_variables(self, options):
        """Update map template variables specific to a clustered circle visual"""
        options.update(dict(
            colorStops=self.color_stops,
            baseColor=self.color_stops[0][1],
            radiusStops=self.radius_stops,
            clusterRadius=self.clusterRadius,
            clusterMaxZoom=self.clusterMaxZoom
        ))
