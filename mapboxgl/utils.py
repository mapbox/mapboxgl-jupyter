
def df_to_geojson(df, properties=None, lat='lat', lon='lon', precision=None):
    """Serialize a Pandas dataframe to a geojson format Python dictionary
    """
    geojson = {'type': 'FeatureCollection', 'features': []}

    if precision:
        df[lat] = df[lat].round(precision)
        df[lon] = df[lon].round(precision)

    if not properties:
        properties = list(df.columns)

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
