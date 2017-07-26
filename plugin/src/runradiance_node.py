# assign inputs
_analysisRecipe, _HBObjects, radScene_, _folder_, _name_, _write, run_ = IN
legendPar = results = None


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
    
    legendPar = _analysisRecipe.legendParameters

    if _write:
        # Add Honeybee objects to the recipe
        _analysisRecipe.hbObjects = _HBObjects
        _analysisRecipe.scene = radScene_

        batchFile = _analysisRecipe.write(_folder_, _name_)

    if _write and run_:
        if _analysisRecipe.run(batchFile, False):
            results = _analysisRecipe.results()


# assign outputs to OUT
OUT = legendPar, results