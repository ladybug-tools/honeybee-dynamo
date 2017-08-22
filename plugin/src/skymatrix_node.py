# assign inputs
name_, north_, _wea, _density_, hoys_ = IN
skymtx = None

try:
    from honeybee.radiance.sky.skymatrix import SkyMatrix
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if _wea:
    skymtx = SkyMatrix(_wea, _density_, north_, hoys_, suffix=name_)

# assign outputs to OUT
OUT = (skymtx,)