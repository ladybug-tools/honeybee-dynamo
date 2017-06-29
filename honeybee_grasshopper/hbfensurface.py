import honeybee.hbfensurface as hbfensrf
from honeybee.utilcol import randomName
from .utilities import extractGeometryPoints, polygon, xyzToGeometricalPoints


class HBFenSurface(hbfensrf.HBFenSurface):
    """Honeybee fenestration surface.

    Args:
        name: A unique string for surface name
        sortedPoints: A list of 3 points or more as tuple or list with three items
            (x, y, z). Points should be sorted. This class won't sort the points.
            If surfaces has multiple subsurfaces you can pass lists of point lists
            to this function (e.g. ((0, 0, 0), (10, 0, 0), (0, 10, 0))).
        isNameSetByUser: If you want the name to be changed by honeybee any case
            set isNameSetByUser to True. Default is set to False which let Honeybee
            to rename the surface in cases like creating a newHBZone.
        radProperties: Radiance properties for this surface. If empty default
            RADProperties will be assigned to surface by Honeybee.
        epProperties: EnergyPlus properties for this surface. If empty default
            epProperties will be assigned to surface by Honeybee.
        isCreatedFromGeometry: ...
    """

    @classmethod
    def fromGeometry(cls, name, geometry, isNameSetByUser=False, radProperties=None,
                     epProperties=None, states=None, group=False):
        """Create a honeybee fenestration surface from Grasshopper geometry."""
        name = name or randomName()
        srfData = extractGeometryPoints(geometry)
        if not group:
            hbsrfs = []
            # create a separate surface for each geometry.
            for gcount, srf in enumerate(srfData):
                for scount, (geo, pts) in enumerate(srf):
                    _name = '%s_%d_%d' % (name, gcount, scount)
                    _srf = cls(_name, pts, isNameSetByUser, radProperties, epProperties,
                               states)
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

            _srf = cls(name, _pts, isNameSetByUser, radProperties, epProperties, states)
            _srf.geometry = _geos
            return _srf

    @property
    def isCreatedFromGeometry(self):
        """Return True."""
        return True

    @property
    def geometry(self):
        """return geometry."""
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
