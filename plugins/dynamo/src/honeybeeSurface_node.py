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
    from honeybeex.hbsurface import HBSurface
    from uuid import uuid4

    # create list from inputs if it's not a list
    _geo = IN[0]

    if _geo:

        # this is not good practice. I need to find a better generic solution for
        # dynamo inputs
        for count, inp in enumerate(IN):
            if not inp:
                IN[count] = (None,)
            elif isinstance(inp, str):
                IN[count] = (inp,)
            elif not hasattr(inp, '__iter__'):
                IN[count] = (inp,)

        _geos, names_, _types_, radProps_, epProps_ = UnwrapElement(IN[:])
        if not names_[0]:
            names_ = ("srf_%s" % uuid4(),)

        HBSrfs = range(len(_geos))

        for count, _geo in enumerate(_geos):
            try:
                name_ = names_[count]
            except IndexError:
                name_ = names_[0] + "_{}".format(count)

            isNameSetByUser = True
            if not name_:
                name_ = "Surface_%s" % uuid4()
                isNameSetByUser = False

            try:
                _type_ = _types_[count]
            except ValueError:
                _type_ = _types_[0]

            isTypeSetByUser = True
            if not _type_:
                isTypeSetByUser = False

            try:
                radProp_ = radProps_[count]
            except ValueError:
                radProp_ = radProps_[0]

            try:
                epProp_ = epProps_[count]
            except ValueError:
                epProp_ = epProps_[0]

            HBSrf = HBSurface.fromGeometry(name_, _geo, _type_, isNameSetByUser,
                                           isTypeSetByUser, radProp_, epProp_)

            HBSrfs[count] = HBSrf


        OUT = HBSrfs

except Exception, e:
    import traceback
    OUT = "ERROR:\n%s" % str(e) + \
        "\n\nIf you think this is a bug submit an issue on github.\n" + \
        "https://github.com/ladybug-analysis-tools/honeybeex/issues" + \
        "\n\n%s" % traceback.format_exc()
