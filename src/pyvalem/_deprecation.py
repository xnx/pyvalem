"""
Warnings about input that PyValem accepts now but will reject in version 3.0.
"""

import os
import sys
import warnings

from .exceptions import PyValemDeprecationWarning

_PACKAGE_DIR = os.path.dirname(__file__) + os.sep


def warn_deprecated(message):
    """Warn that the input described by message will be rejected by PyValem 3.0.

    The warning is attributed to the first caller outside the PyValem package.
    """

    frame, stacklevel = sys._getframe(1), 2
    while frame is not None and frame.f_code.co_filename.startswith(_PACKAGE_DIR):
        frame, stacklevel = frame.f_back, stacklevel + 1
    warnings.warn(
        "{} This will be an error in PyValem 3.0.".format(message),
        PyValemDeprecationWarning,
        stacklevel=stacklevel,
    )
