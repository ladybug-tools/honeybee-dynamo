# assign inputs
_analysisGrid, blindStates_, _occSchedule_, _threshold_, _targetArea_ = IN
sDA = prblmHrs = None


if _analysisGrid:
    sDA, prblmHrs = _analysisGrid.spatialDaylightAutonomy(
         _threshold_, blindStates_, _occSchedule_, _targetArea_
    )

# assign outputs to OUT
OUT = sDA, prblmHrs