# assign inputs
_hbObjects, _folder, _filename, _write = IN
radFile = None

try:
    from honeybee.radiance.radfile import RadFile
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


if _hbObjects and _folder and _filename and _write:
    rf = RadFile(_hbObjects)
    radFile = rf. write(_folder, _filename, mkdir=True)

# assign outputs to OUT
OUT = (radFile,)