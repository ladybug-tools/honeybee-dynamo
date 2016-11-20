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
        _testPoints: A list or a datatree of points. Each branch of the datatree
            will be considered as a point group.
        ptsVectors_: A list or a datatree of vectors. Each vector represents the
            direction of the respective test point in testPoints. If only one
            value is provided it will be used for all the test points. If no value
            is provided (0, 0, 1) will be assigned for all the vectors.
    Returns:
        readMe!: Reports, errors, warnings, etc.
        analysisGrid: Analysis grid. Use this analysis grid to create a grid-based
            analysis.
"""

ghenv.Component.Name = "HoneybeePlus_Analysis Grid"
ghenv.Component.NickName = 'analysisGrid'
ghenv.Component.Message = 'VER 0.0.01\nNOV_18_2016'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = '00 :: Create'
ghenv.Component.AdditionalHelpFromDocStrings = "2"

try:
    from honeybee.radiance.analysisgrid import AnalysisGrid
except ImportError as e:
    msg = '\nFailed to import honeybee. Did you install honeybee on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/ladybug-analysis-tools/honeybee-plus/tree/master/plugin/grasshopper/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/ladybug-analysis-tools/honeybee-plus/issues'
        
    raise ImportError('{}\n\t{}'.format(msg, e))


if _testPoints:
    # match points and vectors
    try:
        from honeybee_grasshopper import datatree
        _testPoints = tuple(i.list for i in datatree.dataTreeToList(_testPoints))
        ptsVectors_ = tuple(i.list for i in datatree.dataTreeToList(ptsVectors_))
    except ImportError:
        # Dynamo
        pass
    else:
        ptsVectors_ = ptsVectors_ or ((),)
        
        ptsVectors_ = tuple(ptsVectors_[i]
                       if i < len(ptsVectors_) else ptsVectors_[-1]
                       for i in range(len(_testPoints)))
        analysisGrid = (AnalysisGrid.fromPointsAndVectors(pts, vectors)
                        for pts, vectors in zip(_testPoints, ptsVectors_))