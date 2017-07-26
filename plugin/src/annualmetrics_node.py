# assign inputs
_analysisGrid, blindStates_, _occSchedule_, _threshold_, _minmax_ = IN
DA = CDA = UDI = UDILess = UDIMore = None

if _analysisGrid:
    states = tuple(eval(t) for t in blinds_state_)
    DA, CDA, UDI, UDILess, UDIMore = _analysisGrid.annualMetrics(
        _threshold_, _minmax_, blindStates_, _occSchedule_
    )

# assign outputs to OUT
OUT = DA, CDA, UDI, UDILess, UDIMore