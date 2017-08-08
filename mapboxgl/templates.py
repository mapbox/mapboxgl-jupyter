
MAP_CSS = ''' body { margin:0; padding:0; }
             .map { position:absolute; top:0; bottom:0; width:100%; }'''

GL_JS_VERSION = 'v0.39.1'

HTML_HEAD = '''
<html><head>
    <meta charset='utf-8' />
    <title>mapboxgl_py viz</title>
    <meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no' />
    <script src='https://api.tiles.mapbox.com/mapbox-gl-js/{gl_js_version}/mapbox-gl.js'></script>
    <link href='https://api.tiles.mapbox.com/mapbox-gl-js/{gl_js_version}/mapbox-gl.css' rel='stylesheet' />
    <style>{map_css}</style>
</head>
<body>
<div id='map' class='map'></div>
<script>
'''.format(gl_js_version=GL_JS_VERSION, map_css=MAP_CSS)

HTML_TAIL = '''</script></body></html>'''

HTML_CIRCLE_VIZ = """
    mapboxgl.accessToken = '{accessToken}';

    // Load the map
    var map = new mapboxgl.Map({{
        container: 'map',
        style: '{styleUrl}', 
        center: {center},
        zoom: {zoom}
    }});

    // Add our data for viz when the map loads
    map.on('load', function() {{
        
        map.addSource("data", {{
            "type": "geojson",
            "data": {geojson_data}, //data from dataframe output to geojson
            "buffer": 1,
            "maxzoom": 14
        }});
        
        map.addLayer({{
            "id": "circle",
            "source": "data",
            "type": "circle",
            "paint": {{
                "circle-color": {{
                    "property": "{colorProperty}", //Data property to style color by from python variable
                    "stops": {colorStops}  // Color stops array to use based on data values from python variable
                }},
                "circle-radius" : {{
                    "stops": [[0,1], [18,10]]
                }},
                "circle-stroke-color": "white",
                "circle-stroke-width": {{
                    "stops": [[0,0.01], [18,1]]
                }}
            }}
        }}, "waterway-label");
        
        // Create a popup
        var popup = new mapboxgl.Popup({{
            closeButton: false,
            closeOnClick: false
        }});
        
        // Show the popup on mouseover
        map.on('mousemove', 'circle', function(e) {{
            map.getCanvas().style.cursor = 'pointer';
            popup.setLngLat(e.features[0].geometry.coordinates)
                .setHTML('<li> {colorProperty}: $' + e.features[0].properties["{colorProperty}"] + '</li>')
                .addTo(map);
        }});

        map.on('mouseleave', 'circle', function() {{
            map.getCanvas().style.cursor = '';
            popup.remove();
        }});
        
        // Fly to on click
        map.on('click', 'circle', function(e) {{
            map.flyTo({{
                center: e.features[0].geometry.coordinates,
                zoom: 10
            }});
        }});
    }});
"""
