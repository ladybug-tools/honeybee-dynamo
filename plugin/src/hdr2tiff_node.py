# assign inputs
_hdrs, _convert = IN
tiff = None

try:
    from honeybee.radiance.command.raTiff import RaTiff
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _convert:
    tiff = []
    for fp in _hdrs:
        output = fp[:-4] + '.tiff'
        RaTiff(fp, output).execute()
        tiff.append(output)

# assign outputs to OUT
OUT = (tiff,)