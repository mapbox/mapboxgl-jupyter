# Roadmap for `mapboxgl-jupyter` 1.0 release

Here are some ideas for future releases. If you're
interested in any of these features and would like to help out,
please start an Issue on github with more details.
    
## Working on Next

- [ ] Support categorical measure data.
- [ ] Add choropleth / fill visualization type
- [ ] PNG image export of map and data to file
- [ ] Add raster data layers (via Rastero, numpy array, or WMS server)

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
