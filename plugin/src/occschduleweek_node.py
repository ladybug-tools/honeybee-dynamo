# assign inputs
_occHours_, _offHours_, _weekend_, _defValue_ = IN
schedule = values = None

try:
    from honeybee.schedule import Schedule
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

schedule = Schedule.fromWorkdayHours(
    _occHours_, _offHours_, _weekend_, _defValue_)

values = schedule.values

# assign outputs to OUT
OUT = schedule, values