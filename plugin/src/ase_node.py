# assign inputs
_analysisGrid, blindStates_, _occSchedule_, _threshold_, _targetHrs_, _targetArea_ = IN
success = ASE = perArea = prblmPts = prblmHrs = legendPar = None

try:
    import ladybug.geometry as lg
    import ladybug.output as output
    import ladybug.legendparameters as lp
    import ladybug.color as color
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))


col = color.Colorset.original()
legendPar = lp.LegendParameters((0, 250), colors=col)

if _analysisGrid:
    states = _analysisGrid.parse_blind_states(blindStates_)
    success, ASE, perArea, prblmPts, prblmHrs = _analysisGrid.annual_solar_exposure(
         _threshold_, states, _occSchedule_, _targetHrs_, _targetArea_
    )

    prblmPts = (lg.point(s.location.x, s.location.y, s.location.z) for s in prblmPts)
    # convert list of lists to data tree
    try:
        prblmHrs = output.list_to_tree(prblmHrs, ghenv.Component.RunCount - 1)
    except NameError:
        # dynamo
        pass

# assign outputs to OUT
OUT = success, ASE, perArea, prblmPts, prblmHrs, legendPar