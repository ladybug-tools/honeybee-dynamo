# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Annual daylight Recipe.

-

    Args:
        _sky: A radiance sky. Find honeybee skies under 02::Daylight::Light Sources.
        _testPoints: A list or a datatree of points. Each branch of the datatree
            will be considered as a point group.
        ptsVectors_: A list or a datatree of vectors. Each vector represents the
            direction of the respective test point in testPoints. If only one
            value is provided it will be used for all the test points. If no value
            is provided (0, 0, 1) will be assigned for all the vectors.
        _skyDensity_: A positive intger for sky density. [1] Tregenza Sky,
            [2] Reinhart Sky, etc. (Default: 1)
    Returns:
        readMe!: Reports, errors, warnings, etc.
        analysisRecipe: Annual analysis recipe. Connect this recipe to Run Radiance
            Analysis to run a annual analysis.
"""

ghenv.Component.Name = "HoneybeePlus_Annual Daylight Recipe"
ghenv.Component.NickName = 'annualRecipe'
ghenv.Component.Message = 'VER 0.0.01\nNOV_16_2016'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '03 :: Daylight :: Recipe'
ghenv.Component.AdditionalHelpFromDocStrings = "1"

try:
    from honeybee.radiance.recipe.annual import HBAnnualAnalysisRecipe
except ImportError as e:
    msg = '\nFailed to import honeybee. Did you install honeybee on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/ladybug-analysis-tools/honeybee-plus/tree/master/plugin/grasshopper/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/ladybug-analysis-tools/honeybee-plus/issues'
        
    raise ImportError('{}\n\t{}'.format(msg, e))


if _epwFile:
    # match points and vectors
    try:
        from honeybee_grasshopper import datatree
    except ImportError:
        # Dynamo
        pass
    else:
        _testPoints = tuple(i.list for i in datatree.dataTreeToList(_testPoints))
        ptsVectors_ = tuple(i.list for i in datatree.dataTreeToList(ptsVectors_))
    
    _skyDensity_= _skyDensity_ or 1
    # set a sunlight hours analysis recipe together if there are points
    analysisRecipe = HBAnnualAnalysisRecipe(_epwFile, _testPoints, ptsVectors_,
                                            _skyDensity_)