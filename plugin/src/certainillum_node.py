# assign inputs
_value_ = IN[0]
sky = None

try:
    from honeybee.radiance.sky.certainIlluminance import CertainIlluminanceLevel
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

_value_ = _value_ or 10000
sky = CertainIlluminanceLevel(_value_)


# assign outputs to OUT
OUT = (sky,)