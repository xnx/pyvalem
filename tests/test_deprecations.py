"""
Unit tests for the helper that warns about input PyValem will stop accepting.
"""

import unittest

from pyvalem import PyValemDeprecationWarning
from pyvalem._deprecation import warn_deprecated


class WarnDeprecatedTest(unittest.TestCase):
    def test_warning(self):
        with self.assertWarnsRegex(PyValemDeprecationWarning, "Something") as cm:
            warn_deprecated("Something is deprecated.")
        self.assertIn("will be an error", str(cm.warning))
        # The warning is attributed to the caller outside PyValem.
        self.assertEqual(cm.filename, __file__)

    def test_shown_by_default(self):
        self.assertTrue(issubclass(PyValemDeprecationWarning, FutureWarning))


if __name__ == "__main__":
    unittest.main()
