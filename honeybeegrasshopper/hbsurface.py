from honeybee.hbsurface import HBAnalysisSurface
import geometryoperation as go

class HBSurface(HBAnalysisSurface):
    """Minimum implementation of Honeybee surface."""

    def __init__(self):
        """Initialize Honeybee Surface."""
        pass

    @property
    def geometry(self):
        """return geometry."""
        return self.__geometry

    @geometry.setter
    def geometry(self, geo):
        """Set geometry."""
        self.__geometry = geo
        # calculate center point and normal
        
        # calculate surface baseplane
