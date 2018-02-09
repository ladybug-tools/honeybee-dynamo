# assign inputs
_sensor, hoys_, blindStates_, _mode_ = IN
values = None

if _sensor:
    _modes = ('total', 'direct', 'diffuse')
    _mode_ = _mode_ or 0
    hoys_ = hoys_ or _sensor.hoys

    assert _mode_ < 3, '_mode_ can only be 0: total, 1: direct or 2: sky.'

    states = _sensor.parse_blind_states(blindStates_)

    print('Loading {} values for several hours.'.format(_modes[_mode_]))
    
    if _mode_ < 2:
        values = (v[_mode_] for v in
                  _sensor.combined_values_by_id(hoys_, blinds_state_ids=states))
    else:
        cValues = _sensor.combined_values_by_id(hoys_, blinds_state_ids=states)
        values = (v[0] - v[1] for v in cValues)

# assign outputs to OUT
OUT = (values,)