# assign inputs
_name_, _testPoints, ptsVectors_, wGroups_ = IN
analysisGrid = None

try:
    from honeybee.radiance.analysisgrid import AnalysisGrid
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if _testPoints:
    analysisGrid = AnalysisGrid.from_points_and_vectors(_testPoints, ptsVectors_,
        _name_, wGroups_)

# assign outputs to OUT
OUT = (analysisGrid,)