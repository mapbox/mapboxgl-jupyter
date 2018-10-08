import json

import numpy

from mapboxgl.utils import color_map, height_map
from mapboxgl import templates
from mapboxgl.utils import img_encode, numeric_map


class AbstractLayer():
    """Abstract class for layers"""

    def __init__(self,
                 data,
                 opacity=1,
                 below_layer='',
                 legend=True,
                 legend_layout='vertical',
                 legend_gradient=False,
                 legend_text_numeric_precision=None,
                 legend_key_shape='square',
                 min_zoom=0,
                 max_zoom=24,
                 *args,
                 **kwargs):
        """Abstract class for layers

                :param opacity: opacity of map data layer
                :param below_layer: the layer to put this one below
                :param legend: boolean for whether to show legend on map
                :param legend_layout: determines if horizontal or vertical legend used
                :param legend_gradient: boolean to determine if legend keys are discrete or gradient
                :param legend_fill: string background color for legend, default is white
                :param legend_header_fill: string background color for legend header (in vertical layout), default is #eee
                :param legend_text_numeric_precision: decimal precision for numeric legend values
                :param legend_key_shape: shape of the legend item keys, default varies by viz type; one of square, contiguous_bar, rounded-square, circle, line
                """
        self.data = data
        self.opacity = opacity
        self.below_layer = below_layer
        self.legend = legend
        self.legend_layout = legend_layout
        self.legend_gradient = legend_gradient
        self.legend_text_numeric_precision = legend_text_numeric_precision
        self.legend_key_shape = legend_key_shape
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

        self.layer_id = None
        self.template = None
        self.label_property = None

    def create_html(self):
        options = dict(
            opacity=self.opacity,
            belowLayer=self.below_layer,
            showLegend=self.legend,
            legendLayout=self.legend_layout,
            legendGradient=json.dumps(self.legend_gradient),
            legendNumericPrecision=json.dumps(self.legend_text_numeric_precision),
            legendKeyShape=self.legend_key_shape,
            layerId=self.layer_id,
            template=self.template,
            minZoom=self.min_zoom,
            maxZoom=self.max_zoom
        )

        if self.label_property is None:
            options.update(labelProperty=None)
        else:
            options.update(labelProperty='{' + self.label_property + '}')

        self.get_layer_specific_variables(options)

        return templates.format(self.template, **options)

    def get_layer_specific_variables(self, options):
        pass


class CircleLayer(AbstractLayer):
    """Create a circle layer"""

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
        super(CircleLayer, self).__init__(data, *args, **kwargs)

        self.template = 'circle'
        self.label_property = label_property
        self.label_color = label_color
        self.label_size = label_size
        self.label_halo_color = label_halo_color
        self.label_halo_width = label_halo_width
        self.color_property = color_property
        self.color_stops = color_stops
        self.radius = radius
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.color_function_type = color_function_type
        self.color_default = color_default
        self.legend_key_shape = legend_key_shape

    def get_layer_specific_variables(self, options):
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
            labelColor=self.label_color,
            labelSize=self.label_size,
            labelHaloColor=self.label_halo_color,
            labelHaloWidth=self.label_halo_width,
        ))


class GraduatedCircleLayer(AbstractLayer):
    """Create a graduated circle layer"""

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
        super(GraduatedCircleLayer, self).__init__(data, *args, **kwargs)

        self.template = 'graduated_circle'
        self.label_property = label_property
        self.label_color = label_color
        self.label_size = label_size
        self.label_halo_color = label_halo_color
        self.label_halo_width = label_halo_width
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

    def get_layer_specific_variables(self, options):
        """Update map template variables specific to graduated circle visual"""
        options.update(dict(
            geojson_data=json.dumps(self.data, ensure_ascii=False),
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
            labelColor=self.label_color,
            labelSize=self.label_size,
            labelHaloColor=self.label_halo_color,
            labelHaloWidth=self.label_halo_width
        ))


