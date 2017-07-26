# assign inputs
_name, _rRef_, _gRef_, _bRef_, _spec_, _rough_ = IN
material = None

try:
    from honeybee.radiance.material.plastic import PlasticMaterial
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _name:
    _rRef_ = _rRef_ or 0.35
    _gRef_ = _gRef_ or 0.35
    _bRef_ = _bRef_ or 0.35
    material = PlasticMaterial(_name, _rRef_, _gRef_, _bRef_, _spec_, _rough_)

# assign outputs to OUT
OUT = (material,)