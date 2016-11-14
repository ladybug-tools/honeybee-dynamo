###### start you code from here ###
from honeybeex.radiance.recipe.gridbased import GridBasedAnalysisRecipe

_HBSky, _testPoints, ptsVectors_, _simType, _radParameters_ = IN

if _HBSky and _testPoints and ptsVectors_:
	analysisRecipe = GridBasedAnalysisRecipe(
		_HBSky, _testPoints, ptsVectors_, _simType, _radParameters_
		)

	OUT = analysisRecipe
