from ...honeybee.radiance.recipe.gridbased import HBGridBasedAnalysisRecipe
from ... import config


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
            --- Grasshopper ---
            ptsT: A Grasshopper DataTree of test points.
            vecT: A Grasshopper DataTree of vectors.
            --- Dynamo ---
                ptsT: List of lists of test points.
                vecT: List of lists of vectors.
        Returns:
            pts: Nested list of points
            vectors: Nested list of vectors
        """
        if config.platform == 'gh':
            pts, vec = self.__matchPointsAndVectorsGH(ptsT, vecT)
        elif config.platform == 'ds' or config.platform == 'rvt':
            pts, vec = self.__matchPointsAndVectorsDS(ptsT, vecT)

        return pts, vec

    def __matchPointsAndVectorsGH(self, ptsT, vecT):
        """Convert a grasshopperDataTree to list.

        Args:
            ptsT: A Grasshopper DataTree of test points.
            vecT: A Grasshopper DataTree of vectors.

        Returns:
            pts: Nested list of points
            vectors: Nested list of vectors
        """
        ptsT.SimplifyPaths()
        vecT.SimplifyPaths()

        pts = range(ptsT.BranchCount)
        vec = range(ptsT.BranchCount)

        for i, path in enumerate(ptsT.Paths):
            p = list(ptsT.Branch(path))
            try:
                v = list(vecT.Branch(path))
            except:
                v = []

            tempPts, tempVectors = self.__matchData(p, v)

            if len(tempPts) > 0:
                pts[i] = tempPts
                vec[i] = tempVectors
            else:
                # empty branch
                pts.remove(i)
                vec.remove(i)

        return pts, vec

    def __matchPointsAndVectorsDS(self, ptsT, vecT):
        """Convert a grasshopperDataTree to list.

        Args:
            ptsT: List of lists of test points.
            vecT: List of lists of vectors.

        Returns:
            pts: Nested list of points
            vectors: Nested list of vectors
        """
        pts = range(len(ptsT))
        vec = range(len(ptsT))

        for i, p in enumerate(ptsT):
            try:
                v = vecT[i]
            except:
                v = []

            tempPts, tempVectors = self.__matchData(
                list(self.flatten(p)), list(self.flatten(v))
            )

            if len(tempPts) > 0:
                pts[i] = tempPts
                vec[i] = tempVectors
            else:
                # empty branch
                pts.remove(i)
                vec.remove(i)

        return pts, vec

    # TODO: move this method to list operation library
    @staticmethod
    def __matchData(guide, follower, noneValue=(0, 0, 1)):
        """Match data between two lists.

        Args:
            guide: Long list.
            follower: Short list.
            noneValue: Place holder for default value if shortlist is an empty lists.
        """
        tempPts = range(len(guide))
        tempVectors = range(len(guide))

        for c, dp in enumerate(guide):
            if dp is not None:
                tempPts[c] = dp
                # match vector in vector list
                try:
                    # check if there is a vector with the same index
                    dv = follower[c]
                except IndexError:
                    try:
                        # try to get the last item provided (longest list match)
                        dv = follower[-1]
                    except IndexError:
                        # use default value
                        dv = noneValue
                finally:
                    if dv is None:
                        # use default value
                        dv = noneValue

                    tempVectors[c] = dv
            else:
                # empty list
                tempPts.remove(c)
                tempVectors(c)

        return tempPts, tempVectors
