"""Wrapper class for outputs in Grasshopper and Dynamo."""


class Wrapper():
    """A Wrapper class to overwrite object __clrtype__ in Ladybug objects.

    Use Wrapper to warp your outputs when the output is a Honeybee or Ladybug
    object.

    Attributes:
        data: The class to be wrapped. check __repr__ method of class to
            be set to a human readable string

    Usage:
        # wrap legend parameters class
        OUT = wrapper(legendpar.LegendParameters())

        # unwarp a wrapped legend parameter
        lp = IN[0].unwarp()
    """

    def __init__(self, data):
        """Create a wrapper."""
        self.__data = data

    def unwrap(self):
        """Unwrap and get data."""
        return self.__data

    def __repr__(self):
        """Return representation of the data class."""
        return self.__data.__repr__()
