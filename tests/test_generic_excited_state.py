"""
Unit tests for the generic_excited_state module of PyValem
"""

import unittest

from pyvalem.states.generic_excited_state import (
    GenericExcitedState,
    GenericExcitedStateError,
)


class GenericExcitedStateTest(unittest.TestCase):
    def test_generic_excited_state_html(self):
        x0 = GenericExcitedState("*")
        self.assertEqual(x0.html, "<sup>*</sup>")
        x1 = GenericExcitedState("**")
        self.assertEqual(x1.html, "<sup>**</sup>")
        x11 = GenericExcitedState("2*")
        self.assertEqual(x11.html, "<sup>**</sup>")
        x2 = GenericExcitedState("***")
        self.assertEqual(x2.html, "<sup>3*</sup>")

        x3 = GenericExcitedState("3*")
        self.assertEqual(x3.int_n, 3)
        self.assertEqual(x3.html, "<sup>3*</sup>")

        x4 = GenericExcitedState("15*")
        self.assertEqual(x4.int_n, 15)
        self.assertEqual(x4.html, "<sup>15*</sup>")

        self.assertRaises(GenericExcitedStateError, GenericExcitedState, "a")
        self.assertRaises(GenericExcitedStateError, GenericExcitedState, "*3")
        self.assertRaises(GenericExcitedStateError, GenericExcitedState, "3 *")
        self.assertRaises(GenericExcitedStateError, GenericExcitedState, "3**")
        self.assertRaises(GenericExcitedStateError, GenericExcitedState, "3**?")
        self.assertRaises(GenericExcitedStateError, GenericExcitedState, "*4**")

    def test_generic_excited_state_repr(self):
        x1a = GenericExcitedState("*")
        x1b = GenericExcitedState("1*")
        x2a = GenericExcitedState("**")
        x2b = GenericExcitedState("2*")
        x3a = GenericExcitedState("***")
        x3b = GenericExcitedState("3*")
        x4a = GenericExcitedState("****")
        x4b = GenericExcitedState("4*")
        for (xa, xb), expected in zip(
            ((x1a, x1b), (x2a, x2b), (x3a, x3b), (x4a, x4b)),
            ("*", "**", "3*", "4*"),
            strict=True,
        ):
            with self.subTest(expected):
                self.assertEqual(repr(xa), expected)
                self.assertEqual(repr(xb), expected)


if __name__ == "__main__":
    unittest.main()
