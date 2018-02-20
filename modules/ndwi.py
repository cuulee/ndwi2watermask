from modules.cloudmask import getBandDir,interpolate_clouds_to_10m
import glob
import rasterio as rio

def ndwi_from_jp2(sceneJp2):
    banddir = getBandDir(sceneJp2)
    file_clouds = banddir + '/cloud.img'

    p3 = glob.glob(banddir + '/*B03.jp2')
    p8 = glob.glob(banddir + '/*B08.jp2')

    #### add clause "in case there is a cloud file"
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
    ndwi = NDWI[not clouds_bin] > 0.5

    with rio.open(banddir + 'ndwi.img', 'w', **profile) as dst:
        dst.write(ndwi.astype(rio.uint8), 1)
    #dst.write(ndwi.astype(rio.float64), 1)
