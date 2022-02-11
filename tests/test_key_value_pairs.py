"""
Unit tests for the key-value pair states module of PyValem
"""

import unittest

from pyvalem.states.key_value_pair import KeyValuePair, KeyValuePairError


class KeyValuePairTest(unittest.TestCase):
    def test_key_value_pair(self):
        kv1 = KeyValuePair("n=1")
        self.assertEqual(kv1.key, "n")
        self.assertEqual(kv1.value, "1")
        self.assertEqual(str(kv1), "n=1")
        self.assertEqual(kv1.html, "n=1")

        self.assertRaises(KeyValuePairError, KeyValuePair, "C = 3")
        self.assertRaises(KeyValuePairError, KeyValuePair, "k= 3")
        self.assertRaises(KeyValuePairError, KeyValuePair, "k =v")

    def test_key_value_pair_equality(self):
        kv1 = KeyValuePair("nd=1")
        kv2 = KeyValuePair("nd=1")
        kv3 = KeyValuePair("dn=1")
        kv4 = KeyValuePair("nd=2")

        self.assertEqual(kv1, kv2)
        self.assertNotEqual(kv1, kv3)
        self.assertNotEqual(kv2, kv4)

    def test_html_escaping(self):
        kv1 = KeyValuePair('S="5<n<9"')
        self.assertEqual(repr(kv1), 'S="5<n<9"')
        self.assertEqual(kv1.html, "S=&quot;5&lt;n&lt;9&quot;")


if __name__ == "__main__":
    unittest.main()
