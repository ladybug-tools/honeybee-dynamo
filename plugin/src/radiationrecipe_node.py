# assign inputs
_skymtx, _analysisGrids, _dmtxPar_, reuseDmtx_ = IN
analysisRecipe = None


#import honeybee
#reload(honeybee.radiance.recipe.recipedcutil)
#reload(honeybee.radiance.recipe.daylightcoeff.gridbased)
#reload(honeybee.radiance.recipe.radiation.gridbased)
try:
    from honeybee.radiance.recipe.radiation.gridbased import GridBased
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if _skymtx and _analysisGrids and _analysisGrids[0] != None:
    reuseDmtx_ = bool(reuseDmtx_)
    analysisRecipe = GridBased(_skymtx, _analysisGrids, _dmtxPar_, reuseDmtx_)

# assign outputs to OUT
OUT = (analysisRecipe,)