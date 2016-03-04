"""Collection of methods for Honeybee geometry operations in Grasshopper."""
from honeybee.geometryoperation import *
import Rhino as rc


# TODO: Add support for non-planar surfaces. The current implementation is a simple
# implementation to prototype the workflow
# TODO: Extract point should support mesh as well as brep surfaces. Currently we have
# two alternative solutions which is not preferred. Currently it only works for Breps.
def extractSurfacePoints(HBSurface, triangulate=False, meshingParameters=None):
    """Calculate list of points for a HBSurface.

    For planar surfaces the length of the list will be only 1. For non-planar
    surfaces or surfaces with internal edges it will be a number of lists.

    Args:
        HBSurface: A HBSurface
        triangulate: If set to True the function returns the points for triangulated
            surfaces (Default: False)
        meshingParameters: Optional Rhino meshingParameters. This will only be uses if the
            surface is non-planar or has an internal edge and needs to be meshed.
            Default:
                Rhino.Geometry.MeshingParameters.Coarse; SimplePlanes = True for planar surfaces
                Rhino.Geometry.MeshingParameters.Smooth for non-planar surfaces
    Returns:
        A list of point lists. For planar surfaces the length of the list will be
        only 1. For non-planar surfaces or surfaces with internal edges it will be
        a number of lists.
    """
    try:
        pts = HBSurface.geometry.DuplicateVertices()
    except AttributeError as e:
        raise TypeError("Input is not a HBSurface: %s" % str(e))
    else:
        # sort points anti clockwise
        # this is only important for energy simulation and won't make a difference
        # for Radiance

        # To sort the points we find border of the surface and evaluate points
        # on border and use the parameter value to sort them
        border = rc.Geometry.Curve.JoinCurves(
            HBSurface.geometry.DuplicateEdgeCurves(True))[0]

        pointsSorted = sorted(pts, key=lambda pt: border.ClosestPoint(pt)[1])

        # make sure points are anti clockwise
        if not isPointsSortedAntiClockwise(pointsSorted, HBSurface.basePlane):
            return pointsSorted.reverse()

        # return sorted points
        return pointsSorted


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


def getSurfaceCenterPtandNormal(HBSurface):
    """Calculate center point and normal for a HBSurface.

    Args:
        HBSurface: A Honeybee surface

    Returns:
        Returns a tuple as (centerPt, normalVector)
    """
    try:
        brepFace = HBSurface.geometry.Faces[0]
    except AttributeError as e:
        raise TypeError("Input is not a HBSurface: %s" % str(e))
    else:
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

        return centerPt, normalVector


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
