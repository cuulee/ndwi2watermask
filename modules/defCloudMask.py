import zipfile
import subprocess
import os
import getPaths as pths
import re

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

    cmd=[gdalBuildvrt,
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
    cmd=[fmaskMakeAngles,
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
    cmd = [fmaskStack,
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
