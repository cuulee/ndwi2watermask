# connect to the API
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date, datetime
import sys 
import os

sys.path.append(os.path.abspath("/users/stud09/martinsd/proj/sar2watermask/parameters"))

from credentials import *

api = SentinelAPI(username, password, 'https://scihub.copernicus.eu/dhus')

# download single scene by known product id
#api.download(<product_id>)

# search by polygon, time, and SciHub query keywords
footprint = geojson_to_wkt(read_geojson('/users/stud09/martinsd/proj/sar2watermask/parameters/extent_ce.geojson'))
products = api.query(footprint,
                     date=(
                         date(datetime.now().year,datetime.now().month,datetime.now().day-7),
                         date(datetime.now().year,datetime.now().month,datetime.now().day)
                     ),
                     producttype="GRD",
                     platformname='Sentinel-1')


# download all results from the search
api.download_all(products,directory_path="/mnt/scratch/martinsd/s1a_scenes/in")
