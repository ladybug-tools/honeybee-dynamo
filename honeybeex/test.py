from honeybee.radiance.sky.certainIlluminance import SkyWithCertainIlluminanceLevel
from honeybee.radiance.recipe.gridbased import HBGridBasedAnalysisRecipe
from honeybee.hbsurface import HBAnalysisSurface

if __name__ == "__main__":
	pts = [(0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0)]
	vectors = [(0, 0, 1)]
	sky = SkyWithCertainIlluminanceLevel(2000)
	hbsrf = HBAnalysisSurface("001", pts, surfaceType=None, isNameSetByUser=True, isTypeSetByUser=True)
	rp = HBGridBasedAnalysisRecipe(sky, pts, vectors, None, [hbsrf])
	rp.writeToFile("c:\ladybug", "test")
	rp.run(False)
