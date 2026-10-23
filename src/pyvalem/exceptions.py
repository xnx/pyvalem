"""
The base class of the exceptions raised by PyValem.
"""


class PyValemError(ValueError):
    """The base class of every exception that PyValem raises for invalid input.

    It derives from ValueError, so existing code that catches ValueError still
    catches it.
    """