class HeatmapLayer(AbstractLayer):
    """Create a heatmap layer"""

    def __init__(self,
                 data,
                 label_property=None,
                 weight_property=None,
                 weight_stops=None,
                 color_stops=None,
                 radius_stops=None,
                 intensity_stops=None,
                 *args,
                 **kwargs):
        """Create a heatmap layer

        :param weight_property: property to determine heatmap weight. EX. "population"
        :param weight_stops: stops to determine heatmap weight.  EX. [[10, 0], [100, 1]]
        :param color_stops: stops to determine heatmap color.  EX. [[0, "red"], [0.5, "blue"], [1, "green"]]
        :param radius_stops: stops to determine heatmap radius based on zoom.  EX: [[0, 1], [12, 30]]
        :param intensity_stops: stops to determine the heatmap intensity based on zoom. EX: [[0, 0.1], [20, 5]]

        """
        super(HeatmapLayer, self).__init__(data, *args, **kwargs)

        self.template = 'heatmap'
        self.label_property = label_property
        self.weight_property = weight_property
        self.weight_stops = weight_stops
        if color_stops:
            # Make the first color stop in a heatmap have opacity 0 for good visual effect
            self.color_stops = [[0.00001, 'rgba(0,0,0,0)']] + color_stops
        self.radius_stops = radius_stops
        self.intensity_stops = intensity_stops

    def get_layer_specific_variables(self, options):
        """Update map template variables specific to heatmap visual"""
        options.update(dict(
            geojson_data=json.dumps(self.data, ensure_ascii=False),
            colorStops=self.color_stops,
            radiusStops=self.radius_stops,
            weightProperty=self.weight_property,
            weightStops=self.weight_stops,
            intensityStops=self.intensity_stops,
        ))


