# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Window Group State

-

    Args:
        _name: A name for this surface. If the name is not provided Honeybee will
            assign a random name to the surface.
        radMat_: A Radiance material. If radiance matrial is not provided the
            component will use the type to assign the default material 
            (%60 transmittance)for the surface.
        HBSrfs_: A list of honeybee surfaces that will be added to the scene at this
            state. You can use this input to add radiance geometries to the scene at
            this state.
    Returns:
        report: Reports, errors, warnings, etc.
        state: A Honeybee SurfaceProperties object for define a state for a
            honeybee surface.
"""

ghenv.Component.Name = "HoneybeePlus_WindowGroup State"
ghenv.Component.NickName = 'HBWinGroupState'
ghenv.Component.Message = 'VER 0.0.02\nJUN_29_2017'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '00 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = "2"

try:
    from honeybee.surfaceproperties import SurfaceProperties, SurfaceState
    from honeybee.surfacetype import Window
    from honeybee.radiance.properties import RadianceProperties
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _name and (radMat_ or HBSrfs_):
    if radMat_:
        radPar = RadianceProperties(radMat_, True)
    else:
        radPar = RadianceProperties()

    state = SurfaceState(_name, SurfaceProperties(Window, radPar), HBSrfs_) 