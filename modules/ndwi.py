from modules.cloudmask import *
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
    file_clouds
    print('debugging 1: '+banddir+'\n')
    p3 = glob.glob(banddir + '/*B03.jp2')
    p8 = glob.glob(banddir + '/*B08.jp2')
    print('debugging 2: getting paths to bands \n')

    #### add clause "in case there is a cloud file"
    try:
        clouds10 = interpolate_clouds_to_10m(file_clouds)
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))

    print('debugging 3: clouds 10 finished\n')

    clouds_bool = (clouds10==2) | (clouds10==3)

    ### the product is provided as a uint16.
    ### usually one could divide by 1000 to get the real TOA values,
    ### but since we are interested in the index, there is no need for that
    dataset3 = rio.open(p3[0])
    band3 = dataset3.read(1)
    ### here we convert it o float so the division will work.
    band3 = band3.astype(float)
    print('debugging 4: band 3 opened and type set\n')

    dataset8 = rio.open(p8[0])
    band8 = dataset8.read(1)
    band8 = band8.astype(float)
    print('debugging 5: band 8 opened and type set\n')

#    profile = dataset3.profile
#    profile.update(dtype=int,driver='GTiff',count=1)
#    print('debugging 6: profile of ndwi set. calculating ndwi\n')

    #### there should not be any zeros in the denominator, because the products are unsigned int!
    #print('debugging 7: avoiding zeros in the denominator')
    #notzeros= (band3+band8 != 0)

    NDWI = (band3-band8)/(band3+band8)

    print('filtering out clouds:\n')

    ndwi_bool = NDWI[np.logical_not(clouds_bool)] > 0

    print('potentially critical point: from boolean to int\n')
    ndwi_int=ndwi_bool.astype('int16')

    print('debugging 8: writing out\n')
    with rio.open(pths.s2aOut + "/" + scene + '.tif', 'w',driver='GTiff',height=ndwi_int.shape[0], width=ndwi_int.shape[1],count=1,dtype=np.int16) as dst:
        dst.write(ndwi_int, 1)
    #dst.write(ndwi.astype(rio.float64), 1)


def ndwi2watermask():
    print("Executing ndwi2watermask():")
    items=os.listdir(pths.s2aIn)
    for item in items:
        item=pths.s2aIn + '/' + item
        if re.search('^.*\.zip$', item):
            sceneJp2 = unzipJp2(item)
            print('building vrt\n')
            runGdalbuildvrt(sceneJp2)
            print('fmask: making angles\n')
            runFmaskMakeAngles(sceneJp2)
            print('fmask: generating cloud mask\n')
            runFmaskStack(sceneJp2)
            print('fmask: finished ' + item+'\n')
            print('creating ndwi: ' + item+'\n')
            ndwi_from_jp2(sceneJp2)
