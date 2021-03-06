# assign inputs
_skymtx, _analysisGrids, _analysisType_, _vmtxPar_, _dmtxPar_, reuseVmtx_, reuseDmtx_ = IN
analysisRecipe = None

#import honeybee
#reload(honeybee.radiance.recipe.daylightcoeff.gridbased)
#reload(honeybee.radiance.recipe.threephase.gridbased)
#reload(honeybee.radiance.recipe.fivephase.gridbased)

try:
    from honeybee.radiance.recipe.fivephase.gridbased import FivePhaseGridBased
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if _skymtx and _analysisGrids:
    reuseVmtx_ = bool(reuseVmtx_)
    reuseDmtx_ = bool(reuseDmtx_)
    assert _analysisType_ == 0, \
        ValueError('3Phase recipe currently only supports illuminance simulation.')
    analysisRecipe = FivePhaseGridBased(
        _skymtx, _analysisGrids, _analysisType_, _vmtxPar_, _dmtxPar_,
        reuseVmtx_, reuseDmtx_)

# assign outputs to OUT
OUT = (analysisRecipe,)