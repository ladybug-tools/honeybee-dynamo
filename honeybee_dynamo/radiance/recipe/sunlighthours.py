from honeybee.radiance.recipe.sunlighthours import HBSunlightHoursAnalysisRecipe
from ladybug.sunpath import LBSunpath
from ._sensor import matchPointsAndVectors


class SunlightHoursAnalysisRecipe(HBSunlightHoursAnalysisRecipe):
    """Sunlight hour analysis.

    This class calculates number of sunlight hours for a group of test points.

    Attributes:
        sunVectors: A list of ladybug sun vectors as (x, y, z) values. Z value
            for sun vectors should be negative (coming from sun toward earth)
        pointGroupsT: A Grasshopper DataTree of Point3d test points. Each branch
            of test points will be converted to a TestPointGroup.
        vectorGroupsT: A DataTree of Vector3d vectors. Each vector represents direction
            of corresponding point in testPts. If the vector is not provided (0, 0, 1)
            will be assigned.
        timestep: The number of timesteps per hour for sun vectors. This number
            should be smaller than 60 and divisible by 60. The default is set to
            1 such that one sun vector is generated for each hour (Default: 1).
    """

    def __init__(self, sunVectors, pointGroupsT, vectorGroupsT=[], timestep=1):
        """Create sunlighthours recipe."""
        # convert DataTrees to lists
        pointGroups, vectorGroups = matchPointsAndVectors(pointGroupsT,
                                                          vectorGroupsT)

        if len(pointGroups) == 0:
            print "No test points!"

        HBSunlightHoursAnalysisRecipe.__init__(self, sunVectors, pointGroups,
                                               vectorGroups, timestep)

    @classmethod
    def fromLBSuns(cls, suns, pointGroups, vectorGroups=[], timestep=1,
                   hbObjects=None, subFolder="sunlighthour"):
        """Create sunlighthours recipe from LB sun objects.

        Attributes:
            suns: A list of ladybug suns.
            pointGroups: A list of (x, y, z) test points or lists of (x, y, z) test
                points. Each list of test points will be converted to a
                TestPointGroup. If testPts is a single flattened list only one
                TestPointGroup will be created.
            vectorGroups: An optional list of (x, y, z) vectors. Each vector
                represents direction of corresponding point in testPts. If the
                vector is not provided (0, 0, 1) will be assigned.
            timestep: The number of timesteps per hour for sun vectors. This number
                should be smaller than 60 and divisible by 60. The default is set to
                1 such that one sun vector is generated for each hour (Default: 1).
        """
        try:
            sunVectors = [s.sunVector for s in suns if s.isDuringDay]
        except AttributeError:
            raise ValueError("%s is not a valid LBSun" % s)

        return cls(sunVectors, pointGroups, vectorGroups, timestep)

    @classmethod
    def fromLocationAndHoys(cls, location, HOYs, pointGroups, vectorGroups=[],
                            timestep=1):
        """Create sunlighthours recipe from Location and hours of year."""
        sp = LBSunpath.fromLocation(location)

        suns = [sp.calculateSunFromHOY(HOY) for HOY in HOYs]

        sunVectors = [s.sunVector for s in suns if s.isDuringDay]

        return cls(sunVectors, pointGroups, vectorGroups, timestep)

    @classmethod
    def fromLocationAndAnalysisPeriod(
        cls, location, analysisPeriod, pointGroups, vectorGroups=[]
    ):
        """Create sunlighthours recipe from Location and analysis period."""
        sp = LBSunpath.fromLocation(location)

        suns = [sp.calculateSunFromHOY(HOY) for HOY in analysisPeriod.floatHOYs]

        sunVectors = [s.sunVector for s in suns if s.isDuringDay]

        return cls(sunVectors, pointGroups, vectorGroups,
                   analysisPeriod.timestep)
