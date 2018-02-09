# assign inputs
_skymtx, _views, _analysisType_, _dmtxPar_, reuseDmtx_ = IN
analysisRecipe = None

#import honeybee
#reload(honeybee.radiance.recipe.dc.imagebased)

try:
    from honeybee.radiance.recipe.daylightcoeff.imagebased import DaylightCoeffImageBased
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if _skymtx and _views:
    # check inputs
    assert _skymtx.sky_density < 2, ValueError(
        'Due to Windows limitations on the maximum number of files that can be\n'
        ' open concurrently image-based analysis only works with skyDensity of 1.')
    
    analysisRecipe = DaylightCoeffImageBased(
        _skymtx, _views, _analysisType_, _dmtxPar_,
        reuse_daylight_mtx=reuseDmtx_)

# assign outputs to OUT
OUT = (analysisRecipe,)