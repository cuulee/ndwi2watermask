import rasterio as rio
from rasterio.windows import Window


import modules.getPaths as pths

import matplotlib.pyplot as plt
import numpy as np
import subprocess
from skimage.filters import threshold_otsu, threshold_local
from defCloudMask import unzipJp2, getBandDir
import re

zipfls=[]
items=os.listdir(pths.s2aIn)

for item in items:
    item=pths.s2aIn + '/' + item
    if re.search('^.*\.zip$', item) :
        zipfls.append(item)
        sceneJp2 = unzipJp2(item)

    banddir = getBandDir(sceneJp2)
    file_clouds = banddir + '/cloud.img'
p3 = banddir + '/*B03.jp2'
p8 = '/home/delgado/scratch/s2a_scenes/in/S2A_MSIL1C_20170728T130251_N0205_R095_T24MUV_20170728T130248.SAFE/GRANULE/L1C_T24MUV_A010960_20170728T130248/IMG_DATA/T24MUV_20170728T130251_B08.jp2'


dataset_clouds = rio.open(file_clouds)
clouds = dataset_clouds.read(1)
clouds10 = np.empty(shape=(int(round(clouds.shape[0] * 2)),
                         int(round(clouds.shape[1] * 2))))

from affine import Affine
aff = dataset_clouds.transform
newaff = Affine(aff[0] / 2, aff[1], aff[2],aff[3], aff[4] / 2, aff[5])

from rasterio.warp import reproject,Resampling

reproject(clouds, clouds10,
    src_transform = aff,
    dst_transform = newaff,
    src_crs = dataset_clouds.crs,
    dst_crs = dataset_clouds.crs,
    resampling = Resampling.nearest)


clouds_bin = (clouds10==2) | (clouds10==3)

plt.imshow(clouds_bin)


#transx=5000
#transy=5000
#h=5000
#w=5000


dataset3 = rio.open(p3)
band3 = dataset3.read(1)
#band3 = dataset3.read(1,window=Window(transx,transy,w,h))

dataset8 = rio.open(p8)
band8 = dataset8.read(1)

profile = dataset3.profile
profile.update(dtype=rio.uint8,count=1)#,height=h,width=w,transform=profile['transform']*Affine.translation(transx,transy))

#fileName='example-ndwi_dummy'

#with rio.open(fileName+'.jp2', 'w', **profile) as dst:
#    dst.write(band.astype(rio.uint8), 1)

NDWI = (band3-band8)/(band3+band8)
NDWI.max()

###### should be between 0 and 1 !!!
ndwi = NDWI[not clouds_bin]>0.5


plt.imshow(ndwi.astype(rio.uint8))

fileName='example-ndwi_manual'

with rio.open(fileName+'.jp2', 'w', **profile) as dst:
    dst.write(ndwi.astype(rio.uint8), 1)
