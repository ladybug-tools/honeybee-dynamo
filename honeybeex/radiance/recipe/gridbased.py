from ...honeybee.radiance.recipe.gridbased import HBGridBasedAnalysisRecipe
from ._sensor import SensorGroup


class GridBasedAnalysisRecipe(HBGridBasedAnalysisRecipe):
    """Grid base analysis recipe.

    Attributes:
        sky: A honeybee sky for the analysis
        pointGroupsT: A Grasshopper DataTree of Point3d test points. Each branch
            of test points will be converted to a TestPointGroup.
        vectorGroupsT: A DataTree of Vector3d vectors. Each vector represents direction
            of corresponding point in testPts. If the vector is not provided (0, 0, 1)
            will be assigned.
        simulationType: 0: Illuminance(lux), 1: Radiation (kWh), 2: Luminance (Candela)
            (Default: 0)
        radParameters: Radiance parameters for this analysis.
            (Default: RadianceParameters.LowQuality)
    """

    def __init__(self, sky, pointGroupsT, vectorGroupsT, simulationType=0,
                 radParameters=None):
        """Create grid-based recipe."""
        # convert DataTrees to lists
        pointGroups, vectorGroups = \
            SensorGroup().matchPointsAndVectors(pointGroupsT, vectorGroupsT)

        if len(pointGroups) == 0:
            print "No test points!"

        HBGridBasedAnalysisRecipe.__init__(self, sky, pointGroups,
                                           vectorGroups, simulationType,
                                           radParameters)
