import zipfile
import subprocess
import os
from getPaths import *
import re

def unzipJp2(zipfl):
    sceneZip = zipfile.ZipFile(zipfl)
    scenefls = sceneZip.namelist()
    sceneJp2=[]
    for line in scenefls:
        if re.search('.*IMG_DATA.*_B[0-9,A]{2}.*.jp2', line) :
            if not os.path.isfile(s2aIn + '/' + line):
                sceneZip.extract(line,s2aIn)
            sceneJp2.append(line)
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
        bandpth.append(s2aIn+ '/' + jp2)
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

    cmd=[gdalBuildvrt,
        "-resolution",
        "user",
        "-tr",
        "20",
        "20",
        "-separate",
        banddir + "/" + "allbands.vrt"] + bandpth

    exitFlag=subprocess.call(cmd)
    return(exitFlag)

def runFmaskMakeAngles(sceneJp2):
    angledir=getAngleDir(sceneJp2)
    banddir=getBandDir(sceneJp2)
    cmd=[fmaskMakeAngles,
        "-i",
        angledir + '/*.xml',
        "-0",
        bandir + '/angles.img']

    exitFlag=subprocess.call(cmd)
    return(exitFlag)

#fmask_sentinel2makeAnglesImage.py -i ../*.xml -o angles.img
#fmaskMakeAngles
