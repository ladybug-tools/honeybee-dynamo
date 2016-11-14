###### start you code from here ###
from honeybeex.radiance.sky.certainIlluminance import SkyWithCertainIlluminanceLevel
_illuminanceValue = IN[0]
if _illuminanceValue:
	OUT = SkyWithCertainIlluminanceLevel(_illuminanceValue)
