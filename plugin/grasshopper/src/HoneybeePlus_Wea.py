# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
epw2wea

-

    Args:
        _epwFile = Fullpath to epw weather file.
    Returns:
        readMe!: Reports, errors, warnings, etc.
        wea: A wea object from epw file.
"""

ghenv.Component.Name = "HoneybeePlus_Wea"
ghenv.Component.NickName = 'Wea'
ghenv.Component.Message = 'VER 0.0.01\nDEC_05_2016'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '02 :: Daylight :: Light Sources'
ghenv.Component.AdditionalHelpFromDocStrings = "2"

try:
    from ladybug.wea import Wea
except ImportError as e:
    msg = '\nFailed to import honeybee. Did you install honeybee on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/ladybug-analysis-tools/honeybee-plus/tree/master/plugin/grasshopper/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/ladybug-analysis-tools/honeybee-plus/issues'
        
    raise ImportError('{}\n\t{}'.format(msg, e))


if _epwFile:
    wea = Wea.fromEpwFile(_epwFile)