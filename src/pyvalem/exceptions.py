"""
The base classes of the exceptions and warnings raised by PyValem.
"""


class PyValemError(ValueError):
    """The base class of every exception that PyValem raises for invalid input.

    It derives from ValueError, so existing code that catches ValueError still
    catches it.
    """


class PyValemDeprecationWarning(FutureWarning):
    """Warns about input that PyValem accepts now but will reject in version 3.0.

    It derives from FutureWarning, which is shown by default, rather than
    DeprecationWarning, which isn't: the input usually comes from data rather
    than from code.
    """
