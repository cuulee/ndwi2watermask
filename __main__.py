import sys

def main():
    """The main routine."""

    if sys.argv[1] is None:
        print("an argument is needed, for example: cleanup or get_scenes")
    elif sys.argv[1]=="getscenes":
        import modules.scenes as scenes
        scenes.getscenes()
    elif sys.argv[1]=="rmclouds":
        import modules.cloudmask as clouds
        clouds.rmclouds()
    elif sys.argv[1]=="ndwi":
        import modules.ndwi as n2w
        n2w.ndwi2watermask()
    elif sys.argv[1]=="test":
        #### tests environment
        import modules.ndwi as n2w
        n2w.test_one_ndwi()
    else:
        print('please provide one of "rmclouds", "getscenes" or "ndwi"')


#if __name__ == "__main__":
#    print main()
