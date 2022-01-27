"""
Unit tests for the rotational_state module of PyValem
"""

import unittest

from pyvalem.states.rotational_state import RotationalState, RotationalStateError


class RotationalStateTest(unittest.TestCase):
    def test_rotational_term_symbol(self):
        rot_state = RotationalState("J=1/2")
        self.assertEqual(rot_state.J, 0.5)
        self.assertEqual(str(rot_state), "J=1/2")
        self.assertEqual(rot_state.html, "J=1/2")

        rot_state = RotationalState("J=2.5")
        self.assertEqual(rot_state.J, 2.5)
        self.assertEqual(str(rot_state), "J=5/2")
        self.assertEqual(rot_state.html, "J=5/2")

        rot_state = RotationalState("J=0")
        self.assertEqual(rot_state.J, 0)
        self.assertEqual(str(rot_state), "J=0")
        self.assertEqual(rot_state.html, "J=0")

        rot_state = RotationalState("J=3/2")
        self.assertEqual(rot_state.J, 1.5)

        rot_state = RotationalState("J=2")
        self.assertEqual(rot_state.J, 2)

        self.assertRaises(RotationalStateError, RotationalState, "0")
        self.assertRaises(RotationalStateError, RotationalState, "J=-2")
        self.assertRaises(RotationalStateError, RotationalState, "J=0x")

        self.assertRaises(RotationalStateError, RotationalState, "J=1/5")
        self.assertRaises(RotationalStateError, RotationalState, "J=1/5x")
        self.assertRaises(RotationalStateError, RotationalState, "J=1\5")

    def test_generic_excited_rotational_state(self):
        j1 = RotationalState("J=*")
        self.assertEqual(str(j1), "J=*")
        self.assertEqual(j1.html, "J=*")

        j2 = RotationalState("J=**")
        self.assertEqual(str(j2), "J=**")
        self.assertEqual(j2.html, "J=**")

        self.assertRaises(RotationalStateError, RotationalState, "J=****")
        self.assertRaises(RotationalStateError, RotationalState, "J=***z")

    def test_rotational_state_equality(self):
        j1 = RotationalState("J=0.5")
        j2 = RotationalState("J=1/2")
        self.assertEqual(j1, j2)

    def test_rotational_state_repr(self):
        j1 = RotationalState("J=**")
        j2 = RotationalState("J = **")
        self.assertTrue(repr(j1) == repr(j2) == "J=**")


if __name__ == "__main__":
    unittest.main()
