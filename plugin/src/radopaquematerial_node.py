# assign inputs
_name, _reflect_, _spec_, _rough_ = IN
material = None

try:
    from honeybee.radiance.material.plastic import PlasticMaterial
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _name:
    _reflect_ = _reflect_ or 0.35
    material = PlasticMaterial.by_single_reflect_value(
        _name, _reflect_, _spec_, _rough_)

# assign outputs to OUT
OUT = (material,)