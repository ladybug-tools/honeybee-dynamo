# assign inputs
north_, _wea, _month_, _day_, _hour_ = IN
sky = None

try:
    from honeybee.radiance.sky.climatebased import ClimateBased
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _wea:
    # set default values if they are not set
    north_ = north_ or 0
    _month_ = _month_ or 6
    _day_ = _day_ or 21
    _hour_ = _hour_ or 12
    sky = ClimateBased.from_wea(_wea, _month_, _day_, _hour_, north_)

# assign outputs to OUT
OUT = (sky,)