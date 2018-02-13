import rasterio as rio
from rasterio.windows import Window
import os
import modules.getPaths as pths

import matplotlib.pyplot as plt
import numpy as np
import subprocess
from skimage.filters import threshold_otsu, threshold_local
from modules.defCloudMask import unzipJp2, getBandDir,interpolate_clouds_to_10m
import glob

zipfls=[]
items=os.listdir(pths.s2aIn)

for item in items:
    item=pths.s2aIn + '/' + item
    if re.search('^.*\.zip$', item) :
        zipfls.append(item)
        sceneJp2 = unzipJp2(item)

    banddir = getBandDir(sceneJp2)
    file_clouds = banddir + '/cloud.img'

p3 = glob.glob(banddir + '/*B03.jp2')
p8 = glob.glob(banddir + '/*B08.jp2')

clouds10 = interpolate_clouds_to_10m(file_clouds)

clouds_bin = (clouds10==2) | (clouds10==3)

dataset3 = rio.open(p3[0])
band3 = dataset3.read(1)
band3 = band3.astype(float)

dataset8 = rio.open(p8)
band8 = dataset8.read(1)
band8 = band8.astype(float)

profile = dataset3.profile
profile.update(dtype=rio.uint8,count=1)

NDWI = (band3-band8)/(band3+band8)

###### should be between 0 and 1 !!!
ndwi = NDWI[not clouds_bin]

with rio.open(banddir + 'ndwi.img', 'w', **profile) as dst:
    dst.write(ndwi.astype(rio.float64), 1)
