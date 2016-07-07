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
    from honeybeex.geometryoperation import GridGenerator

    _surfaces = IN[0]
    _gridSize = IN[1]
    _distanceFromBaseSrf = IN[2]
    _borders = IN[3]

    if _surfaces and _gridSize and _distanceFromBaseSrf:

        if not hasattr(_surfaces, '__iter__'):
            _surfaces = (_surfaces,)

        _borders = _borders if _borders else (getSurfaceBorder(surface)
                                              for surface in _surfaces)

        if not hasattr(_borders, '__iter__'):
            _borders = (_borders,)

        _gg = GridGenerator(_surfaces, _gridSize, _distanceFromBaseSrf, _borders)
        gridGroups = tuple(_gg.grids)

        _testPoints = tuple([] for g in gridGroups)
        _ptsNormal = tuple([] for g in gridGroups)
        _UVs = tuple([] for g in gridGroups)
        _polygons = tuple([] for g in gridGroups)

        for count, grids in enumerate(gridGroups):
             for g in grids:
                 _testPoints[count].append(g.point)
                 _ptsNormal[count].append(g.normal)
                 _UVs[count].append(g.uv)
                 _polygons[count].append(g.polygon)

        OUT = _testPoints, _ptsNormal, _UVs, _polygons

except Exception, e:
    import traceback
    OUT = "ERROR:\n%s" % str(e) + \
        "\n\nIf you think this is a bug submit an issue on github.\n" + \
        "https://github.com/ladybug-analysis-tools/honeybeex/issues" + \
        "\n\n%s" % traceback.format_exc()
