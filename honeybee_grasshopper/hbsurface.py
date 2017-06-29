import honeybee.hbsurface as hbsrf
from honeybee.utilcol import randomName
from .utilities import extractGeometryPoints, polygon, xyzToGeometricalPoints


class HBSurface(hbsrf.HBSurface):
    """Honeybee surface.

    Args:
        name: A unique string for surface name
        sortedPoints: A list of 3 points or more as tuple or list with three items
            (x, y, z). Points should be sorted. This class won't sort the points.
            If surfaces has multiple subsurfaces you can pass lists of point lists
            to this function (e.g. ((0, 0, 0), (10, 0, 0), (0, 10, 0))).
        surfaceType: Optional input for surface type. You can use any of the surface
            types available from surfacetype libraries or use a float number to
            indicate the type. If not indicated it will be assigned based on normal
            angle of the surface which will be calculated from surface points.
                0.0: Wall           0.5: UndergroundWall
                1.0: Roof           1.5: UndergroundCeiling
                2.0: Floor          2.25: UndergroundSlab
                2.5: SlabOnGrade    2.75: ExposedFloor
                3.0: Ceiling        4.0: AirWall
                6.0: Context
        isNameSetByUser: If you do not want the name to be changed by honeybee any case
            set isNameSetByUser to True. Default is set to False which let Honeybee
            to rename the surface in cases like creating a newHBZone (Default: False).
        isTypeSetByUser: If you so not want the type to be changed by honeybee any case
            set isTypeSetByUser to True. Default is set to False which let Honeybee
            to set the surface type based on surface normal (Default: False).
        radProperties: Radiance properties for this surface. If empty default
            RADProperties will be assigned to surface by Honeybee (Default: None).
        epProperties: EnergyPlus properties for this surface. If empty default
            epProperties will be assigned to surface by Honeybee (Default: None).
        states: A list of SurfaceStates if surface has several states.
        group: Group the surfaces if input is a list of geometries or a multi facade
            geometry (Default: False).
    """

    @classmethod
    def fromGeometry(cls, name, geometry, surfaceType=None,
                     isNameSetByUser=False, isTypeSetByUser=False,
                     radProperties=None, epProperties=None, states=None, group=False):
        """Create honeybee surface[s] from a Grasshopper geometry.

        If group is False it will return a list of HBSurfaces.
        """
        name = name or randomName()
        srfData = extractGeometryPoints(geometry)
        if not group:
            hbsrfs = []
            # create a separate surface for each geometry.
            for gcount, srf in enumerate(srfData):
                for scount, (geo, pts) in enumerate(srf):
                    _name = '%s_%d_%d' % (name, gcount, scount)
                    _srf = cls(_name, pts, surfaceType, isNameSetByUser, isTypeSetByUser,
                               radProperties, epProperties, states)
                    _srf.geometry = geometry
                    hbsrfs.append(_srf)

            # check naming and fix it if it's only single geometry
            if gcount == 0 and scount == 0:
                # this is just a single geometry. remove counter
                hbsrfs[0].name = '_'.join(hbsrfs[0].name.split('_')[:-2])
            elif gcount == 0:
                # this is a single geometry with multiple sub surfaces like a polysurface
                for hbs in hbsrfs:
                    bname = hbs.name.split('_')
                    hbs.name = '%s_%s' % ('_'.join(bname[:-2]), bname[-1])
            return hbsrfs
        else:
            _geos = []
            _pts = []
            # collect all the points in a single list
            for srf in srfData:
                for geo, pts in srf:
                    _pts.extend(pts)
                    _geos.append(geo)

            _srf = cls(name, _pts, surfaceType, isNameSetByUser, isTypeSetByUser,
                       radProperties, epProperties, states)
            _srf.geometry = _geos
            return _srf

    @property
    def isCreatedFromGeometry(self):
        """Return True."""
        return True

    @property
    def geometry(self):
        """Return geometry."""
        if self.isCreatedFromGeometry:
            return self._geometry
        else:
            return self.profile

    @geometry.setter
    def geometry(self, geo):
        """Set geometry."""
        self._geometry = geo

    @property
    def profile(self):
        """Get profile curve of this surface."""
        return polygon(tuple(xyzToGeometricalPoints(self.absolutePoints)))
