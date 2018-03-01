from modules.cloudmask import getBandDir,interpolate_clouds_to_10m,unzipJp2,rmclouds
import glob
import rasterio as rio
import zipfile
import os
import modules.getpaths as pths
import numpy as np
import re

def ndwi_from_jp2(sceneJp2):
    scene=sceneJp2[0].split(".SAFE/GRANULE")[0]
    banddir = getBandDir(sceneJp2)
    file_clouds = banddir + '/cloud.img'
    print('debugging 1: '+banddir+'\n')
    p3 = glob.glob(banddir + '/*B03.jp2')
    p8 = glob.glob(banddir + '/*B08.jp2')
    print('debugging 2: getting paths to bands \n')

    #### add clause "in case there is a cloud file"
    if os.path.isfile(file_clouds):
        clouds10 = interpolate_clouds_to_10m(file_clouds)
    else:
        return('please run main with argument "rmclouds"')

    aff = dataset_clouds.transform
    newaff = Affine(aff[0] / 2, aff[1], aff[2],aff[3], aff[4] / 2, aff[5])
    reproject(clouds, clouds10,
        src_transform = aff,
        dst_transform = newaff,
        src_crs = dataset_clouds.crs,
        dst_crs = dataset_clouds.crs,
        resampling = Resampling.nearest)

    print('debugging 3: clouds 10 finished\n')

    clouds_bin = (clouds10==2) | (clouds10==3)

    dataset3 = rio.open(p3[0])
    band3 = dataset3.read(1)
    band3 = band3.astype(float)
    print('debugging 4: band 3 opened and type set\n')

    dataset8 = rio.open(p8[0])
    band8 = dataset8.read(1)
    band8 = band8.astype(float)
    print('debugging 5: band 8 opened and type set\n')

    profile = dataset3.profile
    profile.update(dtype=rio.int8,count=1)
    print('debugging 6: profile of ndwi set\n')

    print('debugging 7: avoiding zeros in the denominator')
    notzeros= (band3+band8 != 0)

    NDWI = (band3[notzeros]-band8[notzeros])/(band3[notzeros]+band8[notzeros])

    ###### should be between 0 and 1 !!!
    ndwi = NDWI[not clouds_bin] > 0.5

    print('debugging 8: writing out\n')
    with rio.open(pths.polOut + "/" + scene + '.tif', 'w', **profile) as dst:
        dst.write(ndwi.astype(rio.int8), 1)
    #dst.write(ndwi.astype(rio.float64), 1)


def ndwi2watermask():
    print("Executing ndwi2watermask():")
    items=os.listdir(pths.s2aIn)
    item=items[0]
    items[0]
    item
    for item in items:
        item=pths.s2aIn + '/' + item
        if re.search('^.*\.zip$', item):
            sceneJp2 = unzipJp2(item)
            ndwi_from_jp2(sceneJp2)
