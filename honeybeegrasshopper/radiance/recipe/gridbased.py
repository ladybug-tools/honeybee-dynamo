from ...honeybee.radiance.recipe.gridbased import HBGridBasedAnalysisRecipe


class GridBasedAnalysisRecipe(HBGridBasedAnalysisRecipe):
    """Grid base analysis recipe.

    Attributes:
        sky: A honeybee sky for the analysis
        pointGroups: A Grasshopper DataTree of Point3d test points. Each branch
            of test points will be converted to a TestPointGroup.
        vectorGroups: A DataTree of Vector3d vectors. Each vector represents direction
            of corresponding point in testPts. If the vector is not provided (0, 0, 1)
            will be assigned.
        radParameters: Radiance parameters for this analysis.
            (Default: RadianceParameters.LowQuality)
    """

    def __init__(self, sky, pointGroupsT, vectorGroupsT, radParameters=None):
        """Create grid-based recipe."""
        # convert DataTrees to lists
        pointGroups, vectorGroups = self.matchPointsAndVectors(pointGroupsT, vectorGroupsT)

        if len(pointGroups) == 0:
            print "No test points!"

        HBGridBasedAnalysisRecipe.__init__(self, sky, pointGroups,
                                           vectorGroups, radParameters)

    def matchPointsAndVectors(self, ptsT, vecT):
        """Convert a grasshopperDataTree to list.

        Args:
            ptsT: A Grasshopper DataTree of test points.
            vecT: A Grasshopper DataTree of vectors.

        Returns:
            pts: Nested list of points
            vectors: Nested list of vectors
        """
        pts = []
        vec = []
        ptsT.SimplifyPaths()
        vecT.SimplifyPaths()

        for i, path in enumerate(ptsT.Paths):
            p = list(ptsT.Branch(path))
            try:
                v = list(vecT.Branch(path))
            except:
                v = []

            tempPts = []
            tempVectors = []

            for c, dp in enumerate(p):
                if dp is not None:
                    tempPts.append(dp)
                    try:
                        dv = v[c]
                    except IndexError:
                        try:
                            dv = v[-1]
                        except IndexError:
                            dv = (0, 0, 1)
                    finally:
                        if dv is None:
                            dv = (0, 0, 1)

                        tempVectors.append(dv)

            if len(tempPts) > 0:
                pts.append(tempPts)
                vec.append(tempVectors)

        return pts, vec
