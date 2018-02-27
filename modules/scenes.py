# connect to the API
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime, timedelta
import sys
import os
from modules.getpaths import *


def getscenes():
    api = SentinelAPI(username, password, 'https://scihub.copernicus.eu/dhus')

    # download single scene by known product id
    #api.download(<product_id>)
    t0 = datetime.now() - timedelta(days=7)
    tf = datetime.now()
    # search by polygon, time, and SciHub query keywords
    footprint = geojson_to_wkt(read_geojson(home['parameters'] + '/extent_ce.geojson'))
    products = api.query(footprint,
                        date=(
                            date(t0.year,t0.month,t0.day),
                            date(tf.year,tf.month,tf.day)
                            ),
                            platformname='Sentinel-2',
                            cloudcoverpercentage = (0, 30))
    products

    # download all results from the search
    #s2aIn = '/home/delgado/Documents/tmp' # in case you are just testing
    api.download_all(products,directory_path=s2aIn)