class ClusteredCircleLayer(AbstractLayer):
    """Create a clustered circle layer"""

    def __init__(self,
                 data,
                 label_property=None,
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
        super(ClusteredCircleLayer, self).__init__(data, *args, **kwargs)

        self.template = 'clustered_circle'
        self.label_property = label_property
        self.label_color = label_color
        self.label_size = label_size
        self.label_halo_color = label_halo_color
        self.label_halo_width = label_halo_width
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

    def get_layer_specific_variables(self, options):
        """Update map template variables specific to a clustered circle visual"""
        options.update(dict(
            geojson_data=json.dumps(self.data, ensure_ascii=False),
            colorStops=self.color_stops,
            colorDefault=self.color_default,
            radiusStops=self.radius_stops,
            clusterRadius=self.clusterRadius,
            clusterMaxZoom=self.clusterMaxZoom,
            strokeWidth=self.stroke_width,
            strokeColor=self.stroke_color,
            radiusDefault=self.radius_default,
            labelColor=self.label_color,
            labelSize=self.label_size,
            labelHaloColor=self.label_halo_color,
            labelHaloWidth=self.label_halo_width
        ))


class ChoroplethLayer(AbstractLayer):
    """Create a choropleth layer"""

    def __init__(self,
                 data,
                 vector_url=None,
                 vector_layer_name=None,
                 vector_join_property=None,
                 data_join_property=None,  # vector only
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
        super(ChoroplethLayer, self).__init__(data, *args, **kwargs)

        self.vector_url = vector_url
        self.vector_layer_name = vector_layer_name
        self.vector_join_property = vector_join_property
        self.data_join_property = data_join_property

        if self.vector_url is not None and self.vector_layer_name is not None:
            self.template = 'vector_choropleth'
            self.vector_source = True
        else:
            self.template = 'choropleth'
            self.vector_source = False

        self.label_property = label_property
        self.color_property = color_property
        self.color_stops = color_stops
        self.color_default = color_default
        self.color_function_type = color_function_type
        self.line_color = line_color
        self.line_stroke = line_stroke
        self.line_width = line_width
        self.height_property = height_property
        self.height_stops = height_stops
        self.height_default = height_default
        self.height_function_type = height_function_type

    def generate_vector_color_map(self):
        """Generate color stops array for use with match expression in mapbox template"""
        vector_stops = []
        for row in self.data:
            # map color to JSON feature using color_property
            color = color_map(row[self.color_property], self.color_stops, self.color_default)

            # link to vector feature using data_join_property (from JSON object)
            vector_stops.append([row[self.data_join_property], color])

        return vector_stops

    def generate_vector_height_map(self):
        """Generate height stops array for use with match expression in mapbox template"""
        vector_stops = []

        if self.height_function_type == 'match':
            match_height = self.height_stops

        for row in self.data:
            # map height to JSON feature using height_property
            height = height_map(row[self.height_property], self.height_stops, self.height_default)

            # link to vector feature using data_join_property (from JSON object)
            vector_stops.append([row[self.data_join_property], height])

        return vector_stops

    def get_layer_specific_variables(self, options):
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
            extrudeChoropleth=self.extrude
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
            options.update(dict(
                vectorUrl=self.vector_url,
                vectorLayer=self.vector_layer_name,
                vectorColorStops=self.generate_vector_color_map(),
                vectorJoinDataProperty=self.vector_join_property,
                joinData=json.dumps(self.data, ensure_ascii=False),
                dataJoinProperty=self.data_join_property,
            ))
            if self.extrude:
                options.update(dict(
                    vectorHeightStops=self.generate_vector_height_map(),
                ))

        # geojson-based choropleth map variables
        else:
            options.update(dict(
                geojson_data=json.dumps(self.data, ensure_ascii=False),
            ))


class ImageLayer(AbstractLayer):
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
        super(ImageLayer, self).__init__(None, *args, **kwargs)

        if type(image) is numpy.ndarray:
            image = img_encode(image)

        self.template = 'image'
        self.image = image
        self.coordinates = coordinates

    def get_layer_specific_variables(self, options):
        """Update map template variables specific to image visual"""
        options.update(dict(
            image=self.image,
            coordinates=self.coordinates))


class RasterTilesLayer(AbstractLayer):
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
        super(RasterTilesLayer, self).__init__(None, *args, **kwargs)

        self.template = 'raster'
        self.tiles_url = tiles_url
        self.tiles_size = tiles_size
        self.tiles_bounds = tiles_bounds
        self.tiles_minzoom = tiles_minzoom
        self.tiles_maxzoom = tiles_maxzoom

    def get_layer_specific_variables(self, options):
        """Update map template variables specific to a raster visual"""
        options.update(dict(
            tiles_url=self.tiles_url,
            tiles_size=self.tiles_size,
            tiles_minzoom=self.tiles_minzoom,
            tiles_maxzoom=self.tiles_maxzoom,
            tiles_bounds=self.tiles_bounds if self.tiles_bounds else 'undefined'))


class LinestringLayer(AbstractLayer):
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
        super(LinestringLayer, self).__init__(data, *args, **kwargs)

        self.vector_url = vector_url
        self.vector_layer_name = vector_layer_name
        self.vector_join_property = vector_join_property
        self.data_join_property = data_join_property

        if self.vector_url is not None and self.vector_layer_name is not None:
            self.template = 'vector_linestring'
            self.vector_source = True
        else:
            self.vector_source = False
            self.template = 'linestring'

        self.label_property = label_property
        self.label_color = label_color
        self.label_size = label_size
        self.label_halo_color = label_halo_color
        self.label_halo_width = label_halo_width
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

    def generate_vector_color_map(self):
        """Generate color stops array for use with match expression in mapbox template"""
        vector_stops = []
        for row in self.data:
            # map color to JSON feature using color_property
            color = color_map(row[self.color_property], self.color_stops, self.color_default)

            # link to vector feature using data_join_property (from JSON object)
            vector_stops.append([row[self.data_join_property], color])

        return vector_stops

    def generate_vector_width_map(self):
        """Generate width stops array for use with match expression in mapbox template"""
        vector_stops = []

        if self.line_width_function_type == 'match':
            match_width = self.line_width_stops

        for row in self.data:
            # map width to JSON feature using width_property
            width = numeric_map(row[self.line_width_property], self.line_width_stops, self.line_width_default)

            # link to vector feature using data_join_property (from JSON object)
            vector_stops.append([row[self.data_join_property], width])

        return vector_stops

    def get_layer_specific_variables(self, options):
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
            labelColor=self.label_color,
            labelSize=self.label_size,
            labelHaloColor=self.label_halo_color,
            labelHaloWidth=self.label_halo_width
        ))

        # vector-based linestring map variables
        if self.vector_source:
            options.update(dict(
                vectorUrl=self.vector_url,
                vectorLayer=self.vector_layer_name,
                vectorJoinDataProperty=self.vector_join_property,
                vectorColorStops=[[0, self.color_default]],
                vectorWidthStops=[[0, self.line_width_default]],
                joinData=json.dumps(self.data, ensure_ascii=False),
                dataJoinProperty=self.data_join_property,
            ))

            if self.color_property:
                options.update(dict(vectorColorStops=self.generate_vector_color_map()))

            if self.line_width_property:
                options.update(dict(vectorWidthStops=self.generate_vector_width_map()))

        # geojson-based linestring map variables
        else:
            options.update(dict(
                geojson_data=json.dumps(self.data, ensure_ascii=False),
            ))
