# assign inputs
_analysisGrid, hoys_, blindStates_, _mode_ = IN
values = None

if _analysisGrid:
    _modes = ('total', 'direct', 'diffuse')
    _mode_ = _mode_ or 0
    hoys_ = hoys_ or _analysisGrid.hoys

    assert _mode_ < 3, '_mode_ can only be 0: total, 1: direct or 2: sky.'
    try:
        states = eval(blindStates_)
    except:
        states = None
    
    print('Loading sum of {} values.'.format(_modes[_mode_]))
    
    if _mode_ < 2:
        values = (v[_mode_] for v in
                  _analysisGrid.sumValuesById(hoys_, blindsStateIds=states))
    else:
        cValues = _analysisGrid.sumValuesById(hoys_, blindsStateIds=states)
        values = (v[0] - v[1] for v in cValues)

# assign outputs to OUT
OUT = (values,)