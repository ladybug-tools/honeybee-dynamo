###### start you code from here ###
from honeybeex.dataoperation import unflatten
_recipe, _HBObjs, _folder_, _name_, _write, run_ = UnwrapElement(IN)

if _HBObjs and _recipe and _write:
	if not hasattr(_HBObjs, '__iter__'):
		_HBObjs = [_HBObjs]

	for count, obj in enumerate(_HBObjs):
		assert hasattr(obj, 'isHBObject'), \
			"Item %d is not a valid Honeybee object." % count

	if _write:
		# Add Honeybee objects to the recipe
		_recipe.hbObjects = _HBObjs
		# try:
		_recipe.writeToFile(_folder_, _name_)
		# except Exception, e:
		#     raise ValueError("Failed to write the files:\n%s" % e)

	if _write and run_:
		if _recipe.run(False):
			OUT = unflatten(_recipe.originalPoints, iter(_recipe.results()))
