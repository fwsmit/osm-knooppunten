import geojson
from node import Node

def import_geojson(filename, rwn_name = None, rcn_name = None):
    with open(filename, 'r') as file:
        data = geojson.load(file)
        print("Geojson data imported")

    nodes = []

    print(len(data['features']))

    for node_data in data['features']:
        rwn_ref_id = -1
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
    points = []
    for node in nodes:
        point = geojson.Point((node.lon, node.lat))
        points.append(point)

    dump = geojson.dumps(points)

    with open(filename, 'w') as f:
        f.write(dump)
