# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Three-pahse daylight Recipe.

-

    Args:
        _skyMTX: A sky matrix or a sky vector. Find honeybee skies under 02::Daylight::Light Sources.
        _analysisGrids: A list of Honeybee analysis grids.
        _analysisType_: Analysis type. [0] illuminance(lux), [1] radiation (kwh),
            [2] luminance (Candela).
        _radiancePar_: Radiance parameters for Grid-based analysis. Find Radiance
            parameters node under 03::Daylight::Recipes.
    Returns:
        readMe!: Reports, errors, warnings, etc.
        analysisRecipe: Annual analysis recipe. Connect this recipe to Run Radiance
            Analysis to run a annual analysis.
"""

ghenv.Component.Name = "HoneybeePlus_Grid-Based Three-Phase Daylight Recipe"
ghenv.Component.NickName = 'threePhaseGBRecipe'
ghenv.Component.Message = 'VER 0.0.02\nJUL_04_2017'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '03 :: Daylight :: Recipe'
ghenv.Component.AdditionalHelpFromDocStrings = "3"

#import honeybee
#reload(honeybee.radiance.recipe.threephase.gridbased)

try:
    from honeybee.radiance.recipe.threephase.gridbased import ThreePhaseGridBased
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if _skyMTX and _analysisGrid:
    reuseDaylightMTX_ = True if reuseDaylightMTX_ is None else reuseDaylightMTX_
    reuseViewMTX_ = True if reuseViewMTX_ is None else reuseViewMTX_
    analysisRecipe = ThreePhaseGridBased(
        _skyMTX, _analysisGrid, _analysisType_, _viewMTXPar_, _DaylightMTXPar_,
        reuseViewMTX_, reuseDaylightMTX_)