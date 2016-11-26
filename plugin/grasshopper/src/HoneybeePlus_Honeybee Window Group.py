# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Honeybee Window Group

A window group is a group of HBWindow surfaces which will be grouped together
for 3-phase daylight analysis. View matrix will be calculated for all the Window
surfaces in a group once. Window surfaces in a group shoudl have the same normal
direction, and same BSDF materials will be assigned to all the windows in this
group.
-

    Args:
        _name: A name for this window group. You can use this name later to add
            or remove this group contribution to 3-Phase analysis.
        _HBWindowSrfs: A list of HBWindow surfaces by similar normal direction.
        _bsdfMaterials: A list of BSDF materials. The first material will overwrite
            the radiance material for window surface. If multiple BSDF materials
            are provided the simulation will run for each material separately as
            a different state of the window group.
    Returns:
        readMe!: Reports, errors, warnings, etc.
        HBWindowGroup: List of HBWindowsSrf for this window group.
"""

ghenv.Component.Name = "HoneybeePlus_Honeybee Window Group"
ghenv.Component.NickName = 'HBWindowGroup'
ghenv.Component.Message = 'VER 0.0.01\nNOV_25_2016'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '00 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = "2"

if _name and _bsdfMaterials and _HBWindowSrfs:
    # check inputs
    try:
        _normal = _HBWindowSrfs[0].normal
    except AttributeError:
        # A None input is connected which will be raised in next loop
        pass

    names = tuple(material.name for material in _bsdfMaterials)
    
    assert len(names) == len(set(names)), \
        'Duplicated name found in bsdfMaterials!\n\t{}'.format(names)
    
    windowGroupSrfs = range(len(_HBWindowSrfs))
    for count, srf in enumerate(_HBWindowSrfs):
        assert hasattr(srf, 'isHBFenSurface'), \
            TypeError('{} is not a HBWindowSurface.'.format(srf))
    
        assert srf.normal == _normal, \
            ValueError('Normal direction of Windows in a window groups should match.\n'
                       '{} from {} does not match {} from {}.'.format(
                       srf.normal, srf, _HBWindowSrfs[0].normal, _HBWindowSrfs[0]
                       ))
        
        newsrf= srf.duplicate()
        # change window group name for this surface
        newsrf.radProperties.windowGroupName = _name
        newsrf.radProperties.radianceMaterial = _bsdfMaterials[0]
        if len(_bsdfMaterials) > 1:
            newsrf.radProperties.alternateMaterials = _bsdfMaterials[1:]
        
        windowGroupSrfs[count] = newsrf

    HBWindowGroup = windowGroupSrfs
    