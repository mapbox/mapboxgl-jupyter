
MAP_CSS = ''' body { margin:0; padding:0; }

             .map { position:absolute; top:0; bottom:0; width:100%; }

            .legend {
                background-color: white;
                color: black;
                border-radius: 3px;
                bottom: 50px;
                width: 100px;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.10);
                font: 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
                padding: 12px;
                position: absolute;
                right: 10px;
                z-index: 1;
            }

            .legend h4 {
                margin: 0 0 10px;
            }

            .legend-title {
                margin: 6px;
                padding: 6px:
                font-weight: bold;
                font-size: 14px;
                font: 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
            }

            .legend div span {
                border-radius: 50%;
                display: inline-block;
                height: 10px;
                margin-right: 5px;
                width: 10px;'''

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
<div id='legend' class='legend'></div>
<script>
'''.format(gl_js_version=GL_JS_VERSION, map_css=MAP_CSS)

CALC_CIRCLE_COLOR_LEGEND = '''
function calcCircleColorLegend(myColorStops, title) {{
    //Calculate a legend element on a Mapbox GL Style Spec property function stops array
    var mytitle = document.createElement('div');
    mytitle.textContent = title;
    mytitle.className = 'legend-title'
    var legend = document.getElementById('legend');
    legend.appendChild(mytitle);

    for (p = 0; p < myColorStops.length; p++) {{
        if (!!document.getElementById('legend-points-value-' + p)) {{
            //update the legend if it already exists

            document.getElementById('legend-points-value-' + p).textContent = myColorStops[p][0];
            document.getElementById('legend-points-id-' + p).style.backgroundColor = myColorStops[p][1];
        }} else {{
            //create the legend if it doesn't yet exist

            var item = document.createElement('div');
            var key = document.createElement('span');
            key.className = 'legend-key';
            var value = document.createElement('span');

            key.id = 'legend-points-id-' + p;
            key.style.backgroundColor = myColorStops[p][1];
            value.id = 'legend-points-value-' + p;

            item.appendChild(key);
            item.appendChild(value);
            legend.appendChild(item);
            
            data = document.getElementById('legend-points-value-' + p)
            data.textContent = myColorStops[p][0];
        }}
    }}
}}'''

HTML_TAIL = '''</script></body></html>'''

HTML_CIRCLE_VIZ = """
    {calcCircleColorLegend}

    mapboxgl.accessToken = '{accessToken}';

    // Load the map
    var map = new mapboxgl.Map({{
        container: 'map',
        style: '{styleUrl}', 
        center: {center},
        zoom: {zoom}
    }});

    calcCircleColorLegend({colorStops}, "{colorProperty}")

    // Add our data for viz when the map loads
    map.on('load', function() {{
        
        map.addSource("data", {{
            "type": "geojson",
            "data": {geojson_data}, //data from dataframe output to geojson
            "buffer": 1,
            "maxzoom": 14
        }});

        map.addLayer({{
            "id": "label",
            "source": "data",
            "type": "symbol",
            "layout": {{
                "text-field": "{{{labelProperty}}}",
                "text-size" : {{ "stops": [[0,8],[22,16]] }},
                "text-offset": [0,-1],
            }},
            "paint": {{
                "text-halo-color": "white",
                "text-halo-width": 1
            }}
        }}, 'waterway-label')
        
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
        }}, "label");
        
        // Create a popup
        var popup = new mapboxgl.Popup({{
            closeButton: false,
            closeOnClick: false
        }});
        
        // Show the popup on mouseover
        map.on('mousemove', 'circle', function(e) {{
            map.getCanvas().style.cursor = 'pointer';
            popup.setLngLat(e.features[0].geometry.coordinates)
                .setHTML('<li> {colorProperty}: ' + e.features[0].properties["{colorProperty}"] + '</li>')
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

HTML_GRADUATED_CIRCLE_VIZ = """
    {calcCircleColorLegend}

    mapboxgl.accessToken = '{accessToken}';

    // Load the map
    var map = new mapboxgl.Map({{
        container: 'map',
        style: '{styleUrl}', 
        center: {center},
        zoom: {zoom}
    }});

    calcCircleColorLegend({colorStops}, "{colorProperty} vs. {radiusProperty}")

    // Add our data for viz when the map loads
    map.on('load', function() {{
        
        map.addSource("data", {{
            "type": "geojson",
            "data": {geojson_data}, //data from dataframe output to geojson
            "buffer": 1,
            "maxzoom": 14
        }});

        map.addLayer({{
            "id": "label",
            "source": "data",
            "type": "symbol",
            "layout": {{
                "text-field": "{{{labelProperty}}}",
                "text-size" : {{ "stops": [[0,8],[22,16]] }},
                "text-offset": [0,-1],
            }},
            "paint": {{
                "text-halo-color": "white",
                "text-halo-width": 1
            }}
        }}, 'waterway-label')

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
                    "property": "{radiusProperty}", //Data property to style radius by from python variable
                    "stops": {radiusStops}  // Radius stops array to adjust radius on data values from python variable
                }},
                "circle-stroke-color": "white",
                "circle-stroke-width": {{
                    "stops": [[0,0.01], [18,1]]
                }}
            }}
        }}, "label");
        
        // Create a popup
        var popup = new mapboxgl.Popup({{
            closeButton: false,
            closeOnClick: false
        }});
        
        // Show the popup on mouseover
        map.on('mousemove', 'circle', function(e) {{
            map.getCanvas().style.cursor = 'pointer';
            popup.setLngLat(e.features[0].geometry.coordinates)
                .setHTML('<ul><li> {colorProperty}: ' + e.features[0].properties["{colorProperty}"] + '</li>' +
                '<li> {radiusProperty}: ' + e.features[0].properties["{radiusProperty}"] + '</li></ul>')
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
