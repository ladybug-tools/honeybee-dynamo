# assign inputs
_name, radMat_, HBSrfs_ = IN
state = None

try:
    from honeybee.surfaceproperties import SurfaceProperties, SurfaceState
    from honeybee.surfacetype import Window
    from honeybee.radiance.properties import RadianceProperties
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _name and (radMat_ or HBSrfs_):
    if radMat_:
        radPar = RadianceProperties(radMat_, True)
    else:
        radPar = RadianceProperties()

    state = SurfaceState(_name, SurfaceProperties(Window, radPar), HBSrfs_) 

# assign outputs to OUT
OUT = (state,)