import geojson
import os
import math
import sys
from node import Node
from compare import dist_complicated
from osm_knooppunten import helper
from export import ExportFile

def import_geojson(filename, rwn_name = None, rcn_name = None, filter_regio = None, filter_province = None):
    try:
        with open(filename, 'r') as file:
            data = geojson.load(file)
    except IOError as er:
        print(er)
        sys.exit(1)

    nodes = []
    invalid_nodes = []

    for node_data in data['features']:
        rwn_ref_id = "-1"
        if filter_regio and node_data['properties']["regio"] != filter_regio:
            continue

        if filter_province and node_data['properties']["provincie"] != filter_province:
            continue

        if rwn_name:
            rwn_ref_id = node_data['properties'][rwn_name]

        rcn_ref_id = "-1"
        if rcn_name:
            rcn_ref_id = node_data['properties'][rcn_name]

        if node_data['geometry']:
            coords = node_data['geometry']['coordinates']
            coord_lon = coords[0]
            coord_lat = coords[1]
        else:
            coord_lon = None
            coord_lat = None

        node = Node(lon=coord_lon, lat=coord_lat, rwn_ref=rwn_ref_id, rcn_ref=rcn_ref_id)
        if not helper.is_number_valid(node.rwn_ref) and not helper.is_number_valid(node.rcn_ref):
            invalid_nodes.append(node)
        else:
            nodes.append(node)

    return nodes, invalid_nodes

def export_geojson(nodes, filename):
    print("Exporting to", filename)
    features = []
    for node in nodes:
        point = geojson.Point((node.lon, node.lat))
        closest_distance = math.inf
        for matched_node in node.matching_nodes + node.bad_matching_nodes:
            closest_distance = min(dist_complicated(matched_node.lat, matched_node.lon, node.lat, node.lon), closest_distance)

        if closest_distance == math.inf:
            closest_distance = -1
        if node.renamed_from:
            properties_dict = {"rwn_ref": node.rwn_ref, "rcn_ref": node.rcn_ref, "distance closest node": closest_distance, "old_name": node.renamed_from}
        else:
            properties_dict = {"rwn_ref": node.rwn_ref, "rcn_ref": node.rcn_ref, "distance closest node": closest_distance}

        feature = geojson.Feature(geometry=point, properties=properties_dict)
        features.append(feature)

    dump = geojson.dumps(features)

    resultsdir = "results"
    try:
        os.mkdir(resultsdir)
    except FileExistsError:
        pass # The directory already exists, move on

    filepath = os.path.join(resultsdir, filename)

    try:
        with open(filepath, 'w') as f:
            f.write(dump)
        return ExportFile(filename=filename, filepath=filepath, n_nodes=len(nodes))
    except IOError as er:
        print(er)
        sys.exit(1)
