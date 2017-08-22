# ##### start you code from here ###
from honeybee.revit import convertRoomsToHBZones

if IN[0]:
    if not hasattr(IN[0], '__iter__'):
        IN[0] = [IN[0]]
    # collect rooms
    _hbZones, _ids = convertRoomsToHBZones(IN[0], boundaryLocation=IN[1])
    OUT = _hbZones, tuple(zone.geometry for zone in _hbZones), _ids
