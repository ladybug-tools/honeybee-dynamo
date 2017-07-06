"""Collection of methods for Honeybee geometry operations."""
import sys

try:
    import clr
    clr.AddReference('DynamoCore')
    clr.AddReference('ProtoGeometry')
    clr.AddReference('ProtoInterface')
    import Autodesk.DesignScript as DesignScript

    __dynamoPath = "\\".join((clr.References[2].Location).split("\\")[:-1])
    sys.path.append(__dynamoPath)
    import Dynamo
except ImportError as e:
    pass

from collections import namedtuple


def extractSurfacePoints(geometry, maxTessellationDivisions=25,
                         joinCoplanarTriFaces=True):
    """Extract points from a surface in Dynamo.

    Args:
        geometry: A Dynamo geometry.
        maxTessellationDivisions: Maximum number of divisions for surface tessellation.
        joinCoplanarTriFaces: Join two triangle faces if there is only two.

    Returns:
        A list of point lists.
    """
    def splitList(li, step=3):
        return [li[x:x + step] for x in range(0, len(li), step)]

    def __getPoints(rp):
        pts = list(rp.MeshVertices)
        # split values in xyz
        xyz = splitList(splitList(pts))
        del(pts)
        return xyz

    rpFactory = Dynamo.Visualization.DefaultRenderPackageFactory()
    tp = DesignScript.Interfaces.TessellationParameters()
    tp.MaxTessellationDivisions = maxTessellationDivisions
    tp.Tolerance = -1
    rp = rpFactory.CreateRenderPackage()
    geometry.Tessellate(rp, tp)
    pts = __getPoints(rp)

    # check if two faces are generated for this geometry and merge them
    if joinCoplanarTriFaces and len(pts) == 2:
        pts[0].insert(2, pts[1][2])
        pts = [pts[0]]
    # clean Dynamo objects
    del(rpFactory)
    del(rp)
    del(tp)

    return pts


# TODO: This should be done in the core library and shared between the libraries
def vectorsCrossProduct(vector1, vector2):
    """Calculate cross product of two vectors."""
    return vector1.X * vector2.X + \
        vector1.Y * vector2.Y + vector1.Z * vector2.Z


# TODO: This should be done in the core library and shared between the libraries
def isPointsSortedAntiClockwise(sortedPoints, normal):
    """Check if an ordered list of points are anti-clockwise."""
    vector0 = DesignScript.Geometry.Vector.ByTwoPoints(sortedPoints[0], sortedPoints[1])
    vector1 = DesignScript.Geometry.Vector.ByTwoPoints(sortedPoints[0], sortedPoints[-1])
    ptsNormal = DesignScript.Geometry.Vector.Cross(vector0, vector1)

    # in case points are anti-clockwise then normals should be parallel
    if vectorsCrossProduct(ptsNormal, normal) > 0:
        return True
    else:
        return False


def getSurfaceCenterPtandNormal(HBSurface):
    """Calculate center point and normal for a HBSurface.

    Args:
        HBSurface: A Honeybee surface

    Returns:
        Returns a tuple as (centerPt, normalVector)
    """
    try:
        geometry = HBSurface.geometry
    except AttributeError as e:
        raise TypeError("{} is not a HBSurface: {}".format(HBSurface, e))

    uv = DesignScript.Geometry.UV.ByCoordinates(0.5, 0.5)
    centerPt = geometry.PointAtParameter(uv.U, uv.V)
    normalVector = geometry.NormalAtParameter(uv.U, uv.V).Normalized()

    SurfaceData = namedtuple('SurfaceData', 'centerPt normalVector')
    return SurfaceData(centerPt, normalVector)


def xyzToGeometricalPoints(xyzPoints):
    """Convert a sequence of (x, y, z) values to Dynamo points."""
    for xyzList in xyzPoints:
        for xyz in xyzList:
            yield DesignScript.Geometry \
                .Point.ByCoordinates(xyz[0], xyz[1], xyz[2])


