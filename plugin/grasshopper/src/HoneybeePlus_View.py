# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Honeybee View.

-

    Args:
        _name: View name.
        _vLocation: Set the view point (-vp) to (x, y, z). This is the focal
            point of a perspective view or the center of a parallel projection.
            Default: (0, 0, 0)
        _vDirection: Set the view direction (-vd) vector to (x, y, z). The
            length of this vector indicates the focal distance as needed by
            the pixle depth of field (-pd) in rpict. Default: (0, 0, 1)
        _vUpVector_: Set the view up (-vu) vector (vertical direction) to (x, y, z).
            Default: (0, 1, 0)
        _viewType_: Set view type (-vt) to one of the choices below.
                0 Perspective (v)
                1 Hemispherical fisheye (h)
                2 Parallel (l)
                3 Cylindrical panorma (c)
                4 Angular fisheye (a)
                5 Planisphere [stereographic] projection (s)
            For more detailed description about view types check rpict manual
            page: (http://radsite.lbl.gov/radiance/man_html/rpict.1.html)
        _hViewAngle_: Set the view horizontal size (-vs). For a perspective
            projection (including fisheye views), val is the horizontal field
            of view (in degrees). For a parallel projection, val is the view
            width in world coordinates.
        _vViewAngle_: Set the view vertical size (-vv). For a perspective
            projection (including fisheye views), val is the horizontal field
            of view (in degrees). For a parallel projection, val is the view
            width in world coordinates.
        _xResolution_: Set the maximum x resolution (-x) to an integer.
        _yResolution_: Set the maximum y resolution (-y) to an integer.
        
    Returns:
        readMe!: Reports, errors, warnings, etc.
        view: Honeybee view.
"""

ghenv.Component.Name = "HoneybeePlus_View"
ghenv.Component.NickName = 'view'
ghenv.Component.Message = 'VER 0.0.01\nDEC_01_2016'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '00 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = "3"

#import honeybee
#reload(honeybee.radiance.view)

try:
    from honeybee.radiance.view import View
except ImportError as e:
    msg = '\nFailed to import honeybee. Did you install honeybee on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/ladybug-analysis-tools/honeybee-plus/tree/master/plugin/grasshopper/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/ladybug-analysis-tools/honeybee-plus/issues'
        
    raise ImportError('{}\n\t{}'.format(msg, e))


if _vLocation and _vDirection:
    _location = (_vLocation.X, _vLocation.Y, _vLocation.Z)
    _direction = (_vDirection.X, _vDirection.Y, _vDirection.Z)
    _upVector = (_vUpVector_.X, _vUpVector_.Y, _vUpVector_.Z)
    view = View(_name, _location, _direction, _upVector, _viewType_,
                _hViewAngle_, _vViewAngle_, _xResolution_, _yResolution_)