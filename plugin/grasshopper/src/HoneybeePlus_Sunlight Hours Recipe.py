# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Sunlight Hours Recipe.

-

    Args:
        _sunVectors: A list of vectors that represents sun vectors. You can use
            Ladybug sunpath to generate the vectors for any time of the year. If
            you're generating the vectors in a different way make sure that the
            vectors are looking downwards from the sun (e.g. z = 0).
        _analysisGrids: List of honeybee analysis grids. Use Analysis grid component
            which you can find under 00 :: Create to create them.
        _timestep_: Timstep for sun vectors. Default is 1 which means each sun vector
            represents an hour of time.
        
    Returns:
        readMe!: Reports, errors, warnings, etc.
        analysisRecipe: Sunlight hours analysis recipe. Connect this recipe to
            Run Radiance Simulation to run a sunlight hours analysis.
"""

ghenv.Component.Name = "HoneybeePlus_Sunlight Hours Recipe"
ghenv.Component.NickName = 'sunlightHoursRecipe'
ghenv.Component.Message = 'VER 0.0.01\nDEC_03_2016'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '03 :: Daylight :: Recipe'
ghenv.Component.AdditionalHelpFromDocStrings = "1"

try:
    from honeybee.radiance.recipe.sunlighthours import SunlightHoursAnalysisRecipe
except ImportError as e:
    msg = '\nFailed to import honeybee. Did you install honeybee on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/ladybug-analysis-tools/honeybee-plus/tree/master/plugin/grasshopper/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/ladybug-analysis-tools/honeybee-plus/issues'
        
    raise ImportError('{}\n\t{}'.format(msg, e))


if _sunVectors and _sunVectors[0] != None and _analysisGrids:
    # set a sunlight hours analysis recipe together if there are points
    analysisRecipe = SunlightHoursAnalysisRecipe(_sunVectors, _analysisGrids,
                                                 _timestep_)