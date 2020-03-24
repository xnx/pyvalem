"""
Unit tests for the vibrational_state module of PyValem
"""

import unittest

from pyvalem.vibrational_state import VibrationalState, VibrationalStateError

class VibrationalStateTest(unittest.TestCase):
    def test_vibrational_state(self):
        # Test basic usage
        v0 = VibrationalState('0')
        self.assertEqual(v0.html, 'v=0')
        self.assertEqual(v0.latex, 'v=0')
        self.assertEqual(str(v0), 'v=0')
        
        # Test basic usage with explicit quantum number assignment
        v1 = VibrationalState('v=5')
        self.assertEqual(v1.html, 'v=5')
        self.assertEqual(v1.latex, 'v=5')
        self.assertEqual(str(v1), 'v=5')
        
        # Test usage with excited vibrational modes, using v instead of ν
        v2 = VibrationalState('3v2+v3')
        self.assertEqual(str(v2), '3ν2+ν3')
        self.assertEqual(v2.html, '3ν<sub>2</sub> + ν<sub>3</sub>')
        self.assertEqual(v2.latex, r'3\nu_{2} + \nu_{3}')
        
        # Test usage with excited vibrational modes using ν
        v3 = VibrationalState('ν1+ν2')
        self.assertEqual(str(v3), 'ν1+ν2')
        self.assertEqual(v3.html, 'ν<sub>1</sub> + ν<sub>2</sub>')
        self.assertEqual(v3.latex, r'\nu_{1} + \nu_{2}')
        
        # Spaces around the '+' are allowed
        v4 = VibrationalState('2v1 + 3v4')
        self.assertEqual(str(v4), '2ν1+3ν4')
        self.assertEqual(v4.html, '2ν<sub>1</sub> + 3ν<sub>4</sub>')
        self.assertEqual(v4.latex, r'2\nu_{1} + 3\nu_{4}')

        # If only one mode is excited, there is no '+'
        v5 = VibrationalState('3v2')
        self.assertTrue(v5.polyatomic)
        self.assertEqual(str(v5), '3ν2')
        self.assertEqual(v5.html, '3ν<sub>2</sub>')
        self.assertEqual(v5.latex, r'3\nu_{2}')
        v6 = VibrationalState('ν3')
        self.assertTrue(v6.polyatomic)
        self.assertEqual(str(v6), 'ν3')
        self.assertEqual(v6.html, 'ν<sub>3</sub>')
        self.assertEqual(v6.latex, r'\nu_{3}')

        # These are all malformed and so raise a VibrationalStateError
        self.assertRaises(VibrationalStateError, VibrationalState, 'abc')
        self.assertRaises(VibrationalStateError, VibrationalState, 'v+v2')
        self.assertRaises(VibrationalStateError, VibrationalState, '1v1+')
        self.assertRaises(VibrationalStateError, VibrationalState, 'v=0x')
        self.assertRaises(VibrationalStateError, VibrationalState, '2ν1+3ν4x')

    def test_generic_excited_vibrational_state(self):
        # Generic vibrational states are *, **, ***.
        v1 = VibrationalState('v=*')
        self.assertIsNone(v1.polyatomic)
        self.assertEqual(str(v1), 'v=*')
        self.assertEqual(v1.html, 'v=*')

        v2 = VibrationalState('**')
        self.assertEqual(str(v2), 'v=**')
        self.assertEqual(v2.html, 'v=**')

        self.assertRaises(VibrationalStateError, VibrationalState, 'v=****')
        self.assertRaises(VibrationalStateError, VibrationalState, 'v=***x')

    def test_vibrational_state_equality(self):

        v1 = VibrationalState('v1 + 3v4')
        v2 = VibrationalState('ν1 + 3ν4')
        v3 = VibrationalState('3v4 + v1')
        v4 = VibrationalState('2v1 + v2')
        self.assertEqual(v1, v2)
        self.assertEqual(v1, v3)
        self.assertNotEqual(v1, v4)

        v5 = VibrationalState('v=0')
        v6 = VibrationalState('v=0')
        v7 = VibrationalState('v=1')
        self.assertEqual(v5, v6)
        self.assertNotEqual(v6, v7)


if __name__ == '__main__':
    unittest.main()
