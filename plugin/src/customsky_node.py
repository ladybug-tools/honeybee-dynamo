# assign inputs
north_, _location, _dirRad, _difRad, _month_, _day_, _hour_ = IN
sky = None

try:
    from honeybee.radiance.sky.climatebased import ClimateBased
    from ladybug.location import Location
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _location and _dirRad is not None and _difRad is not None:
    if not hasattr(_location, 'isLocation'):
        _location = Location.fromLocation(_location)
    
    # set default values if they are not set
    north_ = north_ or 0
    _month_ = _month_ or 6
    _day_ = _day_ or 21
    _hour_ = _hour_ or 12
    sky = ClimateBased(_location, _month_, _day_, _hour_, _dirRad, _difRad, north_)

# assign outputs to OUT
OUT = (sky,)