# assign inputs
_sensor, _blindCombs_, _logic_, data_ = IN
blindStates = blindStIndex = illumTotal = illumDirect = success = None

import copy

if _sensor:
    sensor = _sensor
    
    # print the details to help user set up the combination
    print(sensor.details)
    
    if _logic_:
    
        logic = compile('r = {}'.format(_logic_), '<string>', 'exec')
        data = data_
        def checkLogic(ill, ill_dir, hour, *data, **kwargs):
            exec(logic)
            return r
    
        setattr(sensor, 'logic', checkLogic)
    else:
        setattr(sensor, 'logic', sensor._logic)

    
    states = sensor.parse_blind_states(_blindCombs_)
    results = sensor.blinds_state(sensor.hoys, states)
    if results:
        blindStates = (str(d) for d in results[0])  # tuple is not a standard DS Type
        blindStIndex = results[1]
        illumTotal = results[2]
        illumDirect = results[3]
        success = results[4]

# assign outputs to OUT
OUT = blindStates, blindStIndex, illumTotal, illumDirect, success