# assign inputs
_epwFile = IN[0]
wea = None

try:
    from ladybug.wea import Wea
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _epwFile:
    wea = Wea.from_epw_file(_epwFile)

# assign outputs to OUT
OUT = (wea,)