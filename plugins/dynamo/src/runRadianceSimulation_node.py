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
    from honeybeex.dataoperation import unflatten
    _recipe, _HBObjs, _folder_, _name_, _write, run_ = UnwrapElement(IN)

    if _HBObjs and _recipe and _write:
        if not hasattr(_HBObjs, '__iter__'):
            _HBObjs = [_HBObjs]

        for count, obj in enumerate(_HBObjs):
            assert hasattr(obj, 'isHBObject'), \
                "Item %d is not a valid Honeybee object." % count

        if _write:
            # Add Honeybee objects to the recipe
            _recipe.hbObjects = _HBObjs
            # try:
            _recipe.writeToFile(_folder_, _name_)
            # except Exception, e:
            #     raise ValueError("Failed to write the files:\n%s" % e)

        if _write and run_:
            if _recipe.run(False):
            	OUT = unflatten(_recipe.originalPoints, iter(_recipe.results()))

except Exception, e:
    import traceback
    OUT = "ERROR:\n%s" % str(e) + \
        "\n\nIf you think this is a bug submit an issue on github.\n" + \
        "https://github.com/ladybug-analysis-tools/honeybeex/issues" + \
        "\n\n%s" % traceback.format_exc()
