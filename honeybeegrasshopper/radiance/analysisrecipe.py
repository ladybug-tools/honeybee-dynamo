from sky import *
from radianceparameters import *
from ..honeybee.radiance.analysisrecipe import *

class GridBasedAnalysisRecipe(HBGridBasedAnalysisRecipe):
    """Grid base analysis base class

        Attributes:
            sky: A honeybee sky for the analysis
            radianceParameters: Radiance parameters for this analysis (Default: RadianceParameters.LowQuality)
    """
    def __init__(self, sky, testPts, ptsVectors = None, radParameters = None):

        HBGridBasedAnalysisRecipe.__init__(self, sky, radParameters)
        self.testPts = testPts
        self.ptsVectors = ptsVectors

    @property
    def testPts(self):
        """List of test points
        """
        return self.__testPts

    # TODO: Add check for test points. Remove null test points
    @testPts.setter
    def testPts(self, pts):
        """Set list of test points
        """
        pts.SimplifyPaths()

        # clean datatree
        self.__testPts = pts

    @property
    def ptsVectors(self):
        """List of vectors for each test point.
            +Z Vector will be assigned if vectors are not provided
        """
        return self.__ptsVectors

    # TODO: Add check for vectors. Remove null values. assign 0, 0, 1 in case of None
    @ptsVectors.setter
    def ptsVectors(self, vectors):
        """List of vectors for each test point.
            +Z Vector will be assigned if vectors are not provided
        """
        self.__ptsVectors = vectors

    def __repr__(self):
        return "%s #testPts:%d #gourp:%d"%(self.__class__.__name__, self.__testPts.DataCount, self.__testPts.BranchCount)
