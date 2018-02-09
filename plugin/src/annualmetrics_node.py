# assign inputs
_analysisGrid, blindStates_, _occSchedule_, _threshold_, _minmax_ = IN
DA = CDA = UDI = UDILess = UDIMore = legendPar = None

try:
    import ladybug.legendparameters as lp
    import ladybug.color as color
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

col = color.Colorset.nuanced()
legendPar = lp.LegendParameters((0, 100), colors=col)

if _analysisGrid:
    states = _analysisGrid.parse_blind_states(blindStates_)
    DA, CDA, UDI, UDILess, UDIMore = _analysisGrid.annual_metrics(
        _threshold_, _minmax_, states, _occSchedule_
    )

# assign outputs to OUT
OUT = DA, CDA, UDI, UDILess, UDIMore, legendPar