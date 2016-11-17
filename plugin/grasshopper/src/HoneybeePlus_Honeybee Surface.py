# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Honeybee Surface

-

    Args:
        _geo: An input geometry.
        name_: A name for this surface. If the name is not provided Honeybee will
            assign a random name to the surface.
        _type_: Surface type (). Surface type will be used to set the material and
            construction for the surface if they are not assigned by user.
        radMat_: Radiance material. If radiance matrial is not provided the component
            will use the type to assign the default material for the surface. If type
            is also not assigned by user. Honeybee will guess the type of the surface
            based on surface normal vector direction at the center of the surface.
        epProp_: EnergyPlus properties. If EnergyPlus properties is not provided the
            component will use the "type" to assign the EnergyPlus properties for this
            surface. If type is also not assigned by user Honeybee will guess the type
            of the surface based on surface normal vector direction at the center of
            the surface, and sets EnergyPlus properties based on the type.
        
    Returns:
        readMe!: Reports, errors, warnings, etc.
        HBSrf: Honeybee surface. Use this surface directly for daylight simulation
            or to create a Honeybee zone for Energy analysis.
"""

ghenv.Component.Name = "HoneybeePlus_Honeybee Surface"
ghenv.Component.NickName = 'HBSurface'
ghenv.Component.Message = 'VER 0.0.01\nNOV_16_2016'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '00 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = "1"

try:
    from honeybee_grasshopper.hbsurface import HBSurface
    from honeybee.radiance.properties import RadianceProperties
except ImportError as e:
    msg = '\nFailed to import honeybee. Did you install honeybee on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/ladybug-analysis-tools/honeybee-plus/tree/master/plugin/grasshopper/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/ladybug-analysis-tools/honeybee-plus/issues'
        
    raise ImportError('{}\n\t{}'.format(msg, e))


from uuid import uuid4

if _geo:
    isNameSetByUser = True
    if not name_:
        name_ = "Surface_%s" % uuid4()
        isNameSetByUser = False
        
    isTypeSetByUser = True
    if not _type_:
        isTypeSetByUser = False
    
    radProp_ = RadianceProperties(radMat_, True) if radMat_ else RadianceProperties()
    
    epProp_ = epProp_ if epProp_ else None
    
    HBSrf = HBSurface.fromGeometry(name_, _geo, _type_, isNameSetByUser,
                                   isTypeSetByUser, radProp_, epProp_)