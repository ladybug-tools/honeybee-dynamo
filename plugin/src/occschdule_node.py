# assign inputs
_values, hoys_ = IN
schedule = None

try:
    from honeybee.schedule import Schedule
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

if _values:
    schedule = Schedule(_values, hoys_)

# assign outputs to OUT
OUT = (schedule,)