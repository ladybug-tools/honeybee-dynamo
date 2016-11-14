###### start you code from here ###
from honeybeex.radiance.material.glass import GlassMaterial

_name, _TVis = IN[0], IN[1]
if _name and _TVis is not None:
	OUT = GlassMaterial.bySingleTransValue(_name, _TVis)
