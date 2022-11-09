import unittest
from osm_knooppunten.helper import is_number_valid, is_small_rename

class TestImport(unittest.TestCase):

    def test_helper(self):
        self.assertTrue(is_number_valid("1"))
        self.assertTrue(is_number_valid("30"))
        self.assertTrue(is_number_valid("04"))
        self.assertTrue(is_number_valid("SP16"))
        self.assertTrue(is_number_valid("H04"))
        self.assertTrue(is_number_valid("004"))
        self.assertTrue(is_number_valid("SP53A"))
        self.assertTrue(is_number_valid("K00"))
        self.assertTrue(is_number_valid("*"))
        self.assertFalse(is_number_valid("?"))
        self.assertFalse(is_number_valid("0"))
        self.assertFalse(is_number_valid(""))

    def test_helper(self):
        self.assertTrue(is_small_rename("12a", "12"))
        self.assertTrue(is_small_rename("12", "12a"))
        self.assertTrue(is_small_rename("12", "12A"))
        self.assertTrue(is_small_rename("12B", "12A"))
        self.assertFalse(is_small_rename("12", "123"))
        self.assertFalse(is_small_rename("12", "13"))
        self.assertFalse(is_small_rename("123", "12"))
