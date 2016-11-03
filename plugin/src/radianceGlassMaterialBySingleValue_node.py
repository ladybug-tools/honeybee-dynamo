try:
    # add IronPython path to sys
    import sys
    IronPythonLib = 'C:\Program Files (x86)\IronPython 2.7\Lib'
    sys.path.append(IronPythonLib)

    # Now that the path to IronPython is established we can import libraries
    import os
    import clr
    clr.AddReference('DynamoCore')

    def getPackagePath(packageName):
        """Get path to dynamo package using the package name."""
        _loc = clr.References[2].Location
        _ver = _loc.split('\\')[-2].split(' ')[-1]

        # the path structure has changed after the release of version 1
        dynamoPath_1 = "Dynamo\\Dynamo Revit\\" + _ver
        dynamoPath_0 = "Dynamo\\" + _ver
        appdata = os.getenv('APPDATA')
        path1 = '%s\%s\packages\%s\extra\\' % (appdata, dynamoPath_1, packageName)
        path0 = '%s\%s\packages\%s\extra\\' % (appdata, dynamoPath_0, packageName)

        if os.path.isdir(path1):
            return path1
        elif os.path.isdir(path0):
            return path0
        else:
            raise Exception("Can't find Dynamo installation Folder!")

    # append ladybug path to sys.path
    sys.path.append(getPackagePath('Honeybee'))

    ###### start you code from here ###
    from honeybeex.radiance.material.glass import GlassMaterial

    _name, _TVis = IN[0], IN[1]
    if _name and _TVis is not None:
        OUT = GlassMaterial.bySingleTransValue(_name, _TVis)

except Exception, e:
    import traceback
    OUT = "ERROR:\n%s" % str(e) + \
        "\n\nIf you think this is a bug submit an issue on github.\n" + \
        "https://github.com/ladybug-analysis-tools/honeybeex/issues" + \
        "\n\n%s" % traceback.format_exc()
