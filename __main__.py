import sys

def main():
    """The main routine."""

    if sys.argv[1] is None:
        print("an argument is needed, for example: cleanup or get_scenes")
    elif sys.argv[1]=="getscenes":
        import modules.scenes as scenes
        try:
            scenes.getscenes()
            return 0
        except:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return 1
    elif sys.argv[1]=="rmclouds":
        import modules.cloudmask as clouds
        try:
            clouds.rmclouds()
            return 0
        except:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return 1
    elif sys.argv[1]=="ndwi":
        import modules.ndwi as n2w
        try:
            n2w.ndwi2watermask()
            return 0
        except:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return 1
    elif sys.argv[1]=="test":
        #### tests environment
        import modules.ndwi as n2w
        try:
            n2w.ndwi2watermask()
            return 0
        except:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return 1
    else:
        print('please provide one of "rmclouds", "getscenes" or "ndwi"')


if __name__ == "__main__":
    print main()
