# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Radiance Opaque Material from Single Reflectance Value

-

    Args:
        _name: Material name
        _reflect: Diffuse reflectance
        _spec_: Specularity values above 0.1 are uncommon
        _rough_: Roughness values above 0.2 are uncommon
    Returns:
        readMe!: Reports, errors, warnings, etc.
        material: Radiance opaque material
"""

ghenv.Component.Name = "HoneybeePlus_Radiance Opaque Material"
ghenv.Component.NickName = 'radOpaqueMaterial'
ghenv.Component.Message = 'VER 0.0.01\nNOV_11_2016'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '01 :: Daylight :: Materials'
ghenv.Component.AdditionalHelpFromDocStrings = "1"

try:
    from honeybee.radiance.material.plastic import PlasticMaterial
except ImportError as e:
    msg = '\nFailed to import honeybee. Did you install honeybee on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/ladybug-analysis-tools/honeybee-plus/tree/master/plugin/grasshopper/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/ladybug-analysis-tools/honeybee-plus/issues'
        
    raise ImportError('{}\n\t{}'.format(msg, e))

if _name and _reflect:
    material = PlasticMaterial.bySingleReflectValue(_name, _reflect, _spec_, _rough_)