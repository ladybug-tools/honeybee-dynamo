# assign inputs
north_, _location, _month_, _day_, _hour_, _type_ = IN
sky = None

try:
    from honeybee.radiance.sky.cie import CIE
    from ladybug.location import Location
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _location:
    if not hasattr(_location, 'isLocation'):
        _location = Location.from_location(_location)
    # set default values if they are not set
    north_ = north_ or 0
    _type_ = _type_ or 0
    _month_ = _month_ or 6
    _day_ = _day_ or 21
    _hour_ = _hour_ or 12
    sky = CIE(_location, _month_, _day_, _hour_, _type_, north_)


# assign outputs to OUT
OUT = (sky,)