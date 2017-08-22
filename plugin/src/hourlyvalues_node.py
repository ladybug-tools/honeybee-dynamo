# assign inputs
_analysisGrid, hoy_, blindState_, _mode_ = IN
values = None

from ladybug.dt import DateTime

try:
    from honeybee.radiance.recipe.solaraccess.gridbased import SolarAccessGridBased
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _analysisGrid:
    _modes = ('total', 'direct', 'diffuse')
    _mode_ = _mode_ or 0
    hoy_ = hoy_ or _analysisGrid.hoys[0]
    assert _mode_ < 3, '_mode_ can only be 0: total, 1: direct or 2: sky.'

    try:
        states = eval(blindState_)
    except Exception as e:
        if blindState_:
            raise TypeError('Failed to read blindState_:\n{}'.format(e))
        states = None
    
    print('Loading {} values for {}.'.format(_modes[_mode_], DateTime.fromHoy(hoy_)))
    
    if _mode_ < 2:
        values = (v[_mode_] for v in _analysisGrid.combinedValueById(hoy_, states))
    else:
        cValues = _analysisGrid.combinedValueById(hoy_, states)
        values = (v[0] - v[1] for v in cValues)

# assign outputs to OUT
OUT = (values,)