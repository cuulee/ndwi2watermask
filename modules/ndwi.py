import rasterio.mask
from modules.cloudmask import list_pols,merge_pols,unzipJp2,unzipMasks,getBandDir
import fiona
import glob
import rasterio as rio
import zipfile
import os
import modules.getpaths as pths
import numpy as np
import re
from shutil import rmtree
import json
from rasterio.features import shapes
## some exercises with geotiffs:

#scene='/home/delgado/scratch/s2a_scenes/out/S2A_MSIL1C_20180223T130241_N0206_R095_T24MTT_20180223T192653.tif'
#dataset = rio.open(scene)

## this is not working in current version of rasterio (0.36)
#with rio.open(scene) as src:
#    w = src.read(1, window=Window(0, 0, 10, 10))

#dataset.crs
#band3 = dataset3.read(1)


### some exercises with matrices to make sure everything is working below
#ar=np.random.random_integers(0,100,2500)
#ar.shape=(50,50)
#np.sum(ar > -1)
#ar_out[ar<50] =

#ar_bool.shape

#ar[ar_bool] = 0
#ar.shape
pths.s2aIn="/home/delgado/Documents/tmp"
def ndwi2watermask():
    print("Executing ndwi2watermask():")
    items=os.listdir(pths.s2aIn)
    for item in items:
        item=pths.s2aIn + '/' + item
        if re.search('^.*\.zip$', item):
            sceneJp2 = unzipJp2(item)
            sceneMasks = unzipMasks(item)

            ### use nodata and clouds as masks
            masks = list_pols(sceneMasks)

            scene=sceneJp2[0].split(".SAFE/GRANULE")[0]
            banddir = getBandDir(sceneJp2)
            maskdir = getBandDir(sceneMasks)

            p3 = glob.glob(banddir + '/*B03.jp2')
            p8 = glob.glob(banddir + '/*B08.jp2')

            ### the product is provided as a uint16.
            ### usually one could divide by 1000 to get the real TOA values,
            ### but since we are interested in the index, there is no need for that
            print("Opening band 3\n")
            dataset3 = rio.open(p3[0])
            band3, out_transform =rasterio.mask.mask(dataset3,masks,all_touched=True,invert=False)
            band3 = band3.astype(float)

            print("Opening band 8\n")
            dataset8 = rio.open(p8[0])
            band8, out_transform =rasterio.mask.mask(dataset8,masks,all_touched=True,invert=False)
            band8 = band8.astype(float)



            print("Computing NDWI\n")

            NDWI = (band3-band8)/(band3+band8)
            ndwi_bool = NDWI > 0

            print('potentially critical point: from boolean to int\n')
            ndwi_int=ndwi_bool.astype('int16')

            ### polygonize
            lpols = shapes(ndwi_int)


            #os.remove(item)
            #rmtree(item[:-4]+'.SAFE')



def ndwi_from_jp2(sceneJp2):
#### no interpolation necessary because clouds are being computed in 10 m resolution

#    clouds10 = interpolate_clouds_to_10m(file_clouds)
#    except Exception, err:
#        sys.stderr.write('ERROR: %s\n' % str(err))
    if(os.path.isfile(file_clouds)):
        dataset_clouds = rio.open(file_clouds)
        clouds10 = dataset_clouds.read(1)

    ## proceed only if the cloudmask is smaller than 70% of total scene
        if(np.sum(clouds10) < 0.7*band3.shape[0]*band3.shape[1]):

            clouds_bool = (clouds10==2) | (clouds10==3)
            print('clouds_bool shape:\n')
            print(clouds_bool[1:5,1:5])
            print(clouds_bool.shape)

            ndwi_int[clouds_bool] = 0
            print('ndwi_int shape:\n')
            print(ndwi_int.shape)
            print(ndwi_int[1:5,1:5])

            print('debugging 8: writing out\n')
            with rio.open(pths.s2aOut + "/" + scene + '.tif', 'w',driver='GTiff',crs=dataset3.crs,transform=dataset3.transform,height=ndwi_int.shape[0], width=ndwi_int.shape[1],count=1,dtype=np.int16) as dst:
                dst.write(ndwi_int, 1)

        else:
            print('################\n### skipping calculation of cloudmask because there must be either too many clouds of an error occurred\n##########################\n')
            print("\nWarning: writing out watermask without cloudmask!\n")
            with rio.open(pths.s2aOut + "/" + scene + '.tif', 'w',driver='GTiff',crs=dataset3.crs,transform=dataset3.transform,height=ndwi_int.shape[0], width=ndwi_int.shape[1],count=1,dtype=np.int16) as dst:
                        dst.write(ndwi_int, 1)
    else:
        print("Warning: writing out watermask without cloudmask!\n")
        with rio.open(pths.s2aOut + "/" + scene + '.tif', 'w',driver='GTiff',crs=dataset3.crs,transform=dataset3.transform,height=ndwi_int.shape[0], width=ndwi_int.shape[1],count=1,dtype=np.int16) as dst:
            dst.write(ndwi_int, 1)


def test_one_ndwi():
    print("Executing ndwi2watermask():")
    #items=os.listdir(pths.s2aIn)
    items=['S2A_MSIL1C_20180223T130241_N0206_R095_T24MTT_20180223T192653.zip']
    for item in items:
        item=pths.s2aIn + '/' + item
        if re.search('^.*\.zip$', item):
            sceneJp2 = unzipJp2(item)
            ndwi_from_jp2(sceneJp2)
