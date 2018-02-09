# assign inputs
_geo, names_, _type_, radMat_ = IN
HBSrf = None

try:
    from honeybee.hbsurface import HBSurface
    from honeybee.radiance.properties import RadianceProperties
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if len(_geo)!=0 and _geo[0]!=None:
    isNameSetByUser = False
    if names_:
        isNameSetByUser = True
        
    isTypeSetByUser = True
    if not _type_:
        isTypeSetByUser = False
    
    radProp_ = RadianceProperties(radMat_, True) if radMat_ else RadianceProperties()
    
    epProp_ = None
    
    HBSrf = HBSurface.from_geometry(names_, _geo, _type_, isNameSetByUser,
                                    isTypeSetByUser, radProp_, epProp_)


# assign outputs to OUT
OUT = (HBSrf,)