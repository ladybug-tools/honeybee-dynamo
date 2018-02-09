# ##### start you code from here ###
from honeybee.plus import GridGenerator

_zones = IN[0]
_gridSize = IN[1]
_distanceFromBaseSrf = IN[2]


if _zones and _gridSize and _distanceFromBaseSrf:

    if not hasattr(_zones, '__iter__'):
        _zones = (_zones,)

    _gg = GridGenerator.from_hb_zones(_zones, _gridSize, _distanceFromBaseSrf)
    gridGroups = tuple(_gg.grids)

    _testPoints = tuple([] for g in gridGroups)
    _ptsNormal = tuple([] for g in gridGroups)
    _UVs = tuple([] for g in gridGroups)
    _polygons = tuple([] for g in gridGroups)

    for count, grids in enumerate(gridGroups):
        for g in grids:
            _testPoints[count].append(g.point)
            _ptsNormal[count].append(g.normal)
            _UVs[count].append(g.uv)
            _polygons[count].append(g.polygon)

    OUT = _testPoints, _ptsNormal, _UVs, _polygons
