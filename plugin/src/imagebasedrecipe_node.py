# assign inputs
_sky, _views, _analysisType_, _radiancePar_ = IN
analysisRecipe = None

try:
    from honeybee.radiance.recipe.pointintime.imagebased import ImageBased
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if _sky and _views:
    # set a sunlight hours analysis recipe together if there are points
    analysisRecipe = ImageBased(_sky, _views, _analysisType_, _radiancePar_)

# assign outputs to OUT
OUT = (analysisRecipe,)