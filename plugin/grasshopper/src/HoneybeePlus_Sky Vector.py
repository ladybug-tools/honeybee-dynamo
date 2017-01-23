# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Sky Vector.

-

    Args:
        _epwFile: Full filepath to a weather file.
        _month_: Input a number to indicate month (1..12) (default: 6).
        _day_: Input a number to indicate day (1..31) (default: 21).
        _hour_: Input a number to indicate hour (0..23) (default: 12).
        _skyDensity_: A positive intger for sky density. [1] Tregenza Sky,
            [2] Reinhart Sky, etc. (Default: 1)
    Returns:
        readMe!: Reports, errors, warnings, etc.
        skyVec: Sky vector for multi-phase daylight analysis.
"""

ghenv.Component.Name = "HoneybeePlus_Sky Vector"
ghenv.Component.NickName = 'skyVector'
ghenv.Component.Message = 'VER 0.0.01\nJAN_23_2017'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '02 :: Daylight :: Light Sources'
ghenv.Component.AdditionalHelpFromDocStrings = "1"

try:
    from honeybee.radiance.sky.skymatrix import SkyMatrix
    from ladybug.dt import LBDateTime
except ImportError as e:
    msg = '\nFailed to import honeybee. Did you install honeybee on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/ladybug-analysis-tools/honeybee-plus/tree/master/plugin/grasshopper/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/ladybug-analysis-tools/honeybee-plus/issues'
        
    raise ImportError('{}\n\t{}'.format(msg, e))

if _wea:
    north_ = north_ or 0
    _month_ = _month_ or 6
    _day_ = _day_ or 21
    _hour_ = _hour_ or 12
    dt = LBDateTime(_month_, _day_, _hour_)
    _skyDensity_ = _skyDensity_ or 1
    
    skyVec = SkyMatrix(_wea, _skyDensity_, north_, (int(dt.HOY),))
    