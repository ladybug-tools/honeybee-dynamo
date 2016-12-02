# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Radiance Scene.

Use this class to create a base for the radiance studies by using a number
of radiance files. The main advantage of creating a scene is to avoid re-creating
the geometries and writing the files in parametric studies.

-

    Args:
        _radFiles: List of radiance files. Valid files are *.rad, *.mat and *.oct.
        _copyLocal_: Set to True to copy the files to the analysis folder (Default: True).
        _overwrite_: Set to True to overwrite the files if already exist (Default: False).
"""

ghenv.Component.Name = "HoneybeePlus_Radiance Scene"
ghenv.Component.NickName = 'RadScene'
ghenv.Component.Message = 'VER 0.0.01\nDEC_01_2016'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '00 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = "3"

try:
    from honeybee.radiance.scene import Scene
except ImportError as e:
    msg = '\nFailed to import honeybee. Did you install honeybee on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/ladybug-analysis-tools/honeybee-plus/tree/master/plugin/grasshopper/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/ladybug-analysis-tools/honeybee-plus/issues'
        
    raise ImportError('{}\n\t{}'.format(msg, e))

if _radFiles:
    radScene = Scene(_radFiles, _copyLocal_, _overwrite_)