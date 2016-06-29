"""Collection of functions for Revit."""
import config
from hbzone import HBZone
from hbsurface import HBSurface
from hbfensurface import HBFenSurface

try:
    import clr
    clr.AddReference("RevitAPI")
    from Autodesk.Revit.DB import FilteredElementCollector, \
        BuiltInCategory, Options, Solid

    # objects for spatial calculation
    from Autodesk.Revit.DB import SpatialElementGeometryCalculator, \
        SpatialElementBoundaryOptions, SpatialElementBoundaryLocation

    clr.AddReference("RevitServices")
    from RevitServices.Persistence import DocumentManager

    clr.AddReference("RevitNodes")
    from Revit import GeometryConversion
    # Import ToProtoType, ToRevitType geometry conversion extension methods
    clr.ImportExtensions(GeometryConversion)

    clr.AddReference('ProtoGeometry')
    from Autodesk.DesignScript.Geometry import Point
except ImportError:
    "You can only use revit library from Revit not %s." % config.platform.platform


def collectRooms(document=None):
    """Collect all the rooms in the current Revit document."""
    if not document:
        document = DocumentManager.Instance.CurrentDBDocument
    collector = FilteredElementCollector(document)
    collector.OfCategory(BuiltInCategory.OST_Rooms)
    roomIter = collector.GetElementIdIterator()
    roomIter.Reset()
    return tuple(document.GetElement(elId) for elId in roomIter)


def collectMEPSpaces(document=None):
    """Collect all the spaces in the current Revit document."""
    if not document:
        document = DocumentManager.Instance.CurrentDBDocument
    collector = FilteredElementCollector(document)
    collector.OfCategory(BuiltInCategory.OST_MEPSpaces)
    roomIter = collector.GetElementIdIterator()
    roomIter.Reset()
    return tuple(document.GetElement(elId) for elId in roomIter)


def getChildElemenets(hostElement, addRectOpenings=True, includeShadows=False,
                      includeEmbeddedWalls=False,
                      includeSharedEmbeddedInserts=True):
    """Get child elemsts for a Revit element."""
    ids = hostElement.FindInserts(addRectOpenings,
                                  includeShadows,
                                  includeEmbeddedWalls,
                                  includeSharedEmbeddedInserts)

    return tuple(hostElement.Document.GetElement(i) for i in ids)


def exctractGlazingVertices(hostElement, baseFace, opt):
    """Return glazing vertices for a window family instance.

    I was hoping that revit supports a cleaner way for doing this but for now
    I calculate the bounding box and find the face that it's vertices are coplanar
    with the host face.
    """
    # get 3d faces for the geometry
    # TODO: Take all the vertices for daylight modeling
    faces = (clr.Convert(obj, Solid).Faces
             for obj in hostElement.get_Geometry(opt))

    _outerFace = next(faces)[0].ToProtoType()[0]

    openings = (
        tuple(edge.StartVertex.PointGeometry for edge in loop.CoEdges)
        for face in _outerFace.Faces
        for loop in face.Loops[:-1]
    )

    coordinates = (
        tuple(
            tuple(baseFace.ClosestPointTo(pt) for pt in opening)
            for opening in openings
        ))

    # cleaning up
    (pt.Dispose() for opening in openings for pt in opening)
    (face.Dispose() for faceGroup in faces for face in faceGroup)

    return coordinates


def _getInternalElements(elements):
    """Get internal element from dynamo objects.

    This is similar to UnwrapElement in dynamo but will work fine outside dynamo.
    """
    if not elements:
        return

    if hasattr(elements, '__iter__'):
        return (_getInternalElements(x) for x in elements)
    elif hasattr(elements, 'InternalElement'):
        return elements.InternalElement
    else:
        return elements


def getBoundaryLocation(index=1):
    """Get SpatialElementBoundaryLocation.

    0 > Finish: Spatial element finish face.
    1 > Center: Spatial element centerline.
    """
    index = 1 if not index else index % 2

    _locations = (SpatialElementBoundaryLocation.Finish,
                  SpatialElementBoundaryLocation.Center)

    return _locations[index]


def convertRoomsToHBZones(rooms, boundaryLocation=1):
    """Convert rooms to honeybee zones.

    This script will only work from inside Dynamo nodes. for a similar script
    forRrevit check this link for more details:
    https://github.com/jeremytammik/SpatialElementGeometryCalculator/
        blob/master/SpatialElementGeometryCalculator/Command.cs
    """
    rooms = tuple(_getInternalElements(rooms))

    if not rooms:
        return []

    # create a spatial element calculator to calculate room data
    doc = rooms[0].Document
    options = SpatialElementBoundaryOptions()
    options.SpatialElementBoundaryLocation = getBoundaryLocation(boundaryLocation)
    calculator = SpatialElementGeometryCalculator(doc, options)

    opt = Options()

    _zones = range(len(rooms))
    _surfaces = {} # collect hbSurfaces so I can set adjucent surfaces

    for zoneCount, room in enumerate(rooms):
        # initiate zone based on room id
        _zone = HBZone(room.Id)

        # assert False, room.Id
        elementsData = calculator.CalculateSpatialElementGeometry(room)

        _roomGeo = elementsData.GetGeometry()
        # This can be the same as finish wall or in the center of the wall
        roomDSFaces = tuple(face.ToProtoType()[0] for face in _roomGeo.Faces)

        assert _roomGeo.Faces.Size == len(roomDSFaces), \
            "Number of rooms elements ({}) doesn't match number of faces ({}).\n" \
            "Make sure the Room is bounded.".format(_roomGeo.Faces.Size,
                                                    len(roomDSFaces))

        for count, face in enumerate(_roomGeo.Faces):
            # base face is useful to project the openings to room boundary
            _baseFace = roomDSFaces[count]

            # Revit is strange! if two roofs have a shared wall then it will be
            # duplicated! By checking the values inside the _collector
            _collector = []
            for boundaryFace in elementsData.GetBoundaryFaceInfo(face):
                # boundaryFace is from type SpatialElementBoundarySubface
                # get the element (Wall, Roof, etc)
                boundaryElement = doc.GetElement(
                    boundaryFace.SpatialBoundaryElement.HostElementId
                )

                # initiate honeybee surface
                _ver = tuple(v.PointGeometry for v in _baseFace.Vertices)
                if _ver in _collector:
                    continue

                _hbSurface = HBSurface("%s:%s" % (_zone.name, boundaryElement.Id),
                                       _ver)

                _collector.append(_ver)

                if boundaryElement.Id not in _surfaces:
                    _surfaces[boundaryElement.Id] = _hbSurface
                else:
                    # TODO: set adjacent surface
                    pass

                # check if there is any child elements
                childElements = getChildElemenets(boundaryElement)

                if childElements:
                    _coordinates = exctractGlazingVertices(boundaryElement, _baseFace, opt)

                    for count, coordinate in enumerate(_coordinates):
                        # create honeybee surface - use element id as the name
                        _hbfenSurface = HBFenSurface(
                            childElements[count].Id, coordinate)

                        # add fenestration surface to base honeybee surface
                        _hbSurface.addFenestrationSurface(_hbfenSurface)

                # add hbsurface to honeybee zone
                _zone.addSurface(_hbSurface)
                boundaryElement.Dispose()

        _zones[zoneCount] = _zone
        # clean up!
        elementsData.Dispose()

    calculator.Dispose()

    return _zones
