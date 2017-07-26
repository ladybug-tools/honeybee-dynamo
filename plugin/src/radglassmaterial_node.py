# assign inputs
_name, _tVis_ = IN
material = None

try:
    from honeybee.radiance.material.glass import GlassMaterial
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _name:
    _tVis_ = _tVis_ or 0.6
    material = GlassMaterial.bySingleTransValue(_name, _tVis_)


# assign outputs to OUT
OUT = (material,)