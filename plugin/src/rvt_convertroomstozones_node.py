# ##### start you code from here ###
from honeybee.revit import convert_rooms_to_hb_zones

if IN[0]:
    if not hasattr(IN[0], '__iter__'):
        IN[0] = [IN[0]]
    # collect rooms
    _hbZones, _ids = convert_rooms_to_hb_zones(IN[0], boundary_location=IN[1])
    OUT = _hbZones, tuple(zone.geometry for zone in _hbZones), _ids
