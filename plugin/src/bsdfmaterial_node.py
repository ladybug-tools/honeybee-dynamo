# assign inputs
_xmlfile, _upVector_, thickness_ = IN
material = None

try:
    from honeybee.radiance.material.bsdf import BSDFMaterial
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _xmlfile:
    material = BSDFMaterial(_xmlfile, _upVector_, thickness_)


# assign outputs to OUT
OUT = (material,)