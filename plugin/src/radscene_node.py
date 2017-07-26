# assign inputs
_radFiles, _copyLocal_, _overwrite_ = IN
radScene = None

try:
    from honeybee.radiance.scene import Scene
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _radFiles and _radFiles[0] is not None:
    radScene = Scene(_radFiles, _copyLocal_, _overwrite_)

# assign outputs to OUT
OUT = (radScene,)