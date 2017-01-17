import honeybee.hbsurface as hbsrf
from .utilities import extractSurfacePoints, polygon, xyzToGeometricalPoints


class HBSurface(hbsrf.HBSurface):
    """Honeybee surface.

    Args:
        name: A unique string for surface name
        sortedPoints: A list of 3 points or more as tuple or list with three items
            (x, y, z). Points should be sorted. This class won't sort the points.
            If surfaces has multiple subsurfaces you can pass lists of point lists
            to this function (e.g. ((0, 0, 0), (10, 0, 0), (0, 10, 0))).
        surfaceType: Optional input for surface type. You can use any of the surface
            types available from surfacetype libraries or use a float number to
            indicate the type. If not indicated it will be assigned based on normal
            angle of the surface which will be calculated from surface points.
                0.0: Wall           0.5: UndergroundWall
                1.0: Roof           1.5: UndergroundCeiling
                2.0: Floor          2.25: UndergroundSlab
                2.5: SlabOnGrade    2.75: ExposedFloor
                3.0: Ceiling        4.0: AirWall
                6.0: Context
        isNameSetByUser: If you want the name to be changed by honeybee any case
            set isNameSetByUser to True. Default is set to False which let Honeybee
            to rename the surface in cases like creating a newHBZone.
        radProperties: Radiance properties for this surface. If empty default
            RADProperties will be assigned to surface by Honeybee.
        epProperties: EnergyPlus properties for this surface. If empty default
            epProperties will be assigned to surface by Honeybee.
    """

    @classmethod
    def fromGeometry(cls, name, geometry, surfaceType=None,
                     isNameSetByUser=False, isTypeSetByUser=False,
                     radProperties=None, epProperties=None):
        """Create a honeybee surface from Grasshopper or Dynamo geometry."""
        _pts = extractSurfacePoints(geometry)
        _srf = cls(name, _pts, surfaceType, isNameSetByUser, isTypeSetByUser,
                   radProperties, epProperties)
        _srf.geometry = geometry
        return _srf

    @property
    def isCreatedFromGeometry(self):
        """Return True."""
        return True

    @property
    def geometry(self):
        """Return geometry."""
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
