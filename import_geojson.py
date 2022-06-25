import geojson
import os
from node import Node

def import_geojson(filename, rwn_name = None, rcn_name = None, filter_regio = None):
    with open(filename, 'r') as file:
        data = geojson.load(file)
        print("Geojson data imported")

    nodes = []

    print(len(data['features']))

    for node_data in data['features']:
        rwn_ref_id = -1
        if filter_regio and node_data['properties']["regio"] != filter_regio:
            continue

        if rwn_name:
            rwn_ref_id = node_data['properties'][rwn_name]

        rcn_ref_id = -1
        if rcn_name:
            rcn_ref_id = node_data['properties'][rcn_name]

        if node_data['geometry']:
            coords = node_data['geometry']['coordinates']
            coord_lon = coords[0]
            coord_lat = coords[1]
        else:
            coord_lon = None
            coord_lat = None

        nodes.append(Node(lon=coord_lon, lat=coord_lat, rwn_ref=rwn_ref_id, rcn_ref=rcn_ref_id))

    return nodes

def export_geojson(nodes, filename):
    features = []
    for node in nodes:
        point = geojson.Point((node.lon, node.lat))
        feature = geojson.Feature(geometry=point, properties={"rwn knooppuntnummer": node.rwn_ref, "rcn knooppuntnummer": node.rcn_ref})
        features.append(feature)

    dump = geojson.dumps(features)

    resultsdir = "results"
    try:
        os.mkdir(resultsdir)
    except FileExistsError:
        pass # The directory already exists, move on

    filepath = os.path.join(resultsdir, filename)

    with open(filepath, 'w') as f:
        f.write(dump)
