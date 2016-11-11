"""Methods to matches test points and point vectors."""
from collections import Iterable


def matchPointsAndVectors(ptsT, vecT):
    """Convert a grasshopperDataTree to list.

    Args:
        ptsT: A Grasshopper DataTree of test points.
        vecT: A Grasshopper DataTree of vectors.
    Returns:
        pts: Nested list of points
        vectors: Nested list of vectors
    """
    ptsT.SimplifyPaths()
    vecT.SimplifyPaths()

    pts = range(ptsT.BranchCount)
    vec = range(ptsT.BranchCount)

    for i, path in enumerate(ptsT.Paths):
        p = list(ptsT.Branch(path))
        try:
            v = list(vecT.Branch(path))
        except:
            v = []

        tempPts, tempVectors = __matchData(p, v)

        if len(tempPts) > 0:
            pts[i] = tempPts
            vec[i] = tempVectors
        else:
            # empty branch
            pts.remove(i)
            vec.remove(i)

    return pts, vec


# TODO: move this method to list operation library
def __matchData(guide, follower, noneValue=(0, 0, 1)):
    """Match data between two lists.

    Args:
        guide: Long list.
        follower: Short list.
        noneValue: Place holder for default value if shortlist is an empty lists.
    """
    tempPts = range(len(guide))
    tempVectors = range(len(guide))

    for c, dp in enumerate(guide):
        if dp is not None:
            tempPts[c] = dp
            # match vector in vector list
            try:
                # check if there is a vector with the same index
                dv = follower[c]
            except IndexError:
                try:
                    # try to get the last item provided (longest list match)
                    dv = follower[-1]
                except IndexError:
                    # use default value
                    dv = noneValue
            finally:
                if dv is None:
                    # use default value
                    dv = noneValue

                tempVectors[c] = dv
        else:
            # empty list
            tempPts.remove(c)
            tempVectors(c)

    return tempPts, tempVectors


def flatten(inputList):
    """Return a flattened genertor from an input list.

    Usage:

        inputList = [['a'], ['b', 'c', 'd'], [['e']], ['f']]
        list(flatten(inputList))
        >> ['a', 'b', 'c', 'd', 'e', 'f']
    """
    for el in inputList:
        if isinstance(el, Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el
