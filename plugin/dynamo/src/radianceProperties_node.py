###### start you code from here ###
from honeybeex.radiance.properties import RadianceProperties

_material_ = IN[0]
OUT = RadianceProperties(_material_, True) if _material_ else RadianceProperties()