from modules.cloudmask import *
import glob
import rasterio as rio
import zipfile
import os
import modules.getpaths as pths
import numpy as np
import re


### some exercises with matrices to make sure everything is working below
#ar=np.random.random_integers(0,100,2500)
#ar.shape=(50,50)
#ar_bool = ar > 50
#ar_out[ar<50] =

#ar_bool.shape

#ar[ar_bool] = 0
#ar.shape


def ndwi_from_jp2(sceneJp2):
    scene=sceneJp2[0].split(".SAFE/GRANULE")[0]
    banddir = getBandDir(sceneJp2)
    file_clouds = banddir + '/cloud.img'
    file_clouds
    print('debugging 1: '+banddir+'\n')
    p3 = glob.glob(banddir + '/*B03.jp2')
    p8 = glob.glob(banddir + '/*B08.jp2')
    print('debugging 2: getting paths to bands \n')

    ### the product is provided as a uint16.
    ### usually one could divide by 1000 to get the real TOA values,
    ### but since we are interested in the index, there is no need for that
    dataset3 = rio.open(p3[0])
    band3 = dataset3.read(1)
    ### here we convert it o float so the division will work.
    band3 = band3.astype(float)
    print('debugging 3: band 3 opened and type set\n')

    dataset8 = rio.open(p8[0])
    band8 = dataset8.read(1)
    band8 = band8.astype(float)
    print('debugging 4: band 8 opened and type set\n')

    #### add clause "in case there is a cloud file"
#    try:
    clouds10 = interpolate_clouds_to_10m(file_clouds)
#    except Exception, err:
#        sys.stderr.write('ERROR: %s\n' % str(err))

    print('debugging 5: clouds 10 finished\n')

    clouds_bool = (clouds10==2) | (clouds10==3)

#    profile = dataset3.profile
#    profile.update(dtype=int,driver='GTiff',count=1)
#    print('debugging 6: profile of ndwi set. calculating ndwi\n')

    #### there should not be any zeros in the denominator, because the products are unsigned int!
    #print('debugging 7: avoiding zeros in the denominator')
    #notzeros= (band3+band8 != 0)

    NDWI = (band3-band8)/(band3+band8)

    print('ndwi shape:\n')
    print(NDWI[1:5,1:5])
    print(NDWI.shape)
    print('clouds_bool shape:\n')
    print(clouds_bool[1:5,1:5])
    print(clouds_bool.shape)

    ndwi_bool = NDWI > 0
    print('ndwi_bool shape:\n')
    print(ndwi_bool.shape)
    print(ndwi_bool[1:5,1:5])

    print('potentially critical point: from boolean to int\n')
    ndwi_int=ndwi_bool.astype('int16')
    ndwi_int[clouds_bool] = 0
    print('ndwi_int shape:\n')
    print(ndwi_int.shape)
    print(ndwi_int[1:5,1:5])

    print('debugging 8: writing out\n')
    with rio.open(pths.s2aOut + "/" + scene + '.tif', 'w',driver='GTiff',crs=dataset3.crs,transform=dataset3.transform,height=ndwi_int.shape[0], width=ndwi_int.shape[1],count=1,dtype=np.int16) as dst:
        dst.write(ndwi_int, 1)


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




def test_one_ndwi():
    print("Executing ndwi2watermask():")
    #items=os.listdir(pths.s2aIn)
    items=['S2A_MSIL1C_20180223T130241_N0206_R095_T24MTT_20180223T192653.zip']
    for item in items:
        item=pths.s2aIn + '/' + item
        if re.search('^.*\.zip$', item):
            sceneJp2 = unzipJp2(item)
            ndwi_from_jp2(sceneJp2)
