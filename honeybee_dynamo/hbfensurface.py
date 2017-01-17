import honeybee.hbfensurface as hbfensrf
from .utilities import extractSurfacePoints, polygon, xyzToGeometricalPoints


class HBFenSurface(hbfensrf.HBFenSurface):
    """Honeybee fenestration surface.

    Args:
        name: A unique string for surface name
        sortedPoints: A list of 3 points or more as tuple or list with three items
            (x, y, z). Points should be sorted. This class won't sort the points.
            If surfaces has multiple subsurfaces you can pass lists of point lists
            to this function (e.g. ((0, 0, 0), (10, 0, 0), (0, 10, 0))).
        isNameSetByUser: If you want the name to be changed by honeybee any case
            set isNameSetByUser to True. Default is set to False which let Honeybee
            to rename the surface in cases like creating a newHBZone.
        radProperties: Radiance properties for this surface. If empty default
            RADProperties will be assigned to surface by Honeybee.
        epProperties: EnergyPlus properties for this surface. If empty default
            epProperties will be assigned to surface by Honeybee.
    """

    @classmethod
    def fromGeometry(cls, name, geometry, isNameSetByUser=False,
                     radProperties=None, epProperties=None,
                     isCreatedFromGeometry=True):
        """Create a honeybee fenestration surface from Dynamo geometry."""
        cls.geometry = geometry
        sortedPoints = extractSurfacePoints(cls)

        return cls(name, sortedPoints, isNameSetByUser, radProperties,
                   epProperties)

    @property
    def isCreatedFromGeometry(self):
        """Return True."""
        return True

    @property
    def geometry(self):
        """return geometry."""
        if self.isCreatedFromGeometry:
            return self.__geometry
        else:
            return self.profile

    @geometry.setter
    def geometry(self, geo):
        """Set geometry."""
        self.__geometry = geo

    @property
    def profile(self):
        """Get profile curve of this surface."""
        return polygon(tuple(xyzToGeometricalPoints(self.absolutePoints)))
