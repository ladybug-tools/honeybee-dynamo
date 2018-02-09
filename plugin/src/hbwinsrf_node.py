# assign inputs
_geo, names_, radMat_ = IN
HBWinSrf = None

try:
    from honeybee.hbfensurface import HBFenSurface
    from honeybee.radiance.properties import RadianceProperties
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if len(_geo)!=0 and _geo[0]!=None:
    isNameSetByUser = False
    if names_:
        isNameSetByUser = True

    if radMat_:
        assert radMat_.isGlassMaterial, \
            TypeError('Radiance material must be a Window material not {}.'.format(type(m)))
        radProp_ = RadianceProperties(radMat_, True)
    else:
        radProp_ = RadianceProperties()

    epProp_ = None
    HBWinSrf = HBFenSurface.from_geometry(names_, _geo, isNameSetByUser, radProp_, epProp_)

# assign outputs to OUT
OUT = (HBWinSrf,)