# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Grid-based Recipe.

-

    Args:
        _sky: A radiance sky. Find honeybee skies under 02::Daylight::Light Sources.
        _testPoints: A list or a datatree of points. Each branch of the datatree
            will be considered as a point group.
        ptsVectors_: A list or a datatree of vectors. Each vector represents the
            direction of the respective test point in testPoints. If only one
            value is provided it will be used for all the test points. If no value
            is provided (0, 0, 1) will be assigned for all the vectors.
        _analysisType_: Analysis type. [0] illuminance(lux), [1] radiation (kwh),
            [2] luminance (Candela).
        _radiancePar_: Radiance parameters for Grid-based analysis. Find Radiance
            parameters node under 03::Daylight::Recipes.
    Returns:
        readMe!: Reports, errors, warnings, etc.
        analysisRecipe: Grid-based analysis recipe. Connect this recipe to
            Run Radiance Analysis to run a grid-based analysis.
"""

ghenv.Component.Name = "HoneybeePlus_Grid-Based Recipe"
ghenv.Component.NickName = 'gridBasedRecipe'
ghenv.Component.Message = 'VER 0.0.01\nNOV_16_2016'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '03 :: Daylight :: Recipe'
ghenv.Component.AdditionalHelpFromDocStrings = "1"

try:
    from honeybee.radiance.recipe.gridbased import HBGridBasedAnalysisRecipe
except ImportError as e:
    msg = '\nFailed to import honeybee. Did you install honeybee on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/ladybug-analysis-tools/honeybee-plus/tree/master/plugin/grasshopper/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/ladybug-analysis-tools/honeybee-plus/issues'
        
    raise ImportError('{}\n\t{}'.format(msg, e))


if _sky:
    # match points and vectors
    try:
        from honeybee_grasshopper import datatree
    except ImportError:
        # Dynamo
        pass
    else:
        _testPoints = tuple(i.list for i in datatree.dataTreeToList(_testPoints))
        ptsVectors_ = tuple(i.list for i in datatree.dataTreeToList(ptsVectors_))
    
    # set a sunlight hours analysis recipe together if there are points
    analysisRecipe = HBGridBasedAnalysisRecipe(_sky, _testPoints, ptsVectors_,
                                               _analysisType_, _radiancePar_)