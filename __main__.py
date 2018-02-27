import sys

def main():
    """The main routine."""

    switcher = {
        "rmclouds" : callrmclouds,
        "getscenes" : callgetscenes,
        "ndwi" : callndwi
        }

    if sys.argv[1] is None:
        print("an argument is needed, for example: cleanup or get_scenes")
    else:
        switcher.get(sys.argv[1],'please provide one of rmclouds, getscenes or ndwi')()

def callgetscenes():
    import modules.scenes as scenes
    try:
        scenes.getscenes()
        return 0
    except:
        return 1

def callrmclouds():
    import modules.cloudmask as clouds
    try:
        clouds.rmclouds()
        return 0
    except:
        return 1

def callndwi():
    import modules.ndwi as n2w
    try:
        n2w.ndwi2watermask()
        return 0
    except:
        return 1



if __name__ == "__main__":
    print main()
