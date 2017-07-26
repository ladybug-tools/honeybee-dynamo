# assign inputs
_sunVectors, _hoys, _analysisGrids, _timestep_ = IN
analysisRecipe = None

try:
    from honeybee.radiance.recipe.solaraccess.gridbased import SolarAccessGridBased
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if _sunVectors and _sunVectors[0] != None and \
    _hoys and _hoys[0] != None and _analysisGrids:
    # set a sunlight hours analysis recipe together if there are points
    analysisRecipe = SolarAccessGridBased(
        _sunVectors, _hoys, _analysisGrids, _timestep_)

# assign outputs to OUT
OUT = (analysisRecipe,)