def polygon(pointList):
    """Return a polygon from points."""
    return DesignScript.Geometry.Polygon.ByPoints(pointList)


class Grid(object):
    """Test Grid for Honeybee for Dynamo."""

    __slots__ = ('polygon', 'uv', 'point', 'normal', 'originalPoint')

    def __init__(self, polygon, centerPt, baseSurface, distanceFromBaseSrf=0):
        """Init Dynamo test grid."""
        self.originalPoint = centerPt
        self.uv = baseSurface.UVParameterAtPoint(self.originalPoint)
        self.normal = baseSurface.NormalAtParameter(self.uv.U, self.uv.V)
        _movingVector = self.normal.Scale(distanceFromBaseSrf)
        self.polygon = polygon.Translate(_movingVector)
        self.point = centerPt.Translate(_movingVector)
        polygon.Dispose()

    def ToString(self):
        """Overwrite .NET ToString method."""
        return self.__repr__()

    def __repr__(self):
        """Test Grid."""
        return 'P: {}, {}, {}; V: {}, {}, {}'.format(
            self.point.X, self.point.Y, self.point.Z,
            self.normal.X, self.normal.Y, self.normal.Z
        )


class GridGenerator(object):
    """Grid generator for Dynamo."""

    def __init__(self, surfaces, gridSize, distanceFromBaseSrf=0, borders=None):
        """Init GridGenerator.

        Args:
            surfaces: List of Dynamo surfaces.
            gridSize: Grid size in Revit units.
            borders: List of closed polygons for surfaces borders. Surface border
                will be used if not provided.
        """
        self.surfaces = surfaces
        self.gridSize = gridSize
        self.distanceFromBaseSrf = float(distanceFromBaseSrf)
        self.borders = borders if borders else tuple(self.getSurfaceBorder(surface)
                                                     for surface in surfaces)
        assert len(self.surfaces) == len(self.borders), \
            "Length of surfaces should be equal to length of borders."

        # generate guidePts for trimming
        self.guidePts = (border.Center() for border in self.borders)
        self.uvs = self.calculatUV()

    @classmethod
    def fromHBZones(cls, HBZones, gridSize, distanceFromBaseSrf=0):
        """Create grid for Honeybee zones."""
        for HBZone in HBZones:
            assert hasattr(HBZone, 'isHBZone'), \
                '{} is not a Honeybee Zone.'.format(HBZone)

        # get profile for floors
        borders = tuple(floor.geometry for zone in HBZones for floor in zone.floors)
        surfaces = tuple(border.Patch().FlipNormalDirection() for border in borders)

        return cls(surfaces, gridSize, distanceFromBaseSrf, borders)

    @property
    def grids(self):
        """Generate polygons for each surface based on (u, v)."""
        for surface, (u, v), guidePt, border in zip(self.surfaces,
                                                    self.uvs,
                                                    self.guidePts,
                                                    self.borders):
            yield self.__createGrids(surface, u, v, guidePt, border)

    def calculatUV(self):
        """Calculate number of U, V for a surface based on a grid size.

        Args:
            surfaces: A list of Dynamo surfaces.
            gridSize: A number in Dynamo units.

        Returns:
            A list of (u, v) tuples for surfaces
        """
        for surface in self.surfaces:
            _cornerPt = surface.PointAtParameter(0, 0)
            _endUPt = surface.PointAtParameter(1, 0)
            _endVPt = surface.PointAtParameter(0, 1)
            u = int(round(_cornerPt.DistanceTo(_endUPt) / self.gridSize) + 1)
            v = int(round(_cornerPt.DistanceTo(_endVPt) / self.gridSize) + 1)
            _cornerPt.Dispose()
            _endUPt.Dispose()
            _endVPt.Dispose()
            yield (u, v)

    def __createGrids(self, surface, u, v, guidePt, border):
        """Create grids for a single surface."""
        _uSize = 1.0 / u
        _vSize = 1.0 / v

        for uCount in xrange(u):
            for vCount in xrange(v):
                _cornerPt00 = surface.PointAtParameter(uCount * _uSize, vCount * _vSize)
                _cornerPt10 = surface.PointAtParameter((uCount + 1) * _uSize, vCount * _vSize)
                _cornerPt11 = surface.PointAtParameter((uCount + 1) * _uSize, (vCount + 1) * _vSize)
                _cornerPt01 = surface.PointAtParameter(uCount * _uSize, (vCount + 1) * _vSize)

                _cornerPts = (_cornerPt00, _cornerPt01, _cornerPt11, _cornerPt10)
                # create a Polygon from points
                _pl = DesignScript.Geometry.Polygon.ByPoints(_cornerPts)
                _cenPoint = self.averagePoint(_cornerPts)
                # check if the center point is inside the border
                if border.ContainmentTest(_cenPoint):
                    # scale pl inside to avoid intersection with border for
                    # side polygons
                    _plane = DesignScript.Geometry.Plane.ByOriginNormal(
                        _cenPoint, surface.NormalAtPoint(_cenPoint)
                    )
                    _scaledPl = _pl.Scale(_plane, .95, .95, .95)

                    if not DesignScript.Geometry.Polygon.Intersect(border, _scaledPl):
                        # return plg if polygon center is inside and doesn't intersect
                        self.disposeGeometries(_cornerPts)
                        self.disposeGeometries((_plane, _scaledPl))
                        yield Grid(_pl, _cenPoint, surface,
                                   self.distanceFromBaseSrf)
                    else:
                        # it's inside and intersects. trim with border and return
                        # the inside part.
                        self.disposeGeometries((_plane, _scaledPl))
                        self.disposeGeometries(_cornerPts)
                        _tr = _pl.Trim(border, guidePt)[0]
                        _cenPoint = self.averagePolygonPoints(_tr)
                        _pl = _tr.CloseWithLine()
                        _tr.Dispose()
                        yield Grid(_pl, _cenPoint, surface,
                                   self.distanceFromBaseSrf)

                elif DesignScript.Geometry.Polygon.Intersect(border, _pl):
                    # center point is outside but still intersects
                    _tr = _pl.Trim(border, guidePt)[0]
                    _cenPoint = self.averagePolygonPoints(_tr)
                    if border.ContainmentTest(_cenPoint):
                        _pl = _tr.CloseWithLine()
                        _tr.Dispose()
                        self.disposeGeometries(_cornerPts)
                        yield Grid(_pl, _cenPoint, surface,
                                   self.distanceFromBaseSrf)

    @staticmethod
    def averagePoint(pts):
        """Find averagePoint for a list of points."""
        cen = [0, 0, 0]

        for pt in pts:
            cen[0] += pt.X
            cen[1] += pt.Y
            cen[2] += pt.Z

        return DesignScript.Geometry.Point.ByCoordinates(*(v / len(pts) for v in cen))

    def averagePolygonPoints(self, polygon):
        """Find averagePoint for a polygon."""
        startPt = polygon.Curves()[0].StartPoint
        pts = tuple(c.EndPoint for c in polygon.Curves())
        _len = len(pts)
        cen = [startPt.X, startPt.Y, startPt.Z]

        for pt in pts:
            cen[0] += pt.X
            cen[1] += pt.Y
            cen[2] += pt.Z

        self.disposeGeometries(pts)
        return DesignScript.Geometry.Point.ByCoordinates(*(v / (_len + 1) for v in cen))

    @staticmethod
    def disposeGeometries(geos):
        """Dispose a list of geometries."""
        for geo in geos:
            try:
                geo.Dispose()
            except:
                pass

    @staticmethod
    def getSurfaceBorder(surface):
        """Get surface border."""
        crvs = surface.PerimeterCurves()
        return crvs[0].Join(crvs[1:])
