import sys
#import bin.ndwi2watermask as n2w
import bin.getscenes as scenes

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



    try:
        #n2w.rmclouds()
        #n2w.ndwi2watermask()
        scenes.getscenes()
        return 0
    except:
        return 1



if __name__ == "__main__":
    print main()
