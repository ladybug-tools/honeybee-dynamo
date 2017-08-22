# assign inputs
_sky, _analysisGrids, _analysisType_, _radiancePar_ = IN
analysisRecipe = None

#import honeybee
#reload(honeybee.radiance.recipe.pointintime.gridbased)
try:
    from honeybee.radiance.recipe.pointintime.gridbased import GridBased
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if _sky and _analysisGrids:
    
    # set a sunlight hours analysis recipe together if there are points
    analysisRecipe = GridBased(_sky, _analysisGrids, _analysisType_,
                               _radiancePar_)

# assign outputs to OUT
OUT = (analysisRecipe,)