"""
Run the examples in examples/ and check that they print what examples/output/ has.
"""

import contextlib
import io
import runpy
import sys
import unittest
from pathlib import Path
from unittest import mock

EXAMPLES = Path(__file__).parents[1] / "examples"


class ExamplesTest(unittest.TestCase):
    def test_examples(self):
        if not EXAMPLES.exists():
            raise unittest.SkipTest("the examples are not available")
        scripts = sorted(EXAMPLES.glob("*.py"))
        self.assertTrue(scripts)
        for script in scripts:
            with self.subTest(script.name):
                expected = EXAMPLES / "output" / (script.stem + ".txt")
                output = io.StringIO()
                # Run the script as a program with no arguments.
                with (
                    mock.patch.object(sys, "argv", [str(script)]),
                    contextlib.redirect_stdout(output),
                ):
                    runpy.run_path(str(script), run_name="__main__")
                self.assertEqual(output.getvalue(), expected.read_text(encoding="utf8"))


if __name__ == "__main__":
    unittest.main()
