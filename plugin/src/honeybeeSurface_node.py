###### start you code from here ###
from honeybeex.hbsurface import HBSurface
from uuid import uuid4

# create list from inputs if it's not a list
_geo = IN[0]

if _geo:

	# this is not good practice. I need to find a better generic solution for
	# dynamo inputs
	for count, inp in enumerate(IN):
		if not inp:
			IN[count] = (None,)
		elif isinstance(inp, str):
			IN[count] = (inp,)
		elif not hasattr(inp, '__iter__'):
			IN[count] = (inp,)

	_geos, names_, _types_, radProps_, epProps_ = UnwrapElement(IN[:])
	if not names_[0]:
		names_ = ("srf_%s" % uuid4(),)

	HBSrfs = range(len(_geos))

	for count, _geo in enumerate(_geos):
		try:
			name_ = names_[count]
		except IndexError:
			name_ = names_[0] + "_{}".format(count)

		isNameSetByUser = True
		if not name_:
			name_ = "Surface_%s" % uuid4()
			isNameSetByUser = False

		try:
			_type_ = _types_[count]
		except ValueError:
			_type_ = _types_[0]

		isTypeSetByUser = True
		if not _type_:
			isTypeSetByUser = False

		try:
			radProp_ = radProps_[count]
		except ValueError:
			radProp_ = radProps_[0]

		try:
			epProp_ = epProps_[count]
		except ValueError:
			epProp_ = epProps_[0]

		HBSrf = HBSurface.fromGeometry(name_, _geo, _type_, isNameSetByUser,
									   isTypeSetByUser, radProp_, epProp_)

		HBSrfs[count] = HBSrf


	OUT = HBSrfs
