import codecs
import json
import os

from IPython.core.display import HTML, display

from mapboxgl.errors import TokenError
from mapboxgl import templates


GL_JS_VERSION = 'v0.49.0'


class Map(object):

    def __init__(self,
                 access_token=None,
                 center=(0, 0),
                 opacity=1,
                 div_id='map',
                 height='500px',
                 style='mapbox://styles/mapbox/light-v9?optimize=true',
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
                 legend_fill='white',
                 legend_header_fill='white',
                 legend_text_color='#6e6e6e',
                 legend_title_halo_color='white',
                 legend_key_borders_on=True
                 ):
        """Construct a MapViz object

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
        :param legend_fill: string background color for legend, default is white
        :param legend_header_fill: string background color for legend header (in vertical layout), default is #eee
        :param legend_text_color: string color for legend text default is #6e6e6e
        :param legend_title_halo_color: color of legend title text halo
        :param legend_key_borders_on: boolean for whether to show/hide legend key borders

        """
        if access_token is None:
            access_token = os.environ.get('MAPBOX_ACCESS_TOKEN', '')
        if access_token.startswith('sk'):
            raise TokenError('Mapbox access token must be public (pk), not secret (sk). ' \
                             'Please sign up at https://www.mapbox.com/signup/ to get a public token. ' \
                             'If you already have an account, you can retreive your token at https://www.mapbox.com/account/.')
        self.access_token = access_token
        self.template = 'map'
        self.div_id = div_id
        self.width = width
        self.height = height
        self.style = style
        self.center = center
        self.zoom = zoom
        self.opacity = opacity
        self.label_property = None
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.pitch = pitch
        self.bearing = bearing
        self.box_zoom_on = box_zoom_on
        self.double_click_zoom_on = double_click_zoom_on
        self.scroll_zoom_on = scroll_zoom_on
        self.touch_zoom_on = touch_zoom_on
        self.legend_fill = legend_fill
        self.legend_header_fill = legend_header_fill
        self.legend_text_color = legend_text_color,
        self.legend_title_halo_color = legend_title_halo_color
        self.legend_key_borders_on = legend_key_borders_on
        self.layer_id_counter = 0
        self.layers = []

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
            opacity=self.opacity,
            minzoom=self.min_zoom,
            maxzoom=self.max_zoom,
            pitch=self.pitch,
            bearing=self.bearing,
            boxZoomOn=json.dumps(self.box_zoom_on),
            doubleClickZoomOn=json.dumps(self.double_click_zoom_on),
            scrollZoomOn=json.dumps(self.scroll_zoom_on),
            touchZoomOn=json.dumps(self.touch_zoom_on),
            legendFill=self.legend_fill,
            legendHeaderFill=self.legend_header_fill,
            legendTextColor=self.legend_text_color,
            legendTitleHaloColor=self.legend_title_halo_color,
            legendKeyBordersOn=json.dumps(self.legend_key_borders_on)
            )

        if self.label_property is None:
            options.update(labelProperty=None)
        else:
            options.update(labelProperty='{' + self.label_property + '}')

        html = []
        html.append(templates.format(self.template, **options))
        for layer in self.layers:
            html.append(layer.create_html())
        if filename:
            with codecs.open(filename, "w", "utf-8-sig") as f:
                f.write("\n".join(html))
            return None
        else:
            return "\n".join(html)

    def add_layer(self, layer):
        self.layers.append(layer)
        layer.layer_id = self.layer_id_counter
        self.layer_id_counter +=1

    def remove_layer(self, layer):
        self.layers.remove(layer)
        layer.show_legend = False
