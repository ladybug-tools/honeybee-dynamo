# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Honeybee Window Surface

-

    Args:
        _geo: An input geometry.
        name_: A name for this surface. If the name is not provided Honeybee will
            assign a random name to the surface.
        radMat_: A Radiance material or a list pf BSDF materials.
            If multiple BSDF materials are provided and the 3-Phase recipe is
            used the simulation will run for each material separately as a
            different state for this window.
            If radiance matrial is not provided the component will use the type
            to assign the default material for the surface. If type is also not
            assigned by user. Honeybee will guess the type of the surface based
            on surface normal vector direction at the center of the surface.
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

ghenv.Component.Name = "HoneybeePlus_Honeybee Window Surface"
ghenv.Component.NickName = 'HBWinSrf'
ghenv.Component.Message = 'VER 0.0.01\nNOV_24_2016'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '00 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = "1"


try:
    from honeybee_grasshopper.hbfensurface import HBFenSurface
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
    
    for m in radMat_:
        assert m.isGlassMaterial, \
            TypeError('Radiance material must be a Window material not {}.'.format(type(m)))
    if len(radMat_)==0:
        radProp_ = RadianceProperties()
    elif len(radMat_) == 1:
        radProp_ = RadianceProperties(radMat_[0], True)
    else:
        radProp_ = RadianceProperties(
            radMat_[0], True, alternateMaterials=radMat_[1:])

    epProp_ = epProp_ if epProp_ else None
    HBWindowSrf = HBFenSurface.fromGeometry(name_, _geo, isNameSetByUser, radProp_, epProp_)