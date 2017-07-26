# assign inputs
_name, _rVis_, _gVis_, _bVis_ = IN
material = None

try:
    from honeybee.radiance.material.glass import GlassMaterial
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _name:
    _rVis_ = _rVis_ or 0.6
    _gVis_ = _gVis_ or 0.6
    _bVis_ = _bVis_ or 0.6
    material = GlassMaterial(_name, _rVis_, _gVis_, _bVis_)


# assign outputs to OUT
OUT = (material,)