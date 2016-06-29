from honeybee.hbfensurface import HBFenSurface as FenSurface
import geometryoperation as go
import config


class HBFenSurface(FenSurface):
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
        isCreatedFromGeometry: ...
    """

    def __init__(self, name, sortedPoints=[], isNameSetByUser=False,
                 radProperties=None, epProperties=None,
                 isCreatedFromGeometry=False):
        """Init honeybee fenestration surface."""
        FenSurface.__init__(self, name, sortedPoints=sortedPoints,
                            isNameSetByUser=isNameSetByUser,
                            radProperties=radProperties,
                            epProperties=epProperties)

        self.isCreatedFromGeometry = isCreatedFromGeometry

    def fromGeometry(cls, name, geometry, isNameSetByUser=False,
                     radProperties=None, epProperties=None,
                     isCreatedFromGeometry=True):
        "Create a honeybee fenestration surface from Grasshopper or Dynamo geometry."
        self.geometry = geometry
        sortedPoints = go.extractSurfacePoints(self)

        return cls(name, sortedPoints, isNameSetByUser, radProperties,
                   epProperties, isCreatedFromGeometry=True)

    @property
    def geometry(self):
        """return geometry."""
        if self.isCreatedFromGeometry:
            return self.__geometry
        else:
            return go.polygon(tuple(go.xyzToGeometricalPoints(self.absolutePoints)))

    @geometry.setter
    def geometry(self, geo):
        """Set geometry."""
        self.__geometry = geo
