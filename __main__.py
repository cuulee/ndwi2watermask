import sys
import bin.getscenes as scenes

choices = {'a': 1, 'b': 2}
choices.get('r','default')

def main():
    """The main routine."""

    switcher = {
    "rmclouds" : callrmclouds,
    "getscenes" : callgetscenes,
    "ndwi" : callndwi
    }

    if args is None:
        print("an argument is needed, for example: cleanup or get_scenes")
    else:
        args = sys.argv[1]



def callgetscenes():
    import modules.cloudmask as clouds
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
