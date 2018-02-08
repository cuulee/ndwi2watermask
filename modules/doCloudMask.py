
import os
import subprocess
from getPaths import *

import zipfile

import re



zipfls=[]
items=os.listdir(s2aIn)
for item in items:
    if re.search('^.*\.zip$', item) :
        zipfls.append(item)

zipfl=zipfls[0]
sceneZip = zipfile.ZipFile(s2aIn + '/' + zipfl)
scenefls = sceneZip.namelist()
sceneJp2=[]
for line in scenefls:
    if re.search('.*IMG_DATA.*_B[0-9,A]{2}.*.jp2', line) :
        sceneJp2.append(line)
        sceneZip.extract(line,s2aIn)
sceneZip.close()
os.rename(s2aIn + '/' + zipfl,s2aIn + '/' + zipfl+".finished")

jp2fls=[]

items=os.listdir(s2aIn)

for item in items:
    if re.search('^.*\.jp2$', item) :
        jp2fls.append(item)


print("\n creating cloud masks \n")

subprocess.call([pyGdal,
    gdalbuildvrt,
    "-resolution",
    "user",
    "-tr",
    "20",
    "20",
    "GML",
    polOut + "/" + out_file])

gdalbuildvrt -resolution user -tr 20 20 -separate allbands.vrt *_B0[1-8].jp2 *_B8A.jp2 *_B09.jp2 *_B1[0-2].jp2
fmask_sentinel2makeAnglesImage.py -i ../*.xml -o angles.img
fmask_sentinel2Stacked.py -a allbands.vrt -z angles.img -o cloud.img


subprocess.call([pyFmask,gdalPol,sarOut + "/" + in_file,"-f","GML",polOut + "/" + out_file])
subprocess.call([pyFmask,gdalPol,sarOut + "/" + in_file,"-f","GML",polOut + "/" + out_file])

gdalBuildvrt
fmaskMakeAngles
fmaskStack
