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


def extract_geometry_points(geometries, meshing_parameters=None):
    """Extract points from a surface in Dynamo.

    Args:
        geometry: A Dynamo geometry.
        meshing_parameters:  A tuple for (maxTessellationDivisions, joinCoplanarTriFaces)
            max_tessellation_divisions is the maximum number of divisions for surface
            tessellation. join_coplanar_tri_faces is a boolean to indicate if honeybee
            should join two triangle faces if they are coplanar. This option generates
            a cleaner Radiance geometry but will take longer to generate the file
            (Default: (25, True)).
    Returns:
        A Collection of (geometry, points) in which each geometry is coupled by points.
        For planar surfaces the length of the points list will be only 1. For
        non-planar surfaces, meshes or surfaces with internal edges it will be multiple
        lists.
    """
    def split_list(li, step=3):
        return [li[x:x + step] for x in range(0, len(li), step)]

    def __get_points(rp):
        pts = list(rp.MeshVertices)
        # split values in xyz
        xyz = split_list(split_list(pts))
        del(pts)
        return xyz

    meshing_parameters = meshing_parameters or (25, True)

    max_tessellation_divisions = meshing_parameters[0]
    join_coplanar_tri_faces = meshing_parameters[1]

    if not hasattr(geometries, '__iter__'):
        geometries = (geometries,)

    for geometry in geometries:
        rp_factory = Dynamo.Visualization.DefaultRenderPackageFactory()
        tp = DesignScript.Interfaces.TessellationParameters()
        tp.MaxTessellationDivisions = max_tessellation_divisions
        tp.Tolerance = -1
        rp = rp_factory.CreateRenderPackage()

        geometry.Tessellate(rp, tp)
        pts = __get_points(rp)

        # check if two faces are generated for this geometry and merge them
        if join_coplanar_tri_faces and len(pts) == 2:
            pts[0].insert(2, pts[1][2])
            pts = [pts[0]]

        # matech the data structure
        yield iter(((geometry, pts),))

        # clean Dynamo objects
        del(rp_factory)
        del(rp)
        del(tp)


def xyz_to_geometrical_points(xyz_points):
    """Convert a sequence of (x, y, z) values to Dynamo points."""
    for xyzList in xyz_points:
        for xyz in xyzList:
            yield DesignScript.Geometry \
                .Point.ByCoordinates(xyz[0], xyz[1], xyz[2])


def polygon(point_list):
    """Return a polygon from points."""
    return DesignScript.Geometry.Polygon.ByPoints(point_list)


# ------------------------- End of honeybee[+] methods -----------------------------
# ------------------------------ Utilities -----------------------------------------
# TODO: This should be done in ladybug core library and shared between the libraries
def vectors_cross_product(vector1, vector2):
    """Calculate cross product of two vectors."""
    return vector1.X * vector2.X + \
        vector1.Y * vector2.Y + vector1.Z * vector2.Z


# TODO: This should be done in the core library and shared between the libraries
def is_points_sorted_anti_clockwise(sorted_points, normal):
    """Check if an ordered list of points are anti-clockwise."""
    vector0 = DesignScript.Geometry.Vector.ByTwoPoints(sorted_points[0],
                                                       sorted_points[1])
    vector1 = DesignScript.Geometry.Vector.ByTwoPoints(sorted_points[0],
                                                       sorted_points[-1])
    pts_normal = DesignScript.Geometry.Vector.Cross(vector0, vector1)

    # in case points are anti-clockwise then normals should be parallel
    if vectors_cross_product(pts_normal, normal) > 0:
        return True
    else:
        return False


def get_surface_center_ptand_normal(hb_surface):
    """Calculate center point and normal for a hb_surface.

    Args:
        hb_surface: A Honeybee surface

    Returns:
        Returns a tuple as (center_pt, normalVector)
    """
    try:
        geometry = hb_surface.geometry
    except AttributeError as e:
        raise TypeError("{} is not a HBSurface: {}".format(hb_surface, e))

    uv = DesignScript.Geometry.UV.ByCoordinates(0.5, 0.5)
    center_pt = geometry.PointAtParameter(uv.U, uv.V)
    normal_vector = geometry.NormalAtParameter(uv.U, uv.V).Normalized()

    SurfaceData = namedtuple('SurfaceData', 'center_pt normalVector')
    return SurfaceData(center_pt, normal_vector)


