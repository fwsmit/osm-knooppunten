import unittest
from analyze import do_analysis_internal
from compare import find_matching_point, find_closest_node
from unittest.mock import Mock
from node import Node

class TestAnalysis(unittest.TestCase):

    def setUp(self):
        self.osm_nodes = [
                Node(lat=1, lon=1, rwn_ref="1", rcn_ref=None), # nothing changed
                # added
                Node(lat=2, lon=1, rwn_ref="1", rcn_ref=None), # renamed
                Node(lat=2, lon=0, rwn_ref="1", rcn_ref=None), # removed
                ]
        self.ext_nodes = [
                Node(lat=1, lon=1.000001, rwn_ref="1", rcn_ref=None), # nothing changed
                Node(lat=2, lon=2, rwn_ref="2", rcn_ref=None), # added
                Node(lat=2, lon=1, rwn_ref="3", rcn_ref=None), # renamed
                ]

    def test_run(self):
        results = do_analysis_internal(self.osm_nodes, self.ext_nodes, [], Mock())
        counts = [x.n_nodes for x in results]
        names = [x.filename for x in results]
        d = dict(zip(names, counts))
        print(d)
        self.assertEqual(d["No change_ext.geojson"], 1)
        self.assertEqual(d["Added_ext.geojson"], 1)
        self.assertEqual(d["Renamed_ext.geojson"], 1)
        self.assertEqual(d["Removed_osm.geojson"], 1)

    def test_compare_matching(self):
        self.assertEqual(find_matching_point(self.ext_nodes[0], self.osm_nodes), self.osm_nodes[0])
        self.assertEqual(find_matching_point(self.ext_nodes[1], self.osm_nodes), None)
        self.assertEqual(find_matching_point(self.ext_nodes[2], self.osm_nodes), None)

    def test_compare_closest(self):
        self.assertEqual(find_closest_node(self.ext_nodes[0], self.osm_nodes), self.osm_nodes[0])
        self.assertEqual(find_closest_node(self.ext_nodes[1], self.osm_nodes), self.osm_nodes[1])
        self.assertEqual(find_closest_node(self.ext_nodes[2], self.osm_nodes), self.osm_nodes[1])
