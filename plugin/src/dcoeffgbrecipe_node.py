# assign inputs
_skymtx, _analysisGrids, _analysisType_, _dmtxPar_, reuseDmtx_ = IN
analysisRecipe = None

#import honeybee
#reload(honeybee.radiance.recipe.daylightcoeff.gridbased)

try:
    from honeybee.radiance.recipe.daylightcoeff.gridbased import DaylightCoeffGridBased
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if _skymtx and _analysisGrids and _analysisGrids[0] != None:
    reuseDmtx_ = bool(reuseDmtx_)
    analysisRecipe = DaylightCoeffGridBased(
        _skymtx, _analysisGrids, _analysisType_, _dmtxPar_, reuseDmtx_)

# assign outputs to OUT
OUT = (analysisRecipe,)