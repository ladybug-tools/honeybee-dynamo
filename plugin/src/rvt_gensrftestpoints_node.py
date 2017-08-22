# ##### start you code from here ###
from honeybee.plus import GridGenerator

_surfaces = IN[0]
_gridSize = IN[1]
_distanceFromBaseSrf = IN[2]
_borders = IN[3]

if _surfaces and _gridSize and _distanceFromBaseSrf:

    if not hasattr(_surfaces, '__iter__'):
        _surfaces = (_surfaces,)

    if not hasattr(_borders, '__iter__'):
        _borders = (_borders,)

    _gg = GridGenerator(_surfaces, _gridSize, _distanceFromBaseSrf, _borders)
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
