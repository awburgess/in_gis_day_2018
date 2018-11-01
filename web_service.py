import hug
from sqlalchemy import create_engine

import config

_ENGINE = create_engine(config.CONNECTION_STRING)


@hug.get()
@hug.local()
def burgle_me(lat: hug.types.text, lon: hug.types.text):
    """
    Make yourself paranoid by passing in a lat/lon and finding out how much
    robbery goes on near you

    Args:
        lat: Latitude in Indianapolis
        lon: Longitude in Indianapolis

    Returns:
        GeoJSON object with location and details
    """
    query = config.SQL.format(lat=lat, lon=lon)
    result = _ENGINE.execute(query).fetchall()
    return result[0][0]
