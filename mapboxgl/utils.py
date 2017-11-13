
def df_to_geojson(df, properties=None, lat='lat', lon='lon', precision=None):
    """Serialize a Pandas dataframe to a geojson format Python dictionary
    """
    geojson = {'type': 'FeatureCollection', 'features': []}

    if precision:
        df[lat] = df[lat].round(precision)
        df[lon] = df[lon].round(precision)

    if not properties:
        properties = [c for c in df.columns if c not in [lat, lon]]

    for _, row in df.iterrows():
        feature = {
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'Point',
                'coordinates': [row[lon], row[lat]]}}

        # TODO performance
        for prop in properties:
            feature['properties'][prop] = row[prop]

        geojson['features'].append(feature)

    return geojson


def scale_between(minval, maxval, numStops):
    """ Scale a min and max value to equal interval domain with
        numStops discrete values
    """

    scale = []

    if numStops < 2:
        return [minval, maxval]
    elif maxval < minval:
        raise ValueError()
    else:
        domain = maxval - minval
        interval = domain/numStops
        for i in range(numStops):
            scale.append(round(minval + interval*i, 2))
        return scale


def create_radius_stops(breaks, min_radius, max_radius):
    """Convert a data breaks into a radius ramp
    """
    num_breaks = len(breaks)
    radius_breaks = scale_between(min_radius, max_radius, num_breaks)
    stops = []

    for i, b in enumerate(breaks):
        stops.append([b, radius_breaks[i]])
    return stops


def create_weight_stops(breaks):
    """Convert data breaks into a heatmap-weight ramp
    """
    num_breaks = len(breaks)
    weight_breaks = scale_between(0, 1, num_breaks)
    stops = []

    for i, b in enumerate(breaks):
        stops.append([b, weight_breaks[i]])
    return stops
