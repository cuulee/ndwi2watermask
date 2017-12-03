# connect to the API
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime, timedelta
import sys 
import os

sys.path.append(os.path.abspath("/users/stud09/martinsd/proj/sar2watermask/parameters"))

from credentials import *

api = SentinelAPI(username, password, 'https://scihub.copernicus.eu/dhus')

# download single scene by known product id
#api.download(<product_id>)
t0 = datetime.now() - timedelta(days=7)
tf = datetime.now()
# search by polygon, time, and SciHub query keywords
footprint = geojson_to_wkt(read_geojson('/users/stud09/martinsd/proj/sar2watermask/parameters/extent_ce.geojson'))
products = api.query(footprint,
                     date=(
                         date(t0.year,t0.month,t0.day),
                         date(tf.year,tf.month,tf.day)
                     ),
                     producttype="GRD",
                     platformname='Sentinel-1')


# download all results from the search
api.download_all(products,directory_path="/mnt/scratch/martinsd/s1a_scenes/in")
