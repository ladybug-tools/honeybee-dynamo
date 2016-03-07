from honeybee.hbsurface import HBAnalysisSurface
import geometryoperation as go


class HBSurface(HBAnalysisSurface):
    """Honeybee surface for Grasshopper."""

    def __init__(self, name, geometry, surfaceType=None,
                 isNameSetByUser=False, isTypeSetByUser=False,
                 radProperties=None, epProperties=None):
        """Create a honeybee surface for Grasshopper."""
        # Add geometry to initiate the calculations for surface normal, centroid,
        self.geometry = geometry

        HBAnalysisSurface.__init__(
            self, name, sortedPoints=[], surfaceType=surfaceType,
            isNameSetByUser=isNameSetByUser, isTypeSetByUser=isTypeSetByUser,
            radProperties=radProperties, epProperties=epProperties)

    @property
    def geometry(self):
        """return geometry."""
        return self.__geometry

    @geometry.setter
    def geometry(self, geo):
        """Set geometry."""
        self.__geometry = geo

        # calculate center point and normal
        self.centroid, self.normal = go.getSurfaceCenterPtandNormal(self)

    @property
    def points(self):
        """Get/set points."""
        return go.extractSurfacePoints(self)

    @points.setter
    def points(self, pts):
        # HBSurface in Grasshopper is based on geometry and not points.
        # This will create a place holder for self.__pts but won't effect the
        # outputs.
        HBAnalysisSurface.points = pts
