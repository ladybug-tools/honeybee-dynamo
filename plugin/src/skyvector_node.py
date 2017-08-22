# assign inputs
north_, _wea, _density_, _month_, _day_, _hour_ = IN
skyVec = None

try:
    from honeybee.radiance.sky.skymatrix import SkyMatrix
    from ladybug.dt import DateTime
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))
        
    raise ImportError('{}\n\t{}'.format(msg, e))

if _wea:
    north_ = north_ or 0
    _month_ = _month_ or 6
    _day_ = _day_ or 21
    _hour_ = _hour_ or 12
    dt = DateTime(_month_, _day_, _hour_)
    _density_ = _density_ or 1
    
    skyVec = SkyMatrix(_wea, _density_, north_, (int(dt.hoy),),
                       suffix=str(int(dt.hoy)))
    

# assign outputs to OUT
OUT = (skyVec,)