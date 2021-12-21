"""
Utility functions for the pyvalem package.
"""


def parse_fraction(s):
    """
    Parse an integer or fraction as a pyparsing.ParseResults object resulting
    from a match to '2', '3/2', etc. into a float. If s is None or the empty
    string, return None.
    """
    if not s:
        return None
    if len(s) == 2:
        num, det = s
        return float(num) / int(det)
    elif len(s) == 1:
        if s:
            return float(s[0])

    raise ValueError(s, "does not parse to an integer or fraction")


def float_to_fraction(v):
    """Convert the integer or half-integer float v into a string fraction."""

    if v.is_integer():
        return str(int(v))
    return "{0:d}/2".format(int(2 * v))
