###### start you code from here ###
from honeybeex.radiance.recipe.sunlighthours import SunlightHoursAnalysisRecipe

_sunVectors, _testPoints, _ptsVectors, _timestep_ = IN

if not hasattr(_sunVectors, '__iter__'):
	_sunVectors = (_sunVectors,)

if _sunVectors and _testPoints and _ptsVectors:
	analysisRecipe = SunlightHoursAnalysisRecipe(_sunVectors,
		_testPoints, _ptsVectors, _timestep_
	)

	OUT = analysisRecipe