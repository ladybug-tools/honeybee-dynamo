"""Collection of methods for Honeybee geometry operations in Grasshopper."""
from collections import namedtuple

try:
    import Rhino as rc
except ImportError as e:
    pass


def isPlanar(geometry, tol=1e-3):
    """Check if a surface in planar."""
    return geometry.Faces[0].IsPlanar(tol)


def extractSurfacePoints(geometry, triangulate=False, meshingParameters=None):
    """Calculate list of points for a HBSurface.

    For planar surfaces the length of the list will be only 1. For non-planar
    surfaces or surfaces with internal edges it will be a number of lists.

    Args:
        geometry: A Mesh or Brep
        triangulate: If set to True the function returns the points for triangulated
            surfaces (Default: False)
        meshingParameters: Optional Rhino meshingParameters. This will only be used if the
            surface is non-planar or has an internal edge and needs to be meshed.
            Default:
                Rhino.Geometry.MeshingParameters.Coarse; SimplePlanes = True for planar surfaces
                Rhino.Geometry.MeshingParameters.Smooth for non-planar surfaces
    Returns:
        A list of point lists. For planar surfaces the length of the list will be
        only 1. For non-planar surfaces or surfaces with internal edges it will be
        a number of lists.
    """
    assert isinstance(geometry, rc.Geometry.GeometryBase), \
        TypeError("Input surface should be a Mesh or a Brep not {}.".format(type(geometry)))

    if isinstance(geometry, rc.Geometry.Mesh):
        return extractMeshPoints((geometry,))

    if isinstance(geometry, rc.Geometry.Brep) and not isPlanar(geometry):
        meshes = rc.Geometry.Mesh.CreateFromBrep(geometry, meshingParameters)
        return extractMeshPoints(meshes)

    meshingParameters = meshingParameters or rc.Geometry.MeshingParameters.Coarse
    meshingParameters.SimplePlanes = True
    pts = geometry.DuplicateVertices()
    # sort points anti clockwise
    # this is only important for energy simulation and won't make a difference
    # for Radiance

    # To sort the points we find border of the surface and evaluate points
    # on border and use the parameter value to sort them
    border = rc.Geometry.Curve.JoinCurves(geometry.DuplicateEdgeCurves(True))

    if len(border) == 1:
        pointsSorted = sorted(pts, key=lambda pt: border[0].ClosestPoint(pt)[1])
        # make sure points are anti clockwise
        if not isPointsSortedAntiClockwise(
                pointsSorted, getSurfaceCenterPtandNormal(geometry).normalVector):
            pointsSorted.reverse()

        # return sorted points
        # Wrap in a list as Honeybee accepts list of list of points
        return (pointsSorted,)
    else:
        # mesh the surface
        meshes = rc.Geometry.Mesh.CreateFromBrep(geometry, meshingParameters)
        return extractMeshPoints(meshes)


def extractMeshPoints(meshes):
    """Extract points from a mesh."""
    return tuple(tuple(mesh.Vertices[face[i]] for i in range(4))
                 if face.IsQuad else
                 tuple(mesh.Vertices[face[i]] for i in range(3))
                 for mesh in meshes for face in mesh.Faces)


def vectorsCrossProduct(vector1, vector2):
    """Calculate cross product of two vectors."""
    return vector1.X * vector2.X + \
        vector1.Y * vector2.Y + vector1.Z * vector2.Z


def isPointsSortedAntiClockwise(sortedPoints, normal):
    """Check if an ordered list of points are anti-clockwise."""
    vector0 = rc.Geometry.Vector3d(sortedPoints[1] - sortedPoints[0])
    vector1 = rc.Geometry.Vector3d(sortedPoints[-1] - sortedPoints[0])
    ptsNormal = rc.Geometry.Vector3d.CrossProduct(vector0, vector1)

    # in case points are anti-clockwise then normals should be parallel
    if vectorsCrossProduct(ptsNormal, normal) > 0:
        return True
    else:
        return False


def getSurfaceCenterPtandNormal(geometry):
    """Calculate center point and normal for a HBSurface.

    Args:
        HBSurface: A Honeybee surface

    Returns:
        Returns a tuple as (centerPt, normalVector)
    """
    brepFace = geometry.Faces[0]
    if brepFace.IsPlanar and brepFace.IsSurface:
        u_domain = brepFace.Domain(0)
        v_domain = brepFace.Domain(1)
        centerU = (u_domain.Min + u_domain.Max) / 2
        centerV = (v_domain.Min + v_domain.Max) / 2

        centerPt = brepFace.PointAt(centerU, centerV)
        normalVector = brepFace.NormalAt(centerU, centerV)
    else:
        centroid = rc.Geometry.AreaMassProperties.Compute(brepFace).Centroid
        uv = brepFace.ClosestPoint(centroid)
        centerPt = brepFace.PointAt(uv[1], uv[2])
        normalVector = brepFace.NormalAt(uv[1], uv[2])

    SurfaceData = namedtuple('SurfaceData', 'centerPt normalVector')

    return SurfaceData(centerPt, normalVector)


def checkPlanarity(HBSurface, tolerance=1e-3):
    """Check planarity of a HBSurface.

    Args:
        HBSurface: A Honeybee surface
        tolerance: A float number as tolerance (Default: 1e-3)

    Returns:
        True is the surface is planar, otherwise return False.
    """
    try:
        return HBSurface.geometry.Faces[0].IsPlanar(tolerance)
    except AttributeError as e:
        raise TypeError("Input is not a HBSurface: %s" % str(e))


def checkForInternalEdge(HBSurface):
    """Check if the surface has an internal edge.

    For surfaces with internal edge surfaces needs to be meshed to extract the points.

    Args:
        HBSurface: A Honeybee surface

    Returns:
        True is the surface has an internal edge, otherwise return False.

    """
    # I believe there should be a direct method in RhinoCommon to indicate if a
    # surface is an open brep but since I couldn't find it I'm using this method
    # if Surface has no intenal edges the length of joined border is 1
    try:
        edges = HBSurface.geometry.DuplicateEdgeCurves(True)
    except AttributeError as e:
        raise TypeError("Input is not a HBSurface: %s" % str(e))
    else:
        border = rc.Geometry.Curve.JoinCurves(edges)
        if len(border) > 1:
            return True
        else:
            return False


def xyzToGeometricalPoints(xyzPoints):
    """convert a sequence of (x, y, z) values to Dynamo or Grasshopper points."""
    for xyzList in xyzPoints:
        for xyz in xyzList:
            yield rc.Geometry.Point3d(xyz[0], xyz[1], xyz[2])


def polygon(pointList):
    """Return a polygon from points."""
    return rc.Geometry.Polyline(pointList).ToNurbsCurve()
