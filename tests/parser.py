import unittest
from import_osm import import_osm

class TestImport(unittest.TestCase):

    def test_osm(self):
        nodes = import_osm("tests/data/test.osm")
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].lat, 53.23)
        self.assertEqual(nodes[0].rwn_ref, '82')
        self.assertEqual(nodes[0].rcn_ref, '89')
        self.assertEqual(nodes[1].rcn_ref, None)
        self.assertEqual(nodes[2].rcn_ref, '9')
        self.assertEqual(nodes[2].lon, 6.53)
