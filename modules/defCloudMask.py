import zipfile
import subprocess
import os
import getPaths as pths
import re
from rasterio.warp import reproject,Resampling
from affine import Affine
import rasterio as rio

def unzipJp2(zipfl):
    sceneZip = zipfile.ZipFile(zipfl)
    scenefls = sceneZip.namelist()
    sceneJp2=[]
    for line in scenefls:
        if re.search('.*IMG_DATA.*_B[0-9,A]{2}.*.jp2', line) :
            sceneJp2.append(line)
        if not os.path.isfile(pths.s2aIn + '/' + line):
            sceneZip.extract(line,pths.s2aIn)
    sceneZip.close()
    return(sceneJp2)

def getParentDir(path):
    parentdir=path.split('/')
    parentdir= parentdir[:-1]
    parentdir='/'.join(parentdir)
    return(parentdir)

def getBandPath(sceneJp2):
    bandpth=[]
    for jp2 in sceneJp2:
        bandpth.append(pths.s2aIn+ '/' + jp2)
    return(bandpth)

def getBandDir(sceneJp2):
    bandpth=getBandPath(sceneJp2)
    banddir=getParentDir(bandpth[0])
    return(banddir)

def getAngleDir(sceneJp2):
    banddir=getBandDir(sceneJp2)
    xmldir=getParentDir(banddir)
    return(xmldir)

def runGdalbuildvrt(sceneJp2):
    bandpth=getBandPath(sceneJp2)
    banddir=getBandDir(sceneJp2)

    cmd=[pths.gdalBuildvrt,
        "-resolution",
        "user",
        "-tr",
        "20",
        "20",
        "-separate",
        banddir + "/" + "allbands.vrt"] + bandpth
    cmd=" ".join(cmd)
    exitFlag=subprocess.call(cmd,shell=True)
    return(exitFlag)

def runFmaskMakeAngles(sceneJp2):
    angledir=getAngleDir(sceneJp2)
    banddir=getBandDir(sceneJp2)
    cmd=[pths.fmaskMakeAngles,
        "-i",
        angledir + '/*.xml',
        "-o",
        banddir + '/angles.img']
    cmd=" ".join(cmd)
    exitFlag=subprocess.call(cmd,shell=True)
    return(exitFlag)

#fmask_sentinel2makeAnglesImage.py -i ../*.xml -o angles.img
#fmaskMakeAngles

def runFmaskStack(sceneJp2):
    banddir=getBandDir(sceneJp2)
    cmd = [pths.fmaskStack,
        "-a",
        banddir + "/allbands.vrt",
        "-z",
        banddir + "/angles.img",
        "-o",
        banddir + "/cloud.img"]
    cmd=" ".join(cmd)
    exitFlag=subprocess.call(cmd,shell=True)
    return(exitFlag)

#    fmask_sentinel2Stacked.py -a allbands.vrt -z angles.img -o cloud.img

def interpolate_clouds_to_10m(file_clouds):
    dataset_clouds = rio.open(file_clouds)
    clouds = dataset_clouds.read(1)
    clouds10 = np.empty(shape=(int(round(clouds.shape[0] * 2)),
        int(round(clouds.shape[1] * 2))))

    aff = dataset_clouds.transform
    newaff = Affine(aff[0] / 2, aff[1], aff[2],aff[3], aff[4] / 2, aff[5])
    reproject(clouds, clouds10,
        src_transform = aff,
        dst_transform = newaff,
        src_crs = dataset_clouds.crs,
        dst_crs = dataset_clouds.crs,
        resampling = Resampling.nearest)

    return(clouds10)
