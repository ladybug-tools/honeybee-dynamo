# assign inputs
_geo, _name, radMat_, states_ = IN
HBWinGroup = None


try:
    from honeybee.hbdynamicsurface import HBDynamicSurface
    from honeybee.radiance.properties import RadianceProperties
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _name and len(_geo)!=0 and _geo[0]!=None:

    isNameSetByUser = True

    if radMat_:
        assert radMat_.isGlassMaterial, \
            TypeError('Radiance material must be a Window material not {}.'.format(type(m)))
        radProp_ = RadianceProperties(radMat_, True)
    else:
        radProp_ = RadianceProperties()

    epProp_ = None
    _type_ = 5  # in the interface we use dynamic surfaces only for fenestration
    isTypeSetByUser = True

    HBWinGroup = HBDynamicSurface.from_geometry(
        _name, _geo, _type_, isNameSetByUser, isTypeSetByUser, radProp_,
        epProp_, states_, group=True)


# assign outputs to OUT
OUT = (HBWinGroup,)