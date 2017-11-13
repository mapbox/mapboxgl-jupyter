import json
import os

from IPython.core.display import HTML, display

from mapboxgl.errors import TokenError
from mapboxgl import templates

GL_JS_VERSION = 'v0.41.0'


class CircleViz(object):
    """Create a circle map"""

    def __init__(self,
                 data,
                 access_token=None,
                 center=(0, 0),
                 color_property=None,
                 color_stops=None,
                 label_property=None,
                 div_id='map',
                 height='500px',
                 style_url="mapbox://styles/mapbox/light-v9?optimize=true",
                 width='100%',
                 zoom=0):
        """Construct a Mapviz object

        :param data: GeoJSON Feature Collection

        :param color_property: property to determine circle color
        :param color_stops: property to determine circle color

        :param style_url: url to mapbox style
        :param access_token: Mapbox GL JS access token.
        :param div_id: The HTML div id of the map container in the viz
        :param width: The CSS width of the HTML div id in % or pixels.
        :param height: The CSS height of the HTML map div in % or pixels.
        """
        if access_token is None:
            access_token = os.environ.get('MAPBOX_ACCESS_TOKEN', '')
        if not access_token.startswith('pk'):
            raise TokenError('Mapbox access token must be public (pk)')
        self.access_token = access_token

        self.div_id = div_id
        self.width = width
        self.height = height
        self.data = data
        self.style_url = style_url
        self.center = center
        self.zoom = zoom

        self.color_property = color_property
        self.color_stops = color_stops
        self.label_property = label_property

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
            colorProperty=self.color_property,
            colorStops=self.color_stops)

        if self.label_property is None:
            options.update(labelProperty=None)
        else:
            options.update(labelProperty='{' + self.label_property + '}')

        return templates.format('circle', **options)


class GraduatedCircleViz(object):
    """Create a graduated circle map"""

    def __init__(self,
                 data,
                 access_token=None,
                 center=(0, 0),
                 label_property=None,
                 color_property=None,
                 color_stops=None,
                 radius_property=None,
                 radius_stops=None,
                 div_id='map',
                 height='500px',
                 style_url="mapbox://styles/mapbox/light-v9?optimize=true",
                 width='100%',
                 zoom=0):
        """Construct a Mapviz object

        :param data: GeoJSON Feature Collection

        :param color_property: property to determine circle color
        :param color_stops: property to determine circle color
        :param radius_property: property to determine circle radius
        :param radius_stops: property to determine circle radius

        :param style_url: url to mapbox style
        :param access_token: Mapbox GL JS access token.
        :param div_id: The HTML div id of the map container in the viz
        :param width: The CSS width of the HTML div id in % or pixels.
        :param height: The CSS height of the HTML map div in % or pixels.
        """
        if access_token is None:
            access_token = os.environ.get('MAPBOX_ACCESS_TOKEN', '')
        if not access_token.startswith('pk'):
            raise TokenError('Mapbox access token must be public (pk)')
        self.access_token = access_token

        self.div_id = div_id
        self.width = width
        self.height = height
        self.data = data
        self.style_url = style_url
        self.center = center
        self.zoom = zoom

        self.color_property = color_property
        self.color_stops = color_stops
        self.radius_property = radius_property
        self.radius_stops = radius_stops
        self.label_property = label_property

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
            colorProperty=self.color_property,
            colorStops=self.color_stops,
            radiusProperty=self.radius_property,
            radiusStops=self.radius_stops)

        if self.label_property is None:
            options.update(labelProperty=None)
        else:
            options.update(labelProperty='{' + self.label_property + '}')

        return templates.format('graduated_circle', **options)


class HeatmapViz(object):
    """Create a heatmap viz"""

    def __init__(self,
                 data,
                 access_token=None,
                 center=(0, 0),
                 weight_property=None,
                 weight_stops=None,
                 color_stops=None,
                 radius_stops=None,
                 div_id='map',
                 height='500px',
                 style_url="mapbox://styles/mapbox/light-v9?optimize=true",
                 width='100%',
                 zoom=0):
        """Construct a Mapviz object

        :param data: GeoJSON Feature Collection

        :param weight_property: property to determine heatmap weight. EX. "population"
        :param weight_stops: stops to determine heatmap weight.  EX. [[10, 0], [100, 1]]
        :param color_stops: stops to determine heatmap color.  EX. [[0, "red"], [0.5, "blue"], [1, "green"]]
        :param radius_stops: stops to determine heatmap radius based on zoom.  EX: [[0, 1], [12, 30]]

        :param style_url: url to mapbox style
        :param access_token: Mapbox GL JS access token.
        :param div_id: The HTML div id of the map container in the viz
        :param width: The CSS width of the HTML div id in % or pixels.
        :param height: The CSS height of the HTML map div in % or pixels.
        """
        if access_token is None:
            access_token = os.environ.get('MAPBOX_ACCESS_TOKEN', '')
        if not access_token.startswith('pk'):
            raise TokenError('Mapbox access token must be public (pk)')
        self.access_token = access_token

        self.div_id = div_id
        self.width = width
        self.height = height
        self.data = data
        self.style_url = style_url
        self.center = center
        self.zoom = zoom

        self.weight_property = weight_property
        self.weight_stops = weight_stops
        self.color_stops = color_stops
        self.radius_stops = radius_stops

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
            colorStops=self.color_stops,
            radiusStops=self.radius_stops,
            weightProperty=self.weight_property,
            weightStops=self.weight_stops)

        return templates.format('heatmap', **options)
