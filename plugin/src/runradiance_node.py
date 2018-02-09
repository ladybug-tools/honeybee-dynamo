# assign inputs
_analysisRecipe, _HBObjects, radScene_, _folder_, _name_, _write, run_ = IN
legendPar = outputs = None


try:
    _HBObjects.Flatten()
    _HBObjects = _HBObjects.Branch(0)
except AttributeError:
    # the case for Dynamo
    pass

if _HBObjects and _analysisRecipe and _write:
    try:
        for obj in _HBObjects:
            assert hasattr(obj, 'isHBObject')
    except AssertionError:
        raise ValueError("\n{} is not a valid Honeybee object.".format(obj))
   
    assert hasattr(_analysisRecipe, 'isAnalysisRecipe'), \
        ValueError("\n{} is not a Honeybee recipe.".format(_analysisRecipe))
    
    legendPar = _analysisRecipe.legend_parameters

    if _write:
        # Add Honeybee objects to the recipe
        _analysisRecipe.hb_objects = _HBObjects
        _analysisRecipe.scene = radScene_

        batchFile = _analysisRecipe.write(_folder_, _name_)

    if _write and run_:
        if _analysisRecipe.run(batchFile, False):
            try:
                outputs = _analysisRecipe.results()
            except StopIteration:
                raise ValueError(
                    'Length of the results is smaller than the analysis grids '
                    'point count [{}]. In case you have changed the analysis'
                    ' Grid you must re-calculate daylight/view matrix!'
                    .format(_analysisRecipe.total_point_count)
                )

# assign outputs to OUT
OUT = legendPar, outputs