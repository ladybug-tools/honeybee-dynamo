# assign inputs
_analysisGrid, _index_ = IN
position = sensor = None

try:
    import ladybug.geometry as lg
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _analysisGrid:
    if _analysisGrid.digit_sign == 1:
        _analysisGrid.load_values_from_files()

    id = _index_ or 0
    sensor = _analysisGrid[id]
    pt = (sensor.location.x, sensor.location.y, sensor.location.z)
    position = lg.sphere(pt, 0.5)

# assign outputs to OUT
OUT = position, sensor