# assign inputs
_imgCollection, hoys_, blindStates_, _mode_ = IN
Output = images = None

if _imgCollection:
    _modes = ('combined', 'total', 'direct', 'diffuse')
    _mode_ = _mode_ or 0
    hoys_ = hoys_ or _imgCollection.hoys

    assert _mode_ < 4, \
        '_mode_ can only be 0: combined, 1: total, 2: direct or 3: sky.'

    states = _imgCollection.parse_blind_states(blindStates_)
    
    print(_imgCollection.details)
    print('Loading {} values for several hours.'.format(_modes[_mode_]))
    
    images = _imgCollection.generate_combined_images_by_id(hoys_, states, _mode_) 

# assign outputs to OUT
OUT = Output, images