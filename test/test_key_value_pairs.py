"""
Unit tests for the key-value pair states module of PyValem
"""

import unittest

from pyvalem.key_value_pair import KeyValuePair, KeyValuePairError

class KeyValuePairTest(unittest.TestCase):

    def test_key_value_pair(self):
        kv1 = KeyValuePair('n=1')
        self.assertEqual(kv1.key, 'n')
        self.assertEqual(kv1.value, '1')
        self.assertEqual(str(kv1), 'n=1')
        self.assertEqual(kv1.html, 'n=1')

        kv2 = KeyValuePair('C = 45a#')
        self.assertEqual(kv2.key, 'C')
        self.assertEqual(kv2.value, '45a#')
        self.assertEqual(str(kv2), 'C=45a#')
        self.assertEqual(kv2.html, 'C=45a#')

        self.assertRaises(KeyValuePairError, KeyValuePair, '*')

    def test_key_value_pair_equality(self):
        kv1 = KeyValuePair('nd=1')
        kv2 = KeyValuePair('nd=1')
        kv3 = KeyValuePair('dn=1')
        kv4 = KeyValuePair('nd=2')

        self.assertEqual(kv1, kv2)
        self.assertNotEqual(kv1, kv3)
        self.assertNotEqual(kv2, kv4)

if __name__ == '__main__':
    unittest.main()


