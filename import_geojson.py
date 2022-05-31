import geojson
from node import Node

def import_geojson(filename):
    with open(filename, 'r') as file:
        data = geojson.load(file)
        print("Geojson data imported")

    nodes = []

    print(len(data['features']))

    for node_data in data['features']:
        ref_id = node_data['properties']['KNOOPP_NR']
        if node_data['geometry']:
            coords = node_data['geometry']['coordinates']
            coord_lon = coords[0]
            coord_lat = coords[1]
        else:
            coord_lon = None
            coord_lat = None

        nodes.append(Node(lon=coord_lon, lat=coord_lat, rwn_ref=ref_id, rcn_ref=-1))

    return nodes
