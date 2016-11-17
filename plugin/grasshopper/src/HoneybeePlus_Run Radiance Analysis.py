# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Run Radiance Analysis

-

    Args:
        _analysisRecipe: Radiance analysis recipe. You can find the recipes under
            tab 03 | Daylight | Recipe.
        _HBObjects: A flatten list of Honeybee surfaces and zones.
        _folder_: An optional folder to save the files for this analysis.
        _name_: An optional name for this analysis.
        _write: Set to True to write the files to the folder.
        run_: Set to True to run the analysis. You can only run the analysis if
            _write is also set to True.
    Returns:
        readMe!: Reports, errors, warnings, etc.
        results: Results of the analysis.
"""

ghenv.Component.Name = "HoneybeePlus_Run Radiance Analysis"
ghenv.Component.NickName = 'runRadiance'
ghenv.Component.Message = 'VER 0.0.01\nNOV_16_2016'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '04 :: Daylight :: Daylight'
ghenv.Component.AdditionalHelpFromDocStrings = "1"


_HBObjects.Flatten()
_HBObjects = _HBObjects.Branch(0)

if _HBObjects and _analysisRecipe and _write:
    try:
        for obj in _HBObjects:
            assert hasattr(obj, 'isHBObject')
    except AssertionError:
        raise ValueError("\n{} is not a valid Honeybee object.".format(obj))
   
    assert hasattr(_analysisRecipe, 'isAnalysisRecipe'), \
        ValueError("\n{} is not a Honeybee recipe.".format(_analysisRecipe))
    
    if _write:
        # Add Honeybee objects to the recipe
        _analysisRecipe.hbObjects = _HBObjects
        _analysisRecipe.writeToFile(_folder_, _name_)

    if _write and run_:
        if _analysisRecipe.run(False):
            results = _analysisRecipe.results()
