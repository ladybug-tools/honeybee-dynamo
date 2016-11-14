###### start you code from here ###
from honeybeex.radiance.parameters.gridbased import GridBasedParameters

_quality = IN[0]
if _quality is not None:
	OUT = GridBasedParameters(_quality)
