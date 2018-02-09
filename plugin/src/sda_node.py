# assign inputs
_analysisGrid, blindStates_, _occSchedule_, _threshold_, _targetDA_ = IN
sDA = DA = prblmPts = None

try:
    import ladybug.geometry as lg
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

if _analysisGrid:
    states = _analysisGrid.parse_blind_states(blindStates_)
    sDA, DA, prblmPts = _analysisGrid.spatial_daylight_autonomy(
         _threshold_, _targetDA_, states, _occSchedule_
    )
    prblmPts = (lg.point(s.location.x, s.location.y, s.location.z) for s in prblmPts)

# assign outputs to OUT
OUT = sDA, DA, prblmPts