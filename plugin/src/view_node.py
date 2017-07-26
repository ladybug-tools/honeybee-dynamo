# assign inputs
_name, _vLocation, _vDirection, _vUpVector_, _viewType_, _hViewAngle_, _vViewAngle_, _xResolution_, _yResolution_ = IN
view = None

#import honeybee
#reload(honeybee.radiance.view)

try:
    from honeybee.radiance.view import View
except ImportError as e:
    msg = '\nFailed to import honeybee. Did you install honeybee on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/ladybug-analysis-tools/honeybee-plus/tree/master/plugin/dynamo/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/ladybug-analysis-tools/honeybee-plus/issues'
        
    raise ImportError('{}\n\t{}'.format(msg, e))


if _vLocation and _vDirection:
    _location = (_vLocation.X, _vLocation.Y, _vLocation.Z)
    _direction = (_vDirection.X, _vDirection.Y, _vDirection.Z)
    _upVector = (_vUpVector_.X, _vUpVector_.Y, _vUpVector_.Z)
    view = View(_name, _location, _direction, _upVector, _viewType_,
                _hViewAngle_, _vViewAngle_, _xResolution_, _yResolution_)

# assign outputs to OUT
OUT = (view,)