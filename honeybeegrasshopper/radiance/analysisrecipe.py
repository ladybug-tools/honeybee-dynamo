from ..honeybee.radiance.analysisrecipe import HBGridBasedAnalysisRecipe
from Rhino.Geometry import Vector3d


class GridBasedAnalysisRecipe(HBGridBasedAnalysisRecipe):
    """Grid base analysis base class.

    Attributes:
        sky: A honeybee sky for the analysis
        testPtsT: Test points as a DataTree of Rhino.Geometry.Point3d
        ptsVectorsT: An optional DataTree of point vectors as Rhino.Geometry.Vector3d
            +Z Vector will be assigned if vectors are not provided
        radianceParameters: Radiance parameters for this analysis (Default: RadianceParameters.LowQuality)
    """

    def __init__(self, sky, testPtsT, ptsVectorsT=None, radParameters=None):
        """Initialize analysis recipe."""
        HBGridBasedAnalysisRecipe.__init__(
            self, sky=sky, testPts=[], ptsVectors=[], radParameters=radParameters)
        self.testPts = testPtsT
        """A list of test points as Rhino.Geometry.Point3d."""
        self.ptsVectors = testPtsT
        """An optional list of point vectors as Rhino.Geometry.Vector3d
            +Z Vector will be assigned if vectors are not provided."""

    @property
    def testPts(self):
        """List of test points."""
        return self.__testPts

    # TODO: Add check for test points. Remove null test points
    @testPts.setter
    def testPts(self, pts):
        """Set list of test points."""
        # Flatten DataTree to a flattened generator
        # Save the pattern in self.PtsStructure
        # write a function for datatree to list and list to datatree
        try:
            pts.SimplifyPaths()
        except AttributeError:
            pass

        # clean datatree
        self.__testPts = pts

    @property
    def ptsVectors(self):
        """List of vectors for each test point.

        +Z Vector will be assigned if vectors are not provided
        """
        return self.__ptsVectors

    @ptsVectors.setter
    def ptsVectors(self, vectors):
        """List of vectors for each test point.

        +Z Vector will be assigned if vectors are not provided
        """
        if vectors == []:
            self.__ptsVectors = [Vector3d.ZAxis for pt in self.testPts]
        else:
            assert len(self.testPts) == len(vectors), \
                "Length of test points should be equal to length of vectors."
            self.__ptsVectors = vectors

    def __repr__(self):
        """Represent grid based recipe."""
        return "%s #testPts:%d #gourp:%d" % (self.__class__.__name__, self.__testPts.DataCount, self.__testPts.BranchCount)
