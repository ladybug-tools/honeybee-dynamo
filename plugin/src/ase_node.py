# assign inputs
_analysisGrid, blindStates_, _occSchedule_, _threshold_, _targetHrs_, _targetArea_ = IN
success = perArea = prblmPts = prblmHrs = None


if _analysisGrid:
    success, perArea, prblmPts, prblmHrs = _analysisGrid.annualSolarExposure(
         _threshold_, blindStates_, _occSchedule_, _targetHrs_, _targetArea_
    )

# assign outputs to OUT
OUT = success, perArea, prblmPts, prblmHrs