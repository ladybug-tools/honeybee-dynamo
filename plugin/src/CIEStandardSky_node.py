###### start you code from here ###
from honeybeex.radiance.sky.cieradiancesky import CIERadianceSky
north_, _location, _month_, _day_, _hour_, _skyType_ = IN

if _location:
	OUT = CIERadianceSky(_location, _month_, _day_, _hour_, _skyType_, north_)
