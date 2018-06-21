# Roadmap for `mapboxgl-jupyter` 1.0 release

Here are some ideas for future releases. If you're
interested in any of these features and would like to help out,
please start an Issue on github with more details.
    
## Working on Next

- [ ] Multiple visual layers in one map
- [ ] Hover/Highlight/select styles on mousemove and selection on click
- [ ] PNG/JPG image export of map and data to file
- [ ] Great Arc map layers from source-to-destination point

## Down-the-road

- [ ] Control map interactivity with python vars
- [ ] Add shapely points, lines, and polygons to map (with projection wrapper around non-4326 shapes)
- [ ] `dashboard-like` tabular views with filtering
- [ ] Add user-defined html templates for popups

## Recently completed

- [x] Add methods for determining breaks (jenks, etc)
    * Added jerks support in 0.2.0
- [x] graduated symbols for circleviz
    * Implemented in 0.2.0
- [x] legend
    * Implemented in 0.2.0
- [x] html templates for property display on mouseover
    * Implemented in 0.3.0
- [x] Add heatmap visualization type
    * Implemented in 0.1.0
- [x] Added clustered circle viz type
    * Implemented in 0.1.1
- [x] Use PySAL for data domain natural breaks classification in example
    * Implemented in 0.1.1
- [x] Support categorical measure data.
    * Implemneted in 0.5.1
- [x] Add raster tile and image data layers
    * Added in 0.6.0
- [x] Add choropleth / fill visualization type
    * Added in 0.6.0
- [x] 3D extrusion map
    * Added in 0.7.0
- [x] Linestring map
    * Added in 0.7.0
