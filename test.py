import sys
sys.path.append(r"C:\Users\Administrator\Documents\GitHub\honeybee-grasshopper")

from honeybeegrasshopper.radiance import analysisrecipe, sky

sk = sky.HBCertainIlluminanceLevelSky(200)
analysisrecipe.GridBasedAnalysisRecipe(sk, [])