class Grid(object):
    """Test Grid for Honeybee for Dynamo."""

    __slots__ = ('polygon', 'uv', 'point', 'normal', 'originalPoint')

    def __init__(self, polygon, center_pt, base_surface, distance_from_base_srf=0):
        """Init Dynamo test grid."""
        self.originalPoint = center_pt
        self.uv = base_surface.UVParameterAtPoint(self.originalPoint)
        self.normal = base_surface.NormalAtParameter(self.uv.U, self.uv.V)
        _movingVector = self.normal.Scale(distance_from_base_srf)
        self.polygon = polygon.Translate(_movingVector)
        self.point = center_pt.Translate(_movingVector)
        polygon.Dispose()

    def to_string(self):
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

    def __init__(self, surfaces, grid_size, distance_from_base_srf=0, borders=None):
        """Init GridGenerator.

        Args:
            surfaces: List of Dynamo surfaces.
            grid_size: Grid size in Revit units.
            borders: List of closed polygons for surfaces borders. Surface border
                will be used if not provided.
        """
        self.surfaces = surfaces
        self.grid_size = grid_size
        self.distance_from_base_srf = float(distance_from_base_srf)
        self.borders = borders if borders else \
            tuple(self.get_surface_border(surface) for surface in surfaces)
        assert len(self.surfaces) == len(self.borders), \
            "Length of surfaces should be equal to length of borders."

        # generate guide_pts for trimming
        self.guide_pts = (border.Center() for border in self.borders)
        self.uvs = self.calculat_uv()

    @classmethod
    def from_hb_zones(cls, hb_zones, grid_size, distance_from_base_srf=0):
        """Create grid for Honeybee zones."""
        for HBZone in hb_zones:
            assert hasattr(HBZone, 'isHBZone'), \
                '{} is not a Honeybee Zone.'.format(HBZone)

        # get profile for floors
        borders = tuple(floor.geometry for zone in hb_zones for floor in zone.floors)
        surfaces = tuple(border.Patch().FlipNormalDirection() for border in borders)

        return cls(surfaces, grid_size, distance_from_base_srf, borders)

    @property
    def grids(self):
        """Generate polygons for each surface based on (u, v)."""
        for surface, (u, v), guide_pt, border in zip(self.surfaces,
                                                     self.uvs,
                                                     self.guide_pts,
                                                     self.borders):
            yield self.__create_grids(surface, u, v, guide_pt, border)

    def calculat_uv(self):
        """Calculate number of U, V for a surface based on a grid size.

        Args:
            surfaces: A list of Dynamo surfaces.
            grid_size: A number in Dynamo units.

        Returns:
            A list of (u, v) tuples for surfaces
        """
        for surface in self.surfaces:
            _cornerPt = surface.PointAtParameter(0, 0)
            _endUPt = surface.PointAtParameter(1, 0)
            _endVPt = surface.PointAtParameter(0, 1)
            u = int(round(_cornerPt.DistanceTo(_endUPt) / self.grid_size) + 1)
            v = int(round(_cornerPt.DistanceTo(_endVPt) / self.grid_size) + 1)
            _cornerPt.Dispose()
            _endUPt.Dispose()
            _endVPt.Dispose()
            yield (u, v)

    # TODO(mostapha): Add an option with no border
    def __create_grids(self, surface, u, v, guide_pt=None, border=None):
        """Create grids for a single surface."""
        _uSize = 1.0 / u
        _vSize = 1.0 / v

        for uCount in xrange(u):
            for vCount in xrange(v):
                _cornerPt00 = surface.PointAtParameter(
                    uCount * _uSize, vCount * _vSize)
                _cornerPt10 = surface.PointAtParameter(
                    (uCount + 1) * _uSize, vCount * _vSize)
                _cornerPt11 = surface.PointAtParameter(
                    (uCount + 1) * _uSize, (vCount + 1) * _vSize)
                _cornerPt01 = surface.PointAtParameter(
                    uCount * _uSize, (vCount + 1) * _vSize)

                _cornerPts = (_cornerPt00, _cornerPt01, _cornerPt11, _cornerPt10)
                # create a Polygon from points
                _pl = DesignScript.Geometry.Polygon.ByPoints(_cornerPts)
                _cenPoint = self.average_point(_cornerPts)
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
                        self.dispose_geometries(_cornerPts)
                        self.dispose_geometries((_plane, _scaledPl))
                        yield Grid(_pl, _cenPoint, surface,
                                   self.distance_from_base_srf)
                    else:
                        # it's inside and intersects. trim with border and return
                        # the inside part.
                        self.dispose_geometries((_plane, _scaledPl))
                        self.dispose_geometries(_cornerPts)
                        _tr = _pl.Trim(border, guide_pt)[0]
                        _cenPoint = self.average_polygon_points(_tr)
                        _pl = _tr.CloseWithLine()
                        _tr.Dispose()
                        yield Grid(_pl, _cenPoint, surface,
                                   self.distance_from_base_srf)

                elif DesignScript.Geometry.Polygon.Intersect(border, _pl):
                    # center point is outside but still intersects
                    _tr = _pl.Trim(border, guide_pt)[0]
                    _cenPoint = self.average_polygon_points(_tr)
                    if border.ContainmentTest(_cenPoint):
                        _pl = _tr.CloseWithLine()
                        _tr.Dispose()
                        self.dispose_geometries(_cornerPts)
                        yield Grid(_pl, _cenPoint, surface,
                                   self.distance_from_base_srf)

    @staticmethod
    def average_point(pts):
        """Find average_point for a list of points."""
        cen = [0, 0, 0]

        for pt in pts:
            cen[0] += pt.X
            cen[1] += pt.Y
            cen[2] += pt.Z

        return DesignScript.Geometry.Point.ByCoordinates(*(v / len(pts) for v in cen))

    def average_polygon_points(self, polygon):
        """Find average_point for a polygon."""
        start_pt = polygon.Curves()[0].StartPoint
        pts = tuple(c.EndPoint for c in polygon.Curves())
        _len = len(pts)
        cen = [start_pt.X, start_pt.Y, start_pt.Z]

        for pt in pts:
            cen[0] += pt.X
            cen[1] += pt.Y
            cen[2] += pt.Z

        self.dispose_geometries(pts)
        return DesignScript.Geometry.Point.ByCoordinates(*(v / (_len + 1) for v in cen))

    @staticmethod
    def dispose_geometries(geos):
        """Dispose a list of geometries."""
        for geo in geos:
            try:
                geo.Dispose()
            except Exception:
                pass

    @staticmethod
    def get_surface_border(surface):
        """Get surface border."""
        crvs = surface.PerimeterCurves()
        return crvs[0].Join(crvs[1:])
