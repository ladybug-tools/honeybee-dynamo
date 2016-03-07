# from honeybee.radiance.sky.certainIlluminance import SkyWithCertainIlluminanceLevel
# from honeybee.radiance.analysisrecipe import HBGridBasedAnalysisRecipe
# from honeybee import dataoperation
#
# pts = (0, 0, 0)
# pts1 = [[(0, 0, 0)]]
# pts2 = [(0, 0, 0), (10, 0, 0)], [(0, 0, 10), (10, 0, 10)]
# normals = [(0, 1, 1)]
# # print list(dataoperation.flattenTupleList(pts))
# # print list(dataoperation.flattenTupleList(pts1))
# # print list(dataoperation.flattenTupleList(pts2))
#
# sky = SkyWithCertainIlluminanceLevel(2000)
# rp = HBGridBasedAnalysisRecipe(sky, pts2, normals)
# #
# print rp
# print "vectors:", rp.vectors
# # print rp.toRadString()
# rp.toFile("c:/ladybug/points.pts")


from honeybee.hbsurface import HBAnalysisSurface

pts = ((0, 0, 0), (10, 0, 0), (0, 0, 10))
hbsrf = HBAnalysisSurface("001", pts, surfaceType=None, isNameSetByUser=True, isTypeSetByUser=True)

print hbsrf.normal
