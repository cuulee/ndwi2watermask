
import os
import subprocess
from getPaths import *

import zipfile

import re

#### list zip files

zipfls=[]
items=os.listdir(s2aIn)
for item in items:
    if re.search('^.*\.zip$', item) :
        zipfls.append(item)


def unzipJp2(zipfl):
    sceneZip = zipfile.ZipFile(s2aIn + '/' + zipfl)
    scenefls = sceneZip.namelist()
    sceneJp2=[]
    for line in scenefls:
        if re.search('.*IMG_DATA.*_B[0-9,A]{2}.*.jp2', line) :
            if not os.path.isfile(s2aIn + '/' + line):
                sceneZip.extract(line,s2aIn)
            sceneJp2.append(line)
    sceneZip.close()
    return(sceneJp2)

sceneJp2 = unzipJp2(zipfls[0])

def doGdalbuildvrt(sceneJp2):
    bandpth=[]
    for jp2 in sceneJp2:
        bandpth.append(s2aIn+ '/' + jp2)


cmd=[    gdalBuildvrt,
    "-resolution",
    "user",
    "-tr",
    "200",
    "200",
    "-separate",
    "allbands.vrt",
    " ".join(bandpth)]

subprocess.call(

" ".join(cmd)

gdalBuildvrt

sceneJp2 = unzipJp2(zipfls[0])
print("\n building vrt \n")

doGdalbuildvrt(sceneJp2)


gdalbuildvrt -resolution user -tr 20 20 -separate allbands.vrt *_B0[1-8].jp2 *_B8A.jp2 *_B09.jp2 *_B1[0-2].jp2
fmask_sentinel2makeAnglesImage.py -i ../*.xml -o angles.img
fmask_sentinel2Stacked.py -a allbands.vrt -z angles.img -o cloud.img


subprocess.call([pyFmask,gdalPol,sarOut + "/" + in_file,"-f","GML",polOut + "/" + out_file])
subprocess.call([pyFmask,gdalPol,sarOut + "/" + in_file,"-f","GML",polOut + "/" + out_file])

gdalBuildvrt
fmaskMakeAngles
fmaskStack
