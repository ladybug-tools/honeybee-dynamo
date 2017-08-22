# assign inputs
_analysisGrids, _radiancePar_ = IN
analysisRecipe = None


try:
    from honeybee.radiance.recipe.daylightfactor.gridbased import GridBased
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if _analysisGrids:
    analysisRecipe = GridBased(_analysisGrids, _radiancePar_)

# assign outputs to OUT
OUT = (analysisRecipe,)