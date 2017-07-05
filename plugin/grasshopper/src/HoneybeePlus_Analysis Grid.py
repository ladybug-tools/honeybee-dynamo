# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Analysis Grid.

-

    Args:
        _name_: A name for this analysis grid.
        _testPoints: A list or a datatree of points. Each branch of the datatree
            will be considered as a point group.
        ptsVectors_: A list or a datatree of vectors. Each vector represents the
            direction of the respective test point in testPoints. If only one
            value is provided it will be used for all the test points. If no value
            is provided (0, 0, 1) will be assigned for all the vectors.
        windowGroups: An optional list of windowGroups. This input is only
            important for multi-phase daylight simulation to avoid unnecessary
            view matrix calculations. If this input is left empty for multi-phase
            daylight recipes the view matrix will be calculated for each analysis
            grid and every window group.
    Returns:
        readMe!: Reports, errors, warnings, etc.
        analysisGrid: Analysis grid. Use this analysis grid to create a grid-based
            analysis.
"""

ghenv.Component.Name = "HoneybeePlus_Analysis Grid"
ghenv.Component.NickName = 'analysisGrid'
ghenv.Component.Message = 'VER 0.0.02\nJUL_04_2017'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '00 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = "2"

try:
    from honeybee.radiance.analysisgrid import AnalysisGrid
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if _testPoints:
    analysisGrid = AnalysisGrid.fromPointsAndVectors(_testPoints, ptsVectors_,
        _name_, windowGroups_)