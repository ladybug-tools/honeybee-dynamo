from honeybeex.radiance.recipe.sunlighthours import SunlightHoursAnalysisRecipe

sunVectors = [(0, 10, -10)]
pointGroups = (0, 0, 0)
vectorGroups = (0, 0, 1)
rp = SunlightHoursAnalysisRecipe(sunVectors, pointGroups, vectorGroups,
                                 timestep=1, ambientDivisions=1000, hbObjects=None)
rp.writeToFile("c:\\ladybug",
               "untitled2")
rp.run(False)
print rp.results()
