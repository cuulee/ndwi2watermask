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

def getDirFromAbsPath(path):
    banddir=path[0].split('/')
    banddir= banddir[:-1]
    banddir='/'.join(banddir)
    return(banddir)


def doGdalbuildvrt(sceneJp2):
    bandpth=[]
    for jp2 in sceneJp2:
        bandpth.append(s2aIn+ '/' + jp2)

    banddir=getDirFromAbsPath(bandpth[0])

    cmd=[gdalBuildvrt,
        "-resolution",
        "user",
        "-tr",
        "200",
        "200",
        "-separate",
        banddir + "/" + "allbands.vrt"] + bandpth

    exitFlag=subprocess.call(cmd)
    return(exitFlag)


fmask_sentinel2makeAnglesImage.py -i ../*.xml -o angles.img
fmaskMakeAngles
