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
    elif sys.argv[1] is "getscenes":
        import modules.scenes as scenes
        try:
            scenes.getscenes()
            return 0
        except:
            return 1
    elif sys.argv[1] is "rmclouds":
        import modules.cloudmask as clouds
        try:
            clouds.rmclouds()
            return 0
        except:
            return 1
    elif sys.argv[1] is "ndwi":
        import modules.ndwi as n2w
        try:
            n2w.ndwi2watermask()
            return 0
        except:
            return 1
    else:
        print('please provide one of "rmclouds", "getscenes" or "ndwi"')


if __name__ == "__main__":
    print main()
